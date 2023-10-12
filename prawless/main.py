from .core.logging_config import logger
from .core.base import AbstractHTTPClient
from .clients.reddit_client import RedditHTTPClient
from .entities.submission import Submission
from .entities.user.redditor import User
from .entities.subreddit.sub import Subreddit
from .iterators.submissions_iterator import UserSubmissionIterator
from prawless.entities.comment import Comment


class Reddit:
    """A class for interacting with the Reddit API."""
    def __init__(self, client: AbstractHTTPClient):
        self._client = client

    async def submission(self, id: str) -> 'Submission':
        url = f"/comments/{id}.json"
        logger.debug(f"Fetching submission data for ID: {id}")
        data = await self._client.get(url)
        submission_data = data[0]['data']['children'][0]['data']
        comment_data = data[1]['data']['children']
        submission = Submission(submission_data, self._client)
        submission.comments = [Comment(comment['data']) for comment in comment_data if comment['kind'] == 't1']
        return submission

    async def redditor(self, username: str) -> 'User':
        url = f"/user/{username}/about.json"
        logger.debug(f"Fetching user data for username: {username}")
        data = await self._client.get(url)
        return User(data['data'])

    async def subreddit(self, subreddit_name: str) -> 'Subreddit':
        url = f"/r/{subreddit_name}/about.json"
        logger.debug(f"Fetching subreddit data for subreddit name: {subreddit_name}")
        data = await self._client.get(url)
        return Subreddit(data['data'], self._client)  # Pass both data and client
    

    #placeholder for now, this should be inside the user class
    def user_submissions(self, username: str, limit: int = None):
        return UserSubmissionIterator(self._client, username, limit)
