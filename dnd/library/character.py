from __future__ import annotations
from dnd.library.ability_score import AbilityScore, Skills
from dnd.library.alignment import Alignment
from dnd.utils.dataclass_types import DataClassBase
from typing import FrozenSet, Dict, Any
import dataclasses


@dataclasses.dataclass(frozen=True)
class Character(DataClassBase):
    name: str
    job: str
    age: int
    gender: str
    alignment: Alignment
    level: int
    sub_level: int
    ability_score: AbilityScore
    max_hp: int
    hit_die: int
    learned_features: FrozenSet[str]
    skill_proficiency: dataclasses.InitVar[Skills]
    skills: Skills = dataclasses.field(init=False)

    def __post_init__(self, skill_proficiency: Skills):
        object.__setattr__(self, 'skills',
                           Skills.from_ability_scores(self.ability_score, skill_proficiency, self.level))

    @staticmethod
    def _parse_ability_score(json_elem: Any) -> AbilityScore:
        return AbilityScore(STR=json_elem['STR'],
                            DEX=json_elem['DEX'],
                            CON=json_elem['CON'],
                            INT=json_elem['INT'],
                            WIS=json_elem['WIS'],
                            CHA=json_elem['CHA'])

    @staticmethod
    def _parse_skills_proficiency(json_elem: Any) -> Skills:
        return Skills(athletics=json_elem['athletics'],
                      acrobatics=json_elem['acrobatics'],
                      animal_handling=json_elem['animal_handling'],
                      arcana=json_elem['arcana'],
                      deception=json_elem['deception'],
                      history=json_elem['history'],
                      insight=json_elem['insight'],
                      intimidation=json_elem['intimidation'],
                      investigation=json_elem['investigation'],
                      medicine=json_elem['medicine'],
                      nature=json_elem['nature'],
                      perception=json_elem['perception'],
                      performance=json_elem['performance'],
                      persuasion=json_elem['persuasion'],
                      religion=json_elem['religion'],
                      sleight_of_hand=json_elem['sleight_of_hand'],
                      stealth=json_elem['stealth'],
                      survival=json_elem['survival'])

    @staticmethod
    def from_json(j: Dict) -> Character:
        return Character(name=j['name'],
                         job=j['job'],
                         age=j['age'],
                         gender=j['gender'],
                         alignment=Alignment[j['alignment']],
                         level=j['level'],
                         sub_level=j['sub_level'],
                         ability_score=Character._parse_ability_score(j['ability_score']),
                         skill_proficiency=Character._parse_skills_proficiency(j['skill_proficiency']),
                         max_hp=j['max_hp'],
                         hit_die=j['hit_die'],
                         learned_features=frozenset([] if j['learned_features'] is None else j['learned_features']))


# @dataclasses.dataclass(frozen=True)
# class CharacterHistory(DataClassBase):
#     name: str
#     history: ImmutableDict[Tuple[int, int], Character]
#
#     def set_level_history(self, level: int, sub_level: int, character: Character):
#         dataclasses.replace(self, history=self.history.copy(**{(level, sub_level): character}))
