import os

from pathlib import Path

from typing import List, Dict, Any, Set, Type
import jsonpickle
import pprint
import json
from zipfile import ZipFile
from dnd.library.library import Library
from dnd.library.effect import Effect
from dnd.library.feature import Feature
from dnd.library.option import Option
from dnd.library.job import Job
from dnd.library.location import Location, LocationType, LocationClimate, LocationStatus
from dnd.library.spell import Spell
from dnd.library.npc import NPC
from dnd.library.item import *
from dnd.library.spell import *
from dnd.library.character import Character
from dnd.library.campaign import Campaign
from dnd.game.player import Player, PlayerData
from dnd.library.alignment import Alignment
from dnd.library.ability_score import AbilityScore, Skills
import dnd.utils.jsonpickel_utils as jp_utils


def import_zipped(zipped_file_handle, relative_path: str, obj: Type[DataClassBase]):
    j = json.loads(zipped_file_handle.read(relative_path))
    print(relative_path)
    ret = {}
    for name in j:
        try:
            ret[name] = obj.from_json(j[name])
        except KeyError as e:
            raise KeyError(f'failed to find key {e} in entry {name}')
    return ret


def load(zip_file_path: Path) -> Tuple[Library, List[PlayerData]]:
    with ZipFile(zip_file_path) as z:
        player_files = [info.filename for info in z.infolist() if str(Path(info.filename).parent) == 'players']
        players = [PlayerData.from_json(json.loads(z.read(file))) for file in player_files]
        lib = Library(effects=import_zipped(z, 'library/effects.json', Effect),
                      features=import_zipped(z, 'library/features.json', Feature),
                      options=import_zipped(z, 'library/options.json', Option),
                      jobs=import_zipped(z, 'library/jobs.json', Job),
                      items=import_zipped(z, 'library/items.json', Item),
                      locations=import_zipped(z, 'library/locations.json', Location),
                      spells=import_zipped(z, 'library/spells.json', Spell),
                      npcs=import_zipped(z, 'library/npcs.json', NPC),
                      characters=import_zipped(z, 'library/characters.json', Character),
                      campaigns=import_zipped(z, 'library/campaigns.json', Campaign))

        return lib, players


if __name__ == '__main__':
    l_s, p_s = load(Path(__file__).parent.parent / 'savefile_2.zip')
    print(l_s.effects)
