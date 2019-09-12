from . import machinery
import sys

sys.meta_path.insert(0, machinery.CMakeFinder())
