from pprint import pformat
import dataclasses
from typing import Dict, Optional, Tuple
from enum import Enum
from dnd.utils.json_types import JsonEnum


class ItemType(JsonEnum):
    BASIC = 0
    ARMOR = 1
    WEAPON = 2


@dataclasses.dataclass(frozen=True)
class Item:
    name: str
    desc: str
    item_type: ItemType = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'item_type', ItemType.BASIC)

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.asdict())


class ArmorWeight(JsonEnum):
    LIGHT = 0
    MEDIUM = 1
    HEAVY = 2


class ArmorType(JsonEnum):
    HEAD = 0
    BODY = 1
    SHOULDER = 2
    ARMS = 3
    LEGS = 4
    FEET = 5
    HANDS = 6
    SHIELD = 7


@dataclasses.dataclass(frozen=True)
class Armor(Item):
    armor_type: ArmorType
    ac: int
    weight: ArmorWeight
    minimum_strength: int
    has_stealth_disadvantage: bool
    item_type: ItemType = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'item_type', ItemType.ARMOR)

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.asdict())


class WeaponCategory(JsonEnum):
    SIMPLE = 0
    MARTIAL = 1


class WeaponType(JsonEnum):
    MELEE = 0
    RANGED = 1


class WeightCategory(JsonEnum):
    NONE = 0
    LIGHT = 1
    HEAVY = 2


class DamageType(JsonEnum):
    SLASHING = 0
    PIERCING = 1
    BLUDGEONING = 2


@dataclasses.dataclass(frozen=True)
class Weapon(Item):
    weapon_category: WeaponCategory
    weapon_type: WeaponType
    damage_die: int
    num_die: int
    bonus_damage: int
    damage_type: DamageType
    weapon_range: Tuple[int, int]
    hit_bonus: int
    weight: float
    weight_category: WeightCategory = WeightCategory.NONE
    two_handed: bool = False
    finesse: bool = False
    thrown: bool = False
    loading: bool = False
    ammunition: bool = False

    item_type: ItemType = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'item_type', ItemType.WEAPON)

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.asdict())
