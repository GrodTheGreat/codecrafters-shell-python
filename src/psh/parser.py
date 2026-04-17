from enum import Enum, auto


class State(Enum):
    START = auto()
    ESCAPED = auto()
    WORD = auto()
    IN_SINGLE_QUOTE = auto()
    IN_DOUBLE_QUOTE = auto()
    END = auto()


class ParseError(ValueError): ...


class Parser:
    def __init__(self, data: str) -> None:
        self._data = data
        self._tokens: list[str] = []
        self._state: State = State.START
        self._start: int = 0
        self._position: int = 0

    def parse(self) -> list[str]:
        while not self._is_at_end():
            char = self._advance()
            if char.isspace():
                word = self._data[self._start : self._position - 1]
                self._tokens.append(word)
                self._start = self._position
        return self._tokens

    def _advance(self) -> str:
        if self._position >= len(self._data):
            return ""
        char = self._data[self._position]
        self._position += 1
        return char

    def _is_at_end(self) -> bool:
        return self._position >= len(self._data)

    def _peek(self) -> str:
        if self._position + 1 >= len(self._data):
            return ""
        return self._data[self._position + 1]
