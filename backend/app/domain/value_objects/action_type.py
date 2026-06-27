from enum import Enum


class ActionType(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    BLUR = "blur"
    HIDE = "hide"
    REPLACE = "replace"
    BLOCK = "block"
