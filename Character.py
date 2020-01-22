from copy import deepcopy


# TODO: rename self._stats to self._stats5e
# Change it from dict to class, since it has fixed, known keys
# Provide another self._stats for custom user stats in the future

class Character(object):
    stat_buff_levels = [4, 8, 12, 16, 19]

    def __init__(self, name, job, age, gender, alignment, stats, max_hp, armor_class):
        """
        Args:
            name: [string] - name of character (player)
            job: [uuid] - uuid of the job
            age: [uint] - age of character
            gender: [string] - string describing gender (M,F,etc)
            alignment: [string] - string describing alignment (Neutral Neutral)
            stats: [dict of string:uint] - all stats this character has and their current values
            max_hp: [uint] - maximum hp this character can have
            armor_class: [uint] - the strength of the armor
        """
        self._name = name
        self._job = job
        self._age = str(age)
        self._gender = gender
        self._level = 0
        self._alignment = alignment
        self._learned_features = []  # name strings
        self._inventory = {}  # name string : quantity
        self._equipped_items = {}  # name string : quantity
        self._stats = stats
        self._max_hp = max_hp
        self._armor_class = armor_class
        self._hp = self._max_hp  # uint

    def SetHP(self, val):
        """
        Sets self._hp to val, clips between 0 and self._max_hp if val is out of bounds 
        """
        self._hp = max(0, min(val, self._max_hp))  # clip between zero and max

    def SetMaxHP(self, val):
        """
        Sets self._max_hp, clips below at 0
        TODO: This should be determined using formula and CON stat
        """
        self._max_hp = max(0, val)
        self.SetHP(self.GetHP())  # make sure current HP is clipped to be between 0 and max

    def SetAC(self, val):
        """
        Sets self._armor_class, clips below at 0
        """
        self._armor_class = max(0, val)

    def AddToInventory(self, item_name, quantity):
        """Adds an item to the inventory, or increments the quantity if the item already exists.
        
        Arguments:
            item_name {string} -- name of the item
            quantity {[type]} -- quantity to add (cannot be negative)
        
        Returns:
            bool -- True if arguments are valid, False otherwise
        """
        # If the item is already in inventory, just increment the quantity
        if item_name in self._inventory:
            if quantity >= 0:
                self._inventory[item_name] += quantity
                return True

            print("Quantity can't be negative when adding item to inventory, got [{}]".format(quantity))
            return False

            # If the isn't, create the key and set the value as the quantity
        else:
            if quantity >= 0:
                self._inventory[item_name] = quantity
                return True

            print("Quantity can't be negative when adding item to inventory, got [{}]".format(quantity))
            return False

    def RemoveFromInventory(self, item_name, quantity=None):
        """Removes an item from the inventory by specified quantity, or entirely if quantity is none or final
        quantity is negative.

        Params:
            - item_name (string): name of the item
            - quantity (uint): quantity to add (cannot be negative), None if full removal is desired

        Return:
            - True if arguments are valid, False otherwise
        """

        # Change values only if item is in inventory
        if item_name in self._inventory:
            # If quantity is None, del the item
            if quantity is None:
                del self._inventory[item_name]
                return True

            # Make sure quantity is not negative
            if quantity < 0:
                print("Quantity can't be negative when removing item from inventory, got [{}]".format(quantity))
                return False

            # Update the quantity. if its negative after update, del the item
            self._inventory[item_name] = max(0, self._inventory[item_name] - quantity)
            if self._inventory[item_name] <= 0:
                del self._inventory[item_name]

            return True

        # Item was never in inventory, return true since the end goal is satisfied
        return True

    def Equip(self, item_name, quantity):
        """
        Equips items from the inventory. Item must first be added to inventory, or this returns false
        If the quantity in inventory falls to 0, it will be removed from the inventory
        If the quantity to equip exceeds quantity in inventory, the max possible amount is equipped
        Params:
            - item_name (string): name of the item
            - quantity (uint): quantity to add (cannot be negative)
        Return:
            - True if arguments are valid, False otherwise
        """

        # Make sure the the specified quantity is positive
        if quantity <= 0:
            return False

        # Equip is only possible if item is in inventory
        if not (item_name in self._inventory):
            return False

        # equippable qty is min of desired and available
        quantity_to_equip = min(quantity, self._inventory[item_name])

        # If the item is already equipped, just increase value in dict
        if item_name in self._equipped_items:
            self._equipped_items[item_name] += quantity_to_equip

        # Otherwise, create a new key and set value to equippable qty
        else:
            self._equipped_items[item_name] = quantity_to_equip

        # Remove the equipped amount from the inventory, deleting if necessary
        self.RemoveFromInventory(item_name, quantity_to_equip)
        return True

    def Unequip(self, item_name, quantity=None):
        """
        Unequips equipped items. 
        If quantity specified is higher than value equipped, everything will be unequipped
        If quantity is None, everything will be unequipped.
        Unequipped items are added to inventory, not removed from the character 
        Params:
            - item_name (string): name of the item
            - quantity (uint or None): quantity to add (cannot be negative) (None if all should be removed)
        Return:
            - True if arguments are valid, False otherwise
        """
        # If the quantity is not None and negative, its an invalid input, reject it
        if (quantity is not None) and (quantity <= 0):
            return False

        if not (item_name in self._equipped_items):
            return False

        # If quantity is None, delete the item from equipped after caching the curr qty
        if quantity is None:
            quantity_to_unequip = self._equipped_items[item_name]
            del self._equipped_items[item_name]

        # if the qty is specified, only remove that much
        else:
            quantity_to_unequip = min(quantity, self._equipped_items[item_name])
            self._equipped_items[item_name] -= quantity_to_unequip

        # Add the removed qty to the inventory
        self.AddToInventory(item_name, quantity_to_unequip)

        # If the equipped item qty is now zero, delete it
        if self._equipped_items[item_name] == 0:
            del self._equipped_items[item_name]

        return True

    def IncrementLevel(self, library, selected_options, stat_buffs=None):
        """
        Increments the level of this character by 1, applying any selected options and stat buffs
        Params:
            - selected options (dict UUID:list of UUID)
                - The keys must be UUIDs for all the options unlocked at the upcoming level
                - The list of available options can be acquired using GetNextLevelOptions
                - Only options being unlocked at upcoming level should be in dict
                - The values must be a list of UUIDs of the features that were selected
                - The length of the list must match the 'num_options' key from the GetNextLevelOptions dict
                    for this particular option
                - the list of UUIDs must also all be part of the 'feature_uuids' key from the 
                    GetNextLevelOptions dict for this particular option
            - stat_buffs (list of string):
                - At specified levels, stat_buffs are required and a dict must be provide
                - The list must be either length 1 or 2, containing on of the possible stats that could be upgraded
        """
        # Get the job and options for this level
        opts_for_this_level = self._GetUnlockedOptions(library, self._level + 1, self._learned_features)
        new_learned_features = []

        # Iterate for all options for this level
        for opt_uuid in opts_for_this_level:

            # extract out the expected number of selected features and list of choices for this option 
            num_to_select = opts_for_this_level[opt_uuid]['num_options']
            feature_uuids = opts_for_this_level[opt_uuid]['feature_uuids']

            try:
                # Make sure that the args have the right number of selections for this option
                if len(selected_options[opt_uuid]) != num_to_select:
                    print(("Incorrect number of options selected for [{}], expected [{}] but got [{}]".format(
                        opt_uuid, num_to_select, len(selected_options[opt_uuid]))))
                    return False

                # Make sure every selection is actually valid in this option
                if not all([(opt in feature_uuids) for opt in selected_options[opt_uuid]]):
                    print(("Got invalid features selected, [{}] must all be part of [{}] for option [{}]".format(
                        selected_options[opt_uuid], feature_uuids, opt_uuid)))
                    return False

                # append to our list of all the new learned features
                new_learned_features = new_learned_features + selected_options[opt_uuid]

            # If the selected_options doesn't contain this option, return False
            except KeyError:
                print("Invalid option name [{}] found in selected options".format(opt_uuid))
                return False

        # Make a copy before we update anything
        stats = deepcopy(self._stats)

        # If this is a stat buff level, update stats
        if (self._level + 1) in Character.stat_buff_levels:

            # If stat_buffs is None, return False since it must be specified 
            if stat_buffs is None:
                print("Level [{}] requires the stat_buffs argument to be set".format(self._level + 1))
                return False

            try:
                # If there's only one stat, increment by 2
                if len(stat_buffs) == 1:
                    stats[stat_buffs] += 2

                # If there are two stats, increment each by one
                elif len(stat_buffs) == 2:
                    stats[stat_buffs[0]] += 1
                    stats[stat_buffs[1]] += 1

                # Only 1 and 2 are valid lengths, so return False if its not those
                else:
                    print("Invalid number of keys for stat_buffs, must be either 1 or 2, got [{}]".format(
                        len(stat_buffs)))
                    return False

            # If the is not a valid key, return False
            except KeyError:
                print("Invalid key in stat_buffs, one of [{}] are not a valid stats".format(stat_buffs))

        # Everything went smoothly if we made it this far, so update our actual character now
        self._stats = stats
        self._learned_features = self._learned_features + new_learned_features
        self._level += 1
        return True

    def GetHP(self):
        return self._hp

    def GetMaxHP(self):
        return self._max_hp

    def GetAC(self):
        return self._armor_class

    def GetLearnedFeatures(self):
        return self._learned_features

    def GetInventory(self):
        return self._inventory

    def GetEquippedItems(self):
        return self._equipped_items

    def GetInventoryQuantity(self, item_name):
        if item_name in self._inventory:
            return self._inventory[item_name]
        else:
            return 0

    def GetEquippedQuantity(self, item_name):
        if item_name in self._equipped_items:
            return self._equipped_items[item_name]
        else:
            return 0

    def GetTotalQuantity(self, item_name):
        return self.GetInventoryQuantity(item_name) + self.GetEquippedQuantity(item_name)

    def GetName(self):
        return self._name

    def GetJob(self):
        return self._job

    def GetAge(self):
        return self._age

    def GetGender(self):
        return self._gender

    def GetLevel(self):
        return self._level

    def GetStats(self):
        return self._stats

    def GetNextLevelOptions(self, library):
        """
        Uses the library and this character's job and current level to return a dict of 
        unlockable options for the next level
        """
        # make a copy of the learned_features since we're going to temporarily modify it 
        learned_features = deepcopy(self._learned_features)

        # Get the unlocked features of next level, and append to already learned features
        learned_features = learned_features + self._GetUnlockedFeatures(library, self._level + 1)

        # Get the options unlocked at the next level with current + upcoming known features
        return self._GetUnlockedOptions(library, self._level + 1, learned_features)

    def _GetUnlockedFeatures(self, library, level):
        """
        Get the job object and all possible associated features. Return a list with all that unlock at
        the specified level.
        Return:
            - list of UUIDs - all features that unlock at specified level  
        """
        job_obj = library.Get("jobs", self._job)
        features = job_obj.GetAllFeatures()

        return [name for name in features if (level == library.Get("features", name).GetUnlockLevel())]

    def _GetUnlockedOptions(self, library, level, learned_features):
        """
        Gets the job object and all associated options to determine if anything unlocks at specified level
        with the currently known features.
        
        Return:
        - (dict of dicts) - the keys for the dict are option uuids
                          - the value dicts contain 'num_options' and 'feature_uuids' as keys
                          - 'num_options' (uint) is the number of features that should be selected
                          - 'feature_uuids (list of UUIDs) are the features to select from
                          - if there is nothing to unlock, 'num_option' will be 0 and 'feature_uuids will be []
        """

        # Get the job and all options
        job_obj = library.Get("jobs", self._job)
        options = job_obj.GetAllOptions()

        # Iterate for all options in this job
        unlocked_options = {}
        for option_uuid in options:

            # Get the actual option from the library using the UUID
            this_option = library.Get('options', option_uuid)

            # If it doesn't exist in the library, print the error and continue
            if this_option is None:
                print("Failed to get an option out of the library with uuid <{}>".format(option_uuid))
                continue

            # Get all the features that unlock at this level for this option
            this_option_features = this_option.GetOptions(level, learned_features)

            # Only add to our dict if this option actually has any unlocks for this level
            if this_option_features['num_options'] != 0:
                unlocked_options[option_uuid] = this_option_features

        # Return our dict with all our options
        return unlocked_options
