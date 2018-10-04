'''AppDirs for all operating systems (better Windows support)'''
from importlib import import_module
from pathlib import Path
from typing import List
import os

from .platform import Platform
from . import platform

# Unfortunately this module becomes harder to understand without silo-ing 
# Windows specific code...
if platform.windows(): from . import _windows

def _expand (path: Path) -> str:
    return os.fspath(os.path.expanduser(path))

def _getvar (var, default) -> Path:
    return Path(os.environ.get(var, _expand(default)))

def _getvars (var, defaults) -> List[Path]:
    paths = os.environ.get(var, defaults)
    return list(map(Path, paths.split(os.pathsep)))

def config_dirs () -> List[Path]:
    if platform.windows(): return _windows.config_dirs()
    return _getvars('XDG_CONFIG_DIRS', '/etc/xdg')

def data_dirs () -> List[Path]:
    if platform.windows(): return _windows.data_dirs()
    return _getvars('XDG_DATA_DIRS', '/usr/local/share:/usr/share')

def config_home () -> Path:
    if platform.windows(): return _windows.config_home()
    if platform.macos(): return data_home() / 'Application Support'
    return _getvar('XDG_CONFIG_HOME', Path.home() / '.config')

def cache_home () -> Path:
    if platform.windows(): return _windows.cache_home()
    if platform.macos(): return data_home() / 'Caches'
    return _getvar('XDG_CACHE_HOME', Path.home() / '.cache')

def data_home () -> Path:
    if platform.windows(): return _windows.data_home()
    if platform.macos(): return Path.home() / 'Library'
    return _getvar('XDG_DATA_HOME', Path.home() / '.local' / 'share')

def bin_home () -> Path:
    if platform.windows(): return _windows.bin_home()
    return _getvar('XDG_BIN_HOME', Path.home() / '.local' / 'bin')

CONFIG_DIRS = config_dirs()
DATA_DIRS = data_dirs()

CONFIG_HOME = config_home()
CACHE_HOME = cache_home()
DATA_HOME = data_home()
BIN_HOME = bin_home()
