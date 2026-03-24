import sys

VALID_COMMANDS = []


def main():
    sys.stdout.write("$ ")
    command = input()
    if command not in VALID_COMMANDS:
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
