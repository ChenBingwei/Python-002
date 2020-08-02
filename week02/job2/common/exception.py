"""
Customized exceptions
"""

from selenium.common.exceptions import TimeoutException as selenium_TimeoutException


class BaseException(Exception):
    """An error occurred."""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message or self.__class__.__doc__


class SeleniumOperationError(BaseException):
    pass


class RequestsOperationError(BaseException):
    pass


class SeleniumTimeout(selenium_TimeoutException):
    pass
