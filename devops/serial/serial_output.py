# devops/serial/serial_output.py

import sys
import threading


class SerialOutput:
    def __init__(self):
        self.lock = threading.Lock()

    def write(self, text):
        with self.lock:
            sys.stdout.write(text)
            sys.stdout.flush()

    def render_prompt(self, line):
        with self.lock:
            sys.stdout.write(
                "\r\033[2K"
                + "test> "
                + line
            )
            sys.stdout.flush()

    def submit(self):
        with self.lock:
            sys.stdout.write(
                "\r\033[2K\n"
            )
            sys.stdout.flush()

    def reset_line(self):
        with self.lock:
            sys.stdout.write(
                "\r\033[2K"
            )
            sys.stdout.flush()

    def disconnected(self, device):
        with self.lock:
            sys.stdout.write(
                "\r\033[2K"
                + "-- disconnected from "
                + device
                + "\n"
            )
            sys.stdout.flush()

    def clear(self):
        with self.lock:
            sys.stdout.write(
                "\033[2J\033[H"
            )
            sys.stdout.flush()