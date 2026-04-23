from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class Observation:
    t: float
    props: Dict[str, Any]

    