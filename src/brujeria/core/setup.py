#pylint:disable=E1101
from fnmatch import fnmatchcase
from pathlib import Path
import os

from setuptools.config import ConfigOptionsHandler as _ConfigOptionsHandler
from setuptools import find_packages, PackageFinder
import setuptools

# TODO: This should probably be named differently/imported a bit differently.
# i.e., why are we importing brujeria.core.setup in its entirety, and then a
# few other things? It needs to be spread out a bit better, in my opinion.
# Then again, setuptools doesn't spread it out as much either.
# HOWEVER, we *are* monkey patching *just* setuptools here, and if others wish
# to patch brujeria we should give them better fine-grained access over th
# code.

class ExtensionFinder(PackageFinder):
    '''
    Generate a list of all CMake extensions found within a directory.

    We hijack the PackageFinder behavior, but change what a "package" is, so
    that we can find CMake extensions instead.
    '''

    @classmethod
    def _looks_like_package (cls, path):
        '''Does a directory look like a brujeria *extension*?'''
        return os.path.isfile(os.path.join(path, 'init.cmake'))

class ConfigOptionsHandler(_ConfigOptionsHandler):
    '''Modified ConfigOptionsHandler to support auto-finding extensions

    Works with either 'extensions' or 'ext_modules' under options, *but*
    requires an argument section to use 'options.extensions.find', rather than
    supporting both behaviors.

    We're technically using what the setup.cfg parser considers to be an 'older'
    or 'outdated' name, but that is what the name *should* be, rather than
    'ext_modules', in our opinion.
    '''
    aliases = { 'extensions': 'ext_modules' }

    @property
    def parsers (self):
        parsers = super().parsers
        parsers.update(ext_modules=self._parse_extensions)
        return parsers

    def _parse_extensions (self, value):
        find_directive = 'find:'
        if not value.startswith(find_directive):
            return self._parse_list(value)
        # We reuse the setuptools packages.find parser so we don't have to
        # replicate it.
        find_kwargs = self.parse_section_packages__find(
            self.sections.get('extensions.find', {}))
        return find_extensions(**find_kwargs)

find_extensions = ExtensionFinder.find

def setup (**attrs):
    '''Wrapper around setuptools' setup
    
    Currently patches a few setuptools classes so that our setup.py behavior
    will *just work* when imported.

    extensions are automatically found, if not explicitly given, and the
    correct command classes are set for build_ext. Additional command classes
    are ignored, unless explicitly asked
    '''
    #TODO: Need to manually modify build_ext here.
    setuptools.config.ConfigOptionsHandler = ConfigOptionsHandler

    setuptools.setup(**attrs)