from typing import Callable, Any

from app.exceptions.internal_exceptions import ComponentInitializationError

class InitializationComponent:
    """
    Utility class to handle initalization of components.

    Executes a provided initialization function with its arguments during construction.
    If the initialization fails, it raises a ComponentInitializationError with context.

    This class delegates error handling to the caller, making it suitable for use in
    controlled startup sequences (e.g., inside `create_app` functions).

    Attributes:
        _args (tuple): Positional arguments for the initialization function.
        _init_fn (Callable): The initialization function (e.g., db.init_app).
        _name (str): Human-readable name of the component, for error messages.

    methods:
        _run() -> None: Executes the initialization function with the provided arguments.
    """
    def __init__(self, *args: Any, init_fn: Callable[..., Any], name: str):
        self._args = args
        self._init_fn = init_fn
        self._name = name
        self._run()

    def _run(self) -> None:
        try:
            self._init_fn(*self._args)
        except Exception as e:
            raise ComponentInitializationError(f"Failed to initialize {self._name}: {e}")