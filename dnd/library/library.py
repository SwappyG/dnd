from dnd.library.feature import Feature
from dnd.library.option import Option
from dnd.library.effect import Effect
from dnd.library.item import Item
from dnd.library.job import Job

from typing import Dict
import dataclasses


@dataclasses.dataclass
class Library:
    effects: Dict[str, Effect]
    features: Dict[str, Feature]
    options: Dict[str, Option]
    jobs: Dict[str, Job]
    # items: Dict[str, Item]

    # def __init__(self,
    #              ):
    #     self.fea
    #     self._dicts = {
    #         'features': features,
    #         'effects': effects,
    #         'options': options,
    #         'items': items,
    #         'jobs': jobs
    #     }

    # def features(self):
    #     return self._dicts['features']
    #
    # def effects(self):
    #     return self._dicts['effects']
    #
    # def options(self):
    #     return self._dicts['options']
    #
    # def items(self):
    #     return self._dicts['items']
    #
    # def jobs(self):
    #     return self._dicts['jobs']

    # def get_lib(self, lib_name) -> Dict[str, object]:
    #     try:
    #         return self._dicts[lib_name.lower()]
    #     except KeyError:
    #         return {}
    #
    # def get(self, lib_name, key):
    #
    # def GetDict(self, dict_name):
    #
    #
    # def AddDict(self, name, new_dict):
    #     if name in self._dicts:
    #         print("Can't add new dict with name <{}> because it already exists in library".format(name))
    #         return False
    #
    #     self._dicts[name] = new_dict
    #
    # def Get(self, dict_name, key):
    #     try:
    #         return self.GetDict(dict_name)[this_uuid]
    #     except KeyError:
    #         print("Key <{}> not found in dict <{}>".format(this_uuid, dict_name))
    #         return None
    #
    # def Peek(self, dict_name, this_uuid):
    #     return (this_uuid in self.GetDict(dict_name))
    #
    # def GetUUIDFromName(self, dict_name, name):
    #     try:
    #         name_dict = self.GetNameUUIDAsDict(dict_name)
    #         return name_dict[name]
    #     except:
    #         print("Either the name <{}> or dict_name <{}> was not in library".format(name, dict_name))
    #         return None
    #
    # def GetUUIDs(self, dict_name):
    #     return [this_uuid for this_uuid in self.GetDict(dict_name)]
    #
    # def GetNames(self, dict_name):
    #     this_dict = self.GetDict(dict_name)
    #     return [this_dict[this_uuid].GetName() for this_uuid in this_dict]
    #
    # def GetNameUUIDAsDict(self, dict_name):
    #     this_dict = self.GetDict(dict_name)
    #     return {this_dict[this_uuid].GetName(): this_uuid for this_uuid in this_dict}
