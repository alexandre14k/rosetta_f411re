# devops/serial/serial_device.py


class SerialDevice:
    def __init__(self, backend):
        self.backend = backend
        self.device = None
        self.handle = None

    def devices(self):
        return self.backend.devices()

    def select(self):
        devices = self.devices()

        if not devices:
            print("no serial device found")
            return False

        print("select device:")

        for index, device in enumerate(devices):
            print(
                str(index)
                + " -- "
                + device
            )

        while True:
            try:
                choice = input(
                    "choice: "
                ).strip()
            except KeyboardInterrupt:
                print()
                return False
            except EOFError:
                print()
                return False

            if not choice:
                index = 0
            else:
                try:
                    index = int(choice)
                except ValueError:
                    continue

            if index < 0 or index >= len(devices):
                continue

            self.device = devices[index]

            print(
                "selected "
                + self.device
            )

            return True

    def open(self):
        if self.device is None:
            if not self.select():
                return False

        if self.handle is not None:
            return True

        self.handle = self.backend.open(
            self.device
        )

        if self.handle is None:
            print(
                "unable to connect to "
                + self.device
            )
            return False

        return True

    def close(self):
        self.backend.close(
            self.handle
        )

        self.handle = None

    def read(self):
        if self.handle is None:
            return None

        try:
            return self.backend.read(
                self.handle
            )
        except (
            OSError,
            EOFError,
        ):
            return None
        except Exception:
            return None

    def write(self, data):
        if self.handle is None:
            return False

        try:
            return self.backend.write(
                self.handle,
                data,
            )
        except (
            OSError,
            EOFError,
        ):
            return False
        except Exception:
            return False

    def connected(self):
        return self.handle is not None