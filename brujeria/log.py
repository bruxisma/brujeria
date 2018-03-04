from logbook import Logger, StderrHandler, StreamHandler, SyslogHandler
from logbook.more import ColorizedStderrHandler
from functools import partialmethod
import distutils.log
import logbook
import sys

# TODO: Look into resetting logging info to original
def use_logbook (extensions=True, colors=True, name=True):
    global _global_log
    handler_options = dict(level=logbook.WARNING, bubble=True)
    distutils.log._global_log = _global_log
    distutils.log.log = _global_log.log
    distutils.log.debug = _global_log.debug
    distutils.log.info = _global_log.info
    distutils.log.warn = _global_log.warn
    distutils.log.error = _global_log.error
    distutils.log.fatal = _global_log.fatal
    distutils.log.set_threshold = set_threshold
    distutils.log.set_verbosity = set_verbosity
    distutils.log.INFO = logbook.INFO
    distutils.log.DEBUG = logbook.debug
    distutils.log.ERROR = logbook.ERROR
    distutils.log.WARN = logbook.WARNING
    distutils.log.FATAL = logbook.CRITICAL

    error_handler = ColorizedStderrHandler if colors else StderrHandler
    _global_log.add_handler(error_handler(**handler_options))

    if extensions:
        distutils.log.critical = _global_log.critical
        distutils.log.notice = _global_log.notice
        distutils.log.trace = _global_log.trace
        distutils.log.CRITICAL = logbook.CRITICAL
        distutils.log.NOTICE = logbook.NOTICE
        distutils.log.TRACE = logbook.TRACE

    if name:
        distutils.log.set_name = set_name

class Log:
    def __init__ (self, threshold=logbook.WARNING):
        self._log = Logger('brujeria', level=threshold)

    @property
    def threshold (self): return self._log.level
    
    @threshold.setter
    def threshold (self, value): self._log.level = value

    def add_handler (self, handler):
        self._log.handlers.append(handler)

    def log (self, level, msg, *args, **kwargs):
        # TODO: Improve this attempt at backwards compat. How we detect if
        # something is an old style format string is not so hot.
        # We need to figure out when and where to reraise
        if '%' in msg:
            try: msg = msg % args
            except TypeError: pass
            else: return self._log.log(level, msg)
        self._log.log(level, msg, *args, **kwargs)

    debug = partialmethod(log, logbook.DEBUG)
    info = partialmethod(log, logbook.INFO)
    warn = partialmethod(log, logbook.WARNING)
    error = partialmethod(log, logbook.ERROR)
    fatal = partialmethod(log, logbook.CRITICAL)

    # Extensions
    def critical (self, msg, *args, **kwargs): pass
    def notice (self, msg, *args, **kwargs): pass
    def trace (self, msg, *args, **kwargs): pass

_global_log = Log()

def set_name (name):
    _global_log._log.name = name

def set_threshold (level):
    old = _global_log.threshold
    _global_log.threshold = level
    return old

def set_verbosity (value):
    if value <= 0: set_threshold(logbook.WARNING)
    elif value == 1: set_threshold(logbook.INFO)
    elif value >= 2: set_threshold(logbook.DEBUG)

use_logbook()