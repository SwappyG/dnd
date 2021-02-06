from __future__ import annotations
from typing import FrozenSet, Dict
import dataclasses
from dnd.utils.dataclass_types import DataClassBase


@dataclasses.dataclass(frozen=True)
class Job(DataClassBase):
    name: str
    desc: str
    features: FrozenSet[str]
    options: FrozenSet[str]

    @staticmethod
    def from_json(j: Dict) -> Job:
        return Job(name=j['name'],
                   features=frozenset([] if j['features'] is None else j['features']),
                   options=frozenset([] if j['options'] is None else j['options']),
                   desc=j['desc'])
