from collections.abc import Iterable
from textwrap import indent, fill as textwrap
from functools import partial
from pathlib import Path
from typing import Text, Any
import ninja

'''
This module provides an interface to generating ninja files. This is
effectively a safer wrapper around the ninja_syntax API, while also letting
us construct and modify a fake Ninja file's AST. Only once we're satisfied
with it do we dump it to a file
'''

class Writer:
    def __init__(self, filename: Path):
        self.filename = Path(filename).with_suffix('.ninja')
        self.writer = ninja.Writer(self.filename)
        self.rules = set()
        self.items = []

    def append(self, item: Any):
        if isinstance(item, Rule): return self.rules.add(item)
        self.items.append(item)
    def extend(self, items): self.items.extend(items)

    def close (self):
        for rule in self.rules:
            rule.__write__(self)
        for item in self.items:
            item.__write__(self)
        self.writer.close()

class Comment:
    def __init__ (self, text: Text):
        self.text = text

    def __write__ (self, writer: Writer):
        writer.comment(self.text)

    def __repr__ (self): return f'<Comment: {self.text}>'

class Default:
    def __init__ (self, *names: Text):
        self.names = names

    def __write__ (self, writer: Writer):
        writer.default(self.names)

    def __repr__ (self): return f"<Default: {(', '.join(self.names))}>"

class File:
    def __init__ (self, path: Path):
        self.path = Path(path).with_suffix('.ninja')

    def __write__ (self, writer: Writer):
        writer.include(self.path)

    def __repr__ (self): return f'<File: {self.path}>'

class Scope:
    def __init__ (self, path: Path):
        self.path = Path(path).with_suffix('.ninja')

    def __write__ (self, writer: Writer):
        writer.subninja(self.path)

    def __repr__ (self): return f'<Scope: {self.path}>'

class Variable:
    def __init__ (self, key, value):
        self.value = value
        self.key = key

    def __write__ (self, writer):
        writer.variable(self.key, self.value)

    def __repr__ (self): return f'<Variable: {self.key}={self.value}>'

class Rule:
    def __init__ (self, name: Text, command, **kwargs):
        self.name = name
        self.command = command
        self.description = kwargs.get('description')
        self.depfile = kwargs.get('depfile')
        self.generator = kwargs.get('generator')
        self.pool = kwargs.get('pool')
        self.restat = kwargs.get('restat')
        self.rspfile = kwargs.get('rspfile')
        self.rspfile_content = kwargs.get('rspfile_content')
        self.deps = kwargs.get('deps')

    def __write__ (self, writer):
        writer.rule(self.name, self.command, self.description, self.depfile, self.generator, self.pool, self.restat, self.rspfile, self.rspfile_content, self.deps)

class Target:
    def __init__ (self, rule: Text, outputs, **kwargs):
        self.rule = rule
        self.outputs = outputs
        self.inputs = kwargs.get('inputs', [])
        self.implicit = kwargs.get('implicit')
        self.order_only = kwargs.get('order_only')
        self.variables = kwargs.get('variables')
        self.implicit_outputs = kwargs.get('implicit_outputs')

    def __write__ (self, writer):
        writer.build(
            self.outputs,
            self.rule,
            self.inputs,
            self.implicit,
            self.order_only,
            self.variables,
            self.implicit_outputs)

    def __repr__ (self): return f'<Target: output={self.outputs}, inputs={self.inputs}>'

class Alias:
    def __init__ (self, name, target):
        self.name = name
        self.target = target

    def __write__ (self, writer):
        writer.build(self.name, 'phony', self.target)

    def __repr__ (self): return f'<Alias: {self.target} as {self.name}>'

class Pool:
    def __init__ (self, name, depth):
        self.name = name
        self.depth = depth

    def __writer__ (self, writer):
        writer.pool(self.name, self.depth)

    def __repr__ (self): return f'<Pool: {self.name}:{self.depth}>'