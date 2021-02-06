from __future__ import annotations
from dnd.utils.exceptions import raise_if_true
import dataclasses
from dnd.utils.dataclass_types import DataClassBase
from typing import Dict


@dataclasses.dataclass(frozen=True)
class Money(DataClassBase):
    gold: int
    silver: int
    value: float = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'value', self.gold + self.silver / 10.0)

    @staticmethod
    def from_value(v: float) -> Money:
        raise_if_true(v < 0, "money can't be negative")
        g = int(v // 1)
        s = round((v - g) * 10)
        return Money(g, s)

    @staticmethod
    def from_json(j: Dict) -> Money:
        return Money(gold=j['gold'], silver=j['silver'])

    def __add__(self, other: Money) -> Money:
        return self.from_value(self.value + other.value)

    def __sub__(self, other: Money) -> Money:
        return self.from_value(self.value - other.value)
