from distutils.errors import DistutilsOptionError
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Text

from .ast import Rule

class BuildInfo:
    def __init__ (self, command, inputs, output, includes, args):
        self.command = Path(command)
        self.inputs = list(map(Path, inputs))
        self.includes = includes
        self.output = Path(output)
        self.args = args
    
    def add_arguments(self, *args): self.args.extend(args)

def _parse_cmd (cmd: List[Text], parser: ArgumentParser) -> BuildInfo:
    print(cmd)
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
        input_flag = '/Tc' if info.inputs[0].suffix == '.c' else '/Tp'
        inputs.insert(0, input_flag)
    info.args.append(' $\n')
    includes = ' $\n'.join([f'-I"{include}"' for include in info.includes])
    command = [f'{info.command} $\n', *inputs, output, *info.args, includes]
    return Rule('compile', command, depfile=depfile, deps=deps)

def _create_target_rule (info: BuildInfo, is_posix: bool) -> Rule:
    output = ['-o', '$out']
    includes = ''
    if not is_posix:
        output = ['/OUT:$out']
        includes = ' $\n'.join([f'/LIBPATH:"{include}"' for include in info.includes])
    command = [f'{info.command} $\n', *info.args, *output, '$in', includes]
    return Rule('target', command)