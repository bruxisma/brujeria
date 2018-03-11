from .execute import ExecuteCommand
from .ninja import BuildNinjaExt
from .ninja import BuildNinjaLib
from .purge import PurgeCommand
from .shell import ShellCommand
from .help import HelpCommand

cmdclass = dict(
    build_clib=BuildNinjaLib,
    build_ext=BuildNinjaExt)