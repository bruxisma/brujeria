from importlib.machinery import ModuleSpec
from importlib.abc import MetaPathFinder
from pathlib import Path

import shutil
import sys
import os

from .utility import rpartial
from .loader import BrujeriaCMakeLoader

# TODO: We need to support namespace packages at some point...
class BrujeriaCMakeFinder(MetaPathFinder):

    def __init__ (self, config=None):
        self.config = config
        super().__init__()

    def invalidate_caches (self):
        shutil.rmtree(xdg.CACHE_HOME / 'brujeria')

    def find_spec (self, fullname, path, target=None):
        mod = rpartial(Path, *fullname.split('.'), 'init.cmake')
        paths = path or [Path.cwd(), *sys.path]
        for entry in filter(Path.is_file, map(mod, paths)):
            loader = BrujeriaCMakeLoader(fullname)
            return ModuleSpec(
                fullname,
                loader=loader,
                loader_state=entry) # TODO: Eventually replace with 'Config' as state
