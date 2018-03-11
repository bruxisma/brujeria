from ..command.base import LibraryCommand, ExtensionCommand
from ..command.mixin import BuildNinjaMixin

class build_ninja_clib (BuildNinjaMixin, LibraryCommand): pass
class build_ninja_ext (BuildNinjaMixin, ExtensionCommand): pass