from __future__ import annotations
from typing import FrozenSet, Optional, Dict, Any
import dataclasses
from dnd.utils.dataclass_types import DataClassBase


@dataclasses.dataclass(frozen=True)
class Feature(DataClassBase):
    name: str
    desc: str
    effects: FrozenSet[str]
    prereq_features: FrozenSet[str]
    unlock_level: Optional[int]

    @staticmethod
    def from_json(j: Dict) -> Feature:
        return Feature(name=j['name'],
                       effects=frozenset([] if j['effects'] is None else j['effects']),
                       prereq_features=frozenset([] if j['prereq_features'] is None else j['prereq_features']),
                       unlock_level=int(j['unlock_level']),
                       desc=j['desc'])

    def is_unlocked(self, level: int, already_learned_features: FrozenSet[str]) -> bool:
        """
        Returns T/F if this feature would be unlocked given level + known features
        """
        if level < self.unlock_level:
            return False

        return self.prereq_features.issubset(already_learned_features)
