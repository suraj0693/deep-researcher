from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Memory:
    step: List[str] = None
    plan: List[Dict] = None
