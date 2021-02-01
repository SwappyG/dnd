from enum import Enum


class JsonEnum(Enum):
    def __getstate__(self):
        return self.name
