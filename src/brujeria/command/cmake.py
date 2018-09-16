from setuptools.command.build_ext import build_ext

class CMakeCommand(build_ext):
    def build_extensions (self):
        for ext in self.extensions:
            self.build_extension(ext)
    
    # TODO: This is where the magic happens on both setup.py install as well
    # as an import statement.
    def build_extension (self, ext):
        pass
