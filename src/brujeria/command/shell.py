from distutils.errors import DistutilsOptionError
from distutils import log

from subprocess import check_call, CalledProcessError
from setuptools import Command
import shlex

class ShellCommand (Command):
    '''Run a given shell command'''

    description = 'Runs a shell command'
    user_options = [
        ('command=', None, 'command and all its args')
    ]

    def initialize_options (self):
        self.command = None

    def finalize_options (self):
        if not self.command:
            raise DistutilsOptionError('Must specify --command')

    def run (self):
        try: check_call(self.command, shell=True)
        except CalledProcessError as e:
            log.error('%s', e)
            raise e