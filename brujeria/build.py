from importlib.machinery import ModuleSpec
from distutils.util import get_platform as _platform
from setuptools import setup
from itertools import chain
from pathlib import Path
import sys

from .command import build_ninja_ext
from .target import Extension

def build_library (name):
    pass

def build_module (fullname, filepath, cache_dir) -> Path:
    extensions = ['c', 'cxx', 'cpp', 'cc']
    sources = []
    if filepath.stem == 'init':
        module_dir = filepath.parent
        for ext in extensions:
            sources.extend(module_dir.glob(f'*.{ext}'))
        sources.remove(filepath)
    sources.append(cache_dir / filepath.name)
    build_path = cache_dir / 'build'
    sources = [str(source) for source in sources]
    args = [
        'build_ext', f'--build-temp={build_path}', f'--build-lib={build_path}'
    ]
    ext = Extension(
        fullname,
        sources=sources,
        language='c++')
    
    setup(
        name=fullname,
        ext_modules=[ext],
        script_args=args,
        cmdclass=dict(build_ext=build_ninja_ext))

    platform = _platform().replace('-', '_').replace('.', '_')
    version = sys.version_info

    tag = f'{fullname}.cp{version.major}{version.minor}-{platform}'
    return build_path / f'{tag}.pyd'

#pkg_resources.set_extraction_path(_xdg_cache_home() / 'brujeria' / 'extracted')