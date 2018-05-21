from pathlib import Path
from typing import List
import os

def _expand (path: Path) -> str:
    return os.fspath(os.path.expanduser(path))

def _getvar (var, default) -> Path:
    return Path(os.environ.get(var, _expand(default)))

def _getvars (var, defaults):
    paths = os.environ.get(var, defaults)
    return list(map(Path, paths.split(os.pathsep)))

def config_dirs () -> List[Path]:
    return _getvars('XDG_CONFIG_DIRS', '/etc/xdg')

def data_dirs () -> List[Path]:
    return _getvars('XDG_DATA_DIRS', '/usr/local/share:/usr/share')

def config_home () -> Path:
    return _getvar('XDG_CONFIG_HOME', Path.home() / '.config')

def cache_home () -> Path:
    return _getvar('XDG_CACHE_HOME', Path.home() / '.cache')

def data_home () -> Path:
    return _getvar('XDG_DATA_HOME', Path.home().joinpath('.local', 'share'))

def bin_home () -> Path:
    return _getvar('XDG_BIN_HOME', Path.home().joinpath('.local', 'bin'))