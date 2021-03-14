from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

from dnd.game.runtime_library import RuntimeLibrary
from dnd.game.player import PlayerData
from dnd.utils.importer import load
from typing import Dict, List
import dataclasses


@dataclasses.dataclass
class Session:
    lib: RuntimeLibrary
    players_list: dataclasses.InitVar[List[PlayerData]]
    players: Dict[str, PlayerData] = dataclasses.field(init=False)

    def __post_init__(self, players_list: List[PlayerData]):
        self.players = {p.name: p for p in players_list}

    @staticmethod
    def from_save_file(filepath: Path) -> Session:
        lib, p_data = load(filepath)
        return Session(RuntimeLibrary(lib), p_data)
