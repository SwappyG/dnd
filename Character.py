from Feature import Feature
from Option import Option
from Job import Job
from Item import Item

from copy import deepcopy

class Character(object):

    stat_buff_levels = [4,8,12,16,19]

    def __init__(self, name, job, age, gender, alignment, stats):
        self._name = name
        self._job = job
        self._age = str(age)
        self._gender = gender
        self._level = 0
        self._alignment = alignment # string
        self._learned_features = [] # name strings
        self._inventory = {} # name string : quantity
        self._equipped_items = {} # name string : bool
        self._stats = stats # name string : uint

    def AddToInventory(self, item_name, quantity):
        if quantity < 0:
            print(("Quantity can't be negative when adding item to inventory, got [{}]".format(quantity)))
            return False
        
        if item_name in self._inventory:
            self._inventory[item_name] += quantity
            return True

        self._inventory[item_name] = quantity
        return True


    def RemoveFromInventory(self, item_name, quantity = None):
        if item_name in self._inventory:
            if (quantity == None):
                self._inventory.pop(item_name)
                return True

            if quantity < 0:
                print(("Quantity can't be negative when removing item from inventory, got [{}]".format(quantity)))
                return False

            self._inventory[item_name] = max(0, self._inventory[item_name] - quantity) 
            return True
        return True

    def AddQuantity(self, item_name, quantity):
        if quantity < 0:
            print(("Quantity can't be negative, got [{}]".format(quantity)))
            return False

        if item_name in self._inventory:
            self._inventory[item_name] += quantity
            return True

        return False

    def Equip(self, item_name):
        if item_name in self._inventory:
            self._equipped_items[item_name] = True
            return True
        return False

    def Unequip(self, item_name):
        self._equipped_items.pop(item_name, None)
        
    def IncrementLevel(self, library, selected_options, stat_buffs = None):
        job_obj = library.Get('jobs', self._job)
        opts_for_this_level = job_obj.GetUnlockedOptions(library, self._level+1, self._learned_features)
        new_learned_features = []
        for opt_name in opts_for_this_level:
            num_to_select = opts_for_this_level[opt_name]['num_options']
            feature_uuids = opts_for_this_level[opt_name]['feature_uuids']
            try:
                if len(selected_options[opt_name]) != num_to_select:
                    print(("Incorrect number of options selected for [{}], expected [{}] but got [{}]".format(opt_name, num_to_select, len(selected_options[opt_name]))))
                    return False

                if not all([(opt in feature_uuids) for opt in selected_options[opt_name]]):
                    print(("Got invalid features selected, [{}] must all be part of [{}] for option [{}]".format(selected_options[opt_name], feature_uuids, opt_name)))
                    return False

                new_learned_features = new_learned_features + selected_options[opt_name]
            
            except KeyError:
                print(("Invalid option name [{}] found in selected options".format(opt_name)))
                return False

        if (self._level + 1) in Character.stat_buff_levels:
            if (stat_buffs == None):
                print(("Level [{}] requires the stat_buffs argument to be set".format(self._level + 1)))
                return False

            stats = deepcopy(self._stats)
            try:
                if len(stat_buffs) == 1:
                    stats[stat_buffs] += 2
                elif len(stat_buffs) == 2:
                    stats[stat_buffs[0]] += 1
                    stats[stat_buffs[1]] += 1
                else:
                    print("Invalid number of keys for stat_buffs, must be either 1 or 2, got [{}]".format(len(stat_buffs)))
                    return False
            except KeyError:
                print("Invalid key in stat_buffs, one of [{}] are not a valid stats".format(stat_buffs))

            self._stats = stats

        self._learned_features = self._learned_features + new_learned_features
        self._level += 1
        return True

    def GetLearnedFeatures(self):
        return self._learned_features

    def GetInventory(self):
        return self._inventory

    def GetEquipedItems(self):
        return self._equipped_items

    def GetName(self):
        return self._name

    def GetJobName(self):
        return self._job.GetName()

    def GetAge(self):
        return self._age
    
    def GetGender(self):
        return self._gender

    def GetLevel(self):
        return self._level

    def GetStats(self):
        return self._stats

    def GetNextLevelOptions(self, library):
        learned_features = deepcopy(self._learned_features)
        job_obj = library.Get("jobs", self._job)
        learned_features.append(job_obj.GetUnlockedFeatures(library, self._level + 1))
        return job_obj.GetUnlockedOptions(library, self._level+1, self._learned_features)