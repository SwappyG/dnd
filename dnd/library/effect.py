from typing import NamedTuple, Dict
from pprint import pformat
import dataclasses


@dataclasses.dataclass(frozen=True)
class Effect:
    name: str
    effect_type: str
    duration: str
    desc: str

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.as_dict())
