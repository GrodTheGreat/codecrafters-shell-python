import os
import pathlib
import sys

BUILTIN_COMMANDS = ["echo", "exit", "type"]


def cmd_echo(args: list[str]) -> str:
    return " ".join(args)


def cmd_exit() -> None:
    sys.exit(0)


def cmd_type(arg: str) -> str:
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


def repl_read() -> list[str]:
    command = input("$ ")
    return command.split()


def repl_eval(args: list[str]) -> str:
    response = ""
    length = len(args)
    if length == 0:
        return response
    command = args.pop(0)
    match command:
        case "echo":
            response = cmd_echo(args)
        case "exit":
            cmd_exit()
        case "type":
            response = cmd_type((args[:1] or [""])[0])
        case _:
            response = f"{command}: command not found"
    return response


def repl_print(response: str) -> None:
    print(response)


def main():
    while True:
        args = repl_read()
        response = repl_eval(args=args)
        repl_print(response=response)


if __name__ == "__main__":
    main()
