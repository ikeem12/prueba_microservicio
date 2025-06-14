from typing import Callable, Any

from app.exceptions.internal_exceptions import ComponentInitializationError

class InitializationComponent:
    """
    Initializes a component in a controlled way and catches errors during its configuration.

    This class receives an initialization function (`init_fn`) and its arguments, 
    executes it automatically upon instantiation and throws a custom exception 
    (`ComponentInitializationError`) if something goes wrong.

    Useful for initializing components such as databases, migrations or other critical 
    services on startup of a Flask application.

    Args:
        *args (Any): positional arguments to be passed to `init_fn`.
        init_fn (Callable[..., Any]): Function responsible for initializing the component.
        name (str): Component name (used in error messages for clarity).

    Raises:
        ComponentInitializationError: If `init_fn` throws an exception when executed.
    """
    def __init__(self, *args: Any, init_fn: Callable[..., None], name: str) -> None:
        self._args = args
        self._init_fn = init_fn
        self._name = name
        self._run()

    def _run(self) -> None:
        """
        Executes the initialization function with the provided arguments.

        If an error occurs during execution of `init_fn`, it throws `ComponentInitializationError`
        with a contextualized message.
        """
        try:
            self._init_fn(*self._args)
        except Exception as e:
            raise ComponentInitializationError(f"Failed to initialize {self._name}: {e}")