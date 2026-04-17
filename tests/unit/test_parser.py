from psh.parser import Parser


class TestParser:
    def test_words(self) -> None:
        line = "echo hello world"
        parser = Parser(line)
        tokens = parser.parse()
        assert tokens == ["echo", "hello", "world"]
        line = "echo one two three"
        parser = Parser(line)
        tokens = parser.parse()
        assert tokens == ["echo", "one", "two", "three"]

    class TestSingleQuotes:
        def test_single_quotes_preserve_spaces_within_quotes(self) -> None:
            line = "echo 'hello    world'"
            parser = Parser(line)
            tokens = parser.parse()
            assert tokens == ["echo", "hello    world"]

        def test_consecutive_spaces_collapse_unless_quoted(self) -> None:
            line = "echo hello    world"
            parser = Parser(line)
            tokens = parser.parse()
            assert tokens == ["echo", "hello", "world"]

        def test_adjacent_quoted_strings_are_concatenated(self) -> None:
            line = "echo 'hello''world'"
            parser = Parser(line)
            tokens = parser.parse()
            assert tokens == ["echo", "helloworld"]

        def test_empty_quotes_are_ignored(self) -> None:
            line = "echo hello''world"
            parser = Parser(line)
            tokens = parser.parse()
            assert tokens == ["echo", "helloworld"]

    class TestDoubleQuotes:
        def test_double_quotes_preserve_spaces_within_quotes(self) -> None:
            line = 'echo "hello    world"'
            parser = Parser(line)
            tokens = parser.parse()
            assert tokens == ["echo", "hello    world"]

        def test_quoted_strings_next_to_each_other_are_concatenated(self) -> None:
            line = 'echo "hello""world"'
            parser = Parser(line)
            tokens = parser.parse()
            assert tokens == ["echo", "helloworld"]

        def test_double_quotes_are_separate_arguments(self) -> None:
            line = 'echo "hello" "world"'
            parser = Parser(line)
            tokens = parser.parse()
            assert tokens == ["echo", "hello", "world"]

        def test_double_quotes_single_quotes_within_are_literal(self) -> None:
            line = 'echo "shell\'s test"'
            parser = Parser(line)
            tokens = parser.parse()
            assert tokens == ["echo", "shell's test"]
