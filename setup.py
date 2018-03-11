#!/usr/bin/env python3.6

from distutils.errors import DistutilsOptionError, DistutilsFileError
from setuptools import setup, Command
from distutils import log
from itertools import chain
from pathlib import Path

import subprocess
import shutil
import shlex
import os

from brujeria.command import ExecuteCommand, HelpCommand, PurgeCommand
import brujeria.inject.logging

cmdclass = dict(
    execute=ExecuteCommand,
    purge=PurgeCommand,
    help=HelpCommand)

setup(cmdclass=cmdclass)