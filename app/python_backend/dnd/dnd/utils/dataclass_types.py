import dataclasses
from typing import Dict, Any
import abc


@dataclasses.dataclass(frozen=True)
class DataClassBase(abc.ABC):
    def as_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return str(self.as_dict())

    @staticmethod
    @abc.abstractmethod
    def from_json(j: Dict):
        pass