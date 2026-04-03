import os
import subprocess

from commands import BUILTINS, resolve_executable


def repl_read() -> list[str]:
    command = input("$ ")
    return [arg for arg in command.split() if arg]


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
    else:
        print(f"{cmd}: command not found")


def main():
    while True:
        repl_eval(repl_read())


if __name__ == "__main__":
    main()
