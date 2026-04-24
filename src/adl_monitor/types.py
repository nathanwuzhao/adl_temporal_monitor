from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class Observation:
    t: float
    props: Dict[str, Any]

@dataclass
class Violation:
    t: float
    rule_name: str
    message: str
    severity: str = "warning"