from ..importlib.finder import CXXExtensionFinder
import sys

sys.meta_path.insert(0, CXXExtensionFinder())