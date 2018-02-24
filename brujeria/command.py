from setuptools.command.build_clib import build_clib
from setuptools.command.build_ext import build_ext

from .mixin import BuildNinjaMixin
from .build import ExtensionCommand, LibraryCommand

class build_ninja_clib (BuildNinjaMixin, LibraryCommand): pass
class build_ninja_ext (BuildNinjaMixin, ExtensionCommand): pass