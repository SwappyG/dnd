from Effect import Effect

class Feature(object):
    def __init__(self, name, this_uuid, description, effects, prereq_features, unlock_level = None):
        self._uuid = this_uuid
        self._name = name
        self._description = description
        self._effects = effects # name strings only
        self._prereq_features = prereq_features # list of name strings
        self._unlock_level = unlock_level

    def GetDict(self):
        feature_dict = {}
        feature_dict['uuid'] = self._uuid
        feature_dict['name'] = self._name
        feature_dict['description'] = self._description
        feature_dict['effects'] = self._effects
        feature_dict['prereq_features'] = self._prereq_features
        feature_dict['unlock_level'] = self._unlock_level

    def GetUUID(self):
        return self._uuid

    def GetName(self):
        return self._name
    
    def GetDescription(self):
        return self._description
    
    def GetEffects(self):
        return self._effects

    def GetPrereqFeatures(self):
        return self._prereq_features

    def GetUnlockLevel(self):
        return self._unlock_level

    def IsUnlocked(self, level, already_learned_features):
        if level < self._unlock_level:
            return False

        if not all(self._prereq_features in already_learned_features):
            return False

        return True
        