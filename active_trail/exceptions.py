"""
Exception classes for the ActiveTrail SDK.
"""


class ActiveTrailError(Exception):
    """Base exception for all ActiveTrail errors."""
    pass


class AuthenticationError(ActiveTrailError):
    """Exception raised when authentication fails."""
    pass


class RateLimitError(ActiveTrailError):
    """Exception raised when the API rate limit is exceeded."""
    pass


class ValidationError(ActiveTrailError):
    """Exception raised when the API rejects the request due to validation errors."""
    pass


class NotFoundError(ActiveTrailError):
    """Exception raised when a requested resource is not found."""
    pass


class ServerError(ActiveTrailError):
    """Exception raised when the API server encounters an error."""
    pass


class NetworkError(ActiveTrailError):
    """Exception raised when there's a network communication error."""
    pass 