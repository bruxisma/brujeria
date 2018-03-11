from importlib.machinery import ModuleSpec
from importlib.abc import MetaPathFinder
from pathlib import Path
import sys
import os

from ..core import xdg
from .loader import CXXExtensionFileLoader

class CXXExtensionFinder(MetaPathFinder):

    def __init__ (self, **kwargs):
        suffixes = ['.cxx', '.cpp', '.cc']
        self.source_suffixes = kwargs.get('source_suffixes', suffixes)
        self.cache_name = kwargs.get('cache_name', 'brujeria')
        self.quiet = kwargs.get('quiet', True)

    @property
    def cache_dir (self) -> Path: return xdg.CACHE_HOME / self.cache_name

    def find_module (self, fullname, path): pass

    def find_spec (self, fullname, paths, target=None):
        module_path = Path(*fullname.split('.'))
        paths = paths or [Path().cwd(), *sys.path]
        for entry in map(Path, paths):
            fullpath: Path = entry.joinpath(module_path)
            for suffix in self.source_suffixes:
                namepath: Path = fullpath.with_suffix(suffix)
                initpath: Path = fullpath.joinpath(f'init{suffix}')
                loader = CXXExtensionFileLoader(fullname)
                state = dict(cache_dir=self.cache_dir)
                spec_args = dict(
                    loader_state=state,
                    loader=loader,
                    is_package=False)
                if initpath.is_file(): state['filepath'] = initpath
                elif namepath.is_file(): state['filepath'] = namepath
                else: continue
                for child in fullpath.iterdir():
                    # TODO: Make sure there's actually a file underneath...
                    if child.is_dir():
                        spec_args['is_package'] = True
                        break
                return ModuleSpec(fullname, **spec_args)
            if fullpath.is_dir():
                return ModuleSpec(fullname, loader=None, is_package=True)



    def invalidate_caches (self):
        pass