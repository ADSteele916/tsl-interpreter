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
        self.values = values
        self.outer = outer

    def find(self, key):
        if key in self.values:
            return self.values[key]
        elif self.outer is not None:
            return self.outer.find(key)
        else:
            return None

    def add(self, key, value) -> bool:
        if key not in self.values:
            self.values[key] = value
            return True
        else:
            return False

    def set(self, key, value) -> bool:
        if key in self.values:
            self.values[key] = value
            return True
        else:
            return False
