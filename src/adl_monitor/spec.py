from dataclasses import dataclass, field
from typing import List

@dataclass
class LTLRule:
    name: str
    formula: str
    description: str = ""

@dataclass
class STLRule:
    name: str
    formula: str
    description: str = ""

@dataclass
class ADLSpec:
    name: str
    propositions: List[str] = field(default_factory=list)
    ltl_rules: List[LTLRule] = field(default_factory=list)
    stl_rules: List[STLRule] = field(default_factory=list)