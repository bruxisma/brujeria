from .finder import BrujeriaCMakeFinder
import sys

sys.meta_path.insert(0, BrujeriaCMakeFinder())
