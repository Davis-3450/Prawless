#praw
from ..core.logging_config import logger
from ..entities.submission import Submission

class PrawlessIterator:
    """Base iterator for prawless."""

    def __init__(self, client):
        self._client = client
        self._current_data = None
        self._idx = 0
        self.after = None

    async def _fetch_data(self):
        """Fetches the next batch of data from Reddit."""
        raise NotImplementedError

    def __aiter__(self):
        return self

    async def __anext__(self):
        raise NotImplementedError

class BaseRedditDataIterator(PrawlessIterator):
    """Base iterator for Reddit data that involves pagination."""
    
    def __init__(self, client, limit=100):
        super().__init__(client)
        self.limit = limit
        self.fetched = 0

    async def _fetch_data(self):
        """Fetches the next batch of data from Reddit."""
        raise NotImplementedError

    async def __anext__(self):
        if self.fetched >= self.limit:
            raise StopAsyncIteration

        if not self._current_data or self._idx >= len(self._current_data):
            self._current_data = await self._fetch_data()
            self.after = self._current_data.get('after')
            self._idx = 0

            # If no more data is returned, stop the iteration
            if not self._current_data or not self._current_data.get('children'):
                raise StopAsyncIteration

        data = self._current_data['children'][self._idx]['data']
        self._idx += 1
        self.fetched += 1
        return self._parse_data(data)

    def _parse_data(self, data):
        """Parse the data into the desired object. By default, it returns raw data."""
        return data


class UserSubmissionIterator(BaseRedditDataIterator):
    """An iterator for submissions by a specific user."""

    def __init__(self, client, username, limit=None):
        super().__init__(client)
        self._username = username

    async def _fetch_data(self):
        """Fetches the next batch of submissions from Reddit."""
        batch_limit = min(self.limit - self.fetched, 100)
        url = f"/user/{self._username}/submitted.json?limit={batch_limit}"  # Ensure .json is appended here
        if self.after:
            url += f"&after={self.after}"
        return await self._client.get(url)

    def _parse_data(self, data):
        """Parse the submission data into a Submission object."""
        return Submission(data, client=self._client)


class SubredditSubmissionIterator(BaseRedditDataIterator):
    """An iterator for submissions from a specific subreddit."""

    def __init__(self, client, subreddit_name, listing_type='new', limit=None):
        super().__init__(client)
        self._subreddit_name = subreddit_name
        self._listing_type = listing_type

    async def _fetch_data(self):
        """Fetches the next batch of submissions from Reddit."""
        batch_limit = min(self.limit - self.fetched, 100)
        url = f"/r/{self._subreddit_name}/{self._listing_type}.json?limit={batch_limit}"  # Ensure .json is appended here
        if self.after:
            url += f"&after={self.after}"
        return await self._client.get(url)

    def _parse_data(self, data):
        """Parse the submission data into a Submission object."""
        return Submission(data, client=self._client)
