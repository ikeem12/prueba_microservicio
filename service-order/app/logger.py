import os
import logging
from logging.config import dictConfig

from flask import Flask

class MaxLevelFilter(logging.Filter):
    """Filter that allows log messages up to a specified maximum level.

    This is useful for directing lower-severity logs (e.g., INFO, DEBUG) to a specific handler
    while excluding higher-severity messages (e.g., ERROR)
    
    Attributes:
        max_level (int): The maximum log level to allow. Messages with a level higher than this will be filtered out.
    """
    def __init__(self, max_level: int):
        super().__init__()
        self.max_level = max_level

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter method to determine if a log record should be processed.
        Args:
            record (logging.LogRecord): The log record to evaluate.
        
        Returns:
            bool: True if the log record's level is less than or equal to max_level, False otherwise.
        """
        return record.levelno <= self.max_level

def setup_logging(app: Flask) -> logging.Logger:
    """
    Configures structured logging for the Flask application.

    This function sets up:
    - Console logging for real-time development feedback.
    - File-based logging with rotation:
        - `error_file.log`: stores ERROR and CRITICAL logs.
        - `info_file.log`: stores INFO and WARNING logs up to the specified max level.
    - Custom formatting and log separation by severity.
    - Automatic log directory creation.

    Features:
    - Traceability: Detailed logs include module, function, and line info.
    - Log rotation: Prevents uncontrolled growth of log files.
    - Level separation: Ensures clearer organization of log data.

    Args:
        app (Flask): Flask application instance used for logger naming.

    Returns:
        logging.Logger: The configured `app.logger`.

    Raises:
        OSError: If the log directory cannot be created.
    """
    
    LOG_DIR = 'logs'

    # create the log directory if it doesn't exist
    try:
        os.makedirs('logs', exist_ok=True)
    except OSError as e:
        # Basic logging configuration in case of an error creating the logs directory
        logging.basicConfig(level=logging.ERROR)
        logging.error(f"Error creating logs directory: {e}")
        raise

    # Configure the logging system
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'detailed': {
                'format': '%(asctime)s [%(levelname)s] [%(name)s] [%(module)s:%(funcName)s:%(lineno)d] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'filters': {
        'max_info_level': {
            '()': MaxLevelFilter,
            'max_level': logging.WARNING
        },
    },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'DEBUG',
                'stream': 'ext://sys.stdout',
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'detailed',
                'level': 'ERROR',
                'filename': os.path.join(LOG_DIR, 'error_file.log'),
                'maxBytes': 10000,
                'backupCount': 5
            },
            'info_file': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'standard',
                'level': 'INFO',    
                'filters': ['max_info_level'],
                'filename': os.path.join(LOG_DIR, 'info_file.log'),
                'when': 'midnight',
                'backupCount': 7
            },
        },
        'root': {
            'handlers': [],
            'level': 'WARNING',
        },
        'loggers': {
            f'{app.name}': {
                'handlers': ['console', 'error_file', 'info_file'],
                'level': 'DEBUG',
                'propagate': False
            },
            'werkzeug': {
                'handlers': [],
                'propagate': False
            },
        }
    })

    # return the app.logger cnfigured
    return app.logger