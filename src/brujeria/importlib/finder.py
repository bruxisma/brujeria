from importlib.machinery import ModuleSpec
from importlib.abc import MetaPathFinder
from pathlib import Path
import sys
import os

from ..core.config import config
from ..core import xdg
from .loader import CMakeExtensionLoader

class CMakeExtensionFinder (MetaPathFinder):
    def __init__ (self, **kwargs):
        self.cache_name = kwargs.get('cache_name', 'brujeria')
        self.quiet = kwargs.get('quiet', True)

    @property
    def cache_dir (self) -> Path: return xdg.CACHE_HOME / self.cache_name

    # TODO: Make sure a path dependency of toplevel/module/init.cmake works,
    # as long as toplevel has an __init__.py
    # ALSO: Should we support package namespaces?
    def find_spec (self, fullname, path, target=None):
        module_path = Path(*fullname.split('.'))
        paths = path or [Path.cwd(), *sys.path]
        for entry in map(Path, paths):
            fullpath: Path = entry.joinpath(module_path)
            init = fullpath.joinpath('init.cmake')
            if not init.is_file(): continue
            loader = CMakeExtensionLoader(fullname)
            return ModuleSpec(fullname, loader=loader, loader_state=init)
#            if fullpath.is_dir():
#                return ModuleSpec(fullname, loader=None, is_package=True)