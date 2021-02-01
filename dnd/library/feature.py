from typing import Set, Optional, NamedTuple, Tuple, Dict
from pprint import pformat
import dataclasses


@dataclasses.dataclass(frozen=True)
class Feature:
    name: str
    desc: str
    effects: Set[str]
    prereq_features: Set[str]
    unlock_level: Optional[int]

    def is_unlocked(self, level: int, already_learned_features: Set[str]) -> bool:
        """
        Returns T/F if this feature would be unlocked given level + known features
        """
        if level < self.unlock_level:
            return False

        return self.prereq_features.issubset(already_learned_features)

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.asdict())
