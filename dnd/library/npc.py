from enum import Enum
import dataclasses
from typing import List, Dict, Any
from pprint import pformat


@dataclasses.dataclass
class NPC:
    name: str
    gender: str
    age: str
    race: str
    location: str
    status: str
    affiliations: List[str]
    backgrounds: List[str]
    defining_moments: List[str]

    def as_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.as_dict())
