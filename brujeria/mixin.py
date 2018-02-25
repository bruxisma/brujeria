from distutils.errors import DistutilsOptionError
from collections.abc import Iterable
from contextlib import contextmanager
from argparse import ArgumentParser
from pathlib import Path
from typing import Text, List, Union
from abc import ABC, abstractmethod

import subprocess
import ninja

from .target import Library, Extension
from .utils import BuildInfo, _parse_cmd
from .utils import _create_compile_rule, _create_target_rule
from .ast import Ninja, Rule, Target

class BuildCommandMixin (ABC):

    current_target: Union[Library, Extension, None] = None

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = None

    def _compile (self, _, cmd):
        info = _parse_cmd(cmd, self.parser)
        self.compile(info)

    def _target (self, _, cmd):
        info = _parse_cmd(cmd, self.parser)
        self.target(info)

    @contextmanager
    def build (self): yield

    @abstractmethod
    def compile (self, info: BuildInfo): pass

    @abstractmethod
    def target (self, info: BuildInfo): pass

    @property
    def is_posix (self) -> bool: return self.compiler and self.compiler.compiler_type != 'msvc'

class BuildNinjaMixin(ABC):

    writer: Ninja

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.writer = None

    def _create_writer (self, name: Text):
        if self.writer: return
        self.writer = Ninja(f'{self.build_temp}/{self.current_target.name}')

    def compile (self, info: BuildInfo):
        if self.is_posix: info.add_arguments('-MMD', '-MF', '$out.d')
        else: info.add_arguments('/showIncludes')
        self._create_writer(self.current_target.name)
        # TODO: Clean this up. This is wasteful and we are unnecessarily
        # creating an object every time
        self.writer.append(_create_compile_rule(info, self.is_posix))
        target = Target('compile', info.output, inputs=info.inputs)
        self.writer.append(target)

    def target (self, info: BuildInfo):
        self.writer.append(_create_target_rule(info, self.is_posix))
        target = Target('target', info.output, inputs=info.inputs)
        self.writer.append(target)

    @contextmanager
    def build (self):
        yield
        self.writer.close()
        ninja_program = Path(ninja.BIN_DIR) / 'ninja'
        try: subprocess.check_call([str(ninja_program), '-f', str(self.writer.path)])
        except subprocess.CalledProcessError as e:
            # TODO: log this somewhere if possible
            raise e

