import os
import pathlib
import subprocess
import sys

BUILTIN_COMMANDS = ["echo", "exit", "type"]


def cmd_echo(args: list[str]) -> str:
    return " ".join(args)


def cmd_exit(_: list[str]) -> None:
    sys.exit(0)


def cmd_type(args: list[str]) -> str:
    arg = ""
    if len(args) > 0:
        arg = args[0]
    if arg in BUILTIN_COMMANDS:
        return f"{arg} is a shell builtin"
    path_env = os.getenv("PATH")
    if path_env is None:
        raise Exception("PATH env not set")
    path_segments = path_env.split(os.pathsep)
    path_dirs = list(map(lambda p: pathlib.Path(p).resolve(), path_segments))
    for dir in path_dirs:
        if os.access(dir, os.X_OK):
            for file in dir.iterdir():
                if not file.is_file():
                    continue
                if file.name == arg and os.access(file, os.X_OK):
                    return f"{arg} is {file}"
    return f"{arg}: not found"


BUILTINS = {"echo": cmd_echo, "exit": cmd_exit, "type": cmd_type}


def repl_read() -> list[str]:
    command = input("$ ")
    return command.split()


def repl_eval(args: list[str]) -> str | None:
    length = len(args)
    if length == 0:
        return ""
    command = args[0]
    if command in BUILTINS:
        cmd_args = args[1:]
        return BUILTINS[command](cmd_args)
    path_env = os.getenv("PATH")
    if path_env is None:
        raise Exception("PATH env not set")
    path_segments = path_env.split(os.pathsep)
    path_dirs = list(map(lambda p: pathlib.Path(p).resolve(), path_segments))
    for dir in path_dirs:
        if os.access(dir, os.X_OK):
            for file in dir.iterdir():
                if not file.is_file():
                    continue
                if file.name == command and os.access(file, os.X_OK):
                    subprocess.run(args)
                    return None
    return f"{command}: command not found"


def repl_print(response: str) -> None:
    print(response)


def main():
    while True:
        args = repl_read()
        response = repl_eval(args=args)
        if response:
            repl_print(response=response)


if __name__ == "__main__":
    main()
