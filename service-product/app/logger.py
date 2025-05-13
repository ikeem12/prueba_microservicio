import os
import logging
from logging.config import dictConfig

from flask import Flask

class MaxLevelFilter(logging.Filter):
    """**Custom filter to limit log messages to a maximum level.**

    This filter allows only log messages that are less than or equal to the specified level.
    It is used to control the verbosity of log messages in the logging system.

    Args:
        max_level (int): The maximum log level allowed. Messages with a higher level will be filtered out.
    """

    def __init__(self, level: int):
        super().__init__()
        self.max_level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno <= self.max_level


def configure_logging(app: Flask) -> logging.Logger:
    """
    Configure the system logging for the Flask application.

    This function use `dictConfig`for configuring the logging system for the Flask application.
    Three handlers (console, error_file, info_file) and two formatters (“standard” and “detailed”) 
    are created to handle different levels of logs and formats. (“standard” and “detailed”) 
    to handle different log levels and formats.

    **The design allows**:
    - Traceability: Detailed logs include information such as module, function and line.
    - Level separation: Error logs are stored in a separate file from informational logs.
    - Log rotation: Log files are automatically rotated to avoid uncontrolled growth.

    In addition, it ensures that the log directory exists before configuring the handlers.

    Args:
        app(Flask): Flask application instance to attach the configured logger.

    Returns:
        logging.Logger: The `app.logger` after applying dictConfig.

    Raises:
        OSError: If log directory cannot be created.
    """
    
    # create the log directory if it doesn't exist
    try:
        os.makedirs('logs', exist_ok=True)
    except OSError as e:
        # Basic logging configuration in case of an error creating the logs directory
        logging.basicConfig(level=logging.ERROR)
        logging.error(f"Error creating logs directory: {e}")
        raise

    LOG_DIR = 'logs'

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
        # Definimos el filtro con nivel máximo WARNING (30)
        'max_info_level': {
            '()': MaxLevelFilter,
            'level': logging.WARNING
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