from __future__ import annotations
from typing import FrozenSet, Dict, Optional
from dnd.utils.json_types import JsonEnum
from dnd.utils.dataclass_types import DataClassBase
import dataclasses


class SpellSchool(JsonEnum):
    CONJURATION = 0
    ABJURATION = 1
    EVOCATION = 2
    NECROMANCY = 3
    TRANSMUTATION = 4
    DIVINATION = 5
    ILLUSION = 6
    ENCHANTMENT = 7


class SavingThrowType(JsonEnum):
    STR = 0
    DEX = 1
    CON = 2
    INT = 3
    WIS = 4
    CHA = 5
    ATK = 6
    OTH = 7


@dataclasses.dataclass(frozen=True)
class Spell(DataClassBase):
    name: str
    level: int
    desc: str
    school: SpellSchool
    casting_time: str
    casting_range: str
    casting_targets: str
    duration: str
    saving_throw: Optional[SavingThrowType]
    is_conc: bool  # what is this?
    is_ritual: bool
    mats: str  # what is this?
    cost: str
    valid_jobs: FrozenSet[str]

    @staticmethod
    def from_json(j: Dict) -> Spell:
        return Spell(name=j['name'],
                     level=j['level'],
                     desc=j['desc'],
                     school=SpellSchool[j['school']],
                     casting_time=j['casting_time'],
                     casting_range=j['casting_range'],
                     casting_targets=j['casting_targets'],
                     duration=j['duration'],
                     saving_throw=None if j['saving_throw'] is None else SavingThrowType[j['saving_throw']],
                     is_conc=j['is_conc'],
                     is_ritual=j['is_ritual'],
                     mats=j['mats'],
                     cost=j['cost'],
                     valid_jobs=j['valid_jobs'])
