#prawless/entities/subreddit/submissions.py
from ...core.base import RedditObject
from ...clients.reddit_client import RedditHTTPClient
from ...iterators.submissions_iterator import SubredditSubmissionIterator

class SubredditSubmissions(RedditObject):
    """Handles the logic related to submissions from a subreddit."""

    def __init__(self, subreddit_name, client: RedditHTTPClient):
        self._subreddit_name = subreddit_name
        self._client = client

    def submissions(self, listing_type='new', limit=None):
        """Generates an iterator for different types of submissions from the subreddit.

        Args:
            listing_type (str, optional): The type of listing to fetch. Defaults to 'new'.
            limit (int, optional): The maximum number of submissions to fetch. Defaults to None.

        Returns:
            SubmissionsIterator: An iterator for submissions.
        """
        return SubredditSubmissionIterator(client=self._client, subreddit_name=self._subreddit_name, listing_type=listing_type, limit=limit)

    async def new(self, limit=None):
        """Fetches new submissions from the subreddit."""
        async for submission in self.submissions('new', limit):
            yield submission

    async def hot(self, limit=None):
        """Fetches hot submissions from the subreddit."""
        async for submission in self.submissions('hot', limit):
            yield submission

    async def controversial(self, limit=None):
        """Fetches controversial submissions from the subreddit."""
        async for submission in self.submissions('controversial', limit):
            yield submission

    async def rising(self, limit=None):
        """Fetches rising submissions from the subreddit."""
        async for submission in self.submissions('rising', limit):
            yield submission

    def __aiter__(self):
        """Iterates over new submissions from the subreddit."""
        return self.new()
