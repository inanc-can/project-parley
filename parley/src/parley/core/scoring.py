"""Turn a deal (or a sequence of simultaneous moves) into payoffs."""

from typing import Any

from parley.core.spec import (
    DealField,
    GameSpec,
    MatrixScoring,
    Scoring,
    SurplusScoring,
    ValuationsScoring,
)


class InvalidTerms(ValueError):
    pass


def validate_terms(fields: list[DealField], scoring: Scoring, terms: dict[str, Any]) -> dict:
    """Check offer terms against the deal fields; return them with numbers coerced and text
    stripped."""
    names = {f.name for f in fields}
    extra = set(terms) - names
    if extra:
        raise InvalidTerms(f"unknown deal field(s): {sorted(extra)}; allowed: {sorted(names)}")
    clean: dict[str, Any] = {}
    for f in fields:
        if f.name not in terms:
            raise InvalidTerms(f"missing deal field {f.name!r}")
        v = terms[f.name]
        if f.type == "text":
            if not isinstance(v, str) or not v.strip():
                raise InvalidTerms(f"{f.name!r} must be non-empty text, got {v!r}")
            if len(v) > f.max_length:
                raise InvalidTerms(f"{f.name!r} must be at most {f.max_length} characters")
            clean[f.name] = v.strip()
            continue
        if isinstance(v, bool) or not isinstance(v, int | float):
            raise InvalidTerms(f"{f.name!r} must be a number, got {v!r}")
        if f.type == "integer":
            if float(v) != int(v):
                raise InvalidTerms(f"{f.name!r} must be a whole number, got {v!r}")
            v = int(v)
        if f.min is not None and v < f.min:
            raise InvalidTerms(f"{f.name!r} must be at least {f.min}, got {v}")
        if f.max is not None and v > f.max:
            raise InvalidTerms(f"{f.name!r} must be at most {f.max}, got {v}")
        clean[f.name] = v
    if isinstance(scoring, ValuationsScoring):
        for item, total in scoring.items.items():
            if item in clean and not 0 <= clean[item] <= total:
                raise InvalidTerms(f"{item!r} must be between 0 and {total}")
    return clean


def role_payoff(
    scoring: Scoring, role: str, private_values: dict[str, float], terms: dict[str, Any] | None
) -> float | None:
    """Payoff for one role from a deal (terms) or no deal (None). None if not computable."""
    if isinstance(scoring, SurplusScoring):
        reservation = private_values.get("reservation", 0.0)
        if terms is None:
            return private_values.get("no_deal", 0.0)
        value = terms[scoring.field]
        return value - reservation if scoring.direction[role] == "up" else reservation - value
    if isinstance(scoring, ValuationsScoring):
        if terms is None:
            return private_values.get("no_deal", 0.0)
        total = 0.0
        for item, count in scoring.items.items():
            mine = terms[item] if role == scoring.allocation_role else count - terms[item]
            total += mine * private_values.get(item, 0.0)
        return total
    return None


def deal_payoffs(spec: GameSpec, terms: dict[str, Any] | None) -> dict[str, float]:
    out = {}
    for r in spec.roles:
        p = role_payoff(spec.scoring, r.name, r.private_values, terms)
        if p is not None:
            out[r.name] = p
    return out


def matrix_payoffs(spec: GameSpec, rounds: list[dict[str, str]]) -> dict[str, float]:
    """Sum matrix payoffs over rounds; each round maps role -> move."""
    assert isinstance(spec.scoring, MatrixScoring)
    names = spec.role_names()
    totals = dict.fromkeys(names, 0.0)
    for moves in rounds:
        key = ",".join(moves[n] for n in names)
        for n, p in zip(names, spec.scoring.payoffs[key], strict=True):
            totals[n] += p
    return totals
