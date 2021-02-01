from typing import Set, Dict
from pprint import pformat
import dataclasses


@dataclasses.dataclass
class Job(object):
    name: str
    desc: str
    features: Set[str]
    options: Set[str]

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.asdict())
