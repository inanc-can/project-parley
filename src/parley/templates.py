"""Predefined games. Each is a starting point a room can edit freely."""

from collections.abc import Callable

from parley.core.spec import (
    Alternating,
    DealField,
    GameSpec,
    MatrixScoring,
    Role,
    SimultaneousRounds,
    SurplusScoring,
    ValuationsScoring,
)


def ultimatum(pie: int = 100) -> GameSpec:
    return GameSpec(
        title="Ultimatum game",
        shared_context=(
            f"There are {pie} points to split between a proposer and a responder. "
            "The proposer makes exactly one offer saying how many points they keep. "
            "The responder either accepts it, and both get the proposed split, "
            "or rejects it, and both get nothing. There is no second round."
        ),
        roles=[
            Role(name="proposer", private_brief="You are the proposer. Make one offer."),
            Role(
                name="responder",
                private_brief="You are the responder. Accept or reject the offer.",
                private_values={"reservation": pie},
            ),
        ],
        deal_fields=[
            DealField(
                name="proposer_share",
                type="integer",
                min=0,
                max=pie,
                description="points the proposer keeps; the responder gets the rest",
            )
        ],
        scoring=SurplusScoring(
            field="proposer_share", direction={"proposer": "up", "responder": "down"}
        ),
        protocol=Alternating(max_messages=2, reject_ends=True),
        allowed_actions={"proposer": ["offer"], "responder": ["accept", "reject"]},
        runs=10,
    )


PRISONERS_DILEMMA = {
    "cooperate,cooperate": (3, 3),
    "cooperate,defect": (0, 5),
    "defect,cooperate": (5, 0),
    "defect,defect": (1, 1),
}


def iterated_prisoners_dilemma(rounds: int = 10, talk_messages: int = 2) -> GameSpec:
    return GameSpec(
        title="Iterated prisoner's dilemma",
        shared_context=(
            f"You play {rounds} rounds with the same partner. Before each round you may talk; "
            "then both choose to cooperate or defect at the same time. Points per round: "
            "both cooperate 3 each; both defect 1 each; if one defects and the other "
            "cooperates, the defector gets 5 and the cooperator 0. Maximise your own total."
        ),
        roles=[Role(name="player_a"), Role(name="player_b")],
        scoring=MatrixScoring(payoffs=PRISONERS_DILEMMA),
        protocol=SimultaneousRounds(rounds=rounds, talk_messages=talk_messages),
        runs=10,
    )


def buy_sell(seller_min: float = 8000, buyer_max: float = 9500) -> GameSpec:
    return GameSpec(
        title="Used car sale",
        shared_context=(
            "A 2015 Honda Civic with 90,000 km is for sale. The seller and a buyer "
            "negotiate the price. If no price is agreed, nobody trades."
        ),
        roles=[
            Role(
                name="seller",
                private_brief=f"You are the seller. You will not sell below ${seller_min:,.0f}. "
                "Your profit is the price minus that amount.",
                private_values={"reservation": seller_min},
            ),
            Role(
                name="buyer",
                private_brief=f"You are the buyer. You will not pay more than ${buyer_max:,.0f}. "
                "Your gain is that amount minus the price.",
                private_values={"reservation": buyer_max},
            ),
        ],
        deal_fields=[DealField(name="price", min=0, description="sale price in dollars")],
        scoring=SurplusScoring(field="price", direction={"seller": "up", "buyer": "down"}),
        protocol=Alternating(max_messages=20),
        runs=10,
    )


def multi_issue_trade() -> GameSpec:
    items = {"books": 3, "hats": 2, "balls": 1}
    values = {
        "alex": {"books": 1, "hats": 3, "balls": 1},
        "blair": {"books": 2, "hats": 1, "balls": 2},
    }

    def brief(name):
        v = values[name]
        return (
            f"You are {name}. Each book is worth {v['books']}, each hat {v['hats']} and "
            f"the ball {v['balls']} points to you. The other side may value them differently. "
            "With no deal, you get 0."
        )

    return GameSpec(
        title="Multi-issue trade",
        shared_context=(
            "Two people split 3 books, 2 hats and 1 ball. Every item must go to someone. "
            "Offers say how many of each item alex receives; blair gets the rest."
        ),
        roles=[
            Role(name="alex", private_brief=brief("alex"), private_values=values["alex"]),
            Role(name="blair", private_brief=brief("blair"), private_values=values["blair"]),
        ],
        deal_fields=[
            DealField(name=i, type="integer", min=0, max=n, description=f"{i} alex receives")
            for i, n in items.items()
        ],
        scoring=ValuationsScoring(items=items, allocation_role="alex"),
        protocol=Alternating(max_messages=12),
        runs=10,
    )


TEMPLATES: dict[str, Callable[[], GameSpec]] = {
    "ultimatum": ultimatum,
    "ipd": iterated_prisoners_dilemma,
    "buy_sell": buy_sell,
    "multi_issue_trade": multi_issue_trade,
}
