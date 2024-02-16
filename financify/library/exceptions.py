"""Custom Defined Exceptions"""


class CiError(Exception):
    """Parent Class for CI Exceptions"""


class PlatformException(Exception):
    """Parent Class for Platform Exceptions"""


class MemberException(Exception):
    """Parent class for class member exceptions"""


class InvalidOSException(PlatformException):
    """Raised when operating on an unsupported OS"""


class NoPropException(MemberException):
    """Raised when referencing a non-existent class prop"""
