# -*- coding: utf-8 -*-

project = 'brujería'
copyright = '2018, Isabella Muerte'
author = 'Isabella Muerte'
version = '0.1'
release = '0.1'

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
    'sphinx.ext.extlinks',
    'sphinx.ext.todo',
]

source_suffix = '.rst'
master_doc = 'index'

language = None
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'

extlinks = {
    'github': ('https://github.com/%s', ''),
    'issue': ('https://github.com/slurps-mad-rips/brujeria/issues/%s', 'issue ')
}

intersphinx_mapping = {'https://docs.python.org/': None}
todo_include_todos = True
