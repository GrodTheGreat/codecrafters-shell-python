import subprocess

from psh.parser import Parser

from .commands import BUILTINS, resolve_executable


def repl_read(parser: Parser) -> list[str]:
    command = input("$ ")
    args = parser.parse(command)
    return args


def repl_eval(args: list[str]) -> str | None:
    if not args:
        return
    cmd, *cmd_args = args
    if cmd in BUILTINS:
        BUILTINS[cmd](cmd_args)
        return
    executable = resolve_executable(cmd)
    if executable:
        subprocess.run(args)
    else:
        print(f"{cmd}: command not found")


def main():
    parser = Parser()
    while True:
        repl_eval(repl_read(parser))


if __name__ == "__main__":
    main()
