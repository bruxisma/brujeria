'''Importing this file will automatically patch distutils.log to use logbook'''

from ..core.log import use_logbook

# TODO: Look into resetting logging info to original
use_logbook()