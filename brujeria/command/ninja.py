from .mixin import BuildNinjaMixin
from .base import LibraryCommand, ExtensionCommand

class BuildNinjaExt (BuildNinjaMixin, ExtensionCommand): pass
class BuildNinjaLib (BuildNinjaMixin, LibraryCommand): pass