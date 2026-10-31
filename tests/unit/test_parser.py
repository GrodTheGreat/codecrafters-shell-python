import pytest

from psh.parser import Parser


@pytest.fixture
def parser() -> Parser:
    return Parser()


class TestParser:
    def test_words(self, parser: Parser) -> None:
        line = "echo hello world"
        args = parser.parse(line)
        assert args == ["echo", "hello", "world"]
        line = "echo one two three"
        args = parser.parse(line)
        assert args == ["echo", "one", "two", "three"]

    class TestSingleQuotes:
        def test_single_quotes_preserve_spaces_within_quotes(
            self, parser: Parser
        ) -> None:
            line = "echo 'hello    world'"
            args = parser.parse(line)
            assert args == ["echo", "hello    world"]

        def test_consecutive_spaces_collapse_unless_quoted(
            self, parser: Parser
        ) -> None:
            line = "echo hello    world"
            args = parser.parse(line)
            assert args == ["echo", "hello", "world"]

        def test_adjacent_quoted_strings_are_concatenated(self, parser: Parser) -> None:
            line = "echo 'hello''world'"
            args = parser.parse(line)
            assert args == ["echo", "helloworld"]

        def test_empty_quotes_are_ignored(self, parser: Parser) -> None:
            line = "echo hello''world"
            args = parser.parse(line)
            assert args == ["echo", "helloworld"]

    class TestDoubleQuotes:
        def test_double_quotes_preserve_spaces_within_quotes(
            self, parser: Parser
        ) -> None:
            line = 'echo "hello    world"'
            args = parser.parse(line)
            assert args == ["echo", "hello    world"]

        def test_quoted_strings_next_to_each_other_are_concatenated(
            self, parser: Parser
        ) -> None:
            line = 'echo "hello""world"'
            args = parser.parse(line)
            assert args == ["echo", "helloworld"]

        def test_double_quotes_are_separate_arguments(self, parser: Parser) -> None:
            line = 'echo "hello" "world"'
            args = parser.parse(line)
            assert args == ["echo", "hello", "world"]

        def test_double_quotes_single_quotes_within_are_literal(
            self, parser: Parser
        ) -> None:
            line = 'echo "shell\'s test"'
            args = parser.parse(line)
            assert args == ["echo", "shell's test"]

    class TestBackslash:
        def test_backslash_outside_quotes(self, parser: Parser) -> None:
            line = r"echo multiple\ \ \ \ spaces"
            assert parser.parse(line) == ["echo", "multiple    spaces"]

        def test_backslash_escapes_quotes(self, parser: Parser) -> None:
            line = r"""echo \'\"literal quotes\"\'"""
            assert parser.parse(line) == ["echo", "'\"literal", "quotes\"'"]

        def test_backslash_before_ordinary_char(self, parser: Parser) -> None:
            line = r"echo ignore\_backslash"
            assert parser.parse(line) == ["echo", "ignore_backslash"]

        def test_backslash_escapes_backslash(self, parser: Parser) -> None:
            line = (
                r"cat /tmp/rat/\_ignored_1 /tmp/rat/ignore_\93 /tmp/rat/just_one_\\_51"
            )
            assert parser.parse(line) == [
                "cat",
                "/tmp/rat/_ignored_1",
                "/tmp/rat/ignore_93",
                "/tmp/rat/just_one_\\_51",
            ]
