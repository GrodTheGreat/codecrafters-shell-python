import os
import subprocess
import sys
from pathlib import Path
from typing import Protocol


class Command(Protocol):
    def __call__(self, args: list[str]) -> None: ...


def resolve_executable(name: str) -> Path | None:
    path = os.getenv("PATH", "")
    for segment in path.split(os.pathsep):
        directory = Path(segment).resolve()
        candidate = directory / name
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    return None


def cmd_echo(args: list[str]) -> None:
    print(" ".join(args))


def cmd_exit(args: list[str]) -> None:
    code = int(args[0]) if args else 0
    sys.exit(code)


def cmd_pwd(args: list[str]) -> None:
    current_directory = Path.cwd().resolve()
    print(current_directory)


def cmd_type(args: list[str]) -> None:
    name = args[0] if args else ""
    if name in BUILTINS:
        print(f"{name} is a shell builtin")
    elif executable := resolve_executable(name):
        print(f"{name} is {executable}")
    else:
        print(f"{name}: not found")


BUILTINS: dict[str, Command] = {
    "echo": cmd_echo,
    "exit": cmd_exit,
    "pwd": cmd_pwd,
    "type": cmd_type,
}


def repl_read() -> list[str]:
    command = input("$ ")
    return command.split()


def repl_eval(args: list[str]) -> str | None:
    if not args:
        return
    cmd, *cmd_args = args
    if cmd in BUILTINS:
        BUILTINS[cmd](cmd_args)
        return
    executable = resolve_executable(cmd)
    if executable and os.access(executable, os.X_OK):
        subprocess.run(args)
        return
    print(f"{cmd}: command not found")


def main():
    while True:
        repl_eval(repl_read())


if __name__ == "__main__":
    main()
