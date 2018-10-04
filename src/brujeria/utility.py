from functools import partial
from typing import get_type_hints
import ctypes

class rpartial(partial):
    def __call__ (self, *args, **kwargs):
        kw = self.keywords.copy()
        kw.update(kwargs)
        return self.func(*args, *self.args, **kwargs)

# TODO: This should *definitely* be spun out into its own project
def extern (cdll, name=None):
    '''Use type hints to declare and create ctypes function pointers'''
    def wrapper (func):
        nonlocal name
        if not name: name = func.__name__
        fptr = cdll[name]
        types = get_type_hints(func)
        restype = types.pop('return', ctypes.c_int)
        # typing library special cases this and I personally find it weird
        if restype is type(None): restype = None
        fptr.restype = restype
        fptr.argtypes = list(types.values())
        return fptr
    return wrapper
