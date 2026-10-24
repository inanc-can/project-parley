"""Files added to a game's shared context: converted to text once, when they are added.

Documents (PDF, Word, PowerPoint, Excel, CSV, HTML, JSON, text, …) are converted with
markitdown; images are described by a vision model (PARLEY_VISION_MODEL), so every agent reads
the same text whatever model it runs.
"""

import base64
import hashlib
import io
import os
from pathlib import PurePath

from parley.core.spec import SharedFile
from parley.llm.client import LLMClient

MAX_BYTES = 10_000_000
MAX_CHARS = 200_000  # about 50k tokens: more would crowd out small models' context
VISION_MODEL = "openrouter/qwen/qwen2.5-vl-72b-instruct"

DESCRIBE_PROMPT = (
    "This image was added to the shared context of a conversation between AI agents. Describe "
    "it so someone who cannot see it gets everything that matters: transcribe all text, numbers "
    "and tables exactly, then describe charts, diagrams and anything else shown. Plain text, no "
    "preamble."
)

SUMMARY_PROMPT = """You prepare the shared context for a conversation between AI agents (a \
negotiation, a game, a meeting, any scene). Every agent will read what you write.

Write it from the files below: the situation and the facts everyone should know, with the \
exact names, numbers and dates they contain. Use only what the files say; don't invent details, \
roles or goals. Be concise and neutral, in plain prose or short lists. Reply with the text only.
{existing}
{files}"""


class FileError(ValueError):
    pass


def vision_model() -> str:
    return os.environ.get("PARLEY_VISION_MODEL", "").strip() or VISION_MODEL


async def to_shared_file(name: str, mime: str, data: bytes, client: LLMClient) -> SharedFile:
    if not data:
        raise FileError(f"{name} is empty")
    if len(data) > MAX_BYTES:
        raise FileError(f"{name} is larger than {MAX_BYTES // 1_000_000} MB")
    if mime.startswith("image/"):
        text = await describe_image(mime, data, client)
    else:
        text = convert(name, mime, data)
    text = text.strip()
    if not text:
        raise FileError(f"no text found in {name} (a scanned PDF needs a text layer for now)")
    if len(text) > MAX_CHARS:
        raise FileError(
            f"{name} has {len(text):,} characters of text; the limit is {MAX_CHARS:,}. "
            "Add a shorter part of it."
        )
    return SharedFile(name=name, mime=mime, sha256=hashlib.sha256(data).hexdigest(), text=text)


def convert(name: str, mime: str, data: bytes) -> str:
    from markitdown import MarkItDown, StreamInfo  # slow import; only needed for uploads

    ext = PurePath(name).suffix.lower() or None
    info = StreamInfo(filename=name, extension=ext, mimetype=mime or None)
    try:
        return MarkItDown().convert_stream(io.BytesIO(data), stream_info=info).text_content
    except Exception as e:
        raise FileError(f"couldn't read {name}: {e}") from e


async def describe_image(mime: str, data: bytes, client: LLMClient) -> str:
    url = f"data:{mime};base64,{base64.b64encode(data).decode()}"
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": DESCRIBE_PROMPT},
                {"type": "image_url", "image_url": {"url": url}},
            ],
        }
    ]
    resp = await client.complete(vision_model(), messages, temperature=0, max_tokens=2000)
    return resp.text


async def summarise(files: list[SharedFile], existing: str, client: LLMClient) -> str:
    from parley.api.assistant import assistant_model

    if not files:
        raise FileError("no files to summarise")
    prompt = SUMMARY_PROMPT.format(
        existing=(
            f"\nThe shared context so far (don't repeat it; write only what the files add):\n"
            f"{existing}\n"
            if existing
            else ""
        ),
        files="\n\n".join(f"### {f.name}\n{f.text}" for f in files),
    )
    resp = await client.complete(
        assistant_model(),
        [{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1500,
        cache=False,  # asking again should give a new draft
    )
    return resp.text.strip()
