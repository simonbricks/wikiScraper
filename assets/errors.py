# file with custom Exceptions to help understand and debug wrong code


class ArgValidationError(Exception):
    """Raised when the command-line arguments are invalid."""
    pass
