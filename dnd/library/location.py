from __future__ import annotations
from typing import Optional, FrozenSet, Dict
import dataclasses
from dnd.utils.json_types import JsonEnum
from dnd.utils.dataclass_types import DataClassBase


class LocationType(JsonEnum):
    WILDERNESS = 0
    OUTPOST = 1
    VILLAGE = 2
    TOWN = 3
    CITY = 4
    COUNTRY = 5
    CONTINENT = 6


class LocationStatus(JsonEnum):
    OK = 0
    RAVAGED = 1
    FALLEN = 2
    ABANDONED = 3
    UNKNOWN = 4
    UNDER_ATTACK = 5


class LocationClimate(JsonEnum):
    SEMI_FROST = 0
    PERMA_FROST = 1
    ARID = 2
    THUNDEROUS = 3
    TEMPERATE = 4
    SEASIDE = 5
    RAINY = 6
    DESERT = 7


@dataclasses.dataclass(frozen=True)
class Location(DataClassBase):
    name: str
    description: str
    loc_type: LocationType
    race: FrozenSet[str]
    population: int
    status: LocationStatus
    climate: LocationClimate
    leader: Optional[str]
    country: str

    @staticmethod
    def from_json(j: Dict) -> Location:
        return Location(name=j['name'],
                        description=j['description'],
                        loc_type=LocationType[j['loc_type'].upper()],
                        race=j['race'],
                        population=j['population'],
                        status=LocationStatus[j['status']],
                        climate=LocationClimate[j['climate']],
                        leader=j['leader'],
                        country=j['country'])
