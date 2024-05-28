import sys


def info(message):
    print(message)


def error(message):
    print(f"ERROR: {message}")
    sys.exit(1)
