from distutils.errors import DistutilsFileError, DistutilsOptionError
from distutils import log

from setuptools import Command
from itertools import chain
from pathlib import Path

import shutil
import os

class PurgeCommand(Command):
    '''Deletes all temporary files and returns project to a 'pristine' state'''

    description = 'A stronger version of clean'
    user_options = [
        ('match=', 'm', 'patterns to glob (default: *.egg-info, *.dist-info)'),
        ('items=', 'i', 'dirs to remove (default: .eggs, .pytest_cache, build, dist)'),
    ]

    def initialize_options (self):
        self.match = ['*.egg-info', '*.dist-info']
        self.items = ['.eggs', '.pytest-cache', 'build', 'dist']

    def finalize_options (self):
        error = 'Must specify one or more (comma-separated) {}'
        if not self.match:
            raise DistutilsOptionError(error.format('glob patterns'))
        if not self.items:
            raise DistutilsOptionError(error.format('directories'))

    def run (self):
        current = Path()
        pattern_generator = (current.glob(pattern) for pattern in self.match)
        paths = list(chain.from_iterable(pattern_generator))
        paths.extend([current.joinpath(path) for path in self.items])
        for path in paths:
            if not path.exists():
                log.warn(f"'{path}' does not exist -- can't purge it")
                continue
            log.info(f'Deleting {path}')
            if self.dry_run: continue
            if path.is_dir(): shutil.rmtree(path)
            else: os.unlink(path)