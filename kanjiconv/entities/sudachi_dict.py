from enum import Enum


class SudachiDictType(Enum):
    CORE = "core"
    SMALL = "small"
    FULL = "full"

    def __str__(self):
        return self.value
