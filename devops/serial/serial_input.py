# devops/serial/serial_input.py

import os
import sys


class SerialInput:
    def __init__(self):
        self.attributes = None

        if os.name == "nt":
            import msvcrt

            self.msvcrt = msvcrt
        else:
            import termios
            import tty

            self.termios = termios
            self.tty = tty

    def start(self):
        if os.name == "nt":
            return True

        try:
            fd = sys.stdin.fileno()

            self.attributes = (
                self.termios.tcgetattr(fd)
            )

            self.tty.setraw(fd)

        except (
            OSError,
            self.termios.error,
        ):
            self.attributes = None
            return False

        return True

    def stop(self):
        if os.name == "nt":
            return

        if self.attributes is None:
            return

        try:
            self.termios.tcsetattr(
                sys.stdin.fileno(),
                self.termios.TCSADRAIN,
                self.attributes,
            )
        except (
            OSError,
            self.termios.error,
        ):
            pass

        self.attributes = None

    def read(self):
        if os.name == "nt":
            return self.read_windows()

        return self.read_posix()

    def read_posix(self):
        try:
            character = sys.stdin.read(1)
        except (
            OSError,
            EOFError,
        ):
            return "eof"

        if character == "\x03":
            return "interrupt"

        if character == "\x04":
            return "eof"

        if character in (
            "\r",
            "\n",
        ):
            return "enter"

        if character in (
            "\x7f",
            "\b",
        ):
            return "backspace"

        return character

    def read_windows(self):
        try:
            character = self.msvcrt.getwch()
        except (
            OSError,
            EOFError,
        ):
            return "eof"

        if character == "\x03":
            return "interrupt"

        if character == "\x04":
            return "eof"

        if character in (
            "\r",
            "\n",
        ):
            return "enter"

        if character == "\b":
            return "backspace"

        if character in (
            "\x00",
            "\xe0",
        ):
            self.msvcrt.getwch()
            return ""

        return character