from ..core.base import RedditObject, AbstractHTTPClient

class Submission(RedditObject):
    """A class representing a Reddit submission."""
    def __init__(self, data: dict, client: AbstractHTTPClient):
        super().__init__(data)
        self._client = client
        self.comments = []

    @property
    def title(self) -> str:
        return self._data['title']

    @property
    def author(self) -> str:
        return self._data.get('author', None)

    @property
    def score(self) -> int:
        return self._data.get('score', None)

    @property
    def url(self) -> str:
        return self._data.get('url', None)

    @property
    def selftext(self) -> str:
        return self._data.get('selftext', None)
