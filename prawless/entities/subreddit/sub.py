#prawless/entities/subreddit/sub.py
from ...core.base import RedditObject
from .submissions import SubredditSubmissions
from ...clients.reddit_client import RedditHTTPClient
from .rules import SubredditRules

class Subreddit(RedditObject):
    """A class representing a Reddit subreddit.

    Attributes:
        ...
    """
    def __init__(self, data: dict, client: RedditHTTPClient):
        super().__init__(data)
        self._client = client

    # Properties
    @property
    def display_name(self) -> str:
        """str: The display name of the subreddit."""
        return self._data.get('display_name', None)

    @property
    def title(self) -> str:
        """str: The title of the subreddit."""
        return self._data.get('title', None)

    @property
    def subscribers(self) -> int:
        """int: The number of subscribers to the subreddit."""
        return self._data.get('subscribers', None)

    @property
    def created_utc(self) -> float:
        """float: The UTC timestamp of when the subreddit was created."""
        return self._data.get('created_utc', None)

    @property
    def user_flair_background_color(self) -> str:
        """str: The background color of user flairs in the subreddit."""
        return self._data.get('user_flair_background_color', None)

    @property
    def restrict_posting(self) -> bool:
        """bool: Whether posting is restricted in the subreddit."""
        return self._data.get('restrict_posting', False)

    @property
    def header_img(self) -> str:
        """str: The URL of the subreddit's header image."""
        return self._data.get('header_img', None)

    @property
    def icon_size(self) -> list:
        """list: The size of the subreddit's icon."""
        return self._data.get('icon_size', [])

    @property
    def primary_color(self) -> str:
        """str: The primary color of the subreddit."""
        return self._data.get('primary_color', None)

    @property
    def active_user_count(self) -> int:
        """int: The number of active users in the subreddit."""
        return self._data.get('active_user_count', None)

    @property
    def icon_img(self) -> str:
        """str: The URL of the subreddit's icon image."""
        return self._data.get('icon_img', None)

    @property
    def display_name_prefixed(self) -> str:
        """str: The display name of the subreddit with the prefix."""
        return self._data.get('display_name_prefixed', None)

    @property
    def accounts_active(self) -> int:
        """int: The number of active accounts in the subreddit."""
        return self._data.get('accounts_active', None)

    @property
    def public_traffic(self) -> bool:
        """bool: Whether the subreddit's traffic is public."""
        return self._data.get('public_traffic', False)

    @property
    def quarantine(self) -> bool:
        """bool: Whether the subreddit is quarantined."""
        return self._data.get('quarantine', False)

    @property
    def hide_ads(self) -> bool:
        """bool: Whether ads are hidden in the subreddit."""
        return self._data.get('hide_ads', False)

    @property
    def public_description(self) -> str:
        """str: The public description of the subreddit."""
        return self._data.get('public_description', None)

    @property
    def created(self) -> float:
        """float: The timestamp of when the subreddit was created."""
        return self._data.get('created', None)

    @property
    def wls(self) -> int:
        """int: The whitelist status of the subreddit."""
        return self._data.get('wls', None)

    @property
    def submission_type(self) -> str:
        """str: The type of submissions allowed in the subreddit."""
        return self._data.get('submission_type', None)

    @property
    def user_is_subscriber(self) -> bool:
        """bool: Whether the user is subscribed to the subreddit."""
        return self._data.get('user_is_subscriber', False)

    @property
    def subreddit_type(self) -> str:
        """str: The type of subreddit."""
        return self._data.get('subreddit_type', None)

    @property
    def banner_img(self) -> str:
        """str: The URL of the subreddit's banner image."""
        return self._data.get('banner_img', None)

    @property
    def over18(self) -> bool:
        """bool: Whether the subreddit is NSFW."""
        return self._data.get('over18', False)

    @property
    def header_title(self) -> str:
        """str: The title of the subreddit's header."""
        return self._data.get('header_title', None)

    @property
    def description(self) -> str:
        """str: The description of the subreddit."""
        return self._data.get('description', None)

    @property
    def url(self) -> str:
        """str: The URL of the subreddit."""
        return self._data.get('url', None)

    @property
    def banner_size(self) -> list:
        """list: The size of the subreddit's banner."""
        return self._data.get('banner_size', [])

    @property
    def mobile_banner_image(self) -> str:
        """str: The URL of the subreddit's mobile banner image."""
        return self._data.get('mobile_banner_image', None)
    
    @property
    async def rules(self) -> SubredditRules:
        """SubredditRules: The rules of the subreddit."""
        url = f"/r/{self.display_name}/about/rules.json"
        data = await self._client.get(url)
        return SubredditRules(data['rules'])
    

    @property
    async def rules(self) -> SubredditRules:
        """SubredditRules: The rules of the subreddit."""
        url = f"/r/{self.display_name}/about/rules.json"
        data = await self._client.get(url)
        return SubredditRules(data['rules'])
    
    # Delegate submissions methods to SubredditSubmissions
    def submissions(self, listing_type='new', limit=None):
        submissions_handler = SubredditSubmissions(subreddit_name=self.display_name, client=self._client)
        return submissions_handler.submissions(listing_type=listing_type, limit=limit)

    async def new(self, limit=None):
        submissions_handler = SubredditSubmissions(subreddit_name=self.display_name, client=self._client)
        async for submission in submissions_handler.new(limit):
            yield submission

    async def hot(self, limit=None):
        submissions_handler = SubredditSubmissions(subreddit_name=self.display_name, client=self._client)
        async for submission in submissions_handler.hot(limit):
            yield submission

    async def controversial(self, limit=None):
        submissions_handler = SubredditSubmissions(subreddit_name=self.display_name, client=self._client)
        async for submission in submissions_handler.controversial(limit):
            yield submission

    async def rising(self, limit=None):
        submissions_handler = SubredditSubmissions(subreddit_name=self.display_name, client=self._client)
        async for submission in submissions_handler.rising(limit):
            yield submission

    def __aiter__(self):
        submissions_handler = SubredditSubmissions(subreddit_name=self.display_name, client=self._client)
        return submissions_handler.__aiter__()