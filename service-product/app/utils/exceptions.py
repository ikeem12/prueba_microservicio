class AppInitializationError(Exception):
    """"Exception raised when the application fails to initialize properly."""
    pass

class ComponentInitializationError(Exception):
    """Exception raised when a component fails to initialize."""
    pass
