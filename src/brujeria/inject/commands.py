#pylint: disable=no-name-in-module,import-error
from distutils.command.build_ext import build_ext
from ..command.cmake import CMakeCommand

build_ext = CMakeCommand