from setuptools.dist import Distribution
from .command import CMakeCommand


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


def build(kwargs):
    kwargs.update(cmdclass=dict(build_ext=CMakeCommand), distclass=BinaryDistribution)

