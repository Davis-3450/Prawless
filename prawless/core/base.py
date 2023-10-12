from abc import ABC, abstractmethod

class AbstractHTTPClient(ABC):
    """An abstract base class for HTTP clients."""

    @abstractmethod
    async def get(self, endpoint: str, params: dict = None) -> dict:
        pass

class RedditObject:
    """A base class for Reddit objects."""

    def __init__(self, data: dict):
        self._data = data
