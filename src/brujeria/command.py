# raise NotImplementedError('This interface is currently under development')
# from itertools import chain
# from pathlib import Path
# import os
#
# from distutils.command.build_ext import build_ext
# # Don't want to pull in poetry just so we can stay in lockstep with it...
# #from poetry.masonry.utils.module import Module
# import tomlkit
#
# from .tool import CMake
#
# class CMakeCommand(build_ext):
#
#     def run (self):
#         self.build_extensions()
#
#     def build_extensions (self):
#         pass
#         # We read from the pyproject.toml for configuration settings
#         # from this, we can also read from the poetry project info so we
#         # know where to look in general. From there we generate the list
#         # of known init.cmake locations, and then build them with
# each project in a specific subdirectory of self.build_temp
# We also explicitly set CMAKE_LIBRARY_OUTPUT_DIRECTORY to self.build_lib
#         #with open('pyproject.toml') as config:
#         #    config = tomlkit.parse(config.read())['tool']['poetry']
#         #module = Module(config['name'], packages=config.get('packages'))
#         #paths = [item.base / item.package for item in module.includes]
#         #paths = chain.from_iterable(path.glob('**/init.cmake') for path in paths)
#         #paths = [item.parent for item in paths]
#         # TODO: This is where we do the actual work
#
#
#     # TODO: This is where the magic happens on both setup.py install as well
#     # as an import statement.
#     def build_extension (self, ext):
#         pass
#