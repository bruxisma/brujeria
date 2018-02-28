from setuptools.command.build_clib import build_clib
from setuptools.command.build_ext import build_ext
from distutils.errors import DistutilsSetupError
from distutils import log

from argparse import ArgumentParser, Action
from contextlib import contextmanager
from itertools import chain
from functools import partial
from pathlib import Path
from typing import Tuple, Text, List
from types import MethodType

from .mixin import BuildCommandMixin
from .target import Extension, Library

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
    parser.prefix_chars = '/-'
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

@contextmanager
def patch (obj, attr, value):
    assert not isinstance(obj, type)
    if callable(value): value = MethodType(value, obj)
    original = getattr(obj, attr)
    setattr(obj, attr, value)
    try: yield
    finally: setattr(obj, attr, original)
class ExtensionCommand (BuildCommandMixin, build_ext):

    def _link (self, compiler, *args, **kwargs):
        self.parser = _create_link_parser(self.is_posix)
        with patch(self.compiler, 'spawn', self._target):
            type(self.compiler).link(compiler, *args, **kwargs)

    def build_extensions (self):
        self.check_extensions_list(self.extensions)
        # TODO: This 'begin' and 'end' system is a travesty and needs to be better
        for ext in self.extensions:
            with self.build(), self._filter_build_errors(ext):
                self.build_extension(ext)

    def build_extension(self, ext: Extension):
        log.info(f"building '{ext.name}' extension")
        self.parser = _create_compile_parser(self.is_posix)
        # Technically we could put these all in one with statement, but honestly, it's just not worth it
        with patch(self, 'current_target', ext):
            with patch(self.compiler, 'spawn', self._compile):
                with patch(self.compiler, 'link', self._link):
                    with patch(self, 'force', True):
                        super().build_extension(ext)

class LibraryCommand (BuildCommandMixin, build_clib):

    def _legacy_check_library(self, library: Tuple[Text, dict]):
        log.warn(
            "possible old-style (name, build_info) tuple found in "
            f"libraries for library '{library}' "
            "-- please convert to Library instance")
        try: super().check_library_list([library])
        except DistutilsSetupError as e:
            if "each element of 'libraries' must a 2-tuple" in e.args:
                raise DistutilsSetupError(
                    "each element of 'libraries' option must be a "
                    "Library instance or 2-tuple")
        name, build_info = library
        # We do here what check_extension_list does
        lib = Library(name, build_info['sources'])
        attributes = ('macros',
            'extra_compile_args', # Here for compat with Extension and build_ext. cflags is kind of dumb tbqh
            'extra_link_args',  # Can only be passed when hacking into spawn from create_static_lib
            'extra_objects', # Yes, needed because why not?
            'include_dirs',
            'obj_deps', # these become implicit dependencies in a ninja file (compatibility with setuptools) (dict)
            'cflags') # Combine with extra_compile_args when passing to compiler (compatibility with setuptools)
        for key in attributes:
            value = build_info.get(key)
            if value is not None: setattr(lib, key, value)
        return lib

    def get_library_names(self) -> List[Text]:
        '''Re-implementation from build_clib to work with `brujeria.Library`'''
        if not self.libraries: return None
        self.check_library_list(self.libraries)
        return list(map(lambda lib: lib.name, self.libraries))

    def get_source_files (self) -> List:
        '''Re-implementation from build_clib to work with `brujeria.Library`'''
        self.check_library_list(self.libraries)
        return list(chain.from_iterable(map(lambda lib: lib.sources, self.libraries)))

    def check_library_list (self, libraries):
        '''Ensure that the list of libraries is valid, i.e., is is a list of
        Library objects. We also support the current approach of a list of
        2-tuples, where the tuples are (name, build_info), which are converted
        to Library instances here.

        Raise DistutilsSetupError if the structure is invalid anywhere; just
        returns otherwise
        '''
        for idx, library in enumerate(libraries):
            if isinstance(library, Library): continue
            libraries[idx] = self._legacy_check_library(library)

    def build_libraries (self, libraries):
        for library in libraries:
            with self.build():
                self.build_library(library)

    def build_library (self, library: Library):
        log.info(f"building in '{library.name}'")
        self.parser = _create_compile_parser(self.is_posix)
        with patch(self, 'current_target', library):
            with patch(self.compiler, 'spawn', self._compile):
                with patch(self, 'force', True):
                    objects = self.compiler.compile(
                        library.sources,
                        output_dir=self.build_temp,
                        macros=library.macros or [],
                        include_dirs=library.include_dirs or [],
                        extra_postargs=library.extra_compile_args or [],
                        debug=self.debug)
            self.parser = _create_link_parser(self.is_posix)
            with patch(self.compiler, 'spawn', self._target):
                self.compiler.create_static_lib(
                    objects,
                    library.name,
                    output_dir=self.build_clib,
                    debug=self.debug)
