class RedditWrapperException(Exception):
    """Base exception for the Reddit Wrapper."""

class HTTPException(RedditWrapperException):
    """Raised when an HTTP request fails."""

class DataNotFoundException(RedditWrapperException):
    """Raised when expected data is not found in the response."""

class RateLimitException(RedditWrapperException):
    """Raised when the rate limit is exceeded."""

class BannedException(RedditWrapperException):
    """Raised when the user is banned from the subreddit."""
