from __future__ import annotations
import dataclasses
from dnd.utils.dataclass_types import DataClassBase
from typing import Dict, Any


@dataclasses.dataclass(frozen=True)
class Effect(DataClassBase):
    name: str
    effect_type: str
    duration: str
    desc: str

    @staticmethod
    def from_json(j: Dict) -> Effect:
        return Effect(name=j['name'],
                      effect_type=j['effect_type'],
                      duration=j['duration'],
                      desc=j['desc'])
