from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Union

if TYPE_CHECKING:
    from expressions import Expression, Function, PyFunction


class Environment:
    def __init__(
        self,
        values: Optional[Dict[str, Union[Expression, Function, PyFunction]]] = None,
        outer=None,
    ):
        if values is None:
            values = {}
        self.__values = values
        self.outer = outer

    def find(self, key):
        if key in self.__values:
            return self.__values[key]
        elif self.outer is not None:
            return self.outer.find(key)
        else:
            return None

    def in_outermost(self, key) -> bool:
        if self.outer is None:
            return key in self.__values
        else:
            return self.outer.in_outermost(key)

    def add(self, key, value) -> bool:
        if (
            key not in self.__values
            and self.outer is not None
            and not self.in_outermost(key)
        ):
            self.__values[key] = value
            return True
        else:
            return False

    def set(self, key, value) -> bool:
        if key in self.__values and self.outer is not None:
            self.__values[key] = value
            return True
        else:
            return False
