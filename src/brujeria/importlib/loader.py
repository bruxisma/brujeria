from importlib.machinery import ModuleSpec, ExtensionFileLoader
from pathlib import Path
from subprocess import run
from io import StringIO
import os
from cmake import CMAKE_BIN_DIR

from ..cmake.extension import Extension

class CMakeExtensionLoader(ExtensionFileLoader):
    def __init__ (self, name, path=None):
        self.name = name
        self.path = path

    def create_module (self, spec: ModuleSpec):
        # TODO: run build/generate CMakeLists.txt steps here
        # This is the file that gets included
        name = spec.name.split('.')[-1]
        init = spec.loader_state
        extension = Extension(name, init)
        cmake_prg = os.path.join(CMAKE_BIN_DIR, 'cmake')
        configure = extension.configure()
        build = extension.build()
        run([cmake_prg, *configure]).check_returncode()
        run([cmake_prg, *build]).check_returncode()
        shim = ModuleSpec(spec.name, loader=self, origin=extension.output)
        return super().create_module(shim)
