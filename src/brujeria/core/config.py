'''This module provides a Configuration object that permits changing settings
used throughout brujeria. These are primarily for working with the importlib
machinery when importing an `init.cmake` file.
'''

class Compiler:
    cxx = None
    cc = None

class Tools:
    launcher = None
    cppcheck = None
    tidy = None
    iwyu = None

class Configuration:

    def __init__ (self):
        self.tempname = 'brujeria'
        self.compiler = Compiler()
        self.tools = Tools()

config = Configuration()