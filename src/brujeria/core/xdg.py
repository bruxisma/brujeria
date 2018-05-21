'''XDG Specification, with Windows and MacOS conventions'''
from importlib import import_module
from pathlib import Path
from typing import List

from . import platform

_module = {
    platform.Platform.WINDOWS: 'windows',
    platform.Platform.MACOS: 'macos',
}.get(platform.current(), 'posix')

_config = import_module(f'._{_module}', 'brujeria.core')

config_dirs = _config.config_dirs
data_dirs = _config.data_dirs

config_home = _config.config_home
cache_home = _config.cache_home
data_home = _config.data_home
bin_home = _config.bin_home

CONFIG_DIRS = config_dirs()
DATA_DIRS = data_dirs()

CONFIG_HOME = config_home()
CACHE_HOME = cache_home()
DATA_HOME = data_home()
BIN_HOME = bin_home()