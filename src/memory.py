from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Memory:
    step: List[Dict] = None
    plan: List[Dict] = None


@dataclass
class StepMemory:
    pass
