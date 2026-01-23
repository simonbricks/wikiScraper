# file with custom Exceptions to help understand and debug wrong code


class ArgValidationError(Exception):
    """Raised when the command-line arguments are invalid."""
    pass


class PageValidationError(Exception):
    """
    Raised when the input wiki search phrase 
    doesn't have an existing wikipage.
    """
    pass


class HTMLFileError(Exception):
    """
    Raised when the local HTML file with wiki page contents
    is empty, missing or when there are more then one file
    when the scraper is asked to scrape it.
    """
    pass
