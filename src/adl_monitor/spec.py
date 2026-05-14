from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from adl_monitor.types import Severity

LTLRuleKind = Literal[
    "precedence",
    "safety",
    "eventually",
    "response",
]

STLRuleKind = Literal[
    "eventually_within",
    "duration_limit",
    "timed_safety",
]

@dataclass(frozen=True)
class LTLRule:
    """
    precedence:
        before must become true before after becomes true

    safety:
        forbidden propositions must never be true at the same time

    eventually:
        target must become true at least once

    response:
        if trigger becomes true, target must eventually become true
    """

    name: str
    kind: LTLRuleKind
    description: str = ""
    severity: Severity = "warning"

    # precedence
    before: str | None = None
    after: str | None = None

    # safety
    forbidden: tuple[str, ...] = field(default_factory=tuple)

    # eventually 
    target: str | None = None

    # response 
    trigger: str | None = None


@dataclass(frozen=True)
class STLRule:
    name: str
    kind: STLRuleKind
    description: str = ""
    severity: Severity = "warning"

    # eventually_within:
    # if trigger becomes true, target must become true within horizon seconds
    trigger: str | None = None
    target: str | None = None
    horizon_s: float | None = None

    # duration_limit / timed_safety:
    # condition must not persist longer than max_duration_s
    condition: tuple[str, ...] = field(default_factory=tuple)
    max_duration_s: float | None = None

    # for rtamt
    formula: str | None = None


@dataclass(frozen=True)
class ADLSpec:
    """
    formal specification for an ADL task

    defines:
        - boolean propositions used by LTL style rules
        - real valued signals used by STL style rules
        - LTL style task ordering/safety rules
        - STL style timing/robustness rules
    """

    name: str
    description: str = ""
    propositions: tuple[str, ...] = field(default_factory=tuple)
    signals: tuple[str, ...] = field(default_factory=tuple)
    ltl_rules: tuple[LTLRule, ...] = field(default_factory=tuple)
    stl_rules: tuple[STLRule, ...] = field(default_factory=tuple)

    def validate(self) -> None:
        prop_set = set(self.propositions)

        for rule in self.ltl_rules:
            referenced = _referenced_ltl_props(rule)
            missing = referenced - prop_set
            if missing:
                raise ValueError(
                    f"LTL rule '{rule.name}' references undeclared propositions: "
                    f"{sorted(missing)}"
                )

        for rule in self.stl_rules:
            referenced = _referenced_stl_props(rule)
            missing = referenced - prop_set
            if missing:
                raise ValueError(
                    f"STL rule '{rule.name}' references undeclared propositions: "
                    f"{sorted(missing)}"
                )


def _referenced_ltl_props(rule: LTLRule) -> set[str]:
    refs: set[str] = set()

    for value in [
        rule.before,
        rule.after,
        rule.target,
        rule.trigger,
    ]:
        if value is not None:
            refs.add(value)

    refs.update(rule.forbidden)
    return refs


def _referenced_stl_props(rule: STLRule) -> set[str]:
    refs: set[str] = set()

    for value in [
        rule.trigger,
        rule.target,
    ]:
        if value is not None:
            refs.add(value)

    refs.update(rule.condition)
    return refs