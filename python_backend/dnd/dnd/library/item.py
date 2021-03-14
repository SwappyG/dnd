from __future__ import annotations
import dataclasses
from typing import Tuple, Dict
from dnd.utils.json_types import JsonEnum
from dnd.utils.dataclass_types import DataClassBase


class ItemType(JsonEnum):
    BASIC = 0
    ARMOR = 1
    WEAPON = 2


@dataclasses.dataclass(frozen=True)
class Item(DataClassBase):
    name: str
    desc: str
    item_type: ItemType = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'item_type', ItemType.BASIC)

    @staticmethod
    def from_json(j: Dict) -> Item:
        return Item(name=j['name'],
                    desc=j['desc'])


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

    @staticmethod
    def from_json(j: Dict) -> Armor:
        return Armor(name=j['name'],
                     desc=j['desc'],
                     weight=ArmorWeight[j['weight']],
                     armor_type=ArmorType[j['armor_type']],
                     ac=int(j['ac']),
                     minimum_strength=int(j['minimum_strength']),
                     has_stealth_disadvantage=j['has_stealth_disadvantage'])

    def __post_init__(self):
        object.__setattr__(self, 'item_type', ItemType.ARMOR)


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

    @staticmethod
    def from_json(j: Dict) -> Weapon:
        return Weapon(name=j['name'],
                      desc=j['desc'],
                      weapon_category=WeaponCategory[j['weapon_category']],
                      weapon_type=WeaponType[j['weapon_type']],
                      damage_die=int(j['damage_die']),
                      num_die=int(j['num_die']),
                      bonus_damage=int(j['bonus_damage']),
                      damage_type=DamageType[j['damage_type']],
                      weapon_range=tuple(j['weapon_range']),
                      hit_bonus=int(j['hit_bonus']),
                      weight=float(j['weight']),
                      weight_category=WeightCategory[j['weight_category']],
                      two_handed=j['two_handed'],
                      finesse=j['finesse'],
                      thrown=j['thrown'],
                      loading=j['loading'],
                      ammunition=j['ammunition'])
