from distutils.errors import DistutilsOptionError
from distutils import log

from subprocess import check_call, CalledProcessError
from setuptools import Command
import shlex

class ExecuteCommand (Command):
    '''Executes a given command and its arguments'''

    description = 'Executes a command and its arguments'
    user_options = [
        ('command=', None, 'name of executable (required)'),
        ('args=', None, 'arguments to pass to command')
    ]

    boolean_options = ['use-windows-options']

    def initialize_options (self):
        self.command = None
        self.windows = None
        self.args = None

    def finalize_options (self):
        if not self.command:
            raise DistutilsOptionError('Must specify --command')

    def run (self):
        posix = not self.windows
        cmd = [self.command, *shlex.split(self.args, posix=posix)]
        try: check_call(cmd)
        except CalledProcessError as e:
            log.error('%s', e)
            raise e