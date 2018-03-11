from setuptools import Command

class HelpCommand (Command):
    '''Prints all available commands'''

    description = 'Prints all available commands'
    user_options = []

    def initialize_options (self): pass
    def finalize_options (self): pass

    def run (self):
        commands, descriptions = zip(*self.distribution.get_command_list())
        length = len(max(commands, key=len))
        for cmd, desc in zip(commands, descriptions):
            print(f'  {cmd:{length}} -- {desc}')