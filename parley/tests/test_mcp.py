"""The `parley mcp` tools, called against the real API app."""

import pytest
from fastapi.testclient import TestClient

from parley.api.app import create_app
from parley.mcp_server import ParleyError, Talks, build_server
from parley.storage import Store

from .test_api import FakeClient


@pytest.fixture
def http(tmp_path):
    with TestClient(create_app(Store(tmp_path / "db.sqlite"), FakeClient())) as client:
        yield client


def test_two_agents_talk_through_the_tools(http, tmp_path):
    ada = Talks(web_url="http://web", sessions=tmp_path / "ada.json", http=http)
    bob = Talks(web_url="http://web", sessions=tmp_path / "bob.json", http=http)

    opened = ada.start("Agree who writes the migration", "Ada", "claude-code")
    room = opened["room"]
    assert opened["watch_link"].startswith(f"http://web/room/{room}#token=")
    assert ada.wait(room, 0)["status"] == "not_started"

    joined = bob.join(f"http://web/room/{room}", "Bob", "grok-cli")  # a link works as an invite
    assert joined["goal"] == "Agree who writes the migration"

    assert ada.wait(room)["status"] == "your_turn"
    ada.say(room, "I'll write it if you review.", "offer", "Ada writes it; Bob reviews by Friday")
    assert bob.wait(room)["standing_offer"]["terms"]["agreement"].startswith("Ada writes it")
    bob.say(room, "Agreed.", "accept")

    assert ada.wait(room)["status"] == "ended"
    status = bob.status(room)
    agreed = status["outcome"]["deal"]["terms"]["agreement"]
    assert agreed == "Ada writes it; Bob reviews by Friday"
    assert [t["role"] for t in status["transcript"]] == ["A", "B"]
    assert (tmp_path / "ada.json").stat().st_mode & 0o077 == 0  # tokens are private to the user


def test_unknown_rooms_and_api_errors_are_explained(http, tmp_path):
    talks = Talks(sessions=tmp_path / "s.json", http=http)
    with pytest.raises(ParleyError, match="start or join it first"):
        talks.wait("nope")
    with pytest.raises(ParleyError, match="say what the talk is about"):
        talks.start("", "Ada", "")


async def test_the_server_offers_the_five_tools(tmp_path):
    server = build_server(Talks(sessions=tmp_path / "s.json"))
    names = {t.name for t in await server.list_tools()}
    assert names == {
        "parley_start_talk",
        "parley_join_talk",
        "parley_wait_for_turn",
        "parley_say",
        "parley_status",
    }
