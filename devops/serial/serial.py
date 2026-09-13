# devops/serial/serial.py

import os

from serial_device import SerialDevice
from serial_input import SerialInput
from serial_output import SerialOutput
from serial_terminal import SerialTerminal


def serial_backend_create():
    if os.name == "nt":
        from serial_windows import SerialWindows

        return SerialWindows()

    from serial_posix import SerialPosix

    return SerialPosix()


def serial_main():
    device = SerialDevice(
        serial_backend_create()
    )

    terminal_input = SerialInput()
    terminal_output = SerialOutput()

    terminal = SerialTerminal(
        device,
        terminal_input,
        terminal_output,
    )

    return terminal.menu()


if __name__ == "__main__":
    serial_main()