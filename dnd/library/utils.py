from typing import Set, Dict, Optional
from copy import deepcopy
from dnd.library.library import Library
from dnd.library.item import ItemType
from dnd.library.character import Character, CharacterData
from dnd.library.ability_score import AbilityScore, is_stat_buff_level
from dnd.library.option import OptionReply
from dnd.utils.exceptions import raise_if_false, raise_if_true
import numpy as np

UnlockedOptions = Dict[str, OptionReply]
SelectedOptions = Dict[str, Set[str]]


def _update_learned_features(learned_features: Set[str], option_reply: UnlockedOptions,
                             selected_options: SelectedOptions) -> Set[str]:
    new_feats = deepcopy(learned_features)
    for option_name in option_reply:
        num_options = option_reply[option_name].num_options
        features = option_reply[option_name].features

        raise_if_false(option_name in selected_options,
                       f"[{option_name}] must be part of selected options [{selected_options}]")

        raise_if_false(len(selected_options[option_name]) == num_options,
                       f"[{option_name}] must have [{num_options}] options")

        raise_if_true(any([(feat not in features) for feat in selected_options[option_name]]),
                      f"selected options for [{option_name}] contain invalid features, "
                      f"[{selected_options[option_name]}] isn't a subset of [{features}]")

        new_feats = new_feats.union(selected_options[option_name])

    return new_feats


def _update_max_hp(hit_die: int, curr_max_hp: int, ability_score: AbilityScore, do_roll: bool):
    if do_roll:
        return curr_max_hp + np.random.randint(1, hit_die + 1) + ability_score.modifier().CON

    return curr_max_hp + (hit_die // 2) + 1 + ability_score.modifier().CON


def _update_ability_score(curr_level: int, curr_ability_score: AbilityScore,
                          ability_score_buffs: Optional[AbilityScore]) -> AbilityScore:
    if not is_stat_buff_level(curr_level + 1):
        return curr_ability_score

    raise_if_false(ability_score_buffs is None, f"Level [{curr_level + 1}] requires stat buffs")
    raise_if_false(ability_score_buffs.sum() != 2, f"Stat buff total must be 2 not [{ability_score_buffs.sum()}]")
    return curr_ability_score + ability_score_buffs


def get_ac(library: Library, equipped_items: Dict[str, int]) -> int:
    raise_if_false(any([item_name not in library.items for item_name in equipped_items]),
                   f"equipped items [{equipped_items}] not found in library while trying to retrieve AC")
    return sum([library.items[name].ac for name in equipped_items if library.items[name].item_type == ItemType.ARMOR])


def get_unlocked_features(library: Library, job_name: str, level: int) -> Set[str]:
    """
    Get the job object and all possible associated features. Return a list with all that unlock at
    the specified level.
    Return:
        - list of UUIDs - all features that unlock at specified level
    """
    raise_if_false(job_name in library.jobs, f"[{job_name}] was not in the jobs library")
    feature_names = library.jobs[job_name].features

    raise_if_false(any([name not in library.features for name in feature_names]),
                   f"Some feature names were missing from features library, [{feature_names}]")

    return set([name for name in feature_names if (level == library.features[name].unlock_level)])


def get_unlocked_options_at_next_level(library: Library, job_name: str, curr_level: int,
                                       learned_features: Set[str]) -> UnlockedOptions:
    """
    Gets the job object and all associated options to determine if anything unlocks at specified level
    with the currently known features.

    Return:
    - (dict of dicts) - the keys for the dict are option uuids
                      - the value dicts contain 'num_options' and 'feature_uuids' as keys
                      - 'num_options' (uint) is the number of features that should be selected
                      - 'feature_uuids (list of UUIDs) are the features to select from
                      - if there is nothing to unlock, 'num_option' will be 0 and 'feature_uuids will be []
    """
    raise_if_false(job_name in library.jobs, f"[{job_name}] was not in the jobs library")
    option_names = library.jobs[job_name].options

    learned_features = deepcopy(learned_features).union(get_unlocked_features(library, job_name, curr_level + 1))

    # Iterate for all options in this job
    unlocked_options = {}
    for option_name in option_names:
        raise_if_false(option_name in library.options, f"[{option_name}] was not in the options library")

        option = library.options[option_name]
        option_reply = option.get_feature_options(curr_level, learned_features)
        if option_reply.num_options != 0:
            unlocked_options[option_name] = option_reply

    return unlocked_options


def increment_level(library: Library,
                    character: Character,
                    selected_options: SelectedOptions,
                    roll_for_hp: bool,
                    ability_score_buffs: Optional[AbilityScore]) -> Character:
    """
    Increments the level of this character by 1, applying any selected options and stat buffs
    Params:
        - selected options - dict of option name to set of feature names
            - use get_unlocked_options_at_next_level to build this argument
            - for each option, select the specified number of features from the corresponding list
        - stat_buffs:
            - if this is a stat buff level, provide updated stats
    """
    unlocked_options = get_unlocked_options_at_next_level(library,
                                                          character.character_data.job,
                                                          character.character_data.level,
                                                          character.learned_features())

    new_feats = _update_learned_features(character.learned_features(), unlocked_options, selected_options)
    new_max_hp = _update_max_hp(character.character_data.hit_die, character.character_data.max_hp,
                                character.character_data.ability_score, roll_for_hp)
    new_ability_score = _update_ability_score(character.character_data.level, character.character_data.ability_score,
                                              ability_score_buffs)

    character_data = CharacterData(name=character.character_data.name,
                                   job=character.character_data.job,
                                   age=character.character_data.age,
                                   gender=character.character_data.gender,
                                   alignment=character.character_data.alignment,
                                   level=character.character_data.level + 1,
                                   sub_level=0,
                                   ability_score=new_ability_score,
                                   max_hp=new_max_hp,
                                   hit_die=character.character_data.hit_die)

    return Character(character_data=character_data,
                     money=character.money(),
                     hp=character.hp(),
                     learned_features=character.learned_features().union(new_feats),
                     equipped_items=character.equipped_items(),
                     inventory=character.inventory())
