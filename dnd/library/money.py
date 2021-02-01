from __future__ import annotations
from typing import Dict
from pprint import pformat
from dnd.utils.exceptions import raise_if_true
import dataclasses


@dataclasses.dataclass(frozen=True)
class Money:
    gold: int
    silver: int
    value: dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'value', self.gold + self.silver / 10.0)

    def __add__(self, other: Money) -> Money:
        v = self.value + other.value
        return Money(v // 10, v % 10)

    def __sub__(self, other: Money) -> Money:
        v = self.value - other.value
        raise_if_true(v < 0, "money can't be negative")

        return Money(v // 10, v % 10)

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.asdict())
