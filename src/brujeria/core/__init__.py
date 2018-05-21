#pylint:disable=E1101
from setuptools import find_packages
from fnmatch import fnmatchcase
from pathlib import Path
import os

class ExtensionFinder:
    '''
    Generate a list of all CMake extensions found within a directory
    '''
    @classmethod
    def _iter_dirs (cls, where, exclude, include):
        include = filter(*include)
        exclude = filter(*exclude, '__pycache__', '_deps')
        for root, dirs, _ in os.walk(where, followlinks=True):
            all_dirs = dirs[:]
            dirs[:] = []
            for path in map(Path, all_dirs):
                fullpath = Path(root).joinpath(dir).resolve()
                relative = os.path.relpath(fullpath, where)
                extension = os.fspath(relative).replace(os.path.sep, '.')
                if path.match('.*') or not cls.is_extension(fullpath):
                    continue
                if include(extension) and not exclude(extension):
                    yield extension
                dirs.append(os.fspath(path))

    @classmethod
    def is_extension (cls, path):
        return (Path(path) / 'init.cmake').is_file()

    @classmethod
    def filter (cls, *patterns):
        return lambda name: any(fnmatchcase(name, pat=pat) for pat in patterns)


# TODO: Return list of CMakeExtension (or just cmake.Extension) objects.
# This then gets mutated within brujeria.setup
def find_extensions (where='.', exclude=(), include=('*',)):
    '''Return a list of all CMake extensions found within directory 'where'

    'where' is the root directory which will be searched for extensions. It
    will be treated as a cross-platform path.

    'exclude' is a sequence of extension names to exclude; '*' can be used as a
    wildcard in the names, such that 'foo.*' will exclude all subextensions of
    'foo' (but not 'foo' itself)

    'include' is a sequence of extension names to include. If it's specified,
    only the named extensions will be included. If it's not specified, all found
    packages will be included. 'include' can contain shell style wildcard
    patterns just like 'exclude'.
    '''

def setup (**attrs):
    '''Wrapper around setuptools' setup
    
    extensions are automatically found, if not explicitly given, and the
    correct command classes are set for build_ext. Additional command classes
    are ignored, unless explicitly asked
    '''

    import setuptools
    setuptools.setup(**attrs)