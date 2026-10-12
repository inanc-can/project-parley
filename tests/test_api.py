import json

import pytest
from fastapi.testclient import TestClient

from parley.api.app import create_app
from parley.llm.client import LLMClient, LLMResponse
from parley.storage import Store
from parley.templates import buy_sell


class FakeClient(LLMClient):
    async def _call(self, model, messages, temperature, max_tokens):
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
