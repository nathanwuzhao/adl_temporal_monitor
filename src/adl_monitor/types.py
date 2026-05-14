from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, Literal

Severity = Literal["info", "warning", "error", "critical"]

@dataclass(frozen=True)
class Observation:
    """
    
    single timestamped symbolic observation. 
    boolean propositions for ltl, real-valued signals for stl

    example:
        Observation(
            t=12.0,
            props={
                "water_added": True,
                "pot_on_stove": True,
                "stove_on": False,
            },
            signals={
                "temperature_c": 22.5,
                "stove_confidence": 0.91,
            },
        )

    """

    t: float
    props: dict[str, bool] = field(default_factory=dict)
    signals: dict[str, float] = field(default_factory=dict)
    meta: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Violation:
    t: float
    rule_name: str
    message: str
    severity: Severity = "warning"
    robustness: float | None = None
    details: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class RuleResult:
    rule_name: str
    satisfied: bool
    violations: list[Violation] = field(default_factory=list)
    robustness: float | None = None

@dataclass(frozen=True)
class MonitorResult:
    rule_results: list[RuleResult] = field(default_factory=list)

    @property
    def violations(self) -> list[Violation]:
        return [
            violation
            for result in self.rule_results
            for violation in result.violations
        ]

    @property
    def satisfied(self) -> bool:
        return len(self.violations) == 0