from dnd.library.item import Item
from dnd.library.effect import Effect
from dnd.library.feature import Feature
from dnd.library.option import Option
from dnd.library.spell import Spell
from dnd.library.job import Job
from dnd.library.npc import NPC
from dnd.library.character import Character
from dnd.library.location import Location
from dnd.library.campaign import Campaign

from typing import Dict, Any
import dataclasses


@dataclasses.dataclass
class Library:
    effects: Dict[str, Effect]
    features: Dict[str, Feature]
    options: Dict[str, Option]
    jobs: Dict[str, Job]
    items: Dict[str, Item]
    locations: Dict[str, Location]
    spells: Dict[str, Spell]
    npcs: Dict[str, NPC]
    characters: Dict[str, Character]
    campaigns: Dict[str, Campaign]

    types: Dict[str, Any] = dataclasses.field(init=False, default_factory=dict)

    def __post_init__(self):
        self.types = {
            'effects': Effect,
            'features': Feature,
            'options': Option,
            'jobs': Job,
            'items': Item,
            'locations': Location,
            'spells': Spell,
            'npcs': NPC,
            'characters': Character,
            'campaigns': Campaign,
        }