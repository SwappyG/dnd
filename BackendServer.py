import Importer
from Character import Character
from Library import Library

class Game(object):
    def __init__(self):
        self._characters = {}
        
    def AddCharacter(self, name, job, age, gender, alignment, stats):
        this_character = Character(name, job, age, gender, alignment, stats)
        self._characters.append(this_character)
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


class BackendServer(object):
    def __init__(self):
        self._library = Library()
        self._game = Game()
        self._context = {
            'characters' : {}
            'features': {}
        }

    def AddToInventory(self, character_name, item_name, value):
        if self._game.AddToInventory(character_name, item_name, value):
            self._context['characters']['name']['inventory'] = self._game.GetInventory(character_name)
            return True
        return False

    def RemoveFromInventory(self, character_name, item_name, value):
        if self._game.RemoveFromInventory(character_name, item_name, value):
            self._context['characters']['name']['inventory'] = self._game.GetInventory(character_name)
            return True
        return False

    def Equip(self, character_name, item_name, value):
        if self._game.Equip(character_name, item_name, value):
            self._context['characters']['name']['inventory'] = self._game.GetInventory(character_name)
            self._context['characters']['name']['equiped'] = self._game.GetEquipedItems(character_name)
            return True
        return False

    def Unequip(self, character_name, item_name, value):
        self._game.Unequip(character_name, item_name, value)
            self._context['characters']['name']['inventory'] = self._game.GetInventory(character_name)
            self._context['characters']['name']['equiped'] = self._game.GetEquipedItems(character_name)
            return True
        return False

    def AddCharacter(self, name, job, age, gender, alignment, stats):
        this_character = self._game.AddCharacter(self, name, job, age, gender, alignment, stats)

        if (this_character == None):
            return False

        # Create the dict for front end
        this_character_dict = {}
        this_character_dict['level'] = this_character.GetLevel()
        this_character_dict['age'] = this_character.GetAge()
        this_character_dict['equiped'] = this_character.GetEquipedItems()
        this_character_dict['gender'] = this_character.GetGender()
        this_character_dict['stats'] = this_character.GetStats()
        this_character_dict['inventory'] = this_character.GetInventory()
        this_character_dict['job_uuid'] = this_character.GetJob()

        this_character_dict['learned_features'] = {}
        feature_uuids = this_character.GetLearnedFeatures()
        for feature_uuid in features:
            feature = self._library.Get('features', feature_uuid)
            this_character_dict['learned_features'][feature_uuid] = {}
            this_character_dict['learned_features'][feature_uuid]['name'] = feature.GetName()
            this_character_dict['learned_features'][feature_uuid]['description'] = feature.GetDescription()

        # Get the job from the library to get the name
        this_job = self._library.Get('jobs', this_character.GetJob())
        this_character_dict['job_name'] = this_job.GetName()

        self._context['characters'][name] = this_character_dict
        return True

    def GetContext(self):
        self._context

    def ImportToLibrary(self, dict_name, filepath):
        return Importer.Import(self._library, dict_name, file_path)


