from typing import Callable, Any

from .exceptions import ComponentInitializationError

class SafeInit:
    """
    Utility class to perform safe, one-off initialization of application components.

    Executes a provided initialization function with its arguments during construction.
    If the initialization fails, it raises a ComponentInitializationError with context.

    This class delegates error handling to the caller, making it suitable for use in
    controlled startup sequences (e.g., inside `create_app` functions).

    Attributes:
        _args (tuple): Positional arguments for the initialization function.
        _init_fn (Callable): The initialization function (e.g., db.init_app).
        _name (str): Human-readable name of the component, for error messages.
    """
    def __init__(self, *args: Any, init_fn: Callable[..., Any], name: str):
        self._args = args
        self._init_fn = init_fn
        self._name = name
        self._run()

    def _run(self) -> None:
        """
        Executes the initialization logic.

        Calls the provided function with its arguments. If an exception occurs,
        it wraps it in a ComponentInitializationError with the component name.
        """
        try:
            self._init_fn(*self._args)
        except Exception as e:
            raise ComponentInitializationError(f"Failed to initialize {self._name}: {e}")