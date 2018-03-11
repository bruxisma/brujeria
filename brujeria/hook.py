from importlib.machinery import ModuleSpec, ExtensionFileLoader
from importlib.util import spec_from_file_location
from importlib.abc import MetaPathFinder, Loader
from pathlib import Path
from io import StringIO

from mako.template import Template
from mako.runtime import Context
from distutils import log

from .target import Library
#from .build import build_module, ExtensionInfo
from .core import xdg

import sys
import os

def install (**kwargs):
    sys.meta_path.insert(0, BrujeriaExtensionFinder(**kwargs))

# TODO: Look into the following approaches
#  * iterate through sys.path
#  * Allow users to add custom search paths
#  * use pkg_resources to get directories

from importlib.machinery import ModuleSpec
from distutils.sysconfig import get_config_var
from setuptools import setup
from functools import lru_cache
from pathlib import Path
import sys

from .command.ninja import BuildNinjaExt as build_ninja_ext
from .command.ninja import BuildNinjaLib as build_ninja_clib
from .target import Extension, Library

extensions = ['c', 'cxx', 'cpp', 'cc']
class ExtensionInfo:

    def __init__ (self, fullname, filepath, cache_dir, **kwargs):
        self.cache_dir = cache_dir
        self.fullname = fullname
        self.filepath = filepath
        self.include_dirs = kwargs.get('include_dirs', [])
        self.library_dirs = kwargs.get('library_dirs', [])
        self.compiler_flags = kwargs.get('compiler_flags', [])
        self.linker_flags = kwargs.get('linker_flags', [])
        self.libraries = kwargs.get('libraries', [])

    @property
    @lru_cache(maxsize=1)
    def sources (self):
        sources = []
        sources.append(self.cache_dir / self.filepath.name)
        if self.filepath.stem != 'init': return
        for ext in extensions:
            sources.extend(self.module_dir.glob(f'*.{ext}'))
        sources.remove(self.filepath)
        return [str(source) for source in sources]

    @property
    def suffix (self): return get_config_var('EXT_SUFFIX')

    @property
    def build_path (self): return self.cache_dir / 'build'

    @property
    def module_dir (self): return self.filepath.parent

    @property
    def module_name (self): return self.fullname

    @property
    def module_path (self):
        return self.build_path / self.suffix

def build_module (info: ExtensionInfo) -> Path:
    sources = info.sources
    args = [
        'build_clib'
        'build_ext',
        f'--build-temp={info.build_path}',
        f'--build-clib={info.build_path}',
        f'--build-lib={info.build_path}',
    ]
    ext = Extension(
        info.module_name,
        sources=sources,
        language='c++',
        include_dirs=info.include_dirs,
        extra_compile_args=info.compiler_flags,
        extra_link_args=info.linker_flags,
        library_dirs=[str(info.build_path), *info.library_dirs],
        libraries=[lib.name for lib in info.libraries])

    setup(
        name=info.module_name,
#        libraries=info.libraries,
        ext_modules=[ext],
        script_args=args,
        cmdclass=dict(build_ext=build_ninja_ext, build_clib=build_ninja_clib))

    return info.module_path


'''
Take all flags and convert to Extension flags and settings
get path of output pyd/so from build_module
modify the spec on returned module
return said module
'''

class BrujeriaExtensionFileLoader(ExtensionFileLoader):

    def __init__(self, name):
        self.name = name

    def create_module_init (self, filepath, output_path):
        buffer = StringIO(newline='\n')
        args = dict(
            directory=filepath.parent)
        context = Context(buffer, **args)
        template = Template(
            filename=str(filepath),
            imports=[
                'import brujeria.hook',
                'import sys'
            ],
            enable_loop=False)
        template.render_context(context)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(buffer.getvalue())

    def create_module_info (self, fullname, filepath, cache_dir):
        output_path = cache_dir / filepath.name
        buffer = StringIO(newline='\n')
        args = dict(
            include_dirs=[],
            library_dirs=[],
            compiler_flags=[],
            linker_flags=[],
            libraries=[],
            Library=Library)
        context = Context(buffer, **args)
        template = Template(
            filename=str(filepath),
            imports=['import brujeria.hook'],
            enable_loop=False)
        template.render_context(context)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(buffer.getvalue())
        return ExtensionInfo(fullname, filepath, cache_dir, **args)

    def create_module (self, spec: ModuleSpec):
        if not spec.loader_state: return None
        state = spec.loader_state
        fullname = spec.name
        cache_dir = state['cache_dir'] / fullname
        filepath = state['filepath']
        # TODO: Check if filepath is newer than output_path
        info = self.create_module_info(fullname, filepath, cache_dir)
        self.path = os.fspath(build_module(info))
        shim = ModuleSpec(spec.name, loader=self, origin=self.path)
        module = super().create_module(shim)
        return module

class BrujeriaExtensionFinder(MetaPathFinder):

    def __init__ (self, **kwargs):
        suffixes = ['.c', '.cxx', '.cc', '.cpp']
        self.source_suffixes = kwargs.get('source_suffixes', suffixes)
        self.cache_name = kwargs.get('cache_name', 'brujeria')
        self.quiet = kwargs.get('quiet', True)

    @property
    def cache_dir (self) -> Path: return xdg.CACHE_HOME / self.cache_name

    def find_spec(self, fullname, paths, target=None):
        module_path = Path().joinpath(*fullname.split('.'))
        paths = paths or [os.getcwd(), *sys.path]
        for entry in map(Path, paths):
            fullpath: Path = entry.joinpath(module_path)
            for suffix in self.source_suffixes:
                namepath: Path = fullpath.with_suffix(suffix)
                initpath: Path = fullpath.joinpath(f'init{suffix}')
                loader = BrujeriaExtensionFileLoader(fullname)
                state = dict(cache_dir=self.cache_dir)
                if namepath.is_file(): state['filepath'] = namepath
                if initpath.is_file(): state['filepath'] = initpath
                if 'filepath' not in state: continue
                is_package=False
                for child in fullpath.iterdir():
                    #TODO: Make sure there's a file underneath here
                    if child.is_dir():
                        is_package=True
                        break
                return ModuleSpec(fullname, loader_state=state, loader=loader, is_package=is_package)
            if fullpath.is_dir():
                return ModuleSpec(fullname, loader=None, is_package=True)
 
# TODO: Remove this fuckerrrr
install()
