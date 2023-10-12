import logging
import httpx
import json
import asyncio
from fake_useragent import UserAgent
from ..core.exceptions import RedditWrapperException, HTTPException, DataNotFoundException, RateLimitException, EntityBannedException

logger = logging.getLogger(__name__)

class RedditHTTPClient:
    """An HTTP client for interacting with the Reddit API."""

    BASE_URL = "https://www.reddit.com"

    def __init__(self, proxy: dict = None):
        """
        Initializes a RedditHTTPClient instance.

        Args:
            proxy (dict, optional): A dictionary containing proxy settings.
        """
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random
        }
        self.proxy = proxy

    async def get(self, endpoint: str, params: dict = None, retries=3) -> dict:
        """
        Sends an HTTP GET request to a specified endpoint.

        Args:
            endpoint (str): The API endpoint to request.
            params (dict, optional): Query parameters for the request.
            retries (int, optional): Number of retries before giving up.

        Returns:
            dict: The JSON response from the GET request.
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        for i in range(retries):
            logger.debug(f"Fetching URL: {url} with params: {params} and User-Agent: {self.headers['User-Agent']}")
            
            async with httpx.AsyncClient(headers=self.headers, proxies=self.proxy) as client:
                try:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    content = response.text
                    content = content.replace("&lt;", "<")
                    content = content.replace("&gt;", ">")
                    content = content.replace("&amp;", "&")
                    return json.loads(content)

                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 429:  # HTTP 429 Too Many Requests
                        # Rotate the user agent and retry once immediately
                        self.headers['User-Agent'] = self.ua.random
                        logger.warning(f"Rate limit reached. Rotating User-Agent to: {self.headers['User-Agent']}.")
                        
                        # Now try again with the new User-Agent
                        try:
                            response = await client.get(url, params=params)
                            response.raise_for_status()
                            content = response.text
                            content = content.replace("&lt;", "<")
                            content = content.replace("&gt;", ">")
                            content = content.replace("&amp;", "&")
                            return json.loads(content)

                        except httpx.HTTPStatusError as e2:
                            # If still rate-limited, use the 'x-ratelimit-reset' header to determine how long to wait
                            retry_after = e2.response.headers.get('x-ratelimit-reset', 60)  # Default to 60 seconds if not present
                            logger.warning(f"Rate limit reached again even after rotating User-Agent. Waiting for {retry_after} seconds.")
                            await asyncio.sleep(int(retry_after))
                    else:
                        raise HTTPException(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")

                except Exception as e:
                    raise RedditWrapperException(f"Unexpected error occurred: {str(e)}")

        # If all retries have been exhausted
        raise RedditWrapperException("Max retries exhausted for GET request.")
