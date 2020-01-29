class Option(object):
    def __init__(self, name, this_uuid, description, features, unlock_levels, prereq_features=None):
        self._uuid = this_uuid  # uuid
        self._name = name  # string
        self._description = description  # string
        self._features = features  # name strings only
        self._prereq_features = [] if prereq_features is None else prereq_features  # list of uuids
        self._unlock_levels = unlock_levels  # list of uints

    def GetDict(self):
        return self.__str__

    def GetUUID(self):
        return self._uuid

    def GetName(self):
        return self._name

    def GetDescription(self):
        return self._description

    def GetAllFeatures(self):
        return self._features

    def GetUnlockLevels(self):
        return self._unlock_levels

    def GetPrereqFeatures(self):
        return self._prereq_features

    def HasFeature(self, feature_uuid):
        return feature_uuid in self._features

    def NumUnlocksAtLevel(self, level):
        """
        Get the number of features unlocked at this level
        """
        return len([ii for ii in self._unlock_levels if (int(ii) == level)])

    def NumUnlocksUntilLevel(self, level):
        """
        Get the number of features unlocked up to (excluding) this level
        """
        return len([ii for ii in self._unlock_levels if (int(ii) < level)])

    def RemainingFeatures(self, already_selected_features):
        """
        Returns all the features remaining in this option based on the features already known
        
        Parameters:
            already_selected_features (list of UUID): features to exclude from list
        """
        return [name for name in self._features if (name not in already_selected_features)]

    def GetOptions(self, level, already_selected_features):
        """
        Provides a dict of available features at the specified level

        Parameters:
            level (uint): level at which to see if any features are available
            already_selected_features (list of UUID): all features the character already knows

        Return:
            (dict) - num_options - how many features to select
                   - feature_uuids - the list of features to select from
        """

        # If there are any prerequisite feature, check that they've been satisfied
        if not set(self._prereq_features).issubset(already_selected_features):
            return {'num_options': 0, 'feature_uuids': []}  # 0 options, empty list

        # Get the remaining features and num unlocks that should've happened already
        # If the number of unlocks that should've happened is less than the number that did, we probably satisfied a
        # prereq later than the first unlock level. In that case, we're gonna have some extra unlocks this time
        # NOTE: This assumes that the features in this option are exclusive and cannot be learned by other means
        # If they are learned by other means, this will break
        remaining_features = self.RemainingFeatures(already_selected_features)
        unlocks_until_this_level = self.NumUnlocksUntilLevel(level)
        extra_unlocks = -len(self._features) + len(remaining_features) + unlocks_until_this_level

        # If there's nothing to unlock at this level, 0 and empty list in the dict
        num_unlocks = self.NumUnlocksAtLevel(level)
        if (num_unlocks == 0) and (extra_unlocks == 0):
            return {'num_options': 0, 'feature_uuids': []}  # 0 options, empty list

        # Otherwise, return the num unlocks and the available uuids
        return {
            'num_options': num_unlocks + extra_unlocks,
            'feature_uuids': remaining_features
        }

    def AsDict(self):
        """
        Puts all instance members into a dict and returns it 
        """
        return {
            'uuid': self._uuid,
            'name': self._name,
            'description': self._description,
            'features': self._features,
            'unlock_levels': self._unlock_levels,
            'prereq_features': self._prereq_features
        }
