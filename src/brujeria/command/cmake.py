from setuptools.command.build_ext import build_ext

class CMakeCommand(build_ext):
    def build_extensions (self):
        for ext in self.extensions:
            self.build_extension(ext)
    
    def build_extension (self, ext):
        pass
