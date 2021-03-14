from enum import Enum


class JsonEnum(Enum):
    def __getstate__(self):
        return self.name


class JsonFrozenSet(frozenset):
    def __getstate__(self):
        return list(self.copy())
