from Feature import Feature
from Effect import Effect

class Option(object):
    def __init__(self, name, this_uuid, description, features, prereq_features, unlock_levels):
        self._uuid = this_uuid # uuid
        self._name = name # string
        self._description = description # string
        self._features = features # name strings only
        self._prereq_features = prereq_features # list of uuids
        self._unlock_levels = unlock_levels # list of uints

    def GetDict(self):
        return self.__str__()

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
        return (feature_uuid in self._features)

    def NumUnlocksAtLevel(self, level):
        """
        Get the number of features unlocked at this level
        """
        return len([ii for ii in self._unlock_levels if (int(ii) == level)])

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
        if (self._prereq_features) != []:
            if not all([(feature in already_selected_features) for feature in self._prereq_features]):
                return {'num_options' : 0, 'feature_uuids':[] } # 0 options, empty list

        num_unlocks = self.NumUnlocksAtLevel(level)
        if num_unlocks == 0:
            return {'num_options' : 0, 'feature_uuids':[] } # 0 options, empty list

        return {
            'num_options': num_unlocks,
            'feature_uuids': self.RemainingFeatures(already_selected_features)
        }

    def __str__(self):
        """
        Puts all instance members into a dict and returns it 
        """
        return {
            'uuid' : self._uuid,
            'name' : self._name,
            'description' : self.description,
            'features' : self._features,
            'prereq_features' : self._prereq_features,
            'unlock_levels' : self._unlock_levels
        }