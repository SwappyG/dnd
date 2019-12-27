import Importer
from Character import Character
from Library import Library
from pprint import pprint

class Game(object):
    def __init__(self):
        self._characters = {}
        
    def AddCharacter(self, name, job, age, gender, alignment, stats, max_hp, armour_class):
        this_character = Character(name, job, age, gender, alignment, stats, max_hp, armour_class)
        self._characters[name] = this_character
        return this_character
    
    def AddToInventory(self, character_name, item_name, value):
        if not character_name in self._characters:
            return False
        return self._characters[character_name].AddToInventory(item_name, value)

    def RemoveFromInventory(self, character_name, item_name, value):
        if not character_name in self._characters:
            return False
        return self._characters[character_name].RemoveFromInventory(item_name, value)

    def Equip(self, character_name, item_name, value):
        if not character_name in self._characters:
            return False
        return self._characters[character_name].Equip(item_name, value)

    def Unequip(self, character_name, item_name, value):
        if not character_name in self._characters:
            return False
        return self._characters[character_name].Unequip(item_name, value)

    def GetInventory(self, character_name):
        if not character_name in self._characters:
            return False
        return self._characters[character_name].GetInventory()

    def GetEquipedItems(self, character_name):
        if not character_name in self._characters:
            return False
        return self._characters[character_name].GetEquipedItems()
    
    def IncrementLevel(self, name, library):
        next_level_options = self._characters[name].GetNextLevelOptions(library)

        selected_options = {}
        for option_uuid in next_level_options:
            selected_options[option_uuid] = []
            option_dict = next_level_options[option_uuid]
            for ii in range(option_dict['num_options']):
                selected_options[option_uuid].append(option_dict['feature_uuids'][ii])

        self._characters[name].IncrementLevel(library, selected_options)
        return self._characters[name].GetLevel(), self._characters[name].GetLearnedFeatures()


class BackendServer(object):
    def __init__(self):
        self._library = Library()
        effects = Importer.ImportEffects("effects_lib.csv")
        self._library.AddDict("effects", effects)

        features = Importer.ImportFeatures("features_lib.csv", self._library)
        self._library.AddDict("features", features)
        
        options = Importer.ImportOptions("options_lib.csv", self._library)
        self._library.AddDict("options", options)
        
        jobs = Importer.ImportJobs("jobs_lib.csv", self._library) 
        self._library.AddDict("jobs", jobs)
        self._game = Game()
        self._context = {
            'characters' : {},
            'curr_character': {'name': '', 'job': '', 'level': '', 'age': '', 'gender': '', 
                'stats': {'STR': 0, 'DEX': 0, 'CON': 0, 'INT': 0, 'WIS': 0, 'CHR': 0},
                'HP': 0, 
                'AC': 0,
                'equiped': {},
                'inventory': {},
                'learned_features': {}
            }
        }

    def AddToInventory(self, character_name, item_name, value):
        if self._game.AddToInventory(character_name, item_name, value):
            self._context['characters'][character_name]['inventory'] = self._game.GetInventory(character_name)
            pprint(self._context['characters'][character_name]['inventory'])
            return True
        return False

    def RemoveFromInventory(self, character_name, item_name, value):
        if self._game.RemoveFromInventory(character_name, item_name, value):
            self._context['characters'][character_name]['inventory'] = self._game.GetInventory(character_name)
            return True
        return False

    def Equip(self, character_name, item_name, value):
        if self._game.Equip(character_name, item_name, value):
            self._context['characters'][character_name]['inventory'] = self._game.GetInventory(character_name)
            self._context['characters'][character_name]['equiped'] = self._game.GetEquipedItems(character_name)
            return True
        return False

    def Unequip(self, character_name, item_name, value):
        if self._game.Unequip(character_name, item_name, value):
            self._context['characters'][character_name]['inventory'] = self._game.GetInventory(character_name)
            self._context['characters'][character_name]['equiped'] = self._game.GetEquipedItems(character_name)
            return True
        return False

    def AddCharacter(self, name, job, age, gender, alignment, stats, max_hp, armour_class):
        this_character = self._game.AddCharacter(name, job, age, gender, alignment, stats, max_hp, armour_class)

        if (this_character == None):
            return False

        # Create the dict for front end
        this_character_dict = {}
        this_character_dict['name'] = name
        this_character_dict['level'] = this_character.GetLevel()
        this_character_dict['age'] = this_character.GetAge()
        this_character_dict['equiped'] = this_character.GetEquipedItems()
        this_character_dict['gender'] = this_character.GetGender()
        this_character_dict['stats'] = this_character.GetStats()
        this_character_dict['inventory'] = this_character.GetInventory()
        this_character_dict['job_uuid'] = this_character.GetJob()

        this_character_dict['learned_features'] = {}
        feature_uuids = this_character.GetLearnedFeatures()
        for feature_uuid in feature_uuids:
            feature = self._library.Get('features', feature_uuid)
            this_character_dict['learned_features'][feature_uuid] = {}
            this_character_dict['learned_features'][feature_uuid]['name'] = feature.GetName()
            this_character_dict['learned_features'][feature_uuid]['description'] = feature.GetDescription()

        # Get the job from the library to get the name
        this_job = self._library.Get('jobs', this_character.GetJob())
        this_character_dict['job_name'] = this_job.GetName()

        self._context['characters'][name] = this_character_dict
        return True

    def IncrementLevel(self, name):
        level, learned_features = self._game.IncrementLevel(name, self._library)
        
        self._context['characters'][name]['learned_features'] = {}
        for feature_uuid in learned_features: 
            feature = self._library.Get('features', feature_uuid)
            learned_feature = {}
            learned_feature['name'] = feature.GetName()
            learned_feature['description'] = feature.GetDescription()
            self._context['characters'][name]['learned_features'][''.join([c for c in str(feature_uuid) if c.isalpha()][:6])] = learned_feature

        self._context['characters'][name]['level'] = level

    def GetContext(self):
        return self._context

    def ImportToLibrary(self, dict_name, filepath):
        return Importer.Import(self._library, dict_name, filepath)


