from contextlib import contextmanager
from types import MethodType

@contextmanager
def method (obj, attr, func):
    value = MethodType(func, obj)
    with attribute(obj, attr, value): yield

@contextmanager
def attribute (obj, attr, value):
    original = getattr(obj, attr)
    setattr(obj, attr, value)
    try: yield
    finally: setattr(obj, attr, original)