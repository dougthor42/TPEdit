# -*- coding: utf-8 -*-s
"""
"""
### Imports #################################################################
import datetime
import os.path
import logging
from logging.handlers import TimedRotatingFileHandler as TRFHandler

### Constants ###############################################################
__version__ = "0.0.0.1"
__project_url__ = "https://github.com/dougthor42/TPEdit"
__project_name__ = "TPEdit"

LOG_LEVEL_FILE = logging.DEBUG
LOG_LEVEL_CONSOLE = logging.DEBUG


def _setup_logging():
    """
    Set up logging for the entire package.

    Log strings are sent to both the console and a log file.

    The file is a TimedRotatingFileHandler set up to create a new log file
    every Sunday at midnight. This should keep the log files small-ish
    while also keeping the number of log files down. All log files are
    kept (none are automatically deleted by backupCount parameter).

    Log lines look like so::

        2015-06-23 17:04:10.409 [DEBUG   ] [gui     ] [_color_dol]  message...
        |--------| |----------| |--------| |--------| |----------|  |--------)
             ^          ^            ^          ^            ^          ^
             |          |            |          |            |          |
        Date +          |            |          |            |          |
        Time -----------+            |          |            |          |
        Level Name (8 char) ---------+          |            |          |
        Module Name (8 char) -------------------+            |          |
        Function Name (10 char) -----------------------------+          |
        Message --------------------------------------------------------+

    All dates and times are ISO 8601 format, local time.


    Parameters:
    -----------
    None

    Returns:
    --------
    None

    Notes:
    ------

    1. Since I cannot get ms in the date format, I use the logger `msecs`
       attribute in the log format string.
    2. cx_freeze puts .py files in library.zip, so this means that I have
       to go up one additional level in the directory tree to find the
       `log` folder.

    References:
    -----------
    Logging different levels to different places:
        https://aykutakin.wordpress.com/2013/08/06/logging-to-console-and-file-in-python/

    Adding milliseconds to log string:
        http://stackoverflow.com/a/7517430/1354930

    TimedRotatingFileHandler:
        https://docs.python.org/3.4/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler

    TimedRotatingFileHandler:
        http://www.blog.pythonlibrary.org/2014/02/11/python-how-to-create-rotating-logs/
    """
    logfmt = ("%(asctime)s.%(msecs)03d"
              " [%(levelname)-8.8s]"
              " [%(module)-8.8s]"       # Note implicit string concatenation.
              " [%(funcName)-10.10s]"
              "  %(message)s"
              )
    datefmt = "%Y-%m-%d %H:%M:%S"

    # Create the logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    ### Console Handler #####################################################
    handler = logging.StreamHandler()
    handler.setLevel(LOG_LEVEL_CONSOLE)
    formatter = logging.Formatter(logfmt, datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    ### File Handler ########################################################
    # Build the logfile path.
    dirname = os.path.dirname(os.path.abspath(__file__))
    rootpath = os.path.split(dirname)[0]
    logpath = os.path.join(rootpath, "log")
    logfile = os.path.join(logpath, "PyBank.log")

    # see Note #2
    if not os.path.isdir(logpath):
        rootpath = os.path.split(rootpath)[0]       # up one level
        logpath = os.path.join(rootpath, "log")

    logfile = os.path.join(logpath, "PyBank.log")

    rollover_time = datetime.time.min       # midnight
    handler = TRFHandler(logfile,
                         when="W6",         # Sunday
                         #interval=7,       # when=Sunday -> not needed
                         #backupCount=5,
                         atTime=rollover_time,
                         #delay=True,
                         )
    handler.setLevel(LOG_LEVEL_FILE)
    formatter = logging.Formatter(logfmt, datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


### Module Executions #######################################################
_setup_logging()