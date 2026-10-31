from dataclasses import dataclass


@dataclass
class PlainPart:
    value: str


@dataclass
class SingleQuotePart:
    value: str


@dataclass
class DoubleQuotePart:
    value: str


Part = PlainPart | SingleQuotePart | DoubleQuotePart


class Parser:
    def __init__(self) -> None:
        self.line = ""
        self.current = 0
        self.words = []
        self.parts: list[Part] = []

    def parse(self, line: str) -> list[str]:
        self.__init__()
        self.line = line
        while not self.is_at_end():
            self.word()
        if self.parts:
            self.words.append(self.parts)
        return self.collect()

    def collect(self) -> list[str]:
        words = []
        for word in self.words:
            w = ""
            for part in word:
                match part:
                    case PlainPart(value):
                        parts = []
                        i = 0
                        while i < len(value):
                            c = value[i]
                            if c == "\\":
                                parts.append(value[i + 1])
                                i += 1
                            else:
                                parts.append(value[i])
                            i += 1
                        w += "".join(parts)
                    case SingleQuotePart(value):
                        w += "".join([c for c in value[1:-1]])
                    case DoubleQuotePart(value):
                        w += "".join([c for c in value[1:-1]])
            words.append(w)
        return words

    def word(self) -> None:
        match self.peek():
            case " " | "\r" | "\t" | "\n":
                if self.parts:
                    self.words.append(self.parts)
                self.parts = []
                self.advance()
            case "'":
                self.single_quotes()
            case '"':
                self.double_quotes()
            case _:
                self.plain()

    def plain(self) -> None:
        start = self.current
        while not self.is_at_end() and self.peek() not in " \n\t\r\"'":
            if self.peek() == "\\":
                self.advance()
            self.advance()
        self.parts.append(PlainPart(self.line[start : self.current]))

    def single_quotes(self) -> None:
        start = self.current
        self.advance()
        while not self.is_at_end() and self.peek() != "'":
            self.advance()
        # TODO Could be at end, but a single quoted string would span multiple lines. Throw?
        self.advance()
        self.parts.append(SingleQuotePart(self.line[start : self.current]))

    def double_quotes(self) -> None:
        start = self.current
        self.advance()
        while not self.is_at_end() and self.peek() != '"':
            if self.peek() == "\\":
                self.advance()
            self.advance()
        # TODO Could be at end, but a double quoted string would span multiple lines. Throw?
        self.advance()
        self.parts.append(DoubleQuotePart(self.line[start : self.current]))

    def is_at_end(self) -> bool:
        return self.current >= len(self.line)

    def peek(self) -> str:
        if self.is_at_end():
            return ""
        return self.line[self.current]

    def advance(self) -> str:
        if self.is_at_end():
            raise Exception
        character = self.line[self.current]
        self.current += 1
        return character
