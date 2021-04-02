from . import machinery

# from . import distribution
# from . import command
import sys

sys.meta_path.insert(0, machinery.CMakeFinder())

# def build(kwargs):
#    kwargs.update(cmdclass=dict(), distclass=None)
