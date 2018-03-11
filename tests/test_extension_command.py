from brujeria.command.base import ExtensionCommand
from brujeria import Distribution, Extension
from random import seed, choices, randrange
from string import ascii_lowercase

import pytest

class ExtensionCommandDummy (ExtensionCommand):
    def compile (self, info): assert True
    def target (self, info): pass

@pytest.fixture(params=[ExtensionCommandDummy])
def command (request):
    distribution = Distribution()
    return request.param(distribution)

@pytest.fixture
def build (command, extension, tmpdir_factory):
    command.extensions = [extension]
    command.build_temp = command.build_lib = str(tmpdir_factory)
    command.finalize_options()
    return command

class TestExtensionCommand:
    def test_build_extension (self, build):
        build.run()