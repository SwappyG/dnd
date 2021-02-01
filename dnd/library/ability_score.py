from __future__ import annotations
from typing import Dict
from pprint import pformat
from dnd.utils.exceptions import raise_if_false
import dataclasses

STAT_BUFF_LEVELS = [4, 8, 12, 16, 19]
PROFICIENCY_BONUS = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6]


def _proficiency_bonus(curr_level: int) -> int:
    return PROFICIENCY_BONUS[curr_level]


def is_stat_buff_level(level: int):
    return level in STAT_BUFF_LEVELS


@dataclasses.dataclass
class AbilityScore(object):
    STR: int = 0
    DEX: int = 0
    CON: int = 0
    INT: int = 0
    WIS: int = 0
    CHA: int = 0

    def __add__(self, other) -> AbilityScore:
        return AbilityScore(STR=self.STR + other.STR,
                            DEX=self.DEX + other.DEX,
                            CON=self.CON + other.CON,
                            INT=self.INT + other.INT,
                            WIS=self.WIS + other.WIS,
                            CHA=self.CHA + other.CHA)

    def __sub__(self, other) -> AbilityScore:
        return AbilityScore(STR=self.STR - other.STR,
                            DEX=self.DEX - other.DEX,
                            CON=self.CON - other.CON,
                            INT=self.INT - other.INT,
                            WIS=self.WIS - other.WIS,
                            CHA=self.CHA - other.CHA)

    def sum(self) -> int:
        return self.STR + self.DEX + self.CON + self.INT + self.WIS + self.CHA

    def modifier(self) -> AbilityScore:
        return AbilityScore(STR=int((self.STR - 10) / 2.0),
                            DEX=int((self.DEX - 10) / 2.0),
                            CON=int((self.CON - 10) / 2.0),
                            INT=int((self.INT - 10) / 2.0),
                            WIS=int((self.WIS - 10) / 2.0),
                            CHA=int((self.CHA - 10) / 2.0))

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.as_dict())


@dataclasses.dataclass(frozen=True)
class Skill:
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
    def from_ability_scores(ability_scores: AbilityScore, is_proficient: Skill, curr_level: int) -> Skill:
        raise_if_false(is_proficient.is_binary(), "Skills passed to is_proficient must all be either 0 or 1")
        mods = ability_scores.modifier()
        skills = Skill(athletics=mods.STR,
                       acrobatics=mods.DEX,
                       animal_handling=mods.WIS,
                       arcana=mods.INT,
                       deception=mods.CHA,
                       history=mods.INT,
                       insight=mods.WIS,
                       intimidation=mods.CHA,
                       investigation=mods.INT,
                       medicine=mods.WIS,
                       nature=mods.INT,
                       perception=mods.WIS,
                       performance=mods.CHA,
                       persuasion=mods.CHA,
                       religion=mods.INT,
                       sleight_of_hand=mods.DEX,
                       stealth=mods.DEX,
                       survival=mods.WIS)

        return skills + (is_proficient * _proficiency_bonus(curr_level))

    def is_binary(self):
        return all([((v == 0) or (v == 1)) for k, v in self.as_dict().items()])

    def __mul__(self, multiplier: int) -> Skill:
        return Skill(self.athletics * multiplier,
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

    def __add__(self, other: Skill) -> Skill:
        Skill(self.athletics + other.athletics,
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

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.as_dict())
