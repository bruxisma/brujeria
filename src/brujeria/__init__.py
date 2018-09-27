from .importlib.finder import CMakeExtensionFinder
import sys

sys.meta_path.insert(0, CMakeExtensionFinder())
