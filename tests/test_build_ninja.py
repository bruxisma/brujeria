from brujeria.command import build_ninja_ext, build_ninja_clib
from brujeria import Distribution, Library
import pytest
import pdb

@pytest.fixture
def clib ():
    dist = Distribution()
    return build_ninja_clib(dist)

class TestNinjaExt:
    pass

class TestNinjaLib:

    def test_ninja_clib_writer (self, clib):
        assert hasattr(clib, 'writer')
    
    def test_ninja_clib (self, clib: build_ninja_clib, tmpdir_factory):
        clib.build_temp = clib.build_clib = 'build'
        clib.finalize_options()
        clib.libraries = [Library('test', ['tests/test.cxx'])]
        clib.run()