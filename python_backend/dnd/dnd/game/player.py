from __future__ import annotations

from dnd.library.ability_score import AbilityScore
from dnd.library.character import Character
from dnd.library.money import Money
from dnd.utils.exceptions import raise_if_false
from typing import Set, Dict, Optional
import dataclasses

from pprint import pformat
import numpy as np


@dataclasses.dataclass
class PlayerData:
    name: str
    hp: int
    equipped_items: Dict[str, int]
    inventory: Dict[str, int]
    money: Money
    temp_ability_score: AbilityScore = AbilityScore()

    @staticmethod
    def from_json(j: Dict) -> PlayerData:
        return PlayerData(name=j['name'],
                          hp=j['hp'],
                          equipped_items=dict(j['equipped_items']),
                          inventory=dict(j['inventory']),
                          money=j['money'],
                          temp_ability_score=AbilityScore.from_json(j['temp_ability_score']))

    def as_dict(self):
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return str(self.as_dict())


class Player:
    def __init__(self,
                 character: Character,
                 player_data: PlayerData):
        self.character_data = character
        self._player_data = player_data

    def money(self) -> Money:
        return self._player_data.money

    def hp(self) -> int:
        return self._player_data.hp

    def equipped_items(self) -> Dict[str, int]:
        return self._player_data.equipped_items

    def inventory(self) -> Dict[str, int]:
        return self._player_data.inventory

    def add_money(self, new_money: Money):
        self._player_data.money = self._player_data['money'] + new_money

    def remove_money(self, to_remove: Money):
        self._player_data.money = self._player_data.money - to_remove

    def set_hp(self, val) -> None:
        """
        Sets self._hp to val, clips between 0 and self._max_hp if val is out of bounds 
        """
        self._player_data.hp = np.clip(val, 0, self.character_data.max_hp)

    def set_ac(self, val) -> None:
        self._player_data.ac = max(0, val)

    def add_to_inventory(self, item_name: str, quantity: int) -> None:
        """
        Adds an item to the inventory, or increments the quantity if the item already exists.
        Return:
            - True if arguments are valid, False otherwise
        """
        raise_if_false(quantity >= 0, f"Quantity [{quantity}] can't be negative")

        # If the item is already in inventory, just increment the quantity
        if item_name in self._player_data.inventory:
            self._player_data.inventory[item_name] += quantity
        else:
            self._player_data.inventory[item_name] = quantity

    def remove_from_inventory(self, item_name: str, quantity: Optional[int] = None) -> None:
        """
        Removes an item from the inventory by specified quantity, or entirely if quantity is none or final quantity is
        negative
        """
        raise_if_false(quantity >= 0, f"Quantity [{quantity}] can't be negative")

        # Item was never in inventory, return true since the end goal is satisfied
        if item_name not in self._player_data.inventory:
            return

        # If quantity is None, del the item
        if quantity is None:
            del self._player_data.inventory[item_name]
            return

        # Update the quantity. if its negative after update, del the item
        self._player_data.inventory[item_name] = max(0, self._player_data.inventory[item_name] - quantity)
        if self._player_data.inventory[item_name] <= 0:
            del self._player_data.inventory[item_name]

    def equip(self, item_name: str, quantity: int) -> None:
        """
        Equips items from the inventory. Item must first be added to inventory, or this will raise RuntimeError
        If the quantity in inventory falls to 0, it will be removed from the inventory
        If the quantity to equip exceeds quantity in inventory, the max possible amount is equipped
        """
        raise_if_false(quantity >= 0, f"Quantity [{quantity}] can't be negative")
        raise_if_false(item_name in self._player_data.inventory, f"Can't equip [{item_name}], not in inventory")

        quantity_to_equip = min(quantity, self._player_data.inventory[item_name])
        if item_name in self._player_data.equipped_items:
            self._player_data.equipped_items[item_name] += quantity_to_equip
        else:
            self._player_data.equipped_items[item_name] = quantity_to_equip

        self.remove_from_inventory(item_name, quantity_to_equip)

    def unequip(self, item_name: str, quantity: Optional[int] = None) -> None:
        """
        Unequips equipped items.
        If quantity specified is higher than value equipped, everything will be unequipped
        If quantity is None, everything will be unequipped.
        Unequipped items are added to inventory, not removed from the character
        """
        raise_if_false((quantity is not None) and (quantity <= 0), f"Quantity [{quantity}] can't be negative")
        raise_if_false(item_name in self._player_data.equipped_items, f"Can't unequip [{item_name}], not equipped")

        if quantity is None:
            quantity_to_unequip = self._player_data.equipped_items[item_name]
            del self._player_data.equipped_items[item_name]

        else:
            quantity_to_unequip = min(quantity, self._player_data.equipped_items[item_name])
            self._player_data.equipped_items[item_name] -= quantity_to_unequip

        self.add_to_inventory(item_name, quantity_to_unequip)

        if self._player_data.equipped_items[item_name] == 0:
            del self._player_data.equipped_items[item_name]
