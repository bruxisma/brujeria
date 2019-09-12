from subprocess import run
from distutils import sysconfig
from functools import partial
from pathlib import Path
import os

from cmake import CMAKE_BIN_DIR
import importlib_resources

from .app import CACHE_HOME

CMAKE_PRG = os.path.join(CMAKE_BIN_DIR, "cmake")
SUFFIX = sysconfig.get_config_var("EXT_SUFFIX")


def argument(options, var, value):
    if value is None or not value:
        return
    options.append("-D{}={}".format(var, value))


# TODO: This needs to eventually wrap the curandera library
# Right now we just hope the user hasn't changed the output name of the module
# With the curandera library we can just get the metadata back from the
# configure command.
class CMake:
    def __init__(self, spec, state):
        name = spec.name.split(".")
        self.package = "".join(
            name[:-1]
        )  # Turns into joined path, becomes 'install' root
        self.name = name[-1]
        self.path = state.parent
        self.languages = ["C", "CXX"]
        self.description = None
        self.prelude = None
        self.version = None
        self.output = os.fspath(self.binary_dir / "{}{}".format(self.name, SUFFIX))

    @property
    def source_dir(self) -> Path:
        with importlib_resources.path("brujeria", "data") as path:
            return Path(path)

    @property
    def binary_dir(self) -> Path:
        return CACHE_HOME / "brujeria" / self.package / self.name

    def configure(self):
        if os.path.exists(self.binary_dir):
            return
        options = [
            CMAKE_PRG,
            "-B{}".format(os.fspath(self.binary_dir)),
            "-S{}".format(os.fspath(self.source_dir)),
            "-GNinja",
        ]
        arg = partial(argument, options)
        arg("CMAKE_PROJECT_{}_INCLUDE".format(self.name), self.prelude)
        # arg('CMAKE_CXX_COMPILER', config.compiler.cxx)
        # arg('CMAKE_C_COMPILER', config.compiler.cc)
        arg("BRUJERIA_PROJECT_NAME", self.name)
        arg("BRUJERIA_MODULE_PATH", self.path.as_posix())
        arg("BRUJERIA_MODULE_EXTENSION", SUFFIX)
        arg("BRUJERIA_PROJECT_DESCRIPTION", self.description)
        arg("BRUJERIA_PROJECT_VERSION", self.version)
        # TODO: Add reading various important variables from a config object
        run(options).check_returncode()

    def target(self, target='all'):
        options = [CMAKE_PRG, "--build", os.fspath(self.binary_dir), "--target", target]
        run(options).check_returncode()

    def build(self):
        self.target()

