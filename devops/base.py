# devops/base.py

import shlex


def base_menu_print(path, entries):
    print(path)
    for command, label in entries:
        print(command + " -- " + label)


def base_command_split(line):
    try:
        return shlex.split(line)
    except ValueError:
        return []


def base_command_key(line):
    parts = base_command_split(line)
    if not parts:
        return ""
    return parts[0]