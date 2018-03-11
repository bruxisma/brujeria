from pathlib import Path
from typing import Text
import textwrap

class Variable:
    def __init__ (self, key, value):
        self.key = key
        self.value = value

class Rule:
    def __init__ (self, name: Text, command, **kwargs):
        self.name = name
        self.command = Variable('command', command)

    def __repr__ (self): return f'<Rule: {self.name}>'

class File:
    def __init__ (self, path):
        self.path = Path(path).with_suffix('.ninja')

    def __format__ (self, format_spec): return f'include {self.path}'
    def __repr__ (self): return f'<File:{self.path}>'

class Scope:
    def __init__ (self, path: Path):
        self.path = Path(path).with_suffix('.ninja')

    def __format__ (self, format_spec): return f'subninja {self.path}'
    def __repr__ (self): return f'<Scope: {self.path}>'

class Comment:
    def __init__ (self, text: Text):
        self.text = text

    def __repr__ (self): return f'<Comment: {self.text}>'
    def __format__ (self, format_spec):
        kwargs = dict(width=78, initial_indent='#', subsequent_indent='#')
        return textwrap.fill(self.text, **kwargs)

class Default:
    def __init__ (self, *names):
        self.names = names

    def __format__ (self, format_spec):
        pass

    def __repr__ (self): return f'<Default: {(" ".join(self.names))}>'

class Alias:
    def __init__ (self, name, target):
        self.name = name
        self.target = target

    def __repr__ (self): return f'<Alias: {self.target} as {self.name}>'

    def __format__ (self, format_spec):
        return f'build {self.name}: phony {self.target}'

class Pool:
    def __init__ (self, name, depth):
        self.name = name
        self.depth = depth

    def __repr__ (self): return f'<Pool: {self.name}:{self.depth}>'