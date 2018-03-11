from importlib.machinery import ModuleSpec, ExtensionFileLoader
from mako.template import Template
from mako.runtime import Context
from pathlib import Path
from io import StringIO

class CXXExtensionFileLoader(ExtensionFileLoader):

    def __init__ (self, name):
        self.name = name

    def create_module (self, spec: ModuleSpec):
        pass