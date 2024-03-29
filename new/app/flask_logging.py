import os
import sys
from pathlib import Path
import logging
import logging.handlers
from logging import raiseExceptions
from logging import Logger


BASE_DIR = Path(__file__).resolve().parents[1]
LOG_PATH = os.path.join(BASE_DIR, 'logs')


class AppLogger(Logger):
    '''Custom logger
If the handler name is console it means that all logs greater than or equal to the set level are printed on the terminal
Other handlers record only the log equal to the setting level'''

    def __init__(self, name, level=logging.NOTSET):
        super(AppLogger, self).__init__(name, level)

    def callHandlers(self, record):
        """
        Pass a record to all relevant handlers.

        Loop through all handlers for this logger and its parents in the
        logger hierarchy. If no handler was found, output a one-off error
        message to sys.stderr. Stop searching up the hierarchy whenever a
        logger with the "propagate" attribute set to zero is found - that
        will be the last logger whose handlers are called.
        """
        c = self
        found = 0
        while c:
            for hdlr in c.handlers:
                found = found + 1
                if hdlr.name == 'console':
                    if record.levelno >= hdlr.level:
                        hdlr.handle(record)
                else:
                    if record.levelno == hdlr.level:
                        hdlr.handle(record)
            if not c.propagate:
                c = None  # break out
            else:
                c = c.parent
        if (found == 0) and raiseExceptions and not self.manager.emittedNoHandlerWarning:  # noqa
            sys.stderr.write("No handlers could be found for logger"
                            " \"%s\"\n" % self.name)
            self.manager.emittedNoHandlerWarning = 1


def get_logger(logfile_name=__name__, log_path=LOG_PATH):
    '''save log to diffrent file by deffirent log level into the log path
    and print all log in console'''
    logging.setLoggerClass(AppLogger)
    formatter = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')

    log_files = {
        logging.DEBUG: os.path.join(log_path,  'debug.log'),
        logging.INFO: os.path.join(log_path,  'info.log'),
        logging.WARNING: os.path.join(log_path, 'warning.log'),
        logging.ERROR: os.path.join(log_path,  'error.log'),
        logging.CRITICAL:
        os.path.join(log_path,  'critical.log')
    }
    # The logger is the same as flask by default
    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.DEBUG)
    for log_level, log_file in log_files.items():
        file_handler = logging.handlers.TimedRotatingFileHandler(log_file,
                                                                'midnight')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.name = "console"
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


logger = get_logger()

