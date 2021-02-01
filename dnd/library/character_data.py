from __future__ import annotations

from dnd.library.ability_score import AbilityScore, Skill
from dnd.library.alignment import Alignment
from typing import Set, Dict

from pprint import pformat
import dataclasses


@dataclasses.dataclass(frozen=True)
class CharacterData:
    name: str
    job: str
    age: int
    gender: str
    alignment: Alignment
    level: int
    sub_level: int
    ability_score: AbilityScore
    skill_proficiency: Skill
    max_hp: int
    hit_die: int
    skills: dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'skills',
                           Skill.from_ability_scores(self.ability_score, self.skill_proficiency, self.level))

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.asdict())
