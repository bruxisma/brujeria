from brujeria.build import LibraryCommand
from brujeria import Distribution, Library

from distutils.errors import DistutilsSetupError

import pytest

class LibraryCommandDummy (LibraryCommand):
    def compile (self, info): pass
    def target (self, info): pass

class LibraryCommandCompiled (LibraryCommand):
    def compile (self, info):
        assert info.inputs
        assert info.output
        assert info.inputs[0].suffix in ('.c', '.cxx', '.cpp', '.cc')
        assert info.output.suffix in ('.o', '.obj')
    def target (self, info): pass
class LibraryCommandBuild (LibraryCommand):
    def compile (self, info):
        assert True

    def target (self, info):
        assert True

@pytest.fixture
def dummy ():
    distribution = Distribution()
    return LibraryCommandDummy(distribution)

@pytest.fixture
def compiled ():
    distribution = Distribution()
    return LibraryCommandCompiled(distribution)

@pytest.fixture
def target ():
    distribution = Distribution()
    return LibraryCommandBuild(distribution)

@pytest.fixture
def build_dummy (dummy, library, tempdir):
    dummy.libraries = [library]
    dummy.build_temp = dummy.build_clib = tempdir
    dummy.finalize_options()
    return dummy

@pytest.fixture
def legacy_invalid_sources ():
    return [('example', dict(sources='broken.c'))]

@pytest.fixture
def legacy_valid_sources ():
    return [('example', dict(sources=['broken.c']))]

def setup_build_library (command, library, tempdir):
    command.libraries = [library]
    command.build_temp = command.build_clib = tempdir
    command.finalize_options()

class TestLibraryCommand:
    def test_legacy_check_library_failure (self, dummy, legacy_invalid_sources):
        with pytest.raises(DistutilsSetupError):
            dummy.check_library_list(legacy_invalid_sources)

    def test_legacy_check_library_create (self, dummy, legacy_valid_sources):
        dummy.check_library_list(legacy_valid_sources)
        assert isinstance(legacy_valid_sources[0], Library)

    def test_legacy_build_library_compile (self, dummy, legacy_valid_sources, tempdir):
        setup_build_library(dummy, legacy_valid_sources, tempdir)
        dummy.run()

    def test_get_library_names (self, dummy, library, libraries):
        dummy.libraries = libraries
        names = dummy.get_library_names()
        assert library.name in names

    def test_get_source_files (self, dummy, library, libraries):
        dummy.libraries = libraries
        sources = dummy.get_source_files()
        for source in library.sources:
            assert source in sources

    def test_build_library_sources (self, build_dummy):
        build_dummy.run()

    def test_build_library (self, target, library, tempdir):
        setup_build_library(target, library, tempdir)
        target.run()
