from __future__ import annotations
from dnd.utils.exceptions import raise_if_false
from dnd.utils.dataclass_types import DataClassBase
from typing import Dict
import dataclasses

STAT_BUFF_LEVELS = [4, 8, 12, 16, 19]
PROFICIENCY_BONUS = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6]


def _proficiency_bonus(curr_level: int) -> int:
    return PROFICIENCY_BONUS[curr_level]


def is_stat_buff_level(level: int):
    return level in STAT_BUFF_LEVELS


@dataclasses.dataclass(frozen=True)
class AbilityScore(DataClassBase):
    STR: int = 0
    DEX: int = 0
    CON: int = 0
    INT: int = 0
    WIS: int = 0
    CHA: int = 0

    def __add__(self, other: AbilityScore) -> AbilityScore:
        return AbilityScore(**{k1: v1 + v2 for ((k1, v1), (_, v2)) in zip(self.as_dict(), other.as_dict())})

    def __sub__(self, other: AbilityScore) -> AbilityScore:
        return AbilityScore(**{k1: v1 - v2 for ((k1, v1), (_, v2)) in zip(self.as_dict(), other.as_dict())})

    def __mul__(self, multiplier: int) -> AbilityScore:
        return AbilityScore(**{k1: v1 * multiplier for k1, v1 in self.as_dict()})

    @staticmethod
    def from_json(j: Dict) -> AbilityScore:
        return AbilityScore(STR=j['STR'],
                            DEX=j['DEX'],
                            CON=j['CON'],
                            INT=j['INT'],
                            WIS=j['WIS'],
                            CHA=j['CHA'])

    def is_binary(self) -> bool:
        return all([(v == 1 or v == 0) for _, v in self.as_dict().items()])

    def sum(self) -> int:
        return sum([v for _, v in self.as_dict().items()])

    def modifier(self) -> AbilityScore:
        return AbilityScore(**{k: ((v - 10) / 2.0) for k, v in self.as_dict().items()})


@dataclasses.dataclass(frozen=True)
class Skills(DataClassBase):
    athletics: int = 0
    acrobatics: int = 0
    animal_handling: int = 0
    arcana: int = 0
    deception: int = 0
    history: int = 0
    insight: int = 0
    intimidation: int = 0
    investigation: int = 0
    medicine: int = 0
    nature: int = 0
    perception: int = 0
    performance: int = 0
    persuasion: int = 0
    religion: int = 0
    sleight_of_hand: int = 0
    stealth: int = 0
    survival: int = 0

    @staticmethod
    def from_ability_scores(ability_scores: AbilityScore, is_proficient: Skills, curr_level: int) -> Skills:
        raise_if_false(is_proficient.is_binary(), "Skills passed to is_proficient must all be either 0 or 1")
        mods = ability_scores.modifier()
        skills = Skills(athletics=int(mods.STR),
                        acrobatics=int(mods.DEX),
                        animal_handling=int(mods.WIS),
                        arcana=int(mods.INT),
                        deception=int(mods.CHA),
                        history=int(mods.INT),
                        insight=int(mods.WIS),
                        intimidation=int(mods.CHA),
                        investigation=int(mods.INT),
                        medicine=int(mods.WIS),
                        nature=int(mods.INT),
                        perception=int(mods.WIS),
                        performance=int(mods.CHA),
                        persuasion=int(mods.CHA),
                        religion=int(mods.INT),
                        sleight_of_hand=int(mods.DEX),
                        stealth=int(mods.DEX),
                        survival=int(mods.WIS))

        return skills + (is_proficient * _proficiency_bonus(curr_level))

    @staticmethod
    def from_json(j: Dict):
        return Skills(athletics=int(j['athletics']),
                      acrobatics=int(j['acrobatics']),
                      animal_handling=int(j['animal_handling']),
                      arcana=int(j['arcana']),
                      deception=int(j['deception']),
                      history=int(j['history']),
                      insight=int(j['insight']),
                      intimidation=int(j['intimidation']),
                      investigation=int(j['investigation']),
                      medicine=int(j['medicine']),
                      nature=int(j['nature']),
                      perception=int(j['perception']),
                      performance=int(j['performance']),
                      persuasion=int(j['persuasion']),
                      religion=int(j['religion']),
                      sleight_of_hand=int(j['sleight_of_hand']),
                      stealth=int(j['stealth']),
                      survival=int(j['survival']))

    def is_binary(self):
        return all([((v == 0) or (v == 1)) for k, v in self.as_dict().items()])

    def __mul__(self, multiplier: int) -> Skills:
        return Skills(self.athletics * multiplier,
                      self.acrobatics * multiplier,
                      self.animal_handling * multiplier,
                      self.arcana * multiplier,
                      self.deception * multiplier,
                      self.history * multiplier,
                      self.insight * multiplier,
                      self.intimidation * multiplier,
                      self.investigation * multiplier,
                      self.medicine * multiplier,
                      self.nature * multiplier,
                      self.perception * multiplier,
                      self.performance * multiplier,
                      self.persuasion * multiplier,
                      self.religion * multiplier,
                      self.sleight_of_hand * multiplier,
                      self.stealth * multiplier,
                      self.survival * multiplier)

    def __add__(self, other: Skills) -> Skills:
        return Skills(self.athletics + other.athletics,
                      self.acrobatics + other.acrobatics,
                      self.animal_handling + other.animal_handling,
                      self.arcana + other.arcana,
                      self.deception + other.deception,
                      self.history + other.history,
                      self.insight + other.insight,
                      self.intimidation + other.intimidation,
                      self.investigation + other.investigation,
                      self.medicine + other.medicine,
                      self.nature + other.nature,
                      self.perception + other.perception,
                      self.performance + other.performance,
                      self.persuasion + other.persuasion,
                      self.religion + other.religion,
                      self.sleight_of_hand + other.sleight_of_hand,
                      self.stealth + other.stealth,
                      self.survival + other.survival)
