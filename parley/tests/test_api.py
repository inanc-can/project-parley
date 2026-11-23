import json

import pytest
from fastapi.testclient import TestClient

from parley.api.app import create_app
from parley.core.spec import GameSpec
from parley.llm.client import LLMClient, LLMResponse
from parley.storage import Store
from parley.templates import buy_sell


class FakeClient(LLMClient):
    async def _call(self, model, messages, temperature, max_tokens, **kw):
        if "impartial judge" in messages[-1]["content"]:
            text = json.dumps({"deal_reached": False, "rubric": {}, "summary": "s"})
        else:
            text = json.dumps({"reasoning": "secret plan", "message": "Hello", "action": None})
        return LLMResponse(text=text, model=model)


@pytest.fixture
def api(tmp_path):
    return TestClient(create_app(Store(tmp_path / "db.sqlite"), FakeClient()))


def h(token):
    return {"X-Parley-Token": token}


def test_two_people_agree_set_up_privately_and_play(api):
    r = api.post("/api/rooms", json={"name": "Ada"}).json()
    room, ada = r["room_id"], r["token"]
    bob = api.post(f"/api/rooms/{room}/join", json={"name": "Bob"}).json()["token"]
    assert api.post(f"/api/rooms/{room}/join", json={"name": "Cy"}).status_code == 409  # full
    assert api.get(f"/api/rooms/{room}", headers=h("stranger")).status_code == 403

    # Shared game: Ada edits, both must agree on the same version.
    spec = buy_sell().model_dump(mode="json")
    spec["protocol"]["max_messages"] = 4
    spec["runs"] = 2
    assert api.put(f"/api/rooms/{room}/game", json=spec, headers=h(ada)).status_code == 200
    version = api.get(f"/api/rooms/{room}", headers=h(bob)).json()["game"]["version"]
    assert (
        api.post(
            f"/api/rooms/{room}/game/agree", json={"version": version - 1}, headers=h(bob)
        ).status_code
        == 409
    )  # stale version
    api.post(f"/api/rooms/{room}/game/agree", json={"version": version}, headers=h(ada))
    api.post(f"/api/rooms/{room}/game/agree", json={"version": version}, headers=h(bob))
    state = api.get(f"/api/rooms/{room}", headers=h(ada)).json()
    assert state["game"]["locked"]
    assert api.put(f"/api/rooms/{room}/game", json=spec, headers=h(ada)).status_code == 409

    # Private seats. Models must come from the host's list.
    model = state["settings"]["allowed_models"][0]
    bad = {"seat": {"kind": "llm", "model": "openai/gpt-x"}}
    assert api.put(f"/api/rooms/{room}/seat", json=bad, headers=h(ada)).status_code == 422
    api.put(
        f"/api/rooms/{room}/seat",
        headers=h(ada),
        json={"seat": {"kind": "llm", "model": model, "strategy": "Anchor high."}, "reveal": False},
    )
    api.put(
        f"/api/rooms/{room}/seat",
        headers=h(bob),
        json={"seat": {"kind": "llm", "model": model, "strategy": "Be fair."}, "reveal": True},
    )
    bob_view = api.get(f"/api/rooms/{room}", headers=h(bob)).json()
    assert "Anchor high." not in json.dumps(bob_view)  # Ada's setup stays private
    assert not bob_view["can_start"]

    api.post(f"/api/rooms/{room}/ready", json={"ready": True}, headers=h(ada))
    api.post(f"/api/rooms/{room}/ready", json={"ready": True}, headers=h(bob))
    assert api.get(f"/api/rooms/{room}", headers=h(bob)).json()["can_start"]

    match_id = api.post(f"/api/rooms/{room}/matches", json={}, headers=h(bob)).json()["match_id"]
    result = api.get(f"/api/rooms/{room}/matches/{match_id}", headers=h(bob)).json()
    assert result["status"] == "done" and len(result["episodes"]) == 2
    assert result["summary"]["end_reasons"] == {"limit": 2}

    # Ada did not reveal: Bob sees neither her setup nor her reasoning; his own he sees.
    ep = result["episodes"][0]
    assert ep["seats"]["Ada"] is None and ep["seats"]["Bob"]["strategy"] == "Be fair."
    for t in ep["turns"]:
        mine = ep["assignment"][t["role"]] == "Bob"
        assert (t["reasoning"] == "secret plan") == mine
    ada_ep = api.get(f"/api/rooms/{room}/matches/{match_id}", headers=h(ada)).json()["episodes"][0]
    assert ada_ep["seats"]["Bob"]["strategy"] == "Be fair."  # Bob revealed


def test_editing_clears_agreement(api):
    r = api.post("/api/rooms", json={"name": "Ada"}).json()
    room, ada = r["room_id"], r["token"]
    api.post(f"/api/rooms/{room}/join", json={"name": "Bob"})
    v = api.get(f"/api/rooms/{room}", headers=h(ada)).json()["game"]["version"]
    api.post(f"/api/rooms/{room}/game/agree", json={"version": v}, headers=h(ada))
    spec = buy_sell().model_dump(mode="json")
    api.put(f"/api/rooms/{room}/game", json=spec, headers=h(ada))
    state = api.get(f"/api/rooms/{room}", headers=h(ada)).json()
    assert not any(p["agreed"] for p in state["participants"])
    assert state["game"]["edited_by"] == "Ada"


def test_only_host_changes_settings(api):
    r = api.post("/api/rooms", json={"name": "Ada"}).json()
    room, ada = r["room_id"], r["token"]
    bob = api.post(f"/api/rooms/{room}/join", json={"name": "Bob"}).json()["token"]
    settings = api.get(f"/api/rooms/{room}", headers=h(ada)).json()["settings"]
    assert api.put(f"/api/rooms/{room}/settings", json=settings, headers=h(bob)).status_code == 403
    assert api.put(f"/api/rooms/{room}/settings", json=settings, headers=h(ada)).status_code == 200


def test_assign_me_lets_one_person_run_both_seats(api):
    r = api.post("/api/rooms", json={"name": "Ada"}).json()
    room, ada = r["room_id"], r["token"]
    spec = buy_sell().model_dump(mode="json")
    spec["protocol"]["max_messages"] = 4
    spec["runs"] = 2
    api.put(f"/api/rooms/{room}/game", json=spec, headers=h(ada))
    v = api.get(f"/api/rooms/{room}", headers=h(ada)).json()["game"]["version"]
    api.post(f"/api/rooms/{room}/game/agree", json={"version": v}, headers=h(ada))

    name = api.post(f"/api/rooms/{room}/seats/assign", headers=h(ada)).json()["name"]
    assert name == "Ada 2"
    assert api.post(f"/api/rooms/{room}/seats/assign", headers=h(ada)).status_code == 409  # full
    state = api.get(f"/api/rooms/{room}", headers=h(ada)).json()
    assert state["game"]["locked"]  # Ada's agreement covers the seat she took after agreeing
    assert [p["owner"] for p in state["participants"]] == [None, "Ada"]

    model = state["settings"]["allowed_models"][0]
    for seat_of, strategy in [(None, "Anchor high."), (name, "Be fair.")]:
        body = {"seat": {"kind": "llm", "model": model, "strategy": strategy}, "seat_of": seat_of}
        assert api.put(f"/api/rooms/{room}/seat", json=body, headers=h(ada)).status_code == 200
        ready = {"ready": True, "seat_of": seat_of}
        assert api.post(f"/api/rooms/{room}/ready", json=ready, headers=h(ada)).status_code == 200
    state = api.get(f"/api/rooms/{room}", headers=h(ada)).json()
    assert state["me"]["seat"]["strategy"] == "Anchor high."
    assert state["controlled"][0]["seat"]["strategy"] == "Be fair." and state["can_start"]

    match_id = api.post(f"/api/rooms/{room}/matches", json={}, headers=h(ada)).json()["match_id"]
    ep = api.get(f"/api/rooms/{room}/matches/{match_id}", headers=h(ada)).json()["episodes"][0]
    assert ep["seats"]["Ada 2"]["strategy"] == "Be fair."  # her own seat, even unrevealed
    assert all(t["reasoning"] == "secret plan" for t in ep["turns"])

    # Only the owner can act as or release the seat; releasing reopens the room.
    bad = {"ready": False, "seat_of": "Ada"}
    assert api.post(f"/api/rooms/{room}/ready", json=bad, headers=h("x")).status_code == 403
    rel = {"seat_of": name}
    assert api.post(f"/api/rooms/{room}/seats/release", json=rel, headers=h(ada)).status_code == 200
    state = api.get(f"/api/rooms/{room}", headers=h(ada)).json()
    assert len(state["participants"]) == 1 and not state["game"]["locked"]
    assert api.post(f"/api/rooms/{room}/join", json={"name": "Bob"}).status_code == 200


class ScriptedAssistant(FakeClient):
    """Plays the assistant from a fixed list of replies; match agents get FakeClient's."""

    def __init__(self, replies):
        super().__init__()
        self.replies = list(replies)

    async def _call(self, model, messages, temperature, max_tokens, **kw):
        if "Parley assistant" in messages[0]["content"]:
            return LLMResponse(text=json.dumps(self.replies.pop(0)), model=model)
        return await super()._call(model, messages, temperature, max_tokens, **kw)


def test_assistant_sets_up_the_room_and_starts_a_match(tmp_path):
    model = "openrouter/mistralai/mistral-nemo"  # in the default allowed list
    agent = {"model": model, "strategy": "Be fair.", "temperature": 0.5}
    replies = [
        {
            "message": "Setting up.",
            "actions": [
                {"tool": "use_template", "args": {"name": "buy_sell"}},
                {"tool": "edit_game", "args": {"changes": {"runs": 2}}},
                {"tool": "assign_me", "args": {}},
                {"tool": "set_agent", "args": {"seat": None, **agent}},
                {"tool": "set_agent", "args": {"seat": "Ada 2", **agent}},
                {"tool": "agree_game", "args": {}},
                {"tool": "set_ready", "args": {"seat": None, "ready": True}},
                {"tool": "set_ready", "args": {"seat": "Ada 2", "ready": True}},
                {"tool": "start_match", "args": {"runs": 2}},
                {"tool": "set_agent", "args": {"seat": "Bob", **agent}},  # not hers
            ],
        },
        {"message": "Started a 2-run match.", "actions": []},
    ]
    api = TestClient(create_app(Store(tmp_path / "db.sqlite"), ScriptedAssistant(replies)))
    r = api.post("/api/rooms", json={"name": "Ada"}).json()
    room, ada = r["room_id"], r["token"]
    chat = {"messages": [{"role": "user", "content": "Set up a car sale and run it"}]}
    out = api.post(f"/api/rooms/{room}/assistant", json=chat, headers=h(ada)).json()

    first, last = out["steps"]
    assert [a["ok"] for a in first["actions"]] == [True] * 9 + [False]
    assert "don't control" in first["actions"][-1]["result"]
    assert last == {"message": "Started a 2-run match.", "actions": []}
    state = api.get(f"/api/rooms/{room}", headers=h(ada)).json()
    assert state["game"]["locked"] and len(state["match_ids"]) == 1
    match = api.get(f"/api/rooms/{room}/matches/{state['match_ids'][0]}", headers=h(ada)).json()
    assert match["status"] == "done" and len(match["episodes"]) == 2
    # Someone outside the room can't use the assistant.
    assert api.post(f"/api/rooms/{room}/assistant", json=chat, headers=h("x")).status_code == 403


def test_assistant_reply_parsing_handles_prose_from_real_replies():
    from parley.api.assistant import parse_reply

    # Prose, then a bare object without a message: the prose is the message.
    r = parse_reply('Both agents are ready.\n\nShall I start?\n{"actions": []}')
    assert r == {"actions": [], "message": "Both agents are ready.\n\nShall I start?"}
    # Prose around a fenced object: the object wins.
    fenced = 'Sure.\n```json\n{"message": "Setting up.", "actions": [{"tool": "x"}]}\n```'
    assert parse_reply(fenced)["actions"] == [{"tool": "x"}]
    assert parse_reply("I've updated the agents for the existing seats.") is None


def test_assistant_reprompts_once_when_it_answers_in_prose(tmp_path):
    replies = [
        "I've set up your agent.",  # claims a change without any action
        {"message": "Saving your agent now.", "actions": [{"tool": "room_state", "args": {}}]},
        {"message": "Done.", "actions": []},
    ]

    class Assistant(ScriptedAssistant):
        async def _call(self, model, messages, temperature, max_tokens, **kw):
            if "Parley assistant" in messages[0]["content"]:
                r = self.replies.pop(0)
                return LLMResponse(text=r if isinstance(r, str) else json.dumps(r), model=model)
            return await super()._call(model, messages, temperature, max_tokens, **kw)

    api = TestClient(create_app(Store(tmp_path / "db.sqlite"), Assistant(replies)))
    r = api.post("/api/rooms", json={"name": "Ada"}).json()
    chat = {"messages": [{"role": "user", "content": "set up my agent"}]}
    out = api.post(f"/api/rooms/{r['room_id']}/assistant", json=chat, headers=h(r["token"]))
    steps = out.json()["steps"]
    assert [s["message"] for s in steps] == ["Saving your agent now.", "Done."]  # prose dropped


def test_assistant_streams_its_trace_as_it_works(tmp_path):
    replies = [
        {"message": "Checking.", "actions": [{"tool": "room_state", "args": {}}]},
        {"message": "All set.", "actions": []},
    ]
    api = TestClient(create_app(Store(tmp_path / "db.sqlite"), ScriptedAssistant(replies)))
    r = api.post("/api/rooms", json={"name": "Ada"}).json()
    chat = {"messages": [{"role": "user", "content": "check"}]}
    url = f"/api/rooms/{r['room_id']}/assistant/stream"
    with api.stream("POST", url, json=chat, headers=h(r["token"])) as resp:
        assert "no-transform" in resp.headers["cache-control"]
        events = [json.loads(line) for line in resp.iter_lines() if line]
    kinds = [e["type"] for e in events]
    assert kinds == ["thinking", "message", "action", "result", "thinking", "message"]
    assert events[2]["tool"] == "room_state" and events[3]["ok"]


def test_assistant_cannot_drop_the_reservations_surplus_scoring_needs(tmp_path):
    roles = [
        {"name": "seller", "private_brief": "Sell."},
        {"name": "buyer", "private_brief": "Buy."},
    ]
    replies = [
        {
            "message": "Setting up.",
            "actions": [
                {"tool": "use_template", "args": {"name": "buy_sell"}},
                {"tool": "edit_game", "args": {"changes": {"roles": roles}}},
            ],
        },
        {"message": "Kept the template's roles.", "actions": []},
    ]
    api = TestClient(create_app(Store(tmp_path / "db.sqlite"), ScriptedAssistant(replies)))
    r = api.post("/api/rooms", json={"name": "Ada"}).json()
    chat = {"messages": [{"role": "user", "content": "car sale"}]}
    out = api.post(f"/api/rooms/{r['room_id']}/assistant", json=chat, headers=h(r["token"]))
    use, bad = out.json()["steps"][0]["actions"]
    assert use["ok"] and not bad["ok"] and "reservation" in bad["result"]
    spec = api.get(f"/api/rooms/{r['room_id']}", headers=h(r["token"])).json()["game"]["spec"]
    assert spec["roles"][0]["private_values"]["reservation"] == 8000  # template untouched


class FileAwareClient(FakeClient):
    """Describes images and summarises files; records what each agent prompt contained."""

    def __init__(self):
        super().__init__()
        self.prompts: list[str] = []

    async def _call(self, model, messages, temperature, max_tokens, **kw):
        content = messages[-1]["content"]
        if isinstance(content, list):  # an image to describe
            assert content[1]["image_url"]["url"].startswith("data:image/png;base64,")
            return LLMResponse(text="A chart: revenue 4.2M in 2025.", model=model)
        if "You prepare the shared context" in content:
            return LLMResponse(text="Revenue was 4.2M in 2025.", model=model)
        self.prompts.append(messages[0]["content"])
        return await super()._call(model, messages, temperature, max_tokens, **kw)


def b64(data: bytes) -> str:
    import base64

    return base64.b64encode(data).decode()


def test_shared_files_are_converted_saved_and_read_by_agents(tmp_path):
    client = FileAwareClient()
    api = TestClient(create_app(Store(tmp_path / "db.sqlite"), client))
    room = api.post("/api/rooms", json={"name": "Ann"}).json()
    rid, tok = room["room_id"], room["token"]

    csv = api.post(
        f"/api/rooms/{rid}/files",
        json={"name": "figures.csv", "mime": "text/csv", "data": b64(b"year,revenue\n2025,4.2M\n")},
        headers=h(tok),
    )
    assert csv.status_code == 200, csv.text
    assert "4.2M" in csv.json()["text"] and len(csv.json()["sha256"]) == 64
    img = api.post(
        f"/api/rooms/{rid}/files",
        json={"name": "chart.png", "mime": "image/png", "data": b64(b"\x89PNG fake")},
        headers=h(tok),
    ).json()
    assert img["text"] == "A chart: revenue 4.2M in 2025."

    summary = api.post(
        f"/api/rooms/{rid}/files/summary", json={"files": [csv.json()]}, headers=h(tok)
    )
    assert summary.json() == {"text": "Revenue was 4.2M in 2025."}

    spec = GameSpec.model_validate(buy_sell().model_dump() | {"files": [csv.json(), img]})
    put = api.put(f"/api/rooms/{rid}/game", json=spec.model_dump(), headers=h(tok))
    assert put.status_code == 200
    saved = api.get(f"/api/rooms/{rid}", headers=h(tok)).json()["game"]["spec"]
    assert [f["name"] for f in saved["files"]] == ["figures.csv", "chart.png"]
    assert "### chart.png\nA chart" in spec.full_context()


def test_file_errors_are_explained(api):
    room = api.post("/api/rooms", json={"name": "Ann"}).json()
    rid, tok = room["room_id"], room["token"]
    url = f"/api/rooms/{rid}/files"
    empty = api.post(url, json={"name": "a.txt", "data": ""}, headers=h(tok))
    assert empty.status_code == 400 and "empty" in empty.json()["detail"]
    assert api.post(url, json={"name": "a.txt", "data": "%%"}, headers=h(tok)).status_code == 400
    stranger = api.post(url, json={"name": "a.txt", "data": b64(b"hi")})
    assert stranger.status_code in (401, 403)


def test_research_writes_up_web_results_for_the_shared_context(tmp_path):
    class WebClient(FakeClient):
        async def _call(self, model, messages, temperature, max_tokens, **kw):
            assert model.endswith(":online")
            assert "Topic to research: PET resin prices" in messages[0]["content"]
            assert "Two firms renew a contract." in messages[0]["content"]
            return LLMResponse(text="Prices rose 11% [src](https://example.com).", model=model)

    api = TestClient(create_app(Store(tmp_path / "db.sqlite"), WebClient()))
    room = api.post("/api/rooms", json={"name": "Ann"}).json()
    url = f"/api/rooms/{room['room_id']}/research"
    body = {"topic": "PET resin prices", "context": "Two firms renew a contract."}
    r = api.post(url, json=body, headers=h(room["token"]))
    assert r.json() == {"text": "Prices rose 11% [src](https://example.com)."}
    blank = api.post(url, json={"topic": "  "}, headers=h(room["token"]))
    assert blank.status_code == 400
