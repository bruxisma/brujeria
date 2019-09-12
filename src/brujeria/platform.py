from enum import Enum
import sys


class Platform(Enum):
    WINDOWS = "win32"
    LINUX = "linux"
    MACOS = "darwin"


def current() -> Platform:
    return Platform(sys.platform)


def windows() -> bool:
    return current() == Platform.WINDOWS


def linux() -> bool:
    return current() == Platform.LINUX


def macos() -> bool:
    return current() == Platform.MACOS


def posix() -> bool:
    return not windows()

