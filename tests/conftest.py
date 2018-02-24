from brujeria import Distribution, Extension, Library

from collections import ChainMap
from random import seed, choices, randrange as select
from string import ascii_lowercase

import pytest

def randrange (start, stop):
    return choices(range(start, stop), k=(stop - start))

def genfilenames (_):
    stem = ''.join(choices(ascii_lowercase, k=select(1, 8)))
    suffix = ''.join(choices(['c', 'cxx', 'cpp', 'cc'], k=1))
    return f'{stem}.{suffix}'

def genextension (_):
    name = ''.join(choices(ascii_lowercase, k=5))
    filenames = list(map(genfilenames, randrange(1, 10)))
    return { name : filenames }

def genlibrary (_):
    name = ''.join(choices(ascii_lowercase, k=5))
    filenames = list(map(genfilenames, randrange(1, 10)))
    return { name: filenames }

def targets (cls, cache, key, generator):
    targets = cache.get(f'brujeria/{key}', None)
    if not targets:
        targets = dict(ChainMap(*map(generator, randrange(5, 10))))
        cache.set(f'brujeria/{key}', targets)
    return [cls(name, sources) for name, sources in targets.items()]

@pytest.fixture()
def libraries (cache): return targets(Library, cache, 'libraries', genlibrary)

@pytest.fixture()
def extensions (cache): return targets(Extension, cache, 'extensions', genextension)

def pytest_configure (config):
    seed(42)

# TODO: Generate fake legacy library 2-tuples
# (then selectively match or skip for params based on some kind of schema)
def pytest_generate_tests (metafunc):
    exts = extensions(metafunc.config.cache)
    libs = libraries(metafunc.config.cache)
    ext_ids = list(map(lambda ext: ext.name, exts))
    lib_ids = list(map(lambda lib: lib.name, libs))
    if 'extension' in metafunc.fixturenames: metafunc.parametrize('extension', exts, ids=ext_ids)
    if 'library' in metafunc.fixturenames: metafunc.parametrize('library', libs, ids=lib_ids)