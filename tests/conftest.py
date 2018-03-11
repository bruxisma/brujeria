from brujeria import Distribution, Extension, Library
from brujeria import use_logbook
from brujeria import setup as setuptools

from brujeria.core import xdg

from collections import ChainMap
from functools import lru_cache, partial
from pathlib import Path
from random import seed, choices, choice, randint
from string import ascii_lowercase

from mako.template import Template

import pytest

class Generator:
    '''Quickly slapped together 'data' generator. Integrating tools like
    Faker, etc. is too much, and we'd have to do this work anyway, since this
    approach (i.e., generating randomly named modules) hasn't been done yet.
    '''

    def __init__ (self, start=4, stop=13):
        self._start = start
        self._stop = stop

    @property
    def integer (self): return randint(self.start, self.stop)

    @property
    def start (self): return self._start

    @property
    def stop (self): return self._stop

    @property
    def name (self):
        return ''.join(choices(ascii_lowercase, k=self.integer))

    @property
    def suffix (self): return choice(['c', 'cxx', 'cpp', 'cc'])

    @property
    def filenames (self):
        suffix = self.suffix
        for _ in range(self.integer):
            yield f'{self.name}.{suffix}'

    @property
    def target (self):
        return { self.name: list(self.filenames) }

    @property
    def libraries (self):
        targets = dict(ChainMap(*[self.target for _ in range(self.integer)]))
        return [Library(name, sources) for name, sources in targets.items()]

    @property
    def extensions (self):
        targets = dict(ChainMap(*[self.target for _ in range(self.integer)]))
        return [Extension(name, sources) for name, sources in targets.items()]

    @start.setter
    def start (self, value):
        if value >= self.stop: raise AttributeError('Cannot invalidate range')
        self._start = value

    @stop.setter
    def stop (self, value):
        if value <= self.start: raise AttributeError('Cannot invalidate range')
        self._stop = value

#XXX: cmdclass = dict(build_clib=libcommand, build_ext=extcommand)

@pytest.fixture(scope='session')
def template (tempdir):
    return partial(
        Template,
        module_directory=str(Path(tempdir).joinpath('template')))

@pytest.fixture(scope='session')
def cache_home ():
    '''returns $XDG_CACHE_HOME/brujeria-tests/'''
    return xdg.CACHE_HOME / 'brujeria-tests'

@pytest.fixture(scope='session')
def exttmpdir (cache_home):
    '''returns temporary directory to place extension files into'''
    return Path(cache_home).joinpath('extensions')

@pytest.fixture()
def extdatadir (shared_datadir):
    '''returns "data/ext"'''
    return shared_datadir / 'ext'

@pytest.fixture()
def extfunc (template, extdatadir):
    '''returns render functions for "data/ext/function.cxx.in"'''
    return template(filename=str(extdatadir / 'function.cxx.in')).render

@pytest.fixture()
def extheader (template, extdatadir):
    '''returns render function for "data/ext/header.h.in"'''
    return template(filename=str(extdatadir / 'header.h.in')).render

@pytest.fixture()
def extinit (template, extdatadir):
    '''returns render function for "data/ext/init.cxx.in"'''
    return template(filename=str(extdatadir / 'init.cxx.in')).render

@pytest.fixture
def module (exttmpdir, extfunc, extheader, extinit):
    '''Generates the files necessary to actually build an extension'''
    generator = Generator()
    for name, sources in generator.target.items():
        moduledir = exttmpdir.joinpath(name)
        moduledir.mkdir(parents=True, exist_ok=True)
        paths = [exttmpdir.joinpath(name, f'{source}') for source in sources]
        methods = [str(Path(source).stem) for source in sources]
        module_info = dict(module=name, methods=methods)

        header_path = moduledir.joinpath(f'{name}.h')
        init_path = moduledir.joinpath(f'init.cxx')

        header_path.write_text(extheader(**module_info))
        init_path.write_text(extinit(**module_info))

        for path in paths:
            func_info = dict(module=name, method=path.stem)
            path.write_text(extfunc(**func_info))
    sources = [str(path) for path in [init_path, *paths]]
    print(moduledir)
    return Extension(name, sources=sources)

@pytest.fixture(scope='session')
@lru_cache(maxsize=1)
def libraries ():
    generator = Generator()
    return generator.libraries

@pytest.fixture(scope='session')
@lru_cache(maxsize=1)
def extensions ():
    generator = Generator()
    return generator.libraries

@pytest.fixture(scope='session')
def tempdir (tmpdir_factory): return str(tmpdir_factory.getbasetemp())

@pytest.fixture(scope='session')
def builddir (tmpdir_factory):
    return str(tmpdir_factory.getbasetemp().dirpath('build'))

def pytest_addoption (parser):
    parser.addoption('--generator-seed',
        action='store',
        metavar='SEED',
        default=42, # TODO: Change to the current time for CI
        help='Seed value for data generation')
    parser.addoption('--use-logbook-override',
        action='store_true',
        default=True,
        help='Use logbook monkey patch')

def pytest_configure (config):
    seed(config.getoption('--generator-seed'))
    if config.getoption('--use-logbook-override'): use_logbook()

# TODO: Generate fake legacy library 2-tuples
# (then selectively match or skip for params based on some kind of schema)
def pytest_generate_tests (metafunc):
    exts = extensions()
    libs = libraries()
    ext_ids = list(map(lambda ext: ext.name, exts))
    lib_ids = list(map(lambda lib: lib.name, libs))
    if 'extension' in metafunc.fixturenames: metafunc.parametrize('extension', exts, ids=ext_ids)
    if 'library' in metafunc.fixturenames: metafunc.parametrize('library', libs, ids=lib_ids)