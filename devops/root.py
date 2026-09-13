# devops/root.py

import os
import sys
import subprocess
import platform
import signal

def root_child_default_sigint():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

def root_dir():
    return os.path.dirname(os.path.abspath(__file__))


def base_dir():
    return os.path.dirname(root_dir())


def target_dir():
    return os.path.join(base_dir(), "target")


def release_dir():
    return os.path.join(target_dir(), "release")


def root_platform():
    system = platform.system().lower()
    if system.startswith("win"):
        return "win32"
    if system.startswith("darwin"):
        return "macos"
    return "linux"


def root_run(cmd, cwd=None):
    run_cwd = cwd if cwd else base_dir()
    if root_platform() == "win32":
        process = subprocess.run(
            cmd,
            cwd=run_cwd,
            shell=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        return process.returncode

    old_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        process = subprocess.run(
            cmd,
            cwd=run_cwd,
            stdout=sys.stdout,
            stderr=sys.stderr,
            preexec_fn=root_child_default_sigint,
        )
    finally:
        signal.signal(signal.SIGINT, old_handler)
    return process.returncode


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")