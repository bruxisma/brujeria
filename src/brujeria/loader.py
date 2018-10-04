from importlib.machinery import ModuleSpec, ExtensionFileLoader
from subprocess import run
from pathlib import Path
import os

from .tool import CMake

class BrujeriaCMakeLoader(ExtensionFileLoader):
    def __init__ (self, name, path=None):
        self.name = name
        self.path = path

    def create_module (self, spec: ModuleSpec):
        state = spec.loader_state # will be more than *just* a path soon
        cmake = CMake(spec, state)
        cmake.configure()
        cmake.build()
        spec = ModuleSpec(spec.name, loader=self, origin=cmake.output)
        return super().create_module(spec)
