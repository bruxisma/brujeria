from importlib.machinery import ModuleSpec, ExtensionFileLoader
from importlib.abc import MetaPathFinder
from pathlib import Path

import shutil
import sys

from . import utility
from . import tool  # TODO: Replace with `from curandera import CMake`
from . import app


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
        mod = utility.rpartial(Path, *fullname.split("."), "init.cmake")
        paths = path or [Path.cwd(), *sys.path]
        for entry in filter(Path.is_file, map(mod, paths)):
            loader = CMakeLoader(fullname)
            return ModuleSpec(fullname, loader=loader, loader_state=entry)
