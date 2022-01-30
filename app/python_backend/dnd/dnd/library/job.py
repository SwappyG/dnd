from __future__ import annotations
from typing import FrozenSet, Dict
import dataclasses
from dnd.utils.dataclass_types import DataClassBase
from dnd.utils.json_types import JsonFrozenSet


@dataclasses.dataclass(frozen=True)
class Job(DataClassBase):
    name: str
    desc: str
    features: JsonFrozenSet[str]
    options: JsonFrozenSet[str]

    @staticmethod
    def from_json(j: Dict) -> Job:
        return Job(name=j['name'],
                   features=JsonFrozenSet([] if j['features'] is None else j['features']),
                   options=JsonFrozenSet([] if j['options'] is None else j['options']),
                   desc=j['desc'])
