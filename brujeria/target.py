from distutils.errors import DistutilsSetupError
from setuptools import Extension
from typing import Union, Tuple, List, Text

class Library:
    def __init__(self, name: Text, sources: Union[List, Tuple]):
        if sources is None or not isinstance(sources, (list, tuple)):
            raise DistutilsSetupError(
            "In library '{name}', 'sources' must be present "
            "and an iterable of source filenames")
        self.name = name
        self.sources = sources
        self.extra_compile_args = None
        self.extra_link_args = None
        self.extra_objects = None
        self.include_dirs = None
        self.obj_deps = None
        self.macros = None

    @property
    def cflags (self): return self.extra_compile_args

    @cflags.setter
    def cflags (self, value): self.extra_compile_args.extend(value)