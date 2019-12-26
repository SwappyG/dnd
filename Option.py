from Feature import Feature
from Effect import Effect

class Option(object):
    def __init__(self, name, this_uuid, description, features, prereq_features, unlock_levels):
        self._uuid = this_uuid
        self._name = name
        self._description = description
        self._features = features # name strings only
        self._prereq_features = prereq_features
        self._unlock_levels = unlock_levels

    def GetUUID(self):
        return self._uuid

    def GetName(self):
        return self._name

    def GetDescription(self):
        return self._description

    def HasFeature(self, feature_uuid):
        return (feature_uuid in self._features)
        
    def GetAllFeatures(self):
        return self._features

    def GetUnlockLevels(self):
        return self._unlock_levels

    def GetPrereqFeatures(self):
        return self._prereq_features

    def IsConsistent(self, level, already_selected_features):
        expected_num_features = len([ii for ii in self._unlock_levels if ii <= level])
        return (expected_num_features == len(already_selected_features))

    def NumOptions(self, level):
        return len([ii for ii in self._unlock_levels if int(ii) == level])

    def RemainingFeatures(self, already_selected_features):
        return [name for name in self._features if (name not in already_selected_features)]

    def GetOptions(self, level, already_selected_features):
        """
        Provides a tuple of available features at the specified level

        Parameters:
            level (uint): level at which to see if any features are available
            already_selected_features (list of string): all features the character already knows

        Return:
            None if there's nothing to learn at this level or if prereqs aren't met
            (uint, list of string) - first index is the number of features that can be learned and the second is the list of options
        """
        if (self._prereq_features) != []:
            if not all([(feature in already_selected_features) for feature in self._prereq_features]):
                return None

        if self.NumOptions(level) == 0:
            return None

        return {
            'num_options': self.NumOptions(level),
            'feature_uuids': self.RemainingFeatures(already_selected_features)
        }