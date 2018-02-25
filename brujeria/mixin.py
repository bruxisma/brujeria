from distutils.errors import DistutilsOptionError
from collections.abc import Iterable
from contextlib import contextmanager
from argparse import ArgumentParser
from pathlib import Path
from typing import Text, List, Union
from abc import ABC, abstractmethod

import subprocess
import shlex
import ninja

from .target import Library, Extension
from .ast import Ninja, Rule, Target

class BuildInfo:
    def __init__ (self, command: Text, inputs: List[Text], output: Text, includes: List[Path], args: List[Text]):
        self.command = Path(command)
        self.inputs = list(map(Path, inputs))
        self.includes = includes
        self.output = Path(output)
        self.args = args

    def add_arguments (self, *args):
        self.args.extend(args)

def _parse_cmd (cmd: Text, is_posix: bool, parser: ArgumentParser) -> BuildInfo:
    exe_path, *arguments = cmd #shlex.split(cmd, posix=is_posix)
    args, remainder = parser.parse_known_args(arguments)
    if not args.inputs and not args.output:
        raise DistutilsOptionError(f'Could not extract source and output arguments for {BuildInfo.__qualname__}')
    if not hasattr(args, 'includes'): setattr(args, 'includes', [])
    return BuildInfo(exe_path, args.inputs, args.output, args.includes, remainder)

class BuildCommandMixin (ABC):

    current_target: Union[Library, Extension, None] = None

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = None

    def _compile (self, _, cmd):
        info = _parse_cmd(cmd, self.is_posix, self.parser)
        self.compile(info)

    def _target (self, _, cmd):
        info = _parse_cmd(cmd, self.is_posix, self.parser)
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

    # XXX: This function is hot trash. Make it better
    def _create_compile_rule(self, info: BuildInfo) -> Rule:
        depfile = '$out.d'
        output = '-o $out'
        deps = 'gcc'
        inputs = ['$in']
        if not self.is_posix:
            depfile = None
            output = '/Fo$out'
            input_flag = '/Tc' if info.inputs[0].suffix == '.c' else '/Tp'
            inputs = [input_flag, '$in']
            deps = 'msvc'
        command = [info.command, *inputs, output, *info.args, *info.includes]
        return Rule('compile', command, depfile=depfile, deps=deps)

    def _create_target_rule (self, info: BuildInfo) -> Rule:
        output = ['/OUT:$out']
        if self.is_posix: output = ['-o', '$out']
        command = [info.command, *info.args, *output, '$in']
        return Rule('target', command)

    def compile (self, info: BuildInfo):
        if self.is_posix: info.add_arguments('-MMD', '-MF', '$out.d')
        else: info.add_arguments('/showIncludes')
        self._create_writer(self.current_target.name)
        # TODO: Clean this up. This is wasteful and we are unnecessarily
        # creating an object every time
        self.writer.append(self._create_compile_rule(info))
        target = Target('compile', info.output, inputs=info.inputs)
        self.writer.append(target)

    def target (self, info: BuildInfo):
        self.writer.append(self._create_target_rule(info))
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

