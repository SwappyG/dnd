from __future__ import annotations

from dnd.library.ability_score import AbilityScore
from dnd.library.character_data import CharacterData
from dnd.library.money import Money
from dnd.utils.exceptions import raise_if_false
from typing import Set, Dict, Optional

from pprint import pformat
import numpy as np


class Character:
    def __init__(self,
                 character_data: CharacterData,
                 money: Money,
                 hp: int,
                 learned_features: Set[str],
                 equipped_items: Dict[str, int],
                 inventory: Dict[str, int]):
        self.character_data = character_data
        self._dict = {
            'learned_features': learned_features,
            'hp': hp,
            'equipped_items': equipped_items,
            'inventory': inventory,
            'money': money,
            'temp_ability_score': AbilityScore()
        }

    def money(self) -> Money:
        return self._dict['money']

    def hp(self) -> int:
        return self._dict['hp']

    def learned_features(self) -> Set[str]:
        return self._dict['learned_features']

    def equipped_items(self) -> Dict[str, int]:
        return self._dict['equipped_items']

    def inventory(self) -> Dict[str, int]:
        return self._dict['inventory']

    def add_money(self, new_money: Money):
        self._dict['money'] = self._dict['money'] + new_money

    def remove_money(self, to_remove: Money):
        self._dict['money'] = self._dict['money'] - to_remove

    def set_hp(self, val) -> None:
        """
        Sets self._hp to val, clips between 0 and self._max_hp if val is out of bounds 
        """
        self._dict['hp'] = np.clip(val, 0, self.character_data.max_hp)

    def set_ac(self, val) -> None:
        self._dict['ac'] = max(0, val)

    def add_to_inventory(self, item_name: str, quantity: int) -> None:
        """
        Adds an item to the inventory, or increments the quantity if the item already exists.
        Return:
            - True if arguments are valid, False otherwise
        """
        raise_if_false(quantity >= 0, f"Quantity [{quantity}] can't be negative")

        # If the item is already in inventory, just increment the quantity
        if item_name in self._dict['inventory']:
            self._dict['inventory'][item_name] += quantity
        else:
            self._dict['inventory'][item_name] = quantity

    def remove_from_inventory(self, item_name: str, quantity: Optional[int] = None) -> None:
        """
        Removes an item from the inventory by specified quantity, or entirely if quantity is none or final quantity is
        negative
        """
        raise_if_false(quantity >= 0, f"Quantity [{quantity}] can't be negative")

        # Item was never in inventory, return true since the end goal is satisfied
        if item_name not in self._dict['inventory']:
            return

        # If quantity is None, del the item
        if quantity is None:
            del self._dict['inventory'][item_name]
            return

        # Update the quantity. if its negative after update, del the item
        self._dict['inventory'][item_name] = max(0, self._dict['inventory'][item_name] - quantity)
        if self._dict['inventory'][item_name] <= 0:
            del self._dict['inventory'][item_name]

    def equip(self, item_name: str, quantity: int) -> None:
        """
        Equips items from the inventory. Item must first be added to inventory, or this will raise RuntimeError
        If the quantity in inventory falls to 0, it will be removed from the inventory
        If the quantity to equip exceeds quantity in inventory, the max possible amount is equipped
        """
        raise_if_false(quantity >= 0, f"Quantity [{quantity}] can't be negative")
        raise_if_false(item_name in self._dict['inventory'], f"Can't equip [{item_name}], not in inventory")

        quantity_to_equip = min(quantity, self._dict['inventory'][item_name])
        if item_name in self._dict['equipped_items']:
            self._dict['equipped_items'][item_name] += quantity_to_equip
        else:
            self._dict['equipped_items'][item_name] = quantity_to_equip

        self.remove_from_inventory(item_name, quantity_to_equip)

    def unequip(self, item_name: str, quantity: Optional[int] = None) -> None:
        """
        Unequips equipped items.
        If quantity specified is higher than value equipped, everything will be unequipped
        If quantity is None, everything will be unequipped.
        Unequipped items are added to inventory, not removed from the character
        """
        raise_if_false((quantity is not None) and (quantity <= 0), f"Quantity [{quantity}] can't be negative")
        raise_if_false(item_name in self._dict['equipped_items'], f"Can't unequip [{item_name}], not equipped")

        if quantity is None:
            quantity_to_unequip = self._dict['equipped_items'][item_name]
            del self._dict['equipped_items'][item_name]

        else:
            quantity_to_unequip = min(quantity, self._dict['equipped_items'][item_name])
            self._dict['equipped_items'][item_name] -= quantity_to_unequip

        self.add_to_inventory(item_name, quantity_to_unequip)

        if self._dict['equipped_items'][item_name] == 0:
            del self._dict['equipped_items'][item_name]

    def as_dict(self) -> Dict[str, object]:
        d = self.character_data.as_dict()
        d.update(self._dict)
        return d

    def __str__(self) -> str:
        return pformat(self.as_dict())
