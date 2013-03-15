# -*- coding: utf-8 -*-


class UCGError(Exception):
    """Base class for exceptions in UCG module."""
    def __init__(self, api_error_msg):
        self.api_error_msg = api_error_msg

    def __str__(self):
        if not self.api_error_msg:
            return "Exception occurred."
        else:
            return self.api_error_msg


class NetworkError(UCGError):
    """Raised if there are network problems, like timeout."""


class AuthenticationError(UCGError):
    """Raised when authentication error occurs."""


class InternalError(UCGError):
    """Raised when unexpected error occurs on the
    API server when processing a request."""


class SpinError(UCGError):
    """Raised when spinning article."""


class UnknownError(UCGError):
    """Raised when API call results in an unrecognized error."""


class QuotaError(UCGError):
    """Raised when there is no more credits."""


class QueueError(UCGError):
    """Raised when there are errors with queue id."""


class ArgumentError(UCGError):
    """Raised when there are errors with arguments."""


class ProcessError(UCGError):
    """Server could not process."""


class NotReadyError(UCGError):
    """Server did not process text yet."""


class NotImplementedError(UCGError):
    """Function is not implemented."""
