import sys
from logging import Logger
from typing import Callable, Any

class SafeInit:
    """
    A class to safely initialize components with error handling and logging.

    This class provides a method to initialize components, ensuring that any
    exceptions are logged and the application exits if initialization
    fails.
    """
    def __init__(self, *args: Any, init_fn: Callable[..., Any], name: str, app_logger: Logger) -> None:
        """
        Create a SafeInit instance and immediately run the initialization.

        Args:
            init_fn (Callable[..., Any]): The function or method used to initialize
                a component (e.g., db.init_app, migrate.init_app).
            args (tuple[Any, ...]): Positional arguments to pass to init_fn.
            name (str): Human-readable name of the component being initialized,
                used in log messages.
            app_logger (Logger): Logger used to record status and errors.
        """
        self._args = args
        self._init_fn = init_fn
        self._name = name
        self._app_logger = app_logger
        self._run()

    def _run(self) -> None:
        """
        Execute the initialization function and handle exceptions.

        On success, logs an INFO-level message. On failure, logs a CRITICAL-level
        message including the exception traceback and terminates the program.
        """
        try:
            self._init_fn(*self._args)
            self._app_logger.info("%s initialized successfully.", self._name)
        except Exception as e:
            self._app_logger.critical("Failed to initialize %s: %s", self._name, e, exc_info=True)
            sys.exit(1)