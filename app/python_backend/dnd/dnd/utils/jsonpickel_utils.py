import os

import pandas as pd
from pathlib import Path

import jsonpickle
from dnd.utils.dataclass_types import DataClassBase
from typing import Type, Any, Optional
import json


def json_from_file(filepath: Path) -> Optional[Any]:
    with open(filepath, 'r') as file_handle:
        json_string = file_handle.read()

    return json.loads(json_string)


def open_and_decode(filepath: Path) -> Optional[Any]:
    try:
        with open(filepath, 'r') as file_handle:
            json_string = file_handle.read()

        return jsonpickle.decode(json_string)
    except Exception as e:
        print(f"Failed to open file with path [{filepath}], got [{e}]")
        return None


def encode_and_write(filepath: Path, obj: Type[DataClassBase], unpicklable: bool) -> bool:
    try:
        json_string = jsonpickle.encode(obj, unpicklable=unpicklable, make_refs=False, indent=4)
    except Exception as e:
        print(("Failed to serialize object, got [{}]".format(e)))
        return False

    with open(filepath, 'w+') as a_file:
        a_file.write(json_string)

    return True
