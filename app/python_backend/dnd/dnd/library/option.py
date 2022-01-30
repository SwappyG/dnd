from __future__ import annotations
from typing import Tuple, FrozenSet, Dict, NamedTuple
import dataclasses
from dnd.utils.dataclass_types import DataClassBase
from dnd.utils.json_types import JsonFrozenSet


class OptionReply(NamedTuple):
    num_options: int
    features: FrozenSet[str]


@dataclasses.dataclass(frozen=True)
class Option(DataClassBase):
    name: str
    desc: str
    features: JsonFrozenSet[str]
    prereq_features: JsonFrozenSet[str]
    unlock_levels: Tuple[int]

    @staticmethod
    def from_json(j: Dict) -> Option:
        return Option(name=j['name'],
                      features=JsonFrozenSet([] if j['features'] is None else j['features']),
                      prereq_features=JsonFrozenSet([] if j['prereq_features'] is None else j['prereq_features']),
                      unlock_levels=tuple([] if j['unlock_levels'] is None else j['unlock_levels']),
                      desc=j['desc'])

    def has_feature(self, feature_name: str) -> bool:
        return feature_name in self.features

    def num_unlocks_at_level(self, level: int) -> int:
        return len([ii for ii in self.unlock_levels if (ii == level)])

    def remaining_features(self, already_selected_features: FrozenSet[str]) -> FrozenSet[str]:
        return self.features.difference(already_selected_features)

    def get_feature_options_at_level(self, level: int, already_selected_features: FrozenSet[str]) -> OptionReply:
        if not self.prereq_features.issubset(already_selected_features):
            return OptionReply(num_options=0, features=frozenset({}))

        num_unlocks = self.num_unlocks_at_level(level)
        if num_unlocks == 0:
            return OptionReply(num_options=0, features=frozenset({}))

        return OptionReply(num_options=num_unlocks, features=self.remaining_features(already_selected_features))
