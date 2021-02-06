from dnd.library.library import Library
from threading import Lock
from typing import Any, Dict, Tuple
from dnd.library.effect import Effect
import dataclasses
import copy


class RuntimeLibrary:
    _lib: Library
    _lock: Lock

    def __init__(self, library: Library):
        self._lock = Lock()
        self._lib = library

    def _assert_type(self, dict_name: str, element: Any):
        if not isinstance(element, self._lib.__dict__.get('types')[dict_name]):
            raise ValueError(f"Can't update dictionary [{dict_name}] with object type [{type(element)}]."
                             f"must be of type [{type(self._lib.__dict__.get('types')[dict_name])}]")

    def _assert_valid_dict(self, dict_name: str):
        names_and_types = {f.name: f.type for f in dataclasses.fields(self._lib)}
        if dict_name not in names_and_types:
            raise KeyError(f"No dictionary named [{dict_name}] in library")

    def _assert_key(self, dict_name: str, key_name):
        if key_name not in self._lib.__dict__.get(dict_name):
            raise KeyError(f"No key named [{key_name}] in dictionary [{dict_name}] in library")

    def _assert_not_key(self, dict_name: str, key_name):
        if key_name in self._lib.__dict__.get(dict_name):
            raise KeyError(f"Key named [{key_name}] already in dictionary [{dict_name}] in library")

    @staticmethod
    def _assert_equal(key_name: str, element_name: str):
        if key_name != element_name:
            raise ValueError(f"key name [{key_name}] must not match element name [{element_name}]")

    def lib_names(self) -> Tuple[str]:
        with self._lock:
            return tuple([str(f.name) for f in dataclasses.fields(self._lib)])

    def lib_keys(self, dict_name: str) -> Tuple[str]:
        with self._lock:
            self._assert_valid_dict(dict_name)
            return tuple(self._lib.__dict__.get(dict_name).keys())

    def get(self, dict_name: str, key_name: str) -> Any:
        with self._lock:
            if not any({field.name == dict_name for field in dataclasses.fields(self._lib)}):
                raise KeyError(f"No dictionary named [{dict_name}] in library")

            d = self._lib.__dict__.get(dict_name)
            if key_name not in d:
                raise KeyError(f"No element named [{key_name}] in dictionary [{dict_name}] in library")

            return copy.deepcopy(d[key_name])

    def add(self, dict_name: str, element: Any):
        with self._lock:
            self._assert_valid_dict(dict_name)
            self._assert_type(dict_name, element)
            self._assert_not_key(dict_name, element.name)
            self._lib.__dict__.get(dict_name)[element.name] = element

    def replace(self, dict_name: str, key_name: str, element: Any):
        with self._lock:
            self._assert_valid_dict(dict_name)
            self._assert_type(dict_name, element)
            self._assert_key(dict_name, key_name)
            self._assert_equal(key_name, element.name)
            self._lib.__dict__.get(dict_name)[element.name] = element
