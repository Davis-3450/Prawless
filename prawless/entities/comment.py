from ..core.base import RedditObject

class Comment(RedditObject):
    """A class representing a Reddit comment."""
    def __init__(self, data: dict):
        super().__init__(data)
        self.replies = self._parse_replies()

    @property
    def author(self) -> str:
        return self._data.get('author', None)

    @property
    def body(self) -> str:
        return self._data.get('body', None)

    @property
    def score(self) -> int:
        return self._data.get('score', None)

    def _parse_replies(self) -> list:
        replies_data = self._data.get('replies', {})
        if isinstance(replies_data, str):
            return []
        replies_data = replies_data.get('data', {}).get('children', [])
        return [Comment(reply['data']) for reply in replies_data if reply['kind'] == 't1']
