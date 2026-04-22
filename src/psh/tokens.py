from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    COMMAND = auto()
    ARGUMENT = auto()
    SINGLE_QUOTE = auto()
    DOUBLE_QUOTE = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    token_type: TokenType
    lexeme: str
    literal: Any = None
