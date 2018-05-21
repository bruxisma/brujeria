# TODO: This doesn't work correctly. More work is needed to make sure
# that we can override the setuptools build_ext as well.
from ..command.cmake import CMakeCommand
from distutils.command.build_ext import build_ext

build_ext = CMakeCommand