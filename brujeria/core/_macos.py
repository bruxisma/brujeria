from pathlib import Path
from typing import List

from ._posix import config_dirs, data_dirs, bin_home

def config_home () -> Path: return Path.home() / 'Application Support'
def cache_home () -> Path: return Path.home() / 'Caches'
def data_home () -> Path: return Path.home() / 'Library'