"""
Save Format:
- save_file.zip
    |- library
        |- armor.json
        |- characters.json
        |- effects.json
        |- features.json
        |- items.json
        |- jobs.json
        |- locations.json
        |- npcs.json
        |- options.json
        |- spells.json
        |- weapons.json
        |- campaigns.json
        |- character_history.json
    |- players
        |- player_1.json
        |- player_2.json
        |- ...
"""

import io
import zipfile
from zipfile import ZipFile
from pathlib import Path
from typing import Type, Any, List
from dnd.utils.dataclass_types import DataClassBase
import dnd.utils.jsonpickel_utils as jp_utils
from dnd.library.library import Library
from dnd.game.player import PlayerData
from dnd.library.money import Money
import jsonpickle


def export_lib_type(obj: Type[DataClassBase], root_path: Path, filename: str) -> bool:
    return export_type(filepath=root_path / "library" / (filename + ".json"), obj=obj, unpicklable=True)


def export_type(obj: Type[DataClassBase], filepath: Path, unpicklable: bool) -> bool:
    return jp_utils.encode_and_write(filepath=filepath, obj=obj, unpicklable=unpicklable)


def save(zip_file_path: Path, zip_file_name: str, library: Library, player_datas: List[PlayerData], unpicklable: bool):
    zip_buffer = io.BytesIO()

    def encode(obj: Any):
        return jsonpickle.encode(obj, unpicklable=False, make_refs=False, indent=4)

    lib_path = Path('library')
    with ZipFile(zip_buffer, mode='a', compression=zipfile.ZIP_DEFLATED, allowZip64=False) as z:
        z.writestr(str(lib_path / 'effects.json'), bytes(encode(library.effects), 'utf-8'))
        z.writestr(str(lib_path / 'features.json'), bytes(encode(library.features), 'utf-8'))
        z.writestr(str(lib_path / 'options.json'), bytes(encode(library.options), 'utf-8'))
        z.writestr(str(lib_path / 'jobs.json'), bytes(encode(library.jobs), 'utf-8'))
        z.writestr(str(lib_path / 'items.json'), bytes(encode(library.items), 'utf-8'))
        z.writestr(str(lib_path / 'locations.json'), bytes(encode(library.locations), 'utf-8'))
        z.writestr(str(lib_path / 'spells.json'), bytes(encode(library.spells), 'utf-8'))
        z.writestr(str(lib_path / 'npcs.json'), bytes(encode(library.npcs), 'utf-8'))
        z.writestr(str(lib_path / 'characters.json'), bytes(encode(library.characters), 'utf-8'))
        z.writestr(str(lib_path / 'campaigns.json'), bytes(encode(library.campaigns), 'utf-8'))

    lib_path = Path('players')
    with ZipFile(zip_buffer, mode='a', compression=zipfile.ZIP_DEFLATED, allowZip64=False) as z:
        for player_data in player_datas:
            z.writestr(str(lib_path / (player_data.name + '.json')), bytes(encode(player_data), 'utf-8'))

    print(f'Saving to {zip_file_path / (zip_file_name + ".zip")}')
    with open(zip_file_path / (zip_file_name + '.zip'), 'wb') as f:
        f.write(zip_buffer.getvalue())


if __name__ == '__main__':
    from dnd.utils.importer import load
    import os

    lib, p_data = load(Path(os.path.dirname(__file__)).parent / 'savefile_2.zip')
    print(p_data)
