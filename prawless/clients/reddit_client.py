# prawless/clients/reddit_client.py
import logging
import httpx
import json

logger = logging.getLogger(__name__)

class RedditHTTPClient:
    """An HTTP client for interacting with the Reddit API."""

    BASE_URL = "https://www.reddit.com"
    USER_AGENT = "prawless:v0.1 (by /u/user)" # TODO: implement random user agents,  this is just a placeholder for now.

    def __init__(self, proxy: dict = None):
        """
        Initializes a RedditHTTPClient instance.

        Args:
            proxy (dict, optional): A dictionary containing proxy settings.
        """
        self.headers = {
            'User-Agent': self.USER_AGENT
        }
        self.proxy = proxy
            
        #TODO -> add proxies | priority: low
        #TODO -> implement random user agents | priority: medium
        #TODO -> implement rate limiting handling | priority: high
        #TODO -> implement retry logic | priority: high 
        #TODO -> implement logging (debug, info, warning, error, critical) | priority: medium
        #TODO -> implement Exception handling | priority: high
        

    async def get(self, endpoint: str, params: dict = None) -> dict:
        """
        Sends an HTTP GET request to a specified endpoint.

        Args:
            endpoint (str): The API endpoint to request.
            params (dict, optional): Query parameters for the request.

        Returns:
            dict: The JSON response from the GET request.
        """
        url = f"{self.BASE_URL}{endpoint}"
        logger.debug(f"Fetching URL: {url} with params: {params}")
        async with httpx.AsyncClient(headers=self.headers, proxies=self.proxy) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            content = response.text
            content = content.replace("&lt;", "<")
            content = content.replace("&gt;", ">")
            content = content.replace("&amp;", "&")
            return json.loads(content)
