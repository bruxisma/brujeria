from collections.abc import Iterable
from functools import partial
from pathlib import Path
from typing import Text, List
import textwrap
import ninja
import io

'''
This module provides an interface for generating ninja files without having
to worry about the intricacies of ninja_syntax. We construct fake ASTs (just
lists of ninja build file entries), and then dump them to a file
'''

def ninja_path (): return Path(ninja.BIN_DIR)

def _format_list (items, sep, prefix=''):
    if not items: return ''
    text = sep.join(f'{item}' for item in items)
    return f'{prefix}{text}'

def _var (lookup, key):
    return Variable(key, lookup.get(key, None))

class Ninja:
    def __init__ (self, path):
        self.path = Path(path).with_suffix('.ninja')
        self.items = list()
        self.rules = list()

    def close (self):
        with open(self.path, 'w') as build:
            build.write(_format_list(self.rules, sep='\n'))
            build.write(_format_list(self.items, sep='\n'))
            build.write('\n')
            build.flush()
            #self.path.write_text(buffer.getvalue())
        #self.path.write_text(f'{self}'')
        #self.path.write_text(_format_list(self.items, sep='\n'))
        pass

    def append (self, item):
        if isinstance(item, Rule): return self.rules.append(item)
        self.items.append(item)

    def extend(self, iterable):
        self.items.extend(iterable)

class File:
    def __init__ (self, path):
        self.path = Path(path).with_suffix('.ninja')

    def __repr__ (self): return f'<File:{self.path}>'
    def __format__ (self, format_spec): return f'<File: {self.path}>'

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
        names = _format_list(self.names, sep=' ')
        return f'default {names}'

class Rule:

    def __init__ (self, name: Text, command, **kwargs):
        get = partial(_var, kwargs)
        self.name = name
        self.description = get('description')
        self.depfile = get('depfile')
        self.generator = get('generator')
        self.pool = get('pool')
        self.restat = get('restat')
        self.rspfile = get('rspfile')
        self.rspfile_content = get('rspfile_content')
        self.deps = get('deps')
        self.command = Variable('command', command) #if isinstance(command, List) else Command(command)

    def __repr__ (self): return f'<Rule: {self.name}>'

    def __format__ (self, format_spec): 
        return f'rule {self.name}{self._vars}\n'

    @property
    def _vars (self):
        variables = [
            self.command,
            self.description,
            self.depfile,
            self.generator,
            self.pool,
            self.restat,
            self.rspfile,
            self.rspfile_content,
            self.deps
        ]
        return textwrap.indent(_format_list(filter(None, variables), sep='\n', prefix='\n'), ' ')


#class Command:
#    def __init__ (self, info):
#        self.inputs = info.inputs
#        self.includes = _format_list(info.includes, 
#        self.command = command
#
#    def __format__ (self, format_spec):
#        pass


class Target:

    def __init__ (self, rule: Text, outputs, **kwargs):
        self.rule = rule
        self.outputs = outputs if isinstance(outputs, Iterable) else [outputs]
        self.inputs = kwargs.get('inputs', [])
        self.implicit = kwargs.get('implicit')
        self.order_only = kwargs.get('order_only')
        self.variables = kwargs.get('variables')
        self.implicit_outputs = kwargs.get('implicit_outputs')

    def __repr__ (self):
        return f'<Target: build {self.outputs}: {self.rule} {self.inputs}>'

    def __format__ (self, format_spec):
        outputs = _format_list(self.outputs, sep=' ')
        rule = self.rule if not isinstance(self.rule, Rule) else self.rule.name
        inputs = _format_list(self.inputs, sep=' ')
        implicit = _format_list(self.implicit, sep=' ', prefix='| ')
        implicit_outputs = _format_list(self.implicit_outputs, sep=' ', prefix='|')
        order_only = _format_list(self.order_only, sep=' ', prefix='||')
        variables = textwrap.indent(_format_list(self.variables, sep='\n', prefix='\n'), ' ')
        return f'build {outputs} {implicit_outputs}: {rule} {inputs}{implicit}{order_only}{variables}'

class Alias:
    def __init__ (self, name, target):
        self.name = name
        self.target = target

    def __repr__ (self): return f'<Alias: {self.target} as {self.name}>'

    def __format__ (self, format_spec):
        return f'build {self.name}: phony {self.target}'

class Variable:
    def __init__ (self, key, value):
        self.key = key
        if isinstance(value, List):
            value = _format_list(filter(None, value), ' ')
        self.value = value

    def __repr__ (self):
        return f'<Variable: {self.key}={self.value}>'

    def __bool__ (self): return bool(self.value)

    def __format__ (self, format_spec):
        if self.value is None: return ''
        return f'{self.key} = {self.value}'

class Pool:
    def __init__ (self, name, depth):
        self.name = name
        self.depth = depth

    def __repr__ (self): return f'<Pool: {self.name}:{self.depth}>'