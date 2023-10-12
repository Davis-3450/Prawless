#prawless/misc/random_usernames.py
from ..clients.reddit_client import RedditHTTPClient

async def generate_usernames() -> list:
    """Generates a list of usernames using the Reddit API.
    Returns:
        list: The response from the API, containing multiple users.
    """
    url = "/api/v1/generate_username.json"
    #Note: this endpoint in particular gives loads of rate limit errors.
    async def _wrapper():
        client = RedditHTTPClient()
        r = await client.get(endpoint=url)
        return r["usernames"]
    return await _wrapper()