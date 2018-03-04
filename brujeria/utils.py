from distutils.errors import DistutilsOptionError
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Text
import os

from .ast import Rule

def _escape_path (filepath: Path) -> Path:
    return Path(str(filepath).replace(' ', '$ ').replace(':', '$:'))

def _xdg_cache_home ():
    if os.name == 'nt' and not os.environ.get('XDG_CACHE_HOME'):
        os.environ['XDG_CACHE_HOME'] = os.environ['LOCALAPPDATA']
    return Path(os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache'))

class BuildInfo:
    def __init__ (self, command, inputs, output, includes, args):
        self.command = Path(command)
        self.inputs = list(map(_escape_path, inputs))
        self.includes = includes
        self.output = _escape_path(output)
        self.args = args

    def add_arguments(self, *args): self.args.extend(args)

def _parse_cmd (cmd: List[Text], parser: ArgumentParser) -> BuildInfo:
    exe_path, *arguments = cmd
    args, remainder = parser.parse_known_args(arguments)
    if not args.inputs and not args.output:
        raise DistutilsOptionError(f'Could not extract source and output args')
    if not hasattr(args, 'includes'): setattr(args, 'includes', [])
    return BuildInfo(exe_path, args.inputs, args.output, args.includes, remainder)

def _create_compile_rule (info: BuildInfo, is_posix: bool) -> Rule:
    depfile = '$out.d'
    output = '-o $out'
    deps = 'gcc'
    inputs = ['$in']
    if not is_posix:
        depfile = None
        output = '/Fo$out'
        deps = 'msvc'
        input_flag = '/Tp'
        inputs.insert(0, input_flag)
    includes = ' $\n'.join([f'-I"{include}"' for include in info.includes])
    args = '{} $'.format(' $\n'.join(info.args))
    command = [f'{info.command} $\n', output, *inputs, '@$out.rsp']
    content = '\n'.join([args, includes])
    return Rule('compile', command,
        depfile=depfile,
        deps=deps,
        rspfile='$out.rsp',
        rspfile_content=content)

def _create_target_rule (info: BuildInfo, is_posix: bool) -> Rule:
    output = ['-o', '$out']
    includes = ''
    if not is_posix:
        output = ['/OUT:$out']
        includes = ' $\n'.join([f'/LIBPATH:"{include}"' for include in info.includes])
    args = '{} $'.format(' $\n'.join(info.args))
    content = '\n'.join([args, '$in_newline $', includes])
    command = [f'{info.command} $\n', *output, '@$out.rsp']
    return Rule('target', command, rspfile='$out.rsp', rspfile_content=content)