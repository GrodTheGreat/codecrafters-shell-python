from dataclasses import dataclass
from enum import StrEnum, auto, Enum
from typing import Any


class TokenType(StrEnum):
    WORD = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: Any


class LexerState(Enum):
    DEFAULT = auto()
    IN_WORD = auto()
    IN_SINGLE_QUOTE = auto()
    IN_DOUBLE_QUOTE = auto()
    IN_ESCAPE = auto()


class Lexer:
    def __init__(self, text: str) -> None:
        self._text = text
        self._position: int = 0
        self._current_character: str | None = self._text[self._position]
        self._buffer = ""
        self._state: LexerState = LexerState.DEFAULT
        self._return_state: LexerState = LexerState.DEFAULT
        self._tokens: list[Token] = []
        self._handlers = {
            LexerState.DEFAULT: self._handle_default,
            LexerState.IN_WORD: self._handle_word,
            LexerState.IN_ESCAPE: self._handle_escape,
            LexerState.IN_SINGLE_QUOTE: self._handle_single_quote,
            LexerState.IN_DOUBLE_QUOTE: self._handle_double_quote,
        }

    def tokenize(self) -> list[Token]:
        while self._current_character:
            self._handlers[self._state]()
        self._flush_buffer()
        self._tokens.append(Token(TokenType.EOF, None))
        return self._tokens

    def _advance(self) -> None:
        self._position += 1
        if self._position <= len(self._text) - 1:
            self._current_character = self._text[self._position]
        else:
            self._current_character = None

    def _flush_buffer(self) -> None:
        if self._buffer:
            self._tokens.append(Token(TokenType.WORD, self._buffer))
            self._buffer = ""
        self._state = LexerState.DEFAULT

    def _handle_default(self) -> None:
        if self._current_character.isspace():
            self._flush_buffer()
            self._advance()
        elif self._current_character == "\\":
            self._advance()
            self._state = LexerState.IN_ESCAPE
            self._return_state = LexerState.IN_WORD
        elif self._current_character == '"':
            self._advance()
            self._state = LexerState.IN_DOUBLE_QUOTE
        elif self._current_character == "'":
            self._advance()
            self._state = LexerState.IN_SINGLE_QUOTE
        else:
            self._state = LexerState.IN_WORD

    def _handle_double_quote(self) -> None:
        if self._current_character == '"':
            self._advance()
            self._state = LexerState.IN_WORD
        elif self._current_character == "\\" and self._peek() == '"':
            self._advance()
            self._return_state = LexerState.IN_DOUBLE_QUOTE
            self._state = LexerState.IN_ESCAPE
        else:
            self._buffer += self._current_character
            self._advance()

    def _handle_escape(self) -> None:
        self._buffer += self._current_character
        self._advance()
        self._state = self._return_state

    def _handle_single_quote(self) -> None:
        if self._current_character == "'":
            self._advance()
            self._state = LexerState.IN_WORD
        else:
            self._buffer += self._current_character
            self._advance()

    def _handle_word(self) -> None:
        if self._current_character.isspace():
            self._flush_buffer()
        elif self._current_character == "\\":
            self._advance()
            self._return_state = LexerState.IN_WORD
            self._state = LexerState.IN_ESCAPE
        elif self._current_character == '"':
            self._advance()
            self._state = LexerState.IN_DOUBLE_QUOTE
        elif self._current_character == "'":
            self._advance()
            self._state = LexerState.IN_SINGLE_QUOTE
        else:
            self._buffer += self._current_character
            self._advance()

    def _peek(self) -> str | None:
        next_position = self._position + 1
        if next_position < len(self._text):
            return self._text[next_position]
        return None


text = r'echo "\"Hello World!\""'
lexer = Lexer(text)
tokens = lexer.tokenize()
for token in tokens:
    print(token)
