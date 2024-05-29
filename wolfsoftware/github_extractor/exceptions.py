"""
This module defines custom exceptions for handling various GitHub API errors, including missing tokens, authentication errors, and rate limit exceeded errors.

Exceptions:
- MissingTokenError: Raised when the GitHub API token is missing.
- AuthenticationError: Raised when authentication fails.
- RateLimitExceededError: Raised when the GitHub API rate limit is exceeded.
- RequestError: Raised for general request errors.
- RequestTimeoutError: Raised when a request times out.
- MissingOrgNameError: Raised when the organization name is missing.
- NotFoundError: Raised when a requested resource is not found.

Example usage:
    from .exceptions import (
        MissingTokenError,
        AuthenticationError,
        RateLimitExceededError,
        RequestError,
        RequestTimeoutError,
        MissingOrgNameError,
        NotFoundError
    )

    # Raise MissingTokenError if the token is missing
    if not token:
        raise MissingTokenError("GitHub API token is required.")

    # Raise AuthenticationError if authentication fails
    if not authenticated:
        raise AuthenticationError("Authentication failed.")

    # Raise RateLimitExceededError if the API rate limit is exceeded
    if rate_limit_exceeded:
        raise RateLimitExceededError("Rate limit exceeded.")

    # Raise RequestError for general request errors
    if request_error:
        raise RequestError("An error occurred with the request.")

    # Raise RequestTimeoutError if a request times out
    if timeout:
        raise RequestTimeoutError("Request timed out.")

    # Raise MissingOrgNameError if the organization name is missing
    if not org_name:
        raise MissingOrgNameError("Organization name is required.")

    # Raise NotFoundError if a requested resource is not found
    if resource_not_found:
        raise NotFoundError("Requested resource not found.")
"""


class MissingTokenError(Exception):
    """
    Custom exception for missing GitHub API token.

    This exception is intended to be used when an operation requires a GitHub API
    token, but it is not provided.

    Attributes:
        message (str): A human-readable string describing the exception.
    """

    def __init__(self, message: str = "GitHub API token is required") -> None:
        """
        Initialize the MissingTokenError instance.

        Arguments:
            message (str): A human-readable string describing the exception. Default is "GitHub API token is required."

        Example:
            raise MissingTokenError()
        """
        super().__init__(message)


class AuthenticationError(Exception):
    """
    Custom exception raised when authentication fails.

    This exception is intended to be used when an authentication process fails,
    such as when invalid credentials are provided to an API.

    Attributes:
        message (str): A human-readable string describing the exception.
    """

    def __init__(self, message: str = "Authentication failed: Bad credentials") -> None:
        """
        Initialize the AuthenticationError instance.

        Arguments:
            message (str): A human-readable string describing the exception.

        Example:
            raise AuthenticationError("Invalid API token")
        """
        super().__init__(message)


class RateLimitExceededError(Exception):
    """
    Custom exception raised when the GitHub API rate limit is exceeded.

    This exception is intended to be used when an operation fails because the
    GitHub API rate limit has been exceeded.

    Attributes:
        message (str): A human-readable string describing the exception.
    """

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        """
        Initialize the RateLimitExceededError instance.

        Arguments:
            message (str): A human-readable string describing the exception. Default is "Rate limit exceeded."

        Example:
            raise RateLimitExceededError()
        """
        super().__init__(message)


class RequestError(Exception):
    """
    Custom exception raised for general request errors.

    This exception is intended to be used when an operation fails due to a general
    request error, such as a network issue or invalid request.

    Attributes:
        message (str): A human-readable string describing the exception.
    """

    def __init__(self, message: str = "An error occurred with the request") -> None:
        """
        Initialize the RequestError instance.

        Arguments:
            message (str): A human-readable string describing the exception. Default is "An error occurred with the request."

        Example:
            raise RequestError()
        """
        super().__init__(message)


class RequestTimeoutError(Exception):
    """
    Custom exception raised when a request times out.

    This exception is intended to be used when an operation fails because a request
    to an external service has timed out.

    Attributes:
        message (str): A human-readable string describing the exception.
    """

    def __init__(self, message: str = "Request timed out") -> None:
        """
        Initialize the RequestTimeoutError instance.

        Arguments:
            message (str): A human-readable string describing the exception. Default is "Request timed out."

        Example:
            raise RequestTimeoutError()
        """
        super().__init__(message)


class MissingOrgNameError(Exception):
    """
    Custom exception for missing organization name.

    This exception is intended to be used when an operation requires the name
    of an organization, but it is not provided.

    Attributes:
        message (str): A human-readable string describing the exception.
    """

    def __init__(self, message: str = "Organization name is required") -> None:
        """
        Initialize the MissingOrgNameError instance.

        Arguments:
            message (str): A human-readable string describing the exception. Default is "Organization name is required."

        Example:
            raise MissingOrgNameError()
        """
        super().__init__(message)


class NotFoundError(Exception):
    """
    Custom exception for resource not found.

    This exception is intended to be used when a requested resource is not found.

    Attributes:
        message (str): A human-readable string describing the exception.
    """

    def __init__(self, message: str = "Requested resource not found") -> None:
        """
        Initialize the NotFoundError instance.

        Arguments:
            message (str): A human-readable string describing the exception. Default is "Requested resource not found."

        Example:
            raise NotFoundError()
        """
        super().__init__(message)
