class AppInitializationError(Exception):
    """
    Exception thrown when the application cannot initialize correctly.

    Generally thrown when the environment configuration (APP_SETTINGS) is invalid
    or critical information is missing to start the Flask application.
    """
    pass

class ComponentInitializationError(Exception):
    """
    Exception thrown when a critical component (e.g. database or migrations)
    cannot be initialized correctly.

    It is thrown within the `InitializationComponent` process.
    """
    pass

class BlueprintRegistrationError(Exception):
    """
    Exception thrown when an error occurs when registering a Flask blueprint.

    For example, it may be due to a failed import, dependency error, or internal error
    during path registration.
    """
    pass