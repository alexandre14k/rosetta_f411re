# devops/serial/serial_posix.py

import os
import select
import termios


class SerialPosix:
    def devices(self):
        devices = []

        try:
            names = sorted(
                os.listdir("/dev")
            )
        except OSError:
            return []

        for name in names:
            if (
                name.startswith("ttyUSB")
                or name.startswith("ttyACM")
                or name.startswith("cu.")
            ):
                devices.append(
                    os.path.join(
                        "/dev",
                        name,
                    )
                )

        return devices

    def open(self, device):
        try:
            fd = os.open(
                device,
                os.O_RDWR
                | os.O_NOCTTY,
            )
        except OSError:
            return None

        try:
            self.configure(fd)
        except (
            OSError,
            termios.error,
        ):
            self.close(fd)
            return None

        return fd

    def configure(self, fd):
        attributes = termios.tcgetattr(fd)

        attributes[0] = 0
        attributes[1] = 0

        attributes[2] = (
            termios.CLOCAL
            | termios.CREAD
            | termios.CS8
        )

        attributes[3] = 0

        attributes[2] &= ~termios.PARENB
        attributes[2] &= ~termios.CSTOPB

        if hasattr(termios, "CRTSCTS"):
            attributes[2] &= ~termios.CRTSCTS

        attributes[4] = termios.B115200
        attributes[5] = termios.B115200

        attributes[6][termios.VMIN] = 0
        attributes[6][termios.VTIME] = 0

        termios.tcsetattr(
            fd,
            termios.TCSANOW,
            attributes,
        )

    def close(self, fd):
        if fd is None:
            return 0

        try:
            os.close(fd)
        except OSError:
            pass

        return 0

    def read(self, fd):
        try:
            ready, _, _ = select.select(
                [fd],
                [],
                [],
                0.1,
            )
        except (
            OSError,
            ValueError,
        ):
            return None

        if not ready:
            return b""

        try:
            data = os.read(
                fd,
                4096,
            )
        except OSError:
            return None

        if not data:
            return None

        return data

    def write(self, fd, data):
        if fd is None:
            return False

        offset = 0

        while offset < len(data):
            try:
                count = os.write(
                    fd,
                    data[offset:],
                )
            except OSError:
                return False

            if count <= 0:
                return False

            offset += count

        return True