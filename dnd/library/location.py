from typing import Optional, List, Dict
from enum import Enum
from pprint import pformat
import dataclasses


class LocationType(Enum):
    WILDERNESS = 0
    OUTPOST = 1
    VILLAGE = 2
    TOWN = 3
    CITY = 4
    COUNTRY = 5
    CONTINENT = 6


class LocationStatus(Enum):
    OK = 0
    RAVAGED = 1
    FALLEN = 2
    ABANDONED = 3
    UNKNOWN = 4
    UNDER_ATTACK = 5


class LocationClimate(Enum):
    SEMI_FROST = 0
    PERMA_FROST = 1
    ARID = 2
    THUNDEROUS = 3
    TEMPERATE = 4
    SEASIDE = 5
    RAINY = 6
    DESERT = 7


@dataclasses.dataclass(frozen=True)
class Location(object):
    name: str
    description: str
    loc_type: LocationType
    mayor: Optional[str]
    race: List[str]
    population: int
    status: LocationStatus
    climate: LocationClimate
    leader: Optional[str]
    country: str

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.asdict())
