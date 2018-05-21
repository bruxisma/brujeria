#pylint: disable=no-name-in-module,import-error
#pylint: disable=E1101
from logbook.more import ColorizingStreamHandlerMixin, ColorizedStderrHandler
from logbook import Logger, StderrHandler, StreamHandler
from functools import partialmethod
import distutils.log
import logbook
import sys

class Log:
    def __init__ (self, threshold=logbook.INFO):
        self.logger = Logger('brujeria', level=threshold)

    @property
    def threshold (self): return self.logger.level

    @threshold.setter
    def threshold (self, value):
        self.logger.level = value

    @property
    def name (self): return self.logger.name

    @name.setter
    def name (self, value): self.logger.name = value

    def log (self, level, msg, *args, **kwargs):
        if '%' in msg:
            try: msg = msg % args
            except TypeError: pass
            else: return self.logger.log(level, msg)
        self.logger.log(level, msg, *args, **kwargs)

    debug = partialmethod(log, logbook.DEBUG)
    info = partialmethod(log, logbook.INFO)
    warn = partialmethod(log, logbook.WARNING)
    error = partialmethod(log, logbook.ERROR)
    fatal = partialmethod(log, logbook.CRITICAL)
    
    # extensions
    critical = partialmethod(log, logbook.CRITICAL)
    notice = partialmethod(log, logbook.NOTICE)
    trace = partialmethod(log, logbook.TRACE)

_log = Log()

def set_name (name): _log.name = name

def set_threshold (level):
    old = _log.threshold
    _log.threshold = level
    return old

def set_verbosity (value):
    if value <= 0: set_threshold(logbook.WARNING)
    elif value == 1: set_threshold(logbook.INFO)
    elif value == 2: set_threshold(logbook.DEBUG)

def use_logbook (extensions=True, colors=True, name=True):
    global _log
    handler_options = dict(level=_log.threshold)
    distutils.log._log = _log
    distutils.log.log = _log.log
    distutils.log.debug = _log.debug
    distutils.log.info = _log.info
    distutils.log.warn = _log.warn
    distutils.log.error = _log.error
    distutils.log.fatal = _log.fatal
    distutils.log.set_threshold = set_threshold
    distutils.log.set_verbosity = set_verbosity
    distutils.log.INFO = logbook.INFO
    distutils.log.DEBUG = logbook.debug
    distutils.log.ERROR = logbook.ERROR
    distutils.log.WARN = logbook.WARNING
    distutils.log.FATAL = logbook.CRITICAL

    error_handler = ColorizedStderrHandler if colors else StderrHandler
    error_handler(**handler_options).push_application()

    if extensions:
        distutils.log.critical = _log.critical
        distutils.log.notice = _log.notice
        distutils.log.trace = _log.trace
        distutils.log.CRITICAL = logbook.CRITICAL
        distutils.log.NOTICE = logbook.NOTICE
        distutils.log.TRACE = logbook.TRACE

    if name:
        distutils.log.set_name = set_name