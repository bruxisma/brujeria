from importlib.machinery import ModuleSpec, ExtensionFileLoader
from importlib.util import spec_from_file_location
from importlib.abc import MetaPathFinder, Loader
from pathlib import Path
from io import StringIO

from mako.template import Template
from mako.runtime import Context
from distutils import log

from .utils import _xdg_cache_home
from .build import build_module
from .log import use_logbook

import sys
import os

def install (**kwargs):
    sys.meta_path.insert(0, BrujeriaExtensionFinder(**kwargs))

# TODO: Look into the following approaches
#  * iterate through sys.path
#  * Allow users to add custom search paths
#  * use pkg_resources to get directories


## find module-name
#   if module-name.cxx exists: build_module
#   if module-name/init.cxx exists: build_module
#  return None

def find_extension (fullname): pass

# module-name/__init__.py
# module-name/native/init.cxx <-- This is just generated sort of
# module-name/wrapper/
#   | 
#   +-- include/
#   +-- source/
#   |
#   +-- lib.cxx

'''
Get the main file
run it through templating
If template.sources is none and mainfile.stem == 'init': glob that shit
Take all flags and convert to Extension flags and settings
Run Extension through build_module? or pass BuildFile into build_module
get path of output pyd/so from build_module
call super().create_module()
modify the spec on returned module
return said module
'''

class BrujeriaExtensionFileLoader(ExtensionFileLoader):

    def __init__(self, name):
        self.name = name

    def create_module_init (self, filepath, output_path):
        buffer = StringIO(newline='\n')
        args = dict(directory=filepath.parent)
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

    def create_module (self, spec: ModuleSpec):
        if not spec.loader_state: return None
        state = spec.loader_state
        fullname = spec.name
        cache_dir = state['cache_dir'] / fullname
        filepath = state['filepath']
        output_path = cache_dir / filepath.name
        # TODO: Check if filepath is newer than output_path
        self.create_module_init(filepath, output_path)
        self.path = str(build_module(fullname, filepath, cache_dir))
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
    def cache_dir (self) -> Path: return _xdg_cache_home() / self.cache_name

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
                return ModuleSpec(fullname, loader_state=state, loader=loader)
            if fullpath.is_dir(): return ModuleSpec(fullname, loader=None, is_package=True)
 
# TODO: Remove this fuckerrrr
install()