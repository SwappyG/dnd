class Job(object):
    def __init__(self, name, this_uuid, description, features, options):
        self._uuid = this_uuid  # uuid
        self._name = name  # string
        self._description = description  # string
        self._features = features  # list of uuids
        self._options = options  # list of uuids

    def GetDict(self):
        return self.__str__

    def GetUUID(self):
        return self._uuid

    def GetName(self):
        return self._name

    def GetDescription(self):
        return self._description

    def GetAllOptions(self):
        return self._options

    def GetAllFeatures(self):
        return self._features

    def AsDict(self):
        """
        Puts all instance members into a dict and returns it 
        """
        return str({
            'uuid': self._uuid,
            'name': self._name,
            'description': self._description,
            'features': self._features,
            'options': self._options
        })
