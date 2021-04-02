from importlib.machinery import ModuleSpec, ExtensionFileLoader
from importlib.abc import MetaPathFinder

from functools import partial
from pathlib import Path

import shutil
import sys

from . import tool  # TODO: Replace with `from curandera import CMake`
from . import app


class rpartial(partial):
    def __call__(self, *args, **kwargs):
        kw = self.keywords.copy()
        kw.update(kwargs)
        return self.func(*args, *self.args, **kwargs)


class CMakeLoader(ExtensionFileLoader):
    def __init__(self, name, path=None):
        self.name = name
        self.path = path

    def create_module(self, spec: ModuleSpec):
        state = spec.loader_state
        cmake = tool.CMake(spec, state)
        cmake.configure()
        cmake.build()
        spec = ModuleSpec(spec.name, loader=self, origin=cmake.output)
        return super().create_module(spec)


class CMakeFinder(MetaPathFinder):
    def __init__(self, config=None):
        self.config = config
        super().__init__()

    def invalidate_caches(self):
        shutil.rmtree(app.CACHE_HOME / "brujeria")

    def find_spec(self, fullname, path, target=None):
        mod = rpartial(Path, *fullname.split("."), "init.cmake")
        paths = path or [Path.cwd(), *sys.path]
        for entry in filter(Path.is_file, map(mod, paths)):
            loader = CMakeLoader(fullname)
            return ModuleSpec(fullname, loader=loader, loader_state=entry)
