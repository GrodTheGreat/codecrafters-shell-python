import sys

VALID_COMMANDS = ["exit"]


def exit() -> None:
    sys.exit(0)


def repl_read() -> str:
    command = input("$ ")
    return command


def repl_eval(command: str) -> None:
    match command:
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
