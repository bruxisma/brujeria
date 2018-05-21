'''This module provides a Configuration object that permits changing settings
Used throughout brujeria. These are typically simple things (pragma settings,
output directory, whether to use the module template file, etc.)
'''

class Configuration:
    
    def __init__ (self):
        self.tempname = 'brujeria'
        self.extensions = ['.c', '.cxx', '.cpp', '.cc']

config = Configuration()