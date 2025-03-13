"""
ActiveTrail core client implementation.
"""

import json
import logging
import requests
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional, Union
from urllib.parse import urljoin

from .exceptions import ActiveTrailError, AuthenticationError, RateLimitError
from .contacts import ContactsAPI
from .campaigns import CampaignsAPI
from .messages import MessagesAPI
from .webhooks import WebhooksAPI


logger = logging.getLogger(__name__)


class AsyncActiveTrailClient:
    """Asynchronous client for the ActiveTrail API."""

    BASE_URL = "https://webapi.mymarketing.co.il/api/"
    
    def __init__(self, api_key: str, timeout: int = 30, max_concurrent: int = 10):
        """
        Initialize the Async ActiveTrail client.
        
        Args:
            api_key: The API key for ActiveTrail service
            timeout: Request timeout in seconds
            max_concurrent: Maximum number of concurrent requests
        """
        self.api_key = api_key
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.session = None
        self._semaphore = None
        
    async def setup(self):
        """Set up the client session for async operations."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
            self.session.headers.update({
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            })
            self._semaphore = asyncio.Semaphore(self.max_concurrent)
    
    async def close(self):
        """Close the client session."""
        if self.session:
            await self.session.close()
            self.session = None
            
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None, 
        json: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Make an async request to the ActiveTrail API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint to call
            params: URL parameters
            json: Request payload
            
        Returns:
            Parsed JSON response
            
        Raises:
            ActiveTrailError: On API errors
            AuthenticationError: On auth failures
            RateLimitError: When rate limited
        """
        await self.setup()
        url = urljoin(self.BASE_URL, endpoint)
        
        logger.debug(f"Making async {method} request to {url}")
        
        async with self._semaphore:
            try:
                async with self.session.request(
                    method, url, params=params, json=json, timeout=self.timeout
                ) as response:
                    response.raise_for_status()
                    
                    if response.content_type == "application/json":
                        return await response.json()
                    return await response.text()
                    
            except aiohttp.ClientResponseError as e:
                status_code = e.status
                error_detail = ""
                
                if status_code == 401:
                    raise AuthenticationError(f"Authentication failed: {e.message}")
                elif status_code == 429:
                    raise RateLimitError("Rate limit exceeded")
                else:
                    raise ActiveTrailError(f"HTTP error {status_code}: {e.message}")
                    
            except aiohttp.ClientError as e:
                raise ActiveTrailError(f"Request failed: {str(e)}")
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request."""
        return await self._request("GET", endpoint, params=params)
    
    async def post(self, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Any:
        """Make a POST request."""
        return await self._request("POST", endpoint, params=params, json=json)
    
    async def put(self, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Any:
        """Make a PUT request."""
        return await self._request("PUT", endpoint, params=params, json=json)
    
    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Any:
        """Make a DELETE request."""
        return await self._request("DELETE", endpoint, params=params, json=json)


class ActiveTrailClient:
    """Main client for the ActiveTrail API."""

    BASE_URL = "https://webapi.mymarketing.co.il/api/"
    
    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize the ActiveTrail client.
        
        Args:
            api_key: The API key for ActiveTrail service
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        })
        
        # Initialize the async client
        self.async_client = AsyncActiveTrailClient(api_key, timeout)
        
        # Initialize API endpoints
        self.contacts = ContactsAPI(self)
        self.campaigns = CampaignsAPI(self)
        self.messages = MessagesAPI(self)
        self.webhooks = WebhooksAPI(self)
        
    def _run_async(self, coro):
        """Run an async coroutine in the sync client."""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()
            
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request."""
        return self._run_async(self.async_client.get(endpoint, params=params))
    
    def post(self, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Any:
        """Make a POST request."""
        return self._run_async(self.async_client.post(endpoint, params=params, json=json))
    
    def put(self, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Any:
        """Make a PUT request."""
        return self._run_async(self.async_client.put(endpoint, params=params, json=json))
    
    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Any:
        """Make a DELETE request."""
        return self._run_async(self.async_client.delete(endpoint, params=params, json=json))

    def request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None, 
        data: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Make a request to the ActiveTrail API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint to call
            params: URL parameters
            data: Request payload
            
        Returns:
            Parsed JSON response
            
        Raises:
            ActiveTrailError: On API errors
            AuthenticationError: On auth failures
            RateLimitError: When rate limited
        """
        url = urljoin(self.BASE_URL, endpoint)
        
        logger.debug(f"Making {method} request to {url}")
        
        try:
            if method == "GET":
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method == "POST":
                response = self.session.post(url, params=params, json=data, timeout=self.timeout)
            elif method == "PUT":
                response = self.session.put(url, params=params, json=data, timeout=self.timeout)
            elif method == "DELETE":
                response = self.session.delete(url, params=params, json=data, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            # Some endpoints might not return JSON
            if response.content and response.headers.get("Content-Type", "").startswith("application/json"):
                return response.json()
            return response.content
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_detail = ""
            
            try:
                error_content = e.response.json()
                error_detail = json.dumps(error_content)
            except (ValueError, json.JSONDecodeError):
                error_detail = e.response.text
            
            if status_code == 401:
                raise AuthenticationError(f"Authentication failed: {error_detail}")
            elif status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            else:
                raise ActiveTrailError(f"HTTP error {status_code}: {error_detail}")
                
        except requests.exceptions.RequestException as e:
            raise ActiveTrailError(f"Request failed: {str(e)}") 