from brujeria.command import build_ninja_ext, build_ninja_clib
from brujeria import Distribution, Library, Extension
import pytest
import pdb

@pytest.fixture
def clib ():
    dist = Distribution()
    return build_ninja_clib(dist)

@pytest.fixture
def ext ():
    dist = Distribution()
    dist.ext_modules = [Extension('test', ['tests/test.cxx'])]
    return build_ninja_ext(dist)

class TestNinjaExt:

    def test_ninja_ext_writer (self, ext):
        assert hasattr(ext, 'writer')

    def test_ninja_ext (self, ext: build_ninja_ext, tmpdir_factory):
        ext.build_temp = ext.build_lib = 'build'
        ext.finalize_options()
        ext.run()

class TestNinjaLib:

    def test_ninja_clib_writer (self, clib):
        assert hasattr(clib, 'writer')
    
    def test_ninja_clib (self, clib: build_ninja_clib, tmpdir_factory):
        clib.build_temp = clib.build_clib = 'build'
        clib.finalize_options()
        clib.libraries = [Library('test', ['tests/test.cxx'])]
        clib.run()
