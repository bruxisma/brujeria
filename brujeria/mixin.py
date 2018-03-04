from distutils.errors import DistutilsOptionError
from collections.abc import Iterable
from contextlib import contextmanager
from argparse import ArgumentParser
from pathlib import Path
from typing import Text, List, Union
from abc import ABC, abstractmethod
from distutils import log
import brujeria.log

import subprocess
import ninja
import os

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
        self._compile_rule_created = False
        self.writer = None

    def _create_writer (self, name: Text):
        if self.writer: return
        self.writer = Ninja(f'{self.build_temp}/{self.current_target.name}')

    def _create_compile_rule (self, info: BuildInfo):
        if self._compile_rule_created: return
        self.writer.append(_create_compile_rule(info, self.is_posix))
        self._compile_rule_created = True

    def compile (self, info: BuildInfo):
        if self.is_posix: info.add_arguments('-MMD', '-MF', '$out.d')
        else: info.add_arguments('/showIncludes')
        self._create_writer(self.current_target.name)
        self._create_compile_rule(info)
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
        env = os.environ
        if not self.is_posix:
            # Add vcvarsall.bat to execution
            from distutils._msvccompiler import PLAT_TO_VCVARS, _get_vc_env
            from distutils.util import get_platform
            env = _get_vc_env(PLAT_TO_VCVARS[get_platform()])
        cmd = [str(ninja_program), '-f', str(self.writer.path)]
        import sys
        process = subprocess.Popen(cmd,
            env=env,
            universal_newlines=True,
            stdout=sys.stdout, #subprocess.PIPE,
            stderr=sys.stderr)#subprocess.PIPE)
        out, err = process.communicate()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode,
                cmd,
                output=out,
                stderr=err)
        if out: print(out, end='')