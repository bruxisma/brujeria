from setuptools import setup, find_packages, Distribution, Command

from .target import Extension, Library
from .core.log import use_logbook
