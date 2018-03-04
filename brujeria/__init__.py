from setuptools import setup, find_packages, Distribution, Command

from .target import Extension, Library
from .log import use_logbook