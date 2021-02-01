import os
import zipfile
from pprint import pprint

import pandas as pd
from pathlib import Path
import math
import uuid

from typing import List, Dict, Any
import jsonpickle
import json
from dnd.library.library import Library
from dnd.library.effect import Effect
from dnd.library.feature import Feature
from dnd.library.option import Option
from dnd.library.job import Job
from dnd.library.item import *
from dnd.library.spell import *


def import_csv(file_path):
    data_frame = pd.read_csv(file_path, index_col='Name', sep="|")
    return data_frame.to_dict('index')


def import_library(library, dict_name, file_path):
    effects = import_effects(os.path.join(file_path, 'effects.json'))
    features = import_features(os.path.join(file_path, 'features.json'))
    options = import_options(os.path.join(file_path, 'options.json'))
    jobs = import_jobs(os.path.join(file_path, 'jobs.json'))
    jobs = import_jobs(os.path.join(file_path, 'jobs.json'))

    # TODO: Add exception handling
    if dict_name == 'effects':
        effects = ImportEffects(file_path)
        library.AddDict('effects', effects)
    elif dict_name == 'features':
        features = ImportFeatures(file_path, library)
        library.AddDict('features', features)
    elif dict_name == 'options':
        options = ImportOptions(file_path, library)
        library.AddDict('options', options)
    elif dict_name == 'jobs':
        jobs = ImportOptions(file_path, library)
        library.AddDict('jobs', jobs)
    elif dict_name == 'items':
        print("Item importing is not implemented yet")
        return False

    return True

def import_weapons(file_path):
    with open(file_path, 'r') as fp:
        j = json.load(fp)

    return {name: Weapon(name, j[name]['desc'], j[name]['duration'], j[name]['desc']) for name in j}


def import_effects(file_path):
    with open(file_path, 'r') as fp:
        j = json.load(fp)

    return {name: Effect(name, j[name]['effect_type'], j[name]['duration'], j[name]['desc']) for name in j}


def import_features(file_path) -> Dict[str, Dict[str, object]]:
    with open(file_path, 'r') as fp:
        j = json.load(fp)

    return {name: Feature(name, j[name]['desc'], set(j[name]['effects']), set(j[name]['prereq_features']),
                          j[name]['unlock_level']) for name in j}


def import_options(file_path):
    with open(file_path, 'r') as fp:
        j = json.load(fp)

    return {name: Option(name, j[name]['desc'], set(j[name]['features']), set(j[name]['prereq_features']),
                         j[name]['unlock_levels']) for name in j}


def import_jobs(file_path):
    with open(file_path, 'r') as fp:
        j = json.load(fp)

    return {name: Job(name, j[name]['desc'], set(j[name]['features']), set(j[name]['options'])) for name in j}


# def ImportCharacter(file_path):
#     try:
#         with open(file_path, 'r') as a_file:
#             return jsonpickle.decode(a_file.read())
#     except Exception as e:
#         print(("Failed to open file with path [{}], got [{}]".format(file_path, e)))
#         return None
#
#
# def ExportCharacter(file_path, this_character):
#     try:
#         name = this_character.GetName()
#         json_string = jsonpickle.encode(this_character)
#     except Exception as e:
#         print(("Failed to serial object [{}], got [{}]".format(name, e)))
#
#     with open(file_path, 'w+') as a_file:
#         a_file.write(json_string)
#
#
# def Save(folderpath, zip_name, library, characters):
#     files_to_zip = []
#     for character in characters:
#         this_file = "/character/" + character + ".json"
#         os.makedirs(os.path.dirname(folderpath + this_file), exist_ok=True)
#         Pickle(folderpath + this_file, characters)
#         files_to_zip.append((this_file, folderpath))
#
#     this_file = "/library.json"
#     os.makedirs(os.path.dirname(folderpath + this_file), exist_ok=True)
#     Pickle(folderpath + this_file, library)
#     files_to_zip.append((this_file, folderpath))
#
#     Zip(folderpath, zip_name, files_to_zip)
#
#
# def Load(zip_name):
#     with zipfile.ZipFile(zip_name) as zip:
#         zip.printdir()
#         with zip.open('library.json') as library_json:
#             library = Depickle(library_json.read().decode('UTF-8'))
#
#
# def Zip(location, zip_name, files):
#     # shutil.make_archive("test","zip")
#     with zipfile.ZipFile(zip_name, 'w') as zipf:
#         for filename, folder in files:
#             zipf.write(folder + filename, filename)
#
#
def jsonpickle_decode(json_string: str):
    try:
        # with open(json_string, 'r') as a_file:
        return jsonpickle.decode(json_string)
    except Exception as e:
        print(("Failed to open file with path [{}], got [{}]".format(json_string, e)))
        return None


def jsonpickle_encode(filepath: str, obj: object):
    try:
        json_string = jsonpickle.encode(obj, unpicklable=False, make_refs=False, indent=4)
    except Exception as e:
        print(("Failed to serialize object, got [{}]".format(e)))
        return False

    with open(filepath, 'w+') as a_file:
        a_file.write(json_string)

    return True


def open_and_dump(name: str, obj: object):
    with open(name + '.json', 'w') as fp:
        jsonpickle_encode(name + '.json', obj)


def main():
    root_dir = os.path.join(str(Path(__file__).parent.parent), 'data', 'library')

    lib = Library(
        import_effects(root_dir + '/effects.json'),
        import_features(root_dir + '/features.json'),
        import_options(root_dir + '/options.json'),
        import_jobs(root_dir + '/jobs.json')
    )



def csv_imp():


if __name__ == "__main__":
    csv_imp()
