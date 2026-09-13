import os
import sys
import subprocess
import signal

from devops import root

def run_child_default_sigint():
    signal.signal(signal.SIGINT, signal.SIG_DFL)


def run_script_dir():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "devops"
    )


def run_menu():
    print("m")
    print("b -- setup board")
    print("k -- clear screen")
    print("m -- show the menu")
    print("x -- exit")


def run_exec_board():
    path = os.path.join(
        run_script_dir(),
        "board.py",
    )
    old = signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        process = subprocess.run(
            [sys.executable, "-B", path],
            cwd=run_script_dir(),
            preexec_fn=run_child_default_sigint,
        )
    finally:
        signal.signal(signal.SIGINT, old)
    return process.returncode


def run_dispatch(cmd):
    if cmd == "b":
        run_exec_board()
    elif cmd == "k":
        root.clear()
    elif cmd == "m":
        run_menu()
    elif cmd == "x":
        sys.exit(0)


def run_loop():
    run_menu()
    while True:
        try:
            cmd = input("run> ").strip()
            run_dispatch(cmd)
        except KeyboardInterrupt:
            print()
            return
        except EOFError:
            print()
            return


if __name__ == "__main__":
    run_loop()