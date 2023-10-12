from ...core.base import RedditObject

class User(RedditObject):
    """A class representing a Reddit user."""
    @property
    def name(self) -> str:
        return self._data['name']

    @property
    def link_karma(self) -> int:
        return self._data.get('link_karma', None)

    @property
    def comment_karma(self) -> int:
        return self._data.get('comment_karma', None)

    @property
    def created_utc(self) -> float:
        return self._data.get('created_utc', None)

    @property
    def is_suspended(self) -> bool:
        return self._data.get('is_suspended', False)
