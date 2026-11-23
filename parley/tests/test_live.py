"""Live seats: outside agents (Claude Code, Grok CLI, ...) play their turns through the API."""

import asyncio

import pytest
from fastapi.testclient import TestClient

from parley.agents.live import LiveAgent, Mailbox
from parley.api import rooms as R
from parley.api.app import create_app
from parley.core.engine import run_episode
from parley.core.types import Action, Turn
from parley.storage import Store
from parley.templates import work_talk

from .test_api import FakeClient, h


@pytest.fixture
def api(tmp_path):
    with TestClient(create_app(Store(tmp_path / "db.sqlite"), FakeClient())) as client:
        yield client


def turn(api, room, token, **body):
    assert api.post(f"/api/rooms/{room}/turn", json=body, headers=h(token)).status_code == 200


def wait(api, room, token, seconds=5):
    return api.get(f"/api/rooms/{room}/turn", params={"wait": seconds}, headers=h(token)).json()


def test_two_live_agents_talk_and_agree_in_writing(api, tmp_path):
    opened = api.post(
        "/api/talks",
        json={"goal": "Agree the JSON shape of /users", "name": "Ada", "client": "claude-code"},
    ).json()
    room, ada = opened["room_id"], opened["token"]
    assert wait(api, room, ada, 0)["status"] == "not_started"  # Bob isn't here yet

    joined = api.post(
        f"/api/rooms/{room}/talk/join", json={"name": "Bob", "client": "grok-cli"}
    ).json()
    bob = joined["token"]
    assert joined["match_id"]  # the second agent to arrive starts the talk

    first = wait(api, room, ada)
    assert first["status"] == "your_turn" and first["role"] == "A"
    assert "Agree the JSON shape of /users" in first["prompt"]
    assert "agreement (text" in first["prompt"]
    assert "Reply format" not in first["prompt"]  # live agents answer with parley_say
    again = api.post(f"/api/rooms/{room}/matches", json={}, headers=h(ada))
    assert again.status_code == 409  # one talk at a time
    early = api.post(f"/api/rooms/{room}/turn", json={"message": "hi"}, headers=h(bob))
    assert early.status_code == 409  # not Bob's turn

    turn(
        api,
        room,
        ada,
        message="Proposal attached.",
        action={"type": "offer", "terms": {"agreement": "id: int, name: str"}},
        reasoning="keep it small",
    )
    assert wait(api, room, bob)["standing_offer"]["terms"] == {"agreement": "id: int, name: str"}

    turn(api, room, bob, message="Sure", action={"type": "offer", "terms": {"agreement": ""}})
    refused = wait(api, room, bob)  # empty text is refused and comes back as feedback
    assert refused["status"] == "your_turn" and "non-empty text" in refused["feedback"]
    turn(api, room, bob, message="Deal.", action="accept")

    ended = wait(api, room, ada)
    assert ended["status"] == "ended"
    assert ended["outcome"]["end_reason"] == "accept"
    assert ended["outcome"]["deal"]["terms"] == {"agreement": "id: int, name: str"}

    later = wait(api, room, bob)  # after the talk, from the store once the mailboxes are gone
    assert later["status"] == "ended" and later["outcome"]["end_reason"] == "accept"

    match_id = joined["match_id"]
    episodes = api.get(f"/api/rooms/{room}/matches/{match_id}", headers=h(ada)).json()["episodes"]
    assert len(episodes) == 1  # one talk: no reruns or role swaps
    assert episodes[0]["seats"]["Bob"]["client"] == "grok-cli"
    assert episodes[0]["turns"][0]["reasoning"] == "keep it small"


def test_live_rooms_play_once_without_a_judge():
    room, ada = R.open_talk("Divide the migration work", "Ada", "claude-code")
    assert room.settings.judge_model is None
    assert not room.locked
    bob = R.join_talk(room, "Bob")
    assert room.locked and not R.start_problems(room)
    R.unlock(room, bob)  # someone watching edits the game; agreeing again needs no "ready"
    R.agree(room, ada, room.version)
    R.agree(room, bob, room.version)
    assert not R.start_problems(room)
    cfg = R.match_config(room, runs=5)
    assert (cfg.runs, cfg.swap_roles, cfg.parallel, cfg.episode_attempts) == (1, False, 1, 1)


def test_open_talk_needs_a_goal():
    with pytest.raises(R.RoomError):
        R.open_talk("  ", "Ada")


async def test_a_live_agent_that_never_answers_walks_away():
    spec = work_talk("anything")
    agents = {"A": LiveAgent(Mailbox(), timeout=0.01), "B": LiveAgent(Mailbox(), timeout=5)}
    turns, outcome = await run_episode(spec, agents)
    assert outcome.end_reason == "walk_away"
    assert turns[0].message == "(timed out)"


async def test_mailbox_hands_the_reply_to_the_engine():
    box = Mailbox()
    agent = LiveAgent(box, timeout=5)
    spec = work_talk("anything")

    async def answer():
        await box.wait(5)
        assert box.pending.view.role == "A"
        box.answer(Turn(role="A", message="bye", action=Action(type="walk_away")))

    other = LiveAgent(Mailbox(), timeout=5)
    episode = run_episode(spec, {"A": agent, "B": other})
    (turns, outcome), _ = await asyncio.gather(episode, answer())
    assert outcome.end_reason == "walk_away" and turns[0].message == "bye"
    assert box.pending is None


def test_a_ready_talk_that_never_started_starts_on_the_next_poll(api, tmp_path):
    room, ada = R.open_talk("Agree the release date", "Ada")
    R.join_talk(room, "Bob")
    Store(tmp_path / "db.sqlite").save_room(room.id, room.model_dump_json())
    assert wait(api, room.id, ada)["status"] == "your_turn"


def test_a_failed_talk_ends_for_the_live_agents(api, monkeypatch):
    async def broken(*args, **kwargs):
        raise RuntimeError("provider down")

    monkeypatch.setattr("parley.api.app.run_match", broken)
    room = api.post("/api/talks", json={"goal": "anything", "name": "Ada"}).json()
    api.post(f"/api/rooms/{room['room_id']}/talk/join", json={"name": "Bob"})
    ended = wait(api, room["room_id"], room["token"])
    assert ended["status"] == "ended" and ended["outcome"]["end_reason"] == "error"


async def test_an_answered_turn_is_not_handed_out_again():
    box = Mailbox()
    agent = LiveAgent(box, timeout=5)
    spec = work_talk("anything")
    task = asyncio.create_task(run_episode(spec, {"A": agent, "B": LiveAgent(Mailbox(), 0.01)}))
    await box.wait(5)
    assert box.answer(Turn(role="A", message="hi"))
    assert box.open_turn is None  # answered, though the engine hasn't picked it up yet
    assert not box.answer(Turn(role="A", message="again"))
    await task
