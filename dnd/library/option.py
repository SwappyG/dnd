from typing import List, Set, Dict, NamedTuple
import dataclasses
from pprint import pformat


class OptionReply(NamedTuple):
    num_options: int
    features: Set[str]


@dataclasses.dataclass(frozen=True)
class Option(object):
    name: str
    desc: str
    features: Set[str]
    prereq_features: Set[str]
    unlock_levels: List[int]

    def has_feature(self, feature_name: str) -> bool:
        return feature_name in self.features

    def num_unlocks_at_level(self, level: int) -> int:
        """
        Get the number of features unlocked at this level
        """
        return len([ii for ii in self.unlock_levels if (ii == level)])

    def remaining_features(self, already_selected_features: Set[str]) -> Set[str]:
        """
        Returns all the features remaining in this option based on the features already known
        """
        return {name for name in self.features if (name not in already_selected_features)}

    def get_feature_options(self, level: int, already_selected_features: Set[str]) -> OptionReply:
        """
        Provides a dict of available features at the specified level

        Parameters:
            level (uint): level at which to see if any features are available
            already_selected_features (list of string): all features the character already knows

        Return:
            (dict) - num_options - how many features to select
                   - feature_uuids - the list of features to select from
        """

        # If there are any prerequisite feature, check that they've been satisfied
        if len(self.prereq_features) != 0:
            if any([(feature not in already_selected_features) for feature in self.prereq_features]):
                return OptionReply(num_options=0, features=set([]))

        num_unlocks = self.num_unlocks_at_level(level)
        if num_unlocks == 0:
            return OptionReply(num_options=0, features=set([]))

        return OptionReply(num_options=num_unlocks, features=self.remaining_features(already_selected_features))

    def as_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return pformat(self.asdict())
