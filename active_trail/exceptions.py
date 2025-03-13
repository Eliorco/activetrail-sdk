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