from __future__ import annotations
import dataclasses
from typing import FrozenSet, Dict
from dnd.utils.dataclass_types import DataClassBase
from dnd.utils.json_types import JsonFrozenSet


@dataclasses.dataclass(frozen=True)
class NPC(DataClassBase):
    name: str
    gender: str
    age: int
    race: str
    location: str
    status: str
    background: str
    defining_moments: JsonFrozenSet[str]
    affiliations: JsonFrozenSet[str]

    @staticmethod
    def from_json(j: Dict) -> NPC:
        return NPC(name=j['name'],
                   gender=j['gender'],
                   age=int(j['age']),
                   race=j['race'],
                   location=j['location'],
                   status=j['status'],
                   background=j['background'],
                   defining_moments=JsonFrozenSet([] if j['defining_moments'] is None else j['defining_moments']),
                   affiliations=JsonFrozenSet([] if j['affiliations'] is None else j['affiliations']))

    def update_location(self, location: str):
        dataclasses.replace(self, location=location)

    def update_status(self, status: str):
        dataclasses.replace(self, status=status)

    def remove_affiliation(self, affiliation: str):
        dataclasses.replace(self, affiliations=JsonFrozenSet(self.affiliations.difference({affiliation})))

    def add_affiliation(self, affiliation: str):
        dataclasses.replace(self, affiliations=JsonFrozenSet(self.affiliations.union({affiliation})))

    def add_defining_moment(self, defining_moment: str):
        dataclasses.replace(self, defining_moments=JsonFrozenSet(self.defining_moments.union({defining_moment})))
