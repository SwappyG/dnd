from typing import Set, Dict, Optional
from pprint import pformat
from dnd.utils.json_types import JsonEnum
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
class Spell:
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
    valid_jobs: Set[str]

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.as_dict())
