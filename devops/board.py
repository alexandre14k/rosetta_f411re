# devops/board.py

import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "code",
    ),
)

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "serial",
    ),
)

import base
import code
import root
import serial


def board_exec(name):
    path = os.path.join(root.root_dir(), name)
    return root.root_run(
        [sys.executable, "-B", path],
        root.root_dir(),
    )


def board_serial():
    return serial.serial_main()


def board_menu():
    base.base_menu_print(
        "m>board",
        [
            ("s", "serial"),
            ("k", "clear screen"),
            ("m", "show the menu"),
            ("x", "exit"),
        ],
    )

def board_dispatch(command):
    if command == "s":
        return board_serial()

    if command == "k":
        root.clear()

    if command == "m":
        board_menu()
        return 0

    if command == "x":
        return 1

    return 0


def board_loop():
    board_menu()

    while True:
        try:
            line = input("board> ").strip()
            command = base.base_command_key(line)

            if not command:
                continue

            result = board_dispatch(command)

            if result == 1:
                return 0

        except KeyboardInterrupt:
            print()
            return
        except EOFError:
            print()
            return


if __name__ == "__main__":
    board_loop()