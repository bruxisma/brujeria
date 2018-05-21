from setuptools.command.build_ext import build_ext
from setuptools import Extension
from distutils.errors import DistutilsOptionError
from distutils import log
from argparse import ArgumentParser, Action
from pathlib import Path
from typing import List, Text
from abc import ABC, abstractmethod

import subprocess
import os

from ..core import patch

class _MSVCInputsAction(Action):
    def __call__ (self, _, namespace, value, option):
        setattr(namespace, self.dest, [Path(value[1:])])

class _MSVCCompileAction(Action):
    def __call__(self, _, namespace, value, option):
        if option == '/F' and value[0] != 'o': return
        return setattr(namespace, self.dest, Path(value[1:]))

class _MSVCLinkAction(Action):
    def __call__(self, _, namespace, values, option):
        if option == '/O' and values[:3] != 'UT:': return
        if option == '/L' and values[:7] != 'IBPATH:': return
        if option == '/L':
            paths = getattr(namespace, self.dest)
            paths.append(Path(values[7:]))
            return setattr(namespace, self.dest, paths)
        setattr(namespace, self.dest, Path(values[3:]))

def _set_unix_parser (parser: ArgumentParser):
    parser.add_argument('-o', dest='output', type=Path)
    parser.add_argument('inputs', type=Path, nargs='+')

def _set_msvc_compile_parser(parser: ArgumentParser):
    parser.prefix_chars = '/-' # MSVC supports both styles of inputs
    parser.add_argument('/T', dest='inputs', action=_MSVCInputsAction)
    parser.add_argument('/F', dest='output', action=_MSVCCompileAction)

def _set_msvc_link_parser (parser: ArgumentParser):
    parser.prefix_chars = '/'
    parser.add_argument('/O', dest='output', action=_MSVCLinkAction)
    parser.add_argument('/L', dest='includes', action=_MSVCLinkAction, default=[])
    parser.add_argument('inputs', type=Path, nargs='+')

def _create_compile_parser (is_posix: bool) -> ArgumentParser:
    parser = ArgumentParser()
    if is_posix: _set_unix_parser(parser)
    else: _set_msvc_compile_parser(parser)
    parser.add_argument('-I', dest='includes', type=Path, action='append')
    return parser

def _create_link_parser (is_posix: bool) -> ArgumentParser:
    parser = ArgumentParser()
    if is_posix: _set_unix_parser(parser)
    else: _set_msvc_link_parser(parser)
    return parser

def _parse_cmd (cmd: List[Text], parser: ArgumentParser):
    exe_path, *arguments = cmd
    args, remainder = parser.parse_known_args(arguments)
    if not args.inputs and not args.output:
        raise DistutilsOptionError(f'Could not extract source and output args')
    if not hasattr(args, 'includes'): setattr(args, 'includes', [])
    return BuildInfo(exe_path, args.inputs, args.output, args.includes, remainder)

class BuildInfo:
    def __init__ (self, command, inputs, output, includes, args):
        self.command = Path(command)
        self.inputs = inputs
        self.includes = includes
        self.output = output
        self.args = args

    def add_arguments(self, *args): self.args.extend(args)

class ExtensionCommandMixin (ABC):

    current_target = None

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = None
        self.force = True

    def _compile (self, _, cmd):
        self.on_compile(_parse_cmd(cmd, self.parser))

    def _target (self, _, cmd):
        self.on_target(_parse_cmd(cmd, self.parser))

    def _link (self, compiler, *args, **kwargs):
        self.parser = _create_link_parser(self.is_posix)
        with patch.method(self.compiler, 'spawn', self._target):
            type(self.compiler).link(compiler, *args, **kwargs)

    def build_extensions (self):
        self.on_build_begin()
        self.check_extensions_list(self.extensions)
        for ext in self.extensions:
            with self._filter_build_errors(ext):
                self.build_extension(ext)
        self.on_build_end()

    def build_extension(self, ext: Extension):
        log.info(f"building '{ext.name}' extension")
        self.parser = _create_compile_parser(self.is_posix)
        # Technically we could put these all in one with statement, but
        # honestly, it's just not worth it
        with patch.attribute(self, 'current_target', ext):
            with patch.attribute(self.compiler, 'force', True):
                with patch.method(self.compiler, 'spawn', self._compile):
                    with patch.method(self.compiler, 'link', self._link):
                        super().build_extension(ext) 

    @abstractmethod
    def on_compile (self, info: BuildInfo): pass

    @abstractmethod
    def on_target (self, info: BuildInfo): pass

    @abstractmethod
    def on_build_begin (self): pass

    @abstractmethod
    def on_build_end (self): pass

    @property
    def is_posix (self) -> bool:
        return self.compiler and self.compiler.compiler_type != 'msvc'