import os
import zipfile
import jsonpickle
from pprint import pprint

import pandas as pd
from pathlib import Path
import uuid

from typing import Dict
import jsonpickle
from dnd.library.effect import Effect
from dnd.library.feature import Feature
from dnd.library.option import Option
from dnd.library.job import Job


def import_csv(file_path):
    data_frame = pd.read_csv(file_path, index_col='Name', sep="|")
    return data_frame.to_dict('index')


def get_school(school: str) -> SpellSchool:
    school = school.lower()
    if 'illus' in school:
        return SpellSchool.ILLUSION
    if 'trans' in school:
        return SpellSchool.TRANSMUTATION
    if 'conj' in school:
        return SpellSchool.CONJURATION
    if 'evoc' in school:
        return SpellSchool.EVOCATION
    if 'abjur' in school:
        return SpellSchool.ABJURATION
    if 'necro' in school:
        return SpellSchool.NECROMANCY
    if 'divin' in school:
        return SpellSchool.DIVINATION
    if 'ench' in school:
        return SpellSchool.ENCHANTMENT

    raise ValueError(f"{school} is not a valid school")


def get_valid_jobs(spells_csv_row: Dict[str, Any], fields: List[str]) -> Set[str]:
    valid_jobs = []
    for field in fields:
        if isinstance(spells_csv_row[field], str) and spells_csv_row[field].lower() == 'true':
            valid_jobs.append(field)
        elif isinstance(spells_csv_row[field], bool) and spells_csv_row[field] == True:
            valid_jobs.append(field)
    return set(valid_jobs)


def get_saving_throw(saving_throw: str) -> SavingThrowType:
    if not isinstance(saving_throw, str):
        return None

    if saving_throw.lower() == '-':
        return None

    if saving_throw.upper() in SavingThrowType.__dict__:
        return SavingThrowType[saving_throw.upper()]

    if saving_throw.lower() == 'attack':
        return SavingThrowType['ATK']

    return SavingThrowType.OTH


def import_spells():
    root_dir = os.path.join(str(Path(__file__).parent.parent))
    spells_csv = import_csv(os.path.join(root_dir, 'obsolete_data', 'spells.csv'))
    spells = {}
    for name in spells_csv:
        print(name)
        row = spells_csv[name]
        desc = row['Effect']
        level = row['Level']
        school = get_school(row['School'])
        casting_time = row['Casting Time']
        casting_range = row['Range']
        casting_targets = row['Area or Targets']
        duration = row['Duration']
        is_conc = isinstance(row['Conc'], str) and (row['Conc'].lower() == 'yes')
        is_ritual = True if isinstance(row['Ritual'], str) and row['Ritual'].lower() == 'yes' else False
        mats = row['Mats']
        cost = "" if not isinstance(row['Cost'], str) else row['Cost']
        saving_throw = get_saving_throw(row['Save or Attack'])
        valid_jobs = get_valid_jobs(row,
                                    ['Arcane Trickster', 'Bard', 'Cleric', 'Druid', 'Eldritch Knight', 'Paladin',
                                     'Ranger', 'Sorcerer', 'Warlock', 'Wizard'])

        spells[name] = Spell(name=name,
                             level=level,
                             desc=desc,
                             school=school,
                             casting_time=casting_time,
                             casting_range=casting_range,
                             casting_targets=casting_targets,
                             duration=duration,
                             saving_throw=saving_throw,
                             is_conc=is_conc,
                             is_ritual=is_ritual,
                             mats=mats,
                             cost=cost,
                             valid_jobs=valid_jobs)

    jsonpickle_encode(os.path.join(root_dir, 'data', 'library', 'spells.json'), spells)

def import_armor():
    root_dir = os.path.join(str(Path(__file__).parent.parent))
    armor_csv = import_csv(os.path.join(root_dir, 'obsolete_data', 'armor.csv'))
    armors = {}
    for name in armor_csv:
        weight_token = armor_csv[name]['weight'].lower()
        armor_weight = ArmorWeight.MEDIUM if weight_token == 'medium' else ArmorWeight.LIGHT
        armor_weight = ArmorWeight.HEAVY if weight_token == 'heavy' else armor_weight

        ac = int(armor_csv[name]['ac'])
        minimum_strength = int(armor_csv[name]['str_req'])
        has_stealth_disadvantage = armor_csv[name]['stealth_disadvantage'] == 'y'
        armors[name] = Armor(name=name, desc="", armor_type=ArmorType.BODY, ac=ac, weight=armor_weight,
                             minimum_strength=minimum_strength,
                             has_stealth_disadvantage=has_stealth_disadvantage)


def import_weapons():
    weapons_csv = import_csv(os.path.join(root_dir, 'obsolete_data', 'weapons.csv'))
    weapons = {}
    for name in weapons_csv:
        num_die, damage_die = weapons_csv[name]['damage'].split('d')
        if isinstance(weapons_csv[name]['properties'], float):
            weapons_csv[name]['properties'] = ""
        property_tokens = [val.lower() for val in weapons_csv[name]['properties'].replace(" ", "").split(',')]
        is_two_handed = ('two-handed' in property_tokens)
        is_finesse = 'finesse' in property_tokens
        is_ammunition = 'ammunition' in property_tokens
        is_loading = 'loading' in property_tokens
        is_thrown = 'thrown' in property_tokens
        weight_category = WeightCategory.HEAVY if 'heavy' in property_tokens else WeightCategory.NONE
        weight_category = WeightCategory.HEAVY if 'light' in property_tokens else weight_category

        category_token = weapons_csv[name]['category'].lower()
        weapon_category = WeaponCategory.SIMPLE if category_token == 'simple' else WeaponCategory.MARTIAL

        weapon_type_token = weapons_csv[name]['weapon_type'].lower()
        weapon_type = WeaponType.RANGED if weapon_type_token == 'ranged' else WeaponType.MELEE

        damage_type_token = weapons_csv[name]['damage_type'].lower()
        damage_type = DamageType.SLASHING if damage_type_token == 'slashing' else DamageType.BLUDGEONING
        damage_type = DamageType.PIERCING if damage_type_token == 'piercing' else damage_type

        damage_range = (5, 5)
        for token in property_tokens:
            if 'range' not in token:
                continue
            min_range, max_range = token.split('(')[1].replace(')', "").split("/")
            damage_range = (int(min_range), int(max_range))

        try:
            weight = float(weapons_csv[name]['weight'])
        except ValueError:
            weight = 0

        weapons[name] = Weapon(name=name,
                               desc="",
                               weapon_category=weapon_category,
                               weapon_type=weapon_type,
                               damage_die=int(damage_die),
                               num_die=int(num_die),
                               bonus_damage=0,
                               damage_type=damage_type,
                               weapon_range=damage_range,
                               hit_bonus=0,
                               weight=weight,
                               weight_category=weight_category,
                               two_handed=is_two_handed,
                               finesse=is_finesse,
                               thrown=is_thrown,
                               loading=is_loading,
                               ammunition=is_ammunition)




def import_effects(file_path):
    effects_dict = import_csv(file_path)
    effects = {}
    for name in effects_dict:
        print("importing Effect <{}>".format(name))
        duration = effects_dict[name]['Duration']
        effect_type = effects_dict[name]['Type']
        description = effects_dict[name]['Description']
        effects[name] = Effect(name, effect_type, duration, description).as_dict()

    return effects


def import_features(file_path) -> Dict[str, Dict[str, object]]:
    # Import the CSV file
    features_dict = import_csv(file_path)

    # Dict of all our imported features
    features = {}

    # Create all the features
    for name in features_dict:
        print("importing Feature <{}>".format(name))
        unlock_level = features_dict[name]['Unlock Level']
        effect_names = set(features_dict[name]['Effects'].split(";")) if features_dict[name][
                                                                             'Effects'] != "None" else set([])
        prereq_feature_names = set(features_dict[name]['Prereq Features'].split(";")) if features_dict[name][
                                                                                             'Prereq Features'] != "None" else set(
            [])
        features[name] = Feature(name,
                                 features_dict[name]['Description'],
                                 effect_names,
                                 prereq_feature_names,
                                 unlock_level).as_dict()

    return features


def import_options(file_path):
    options_dict = import_csv(file_path)
    options = {}

    for name in options_dict:
        print("Importing Option <{}>".format(name))
        options[name] = Option(name,
                               options_dict[name]['Description'],
                               set(options_dict[name]['Features'].split(";")),
                               set(options_dict[name]['Prereq Features'].split(";")) if options_dict[name][
                                                                                            'Prereq Features'] != "None" else set(
                                   []),
                               options_dict[name]['Unlock Levels'].split(";")).as_dict()

    return options


#
#
def import_jobs(file_path):
    jobs_dict = import_csv(file_path)
    jobs = {}
    for name in jobs_dict:
        print("Importing Job <{}>".format(name))
        jobs[name] = Job(name,
                         jobs_dict[name]['Description'],
                         set(jobs_dict[name]['Features'].split(";")),
                         set(jobs_dict[name]['Options'].split(";"))).as_dict()

    return jobs


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
        json_string = jsonpickle.encode(obj, unpicklable=False, indent=4)
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
    root_dir = os.path.join(str(Path(__file__).parent.parent), 'obsolete_data')
    open_and_dump('effects', import_effects(os.path.join(root_dir, 'effects_lib.csv')))
    open_and_dump('features', import_features(os.path.join(root_dir, 'features_lib.csv')))
    open_and_dump('options', import_options(os.path.join(root_dir, 'options_lib.csv')))
    open_and_dump('jobs', import_jobs(os.path.join(root_dir, 'jobs_lib.csv')))


def test():
    e = Effect(name='a', effect_type='normal', duration='instant', desc='no desc')
    effects = {'a': e}
    print(effects)


if __name__ == "__main__":
    main()
