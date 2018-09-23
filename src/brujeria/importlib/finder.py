from importlib.machinery import ModuleSpec
from importlib.abc import MetaPathFinder
from functools import partial
from pathlib import Path
import sys
import os

from ..core.config import config
from ..core import xdg
from .loader import CMakeExtensionLoader

class rpartial(partial):
    def __call__ (self, *args, **kwargs):
        kw = self.keywords.copy()
        kw.update(kwargs)
        return self.func(*args, *self.args, **kwargs)

class CMakeExtensionFinder (MetaPathFinder):
    def __init__ (self, **kwargs):
        self.cache_name = kwargs.get('cache_name', 'brujeria')
        self.quiet = kwargs.get('quiet', True)

    @property
    def cache_dir (self) -> Path: return xdg.CACHE_HOME / self.cache_name

    # TODO: Make sure a path dependency of toplevel/module/init.cmake works,
    # as long as toplevel has an __init__.py
    def find_spec (self, fullname, path, target=None):
        mod = rpartial(Path, *fullname.split('.'), 'init.cmake')
        paths = path or [Path.cwd(), *sys.path]
        for entry in filter(Path.is_file, map(mod, paths)):
            loader = CMakeExtensionLoader(fullname)
            return ModuleSpec(fullname, loader=loader, loader_state=entry)
