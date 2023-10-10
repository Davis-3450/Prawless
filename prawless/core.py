import httpx
from typing import List, Dict, Any, Generator
from fake_useragent import UserAgent
# Custom Exceptions
class RedditWrapperException(Exception):
    """Base exception for the Reddit Wrapper."""

class HTTPException(RedditWrapperException):
    """Raised when an HTTP request fails."""

class RateLimitException(RedditWrapperException):
    """Raised when a rate limit is hit."""

class DataNotFoundException(RedditWrapperException):
    """Raised when expected data is not found in the response."""

class ForbiddenResourceError(RedditWrapperException):
    """Raised when a resource is forbidden (HTTP 403)."""
    pass


# Base Reddit Object
class RedditObject:
    BASE_URL: str = 'https://www.reddit.com'
    ua = UserAgent()


    def __init__(self, data: Dict[str, Any]):
        self._data = data
        self.ua = UserAgent()

    @property
    def json_data(self) -> Dict[str, Any]:
        return self._data

    @staticmethod
    def request_json(url: str, retries: int = 3, timeout: int = 30) -> Dict[str, Any]:
        for _ in range(retries):
            with httpx.Client(headers={'User-Agent': RedditObject.ua.random}, timeout=timeout) as client:
                response = client.get(url)
                if response.status_code == 429:  # Rate Limiting
                    raise RateLimitException("Rate limit exceeded!")
                elif response.status_code != 200:
                    raise HTTPException(f"HTTP request failed with status {response.status_code}")
                json_data = response.json()
                if "data" not in json_data:
                    raise DataNotFoundException("Expected 'data' key not found in the response.")
                return json_data
        raise HTTPException("Maximum retries exceeded.")


# Main Reddit class
class Reddit:
    def submission(self, id: str) -> 'Submission':
        url = f"{RedditObject.BASE_URL}/r/all/comments/{id}/about.json"
        data = RedditObject.request_json(url)
        return Submission(data['data'])

    def redditor(self, username: str) -> 'User':
        url = f"{RedditObject.BASE_URL}/user/{username}/about.json"
        data = RedditObject.request_json(url)
        return User(data['data'])

    def subreddit(self, subreddit_name: str) -> 'Subreddit':
        return Subreddit(subreddit_name)

# Submission Model
class Submission(RedditObject):
    @property
    def title(self) -> str:
        return self.json_data['title']

    @property
    def author(self) -> str:
        return self.json_data['author']

    @property
    def score(self) -> int:
        return self.json_data['score']

    @property
    def num_comments(self) -> int:
        return self.json_data['num_comments']

    @property
    def subreddit(self) -> str:
        return self.json_data['subreddit']

    @property
    def url(self) -> str:
        return self.json_data['url']

    @property
    def selftext(self) -> str:
        return self.json_data['selftext']

# User Model
class User(RedditObject):
    @property
    def link_karma(self) -> int:
        return self.json_data['link_karma']

    @property
    def comment_karma(self) -> int:
        return self.json_data['comment_karma']

    @property
    def created_utc(self) -> float:
        return self.json_data['created_utc']

    @property
    def name(self) -> str:
        return self.json_data['name']

    @property
    def is_suspended(self) -> bool:
        return self.json_data.get('is_suspended', False)


    def submissions(self, sort_by: str = 'new', limit: int = 100) -> Generator['Submission', None, None]:
        assert sort_by in ['new', 'hot', 'top'], "Invalid sort type. Must be 'new', 'hot', or 'top'."
        yield from self._fetch_posts(sort_by, limit)

    def _fetch_posts(self, sort_by: str, limit: int) -> Generator['Submission', None, None]:
        url = f"{self.BASE_URL}/user/{self.name}/submitted/{sort_by}.json?limit={limit}"
        data = self.request_json(url)
        for post_data in data['data']['children']:
            yield Submission(post_data['data'])


# Subreddit Model
class Subreddit(RedditObject):
    @property
    def display_name(self) -> str:
        return self.json_data['display_name']

    def __init__(self, subreddit_name: str):
        self.subreddit_name = subreddit_name

    def top(self, time_filter: str = 'all', limit: int = 1000) -> Generator['Submission', None, None]:
        yield from self._fetch_submissions('top', time_filter, limit)

    def new(self, limit: int = 1000) -> Generator['Submission', None, None]:
        yield from self._fetch_submissions('new', 'all', limit)

    def controversial(self, time_filter: str = 'all', limit: int = 1000) -> Generator['Submission', None, None]:
        yield from self._fetch_submissions('controversial', time_filter, limit)

    def rising(self, limit: int = 1000) -> Generator['Submission', None, None]:
        yield from self._fetch_submissions('rising', 'all', limit)

    def _fetch_submissions(self, submission_type: str, time_filter: str, limit: int) -> Generator['Submission', None, None]:
        url = f"{self.BASE_URL}/r/{self.subreddit_name}/{submission_type}.json?limit={limit}&t={time_filter}"
        data = self.request_json(url)
        for post in data['data']['children']:
            yield Submission(post['data'])
