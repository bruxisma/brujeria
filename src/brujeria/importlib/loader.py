from importlib.machinery import ModuleSpec, ExtensionFileLoader
from pathlib import Path
from io import StringIO
import os

class CMakeExtensionLoader(ExtensionFileLoader):
    def __init__ (self, name, path=None):
        self.name = name
        self.path = path

    def create_module (self, spec: ModuleSpec):
        # TODO: run build/generate CMakeLists.txt steps here
        self.path = os.fspath(spec.loader_state)
        shim = ModuleSpec(spec.name, loader=self, origin=self.path)
        return super().create_module(shim)