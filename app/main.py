import sys

BUILTIN_COMMANDS = ["echo", "exit", "type"]


def cmd_echo(args: list[str]) -> str:
    return " ".join(args)


def cmd_exit() -> None:
    sys.exit(0)


def cmd_type(args: list[str]) -> str:
    if args[0] in BUILTIN_COMMANDS:
        return f"{args[0]} is a shell function"
    return f"{args[0]}: not found"


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
            response = cmd_type(args)
        case _:
            response = f"{command}: command not found"
    return response


def repl_print():
    # Is there any point in this function?
    pass


def main():
    while True:
        args = repl_read()
        repl_eval(args=args)


if __name__ == "__main__":
    main()
