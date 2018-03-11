from pathlib import Path

from .ast import Rule

class Writer:
    def __init__ (self, path):
        self.path = Path(path).with_suffix('.ninja')
        self.items = []
        self.rules = []

    def close (self):
        raise NotImplementedError('Justin PWEASE let me keep him')

    def append (self, item):
        if isinstance(item, Rule): return self.rules.append(item)
        self.items.append(item)

    def extend (self, iterable):
        self.items.extend(iterable)