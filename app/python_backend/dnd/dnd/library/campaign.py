from __future__ import annotations
from typing import FrozenSet, Dict
from dnd.utils.dataclass_types import DataClassBase
import dataclasses


@dataclasses.dataclass(frozen=True)
class Campaign(DataClassBase):
    name: str
    season: int
    characters: FrozenSet[str]
    locations: FrozenSet[str]
    npcs: FrozenSet[str]

    @staticmethod
    def from_json(j: Dict) -> Campaign:
        return Campaign(name=j['name'],
                        season=j['season'],
                        characters=j['characters'],
                        locations=j['locations'],
                        npcs=j['npcs'])

    def add_character(self, character_name: str):
        dataclasses.replace(self, characters=self.characters.union({character_name}))

    def add_location(self, location_name: str):
        dataclasses.replace(self, locations=self.locations.union({location_name}))

    def add_npc(self, npc_name: str):
        dataclasses.replace(self, npcs=self.npcs.union({npc_name}))

    def remove_character(self, character_name: str):
        dataclasses.replace(self, characters=self.characters.difference({character_name}))

    def remove_location(self, location_name: str):
        dataclasses.replace(self, locations=self.locations.difference({location_name}))

    def remove_npc(self, npc_name: str):
        dataclasses.replace(self, npcs=self.npcs.difference({npc_name}))

# @dataclasses.dataclass(frozen=True)
# class CampaignHistory(DataClassBase):
#     name: str
#     history: frozendict[int, Campaign]
#
#     def set_season_history(self, season: int, campaign: Campaign):
#         dataclasses.replace(self, history=self.history.copy(**{season: campaign}))
