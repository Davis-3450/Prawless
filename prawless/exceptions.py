class RedditWrapperException(Exception):
    """Base exception for the Reddit Wrapper."""


class HTTPException(RedditWrapperException):
    """Raised when an HTTP request fails."""


class RateLimitException(RedditWrapperException):
    """Raised when a rate limit is hit."""


class DataNotFoundException(RedditWrapperException):
    """Raised when expected data is not found in the response."""
