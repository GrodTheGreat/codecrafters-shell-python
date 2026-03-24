VALID_COMMANDS = []


def repl_read() -> str:
    command = input("$ ")
    return command


def repl_eval(command: str) -> None:
    if command not in VALID_COMMANDS:
        print(f"{command}: command not found")


def repl_print():
    pass


def main():
    while True:
        command = repl_read()
        repl_eval(command=command)


if __name__ == "__main__":
    main()
