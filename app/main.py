import sys

VALID_COMMANDS = ["echo", "exit"]


def echo(arg: str) -> None:
    print(arg)


def exit() -> None:
    sys.exit(0)


def repl_read() -> list[str]:
    command = input("$ ")
    return command.split()


def repl_eval(command: list[str]) -> None:
    length = len(command)
    if length == 0:
        return
    match command:
        case "echo":
            arg = ""
            if length > 1:
                arg = command[1]
            echo(arg)
        case "exit":
            exit()
        case _:
            print(f"{command}: command not found")


def repl_print():
    # Is there any point in this function?
    pass


def main():
    while True:
        command = repl_read()
        repl_eval(command=command)


if __name__ == "__main__":
    main()
