from dnd.game.runtime_library import RuntimeLibrary
from dnd.library.library import Library
from dnd.game.player import PlayerData, Player
from dnd.utils.importer import load

from typing import List
from pathlib import Path

def _make_players_from_player_data(library: Library, player_data_list: List[PlayerData]):
    players = {}
    for player_data in player_data_list:
        character = library.characters.get(player_data.character_name)
        if character is None:
            raise ValueError(f"player {player_data.name}'s character {player_data.character_name} was not found in the library")
        players[player_data.name] = Player(character, player_data)
    
    return players

class Game:
    def __init__(self, library: Library, player_data_list: List[PlayerData]):
        self._runtime_lib = RuntimeLibrary(library)
        self._players = _make_players_from_player_data(library, player_data_list)

    @staticmethod
    def from_save_file(filepath: Path):
        lib, p_data = load(filepath)
        return Game(lib, p_data)

    

# import Importer
# from Character import Character
# from Library import Library
# from pprint import pprint
#
# class Game(object):
#
#     def __init__(self):
#         self._characters = {}
#         self._library = Library()
#
#     def Save(self, folderpath, save_name):
#         Importer.Save(folderpath, save_name, self._library, self._characters)
#
#     def Load(self, zip_name):
#         Importer.Load(zip_name)
#
#     def ImportToLibrary(self, dict_name, filepath):
#         return self._library.AddDict(dict_name, filepath)
#
#     def AddCharacter(self, name, job, age, gender, alignment, stats, max_hp, armour_class):
#         if name in self._characters:
#             print("All characters must have unique names, <{}> is a duplicate".format(name))
#             return False
#
#         this_character = Character(name, job, age, gender, alignment, stats, max_hp, armour_class)
#         self._characters[name] = this_character
#         return False
#
#     def AddToInventory(self, character_name, item_name, value):
#         if not character_name in self._characters:
#             return False
#         return self._characters[character_name].AddToInventory(item_name, value)
#
#     def RemoveFromInventory(self, character_name, item_name, value):
#         if not character_name in self._characters:
#             return False
#         return self._characters[character_name].RemoveFromInventory(item_name, value)
#
#     def Equip(self, character_name, item_name, value):
#         if not character_name in self._characters:
#             return False
#         return self._characters[character_name].Equip(item_name, value)
#
#     def Unequip(self, character_name, item_name, value):
#         if not character_name in self._characters:
#             return False
#         return self._characters[character_name].Unequip(item_name, value)
#
#     def IncrementLevel(self, name, selected_options):
#         try:
#             return self._characters[name].IncrementLevel(self._library, selected_options)
#         except KeyError:
#             print("Name <{}> is not a character in the game", name)
#             return False
#
#     def GetContext(self, context_name, **kwargs):
#         if context_name == "character_detail":
#             character_name = kwargs["character_name"]
#             character = self._characters(character_name)
#
#             context_dict = {}
#             context_dict['name'] = character.GetName()
#             context_dict['level'] = character.GetLevel()
#             context_dict['age'] = character.GetAge()
#             context_dict['gender'] = character.GetGender()
#             context_dict['job_uuid'] = character.GetJob()
#             context_dict['job_name'] = self._library.Get('jobs', context_dict['job_uuid']).GetName()
#
#         elif context_name == 'equiped':
#             character_name = kwargs.get("character_name")
#             character = self._characters(character_name)
#
#             return character.GetEquipedItems()
#
#         elif context_name == 'stats':
#             character_name = kwargs.get("character_name")
#             character = self._characters(character_name)
#
#             stats = character.GetStats()
#             stats['hp'] = character.GetHP()
#             stats['max_hp'] = character.GetMaxHP()
#             stats['armor_class'] = character.GetAC()
#             return stats
#
#         elif context_name == 'inventory':
#             character_name = kwargs.get("character_name")
#             character = self._characters(character_name)
#
#             return character.GetInventory()
#
#         elif context_name == 'learned_features':
#             character_name = kwargs.get("character_name")
#             character = self._characters(character_name)
#
#             context_dict = {}
#             feature_uuids = character.GetLearnedFeatures()
#             for feature_uuid in feature_uuids:
#                 feature = self._library.Get('features', feature_uuid)
#                 context_dict[feature_uuid] = {}
#                 context_dict[feature_uuid]['name'] = feature.GetName()
#                 context_dict[feature_uuid]['description'] = feature.GetDescription()
#
#             return context_dict
#
#         elif context_name == 'library_summary':
#             dict_name = kwargs.get("dict_name")
#             return self._library.GetNameUUIDAsDict(dict_name)
#
#         elif context_name == 'feature_detail':
#             # Get the features and effects dicts and necessary kwargs
#             features_dict = self._library.Get('features')
#             effects_dict = self._library.Get('effects')
#             feature_uuid = kwargs.get('uuid')
#
#             # Get the feature instance from the dict and corresponding dict representation
#             this_feature = features_dict[feature_uuid]
#             this_feature_as_dict = this_feature.GetDict()
#
#             # For all prereqs, create a dict of uuid:name
#             prereqs = {}
#             for prereq_uuid in this_feature_as_dict['prereq_features']:
#                 prereqs[prereq_uuid] = features_dict[prereq_uuid].GetName()
#
#             # For all effects, create a dict of uuid:name
#             effects = {}
#             for effect_uuid in this_feature_as_dict['effects']:
#                 effects[effect_uuid] = effects_dict[effect_uuid].GetName()
#
#             # Replace the list of prereqs/effects with uuid:name dicts instead
#             this_feature_as_dict['prereq_features'] = prereqs
#             this_feature_as_dict['effects'] = effects
#             return this_feature_as_dict
#
#         elif context_name == 'option_detail':
#             # Get the features and effects dicts and necessary kwargs
#             features_dict = self._library.Get('features')
#             options_dict = self._library.Get('options')
#             option_uuid = kwargs.get('uuid')
#
#             # Get the feature instance from the dict and corresponding dict representation
#             this_option = options_dict[option_uuid]
#             this_option_as_dict = this_option.GetDict()
#
#             # For all prereqs, create a dict of uuid:name
#             prereqs = {}
#             for prereq_uuid in this_option_as_dict['prereq_features']:
#                 prereqs[prereq_uuid] = features_dict[prereq_uuid].GetName()
#
#             # For all features, create a dict of uuid:name
#             features = {}
#             for feature_uuid in this_option_as_dict['features']:
#                 features[feature_uuid] = features_dict[feature_uuid].GetName()
#
#             # Replace the list of prereqs/effects with uuid:name dicts instead
#             this_option_as_dict['prereq_features'] = prereqs
#             this_option_as_dict['features'] = effects
#             return this_option_as_dict
#
#         elif context_name == 'job_detail':
#             jobs_dict = self._library.Get('jobs')
#             features_dict = self._library.Get('features')
#             options_dict = self._library.Get('options')
#
#             job_uuid = kwargs.get('uuid')
#             this_job = jobs_dict[job_uuid]
#             this_job_as_dict = this_job.GetDict()
#
#             # For all features, create a dict of uuid:name
#             features = {}
#             for feature_uuid in this_job_as_dict['features']:
#                 features[feature_uuid] = features_dict[feature_uuid].GetName()
#
#             # For all options, create a dict of uuid:name
#             options = {}
#             for option_uuid in this_job_as_dict['features']:
#                 options[option_uuid] = options_dict[option_uuid].GetName()
#
#             # Replace the list of prereqs/effects with uuid:name dicts instead
#             this_job_as_dict['options'] = options
#             this_job_as_dict['features'] = features
#
#
#         elif context_name == 'next_level_options':
#             pprint (kwargs["character_name"])
#             character_name = kwargs["character_name"]
#             character = self._characters[character_name]
#             return character.GetNextLevelOptions(self._library)
#
#         else:
#             print("<{}> is not a valid key for GetContext", context_name)
#             return {}