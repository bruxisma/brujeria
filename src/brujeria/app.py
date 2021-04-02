"""Application directories for all operating systems with better Windows support"""

from pathlib import Path
from typing import Iterator, Text
import os

from . import platform

# This module becomes MUCH harder to understand if we don't silo away
# a bunch of Windows specific code.
if platform.windows():
    from . import _windows


def _getvars(var: Text, defaults: Text) -> Iterator[Path]:
    paths = os.environ.get(var, defaults)
    return map(Path, paths.split(os.pathsep))


def config_dirs() -> Iterator[Path]:
    if platform.windows():
        return _windows.config_dirs()
    return _getvars("XDG_CONFIG_DIRS", "/etc/xdg")


def data_dirs() -> Iterator[Path]:
    if platform.windows():
        return _windows.data_dirs()
    return _getvars("XDG_DATA_DIRS", "/usr/local/share:/usr/share")


def config_home() -> Path:
    if platform.windows():
        return _windows.config_home()
    if platform.macos():
        return data_home().joinpath("Application Support")
    return Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()


def cache_home() -> Path:
    if platform.windows():
        return _windows.cache_home()
    if platform.macos():
        return data_home().joinpath("Caches")
    return Path(os.environ.get("XDG_CACHE_HOME", "~/.cache")).expanduser()


def data_home() -> Path:
    if platform.windows():
        return _windows.data_home()
    if platform.macos():
        return Path("~/Library").expanduser()
    return Path(os.environ.get("XDG_DATA_HOME", "~/.local/share")).expanduser()


CONFIG_DIRS = config_dirs()
DATA_DIRS = data_dirs()

CONFIG_HOME = config_home()
CACHE_HOME = cache_home()
DATA_HOME = data_home()
