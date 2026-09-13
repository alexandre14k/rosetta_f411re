# devops/serial/serial_terminal.py

import threading


class SerialTerminal:
    def __init__(
        self,
        device,
        terminal_input,
        terminal_output,
    ):
        self.device = device
        self.input = terminal_input
        self.output = terminal_output

        self.running = False
        self.disconnect = False
        self.reader_thread = None

        self.lock = threading.Lock()

    def menu(self):
        self.menu_print()

        try:
            while True:
                try:
                    line = input(
                        "serial> "
                    ).strip()
                except KeyboardInterrupt:
                    print()
                    self.close()
                    return 0
                except EOFError:
                    print()
                    self.close()
                    return 0

                if not line:
                    continue

                if line == "c":
                    result = self.session()

                    if result != 0:
                        return result

                    continue

                if line == "s":
                    self.device.select()
                    continue

                if line == "k":
                    self.clear()
                    continue

                if line == "m":
                    self.menu_print()
                    continue

                if line == "x":
                    self.close()
                    return 0

        except KeyboardInterrupt:
            print()
            self.close()
            return 0

        except EOFError:
            print()
            self.close()
            return 0

    def menu_print(self):
        print("m>board>serial")
        print("c -- connect")
        print("s -- setup")
        print("k -- clear screen")
        print("m -- show the menu")
        print("x -- exit")

    def session(self):
        if not self.device.open():
            return 1

        print(
            "-- connected to "
            + self.device.device
        )
        print(
            "-- type enter to begin"
        )
        print(
            "-- hit Ctrl+C to end"
        )

        self.running = True
        self.disconnect = False

        if not self.input.start():
            self.device.close()
            self.running = False
            return 1

        self.reader_thread = threading.Thread(
            target=self.reader_loop,
            daemon=True,
        )

        self.reader_thread.start()

        try:
            while self.running:
                key = self.input.read()

                if key == "interrupt":
                    break

                if key == "eof":
                    break

                if self.disconnect:
                    break

                if key == "enter":
                    self.device.write(
                        b"\r\n"
                    )
                    continue

                if key == "backspace":
                    self.device.write(
                        b"\x08"
                    )
                    continue

                if not key:
                    continue

                self.device.write(
                    key.encode(
                        "utf-8"
                    )
                )

        finally:
            self.running = False
            self.input.stop()

            if self.reader_thread is not None:
                self.reader_thread.join(
                    timeout=1.0
                )

            self.reader_thread = None

            self.device.close()

            self.output.disconnected(
                self.device.device
            )

        return 0

    def reader_loop(self):
        while self.running:
            data = self.device.read()

            if data is None:
                self.disconnect = True
                return

            if not data:
                continue

            try:
                text = data.decode(
                    "utf-8",
                    errors="replace",
                )
            except Exception:
                continue

            self.output.write(text)

    def clear(self):
        self.output.clear()
        return 0

    def close(self):
        self.running = False
        self.input.stop()
        self.device.close()