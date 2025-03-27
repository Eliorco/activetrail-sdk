"""
ActiveTrail core client implementation.
"""

import json
import logging
import requests
from typing import Dict, List, Any, Optional, Union
from urllib.parse import urljoin

from .exceptions import (
    ActiveTrailError, 
    AuthenticationError, 
    RateLimitError,
    ValidationError,
    NotFoundError,
    ServerError,
    NetworkError
)

logger = logging.getLogger(__name__)


class ActiveTrailClient:
    """
    Main client for the ActiveTrail API.
    
    This client provides synchronous access to the ActiveTrail API,
    following the official API documentation from webapi.mymarketing.co.il/api/docs.
    
    Example:
        ```python
        client = ActiveTrailClient(api_key="your_api_key")
        contacts = client.contacts.list(limit=10)
        ```
    """

    BASE_URL = "https://webapi.mymarketing.co.il/api/"
    
    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize the ActiveTrail client.
        
        Args:
            api_key: The API key for ActiveTrail service
            timeout: Request timeout in seconds
        
        Example:
            ```python
            client = ActiveTrailClient(api_key="your_api_key", timeout=60)
            ```
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{api_key}"
        })
        
        # Initialize API modules when they are first accessed
        self._contacts = None
        self._sms_campaigns = None
        self._groups = None
    
    @property
    def contacts(self):
        """Lazy-loaded Contacts API module."""
        if self._contacts is None:
            from .contacts import ContactsAPI
            self._contacts = ContactsAPI(self)
        return self._contacts
    
    @property
    def sms_campaigns(self):
        """Lazy-loaded SMS Campaigns API module."""
        if self._sms_campaigns is None:
            from .sms_campaigns import SMSCampaignsAPI
            self._sms_campaigns = SMSCampaignsAPI(self)
        return self._sms_campaigns
    
    @property
    def groups(self):
        """Lazy-loaded Groups API module."""
        if self._groups is None:
            from .groups import GroupsAPI
            self._groups = GroupsAPI(self)
        return self._groups
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a GET request to the ActiveTrail API.
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            
        Returns:
            Parsed JSON response
            
        Raises:
            ActiveTrailError: On API errors
            
        Example:
            ```python
            data = client.get("contacts", params={"limit": 10})
            ```
        """
        return self.request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a POST request to the ActiveTrail API.
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            json: JSON payload
            
        Returns:
            Parsed JSON response
            
        Raises:
            ActiveTrailError: On API errors
            
        Example:
            ```python
            data = client.post("contacts", json={"email": "example@example.com"})
            ```
        """
        return self.request("POST", endpoint, params=params, data=json)
    
    def put(self, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a PUT request to the ActiveTrail API.
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            json: JSON payload
            
        Returns:
            Parsed JSON response
            
        Raises:
            ActiveTrailError: On API errors
            
        Example:
            ```python
            data = client.put("contacts/123", json={"first_name": "John"})
            ```
        """
        return self.request("PUT", endpoint, params=params, data=json)
    
    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a DELETE request to the ActiveTrail API.
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            json: JSON payload
            
        Returns:
            Parsed JSON response
            
        Raises:
            ActiveTrailError: On API errors
            
        Example:
            ```python
            client.delete("contacts/123")
            ```
        """
        return self.request("DELETE", endpoint, params=params, data=json)

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
            ValidationError: When request validation fails
            NotFoundError: When resource not found
            ServerError: On server errors
            NetworkError: On network communication errors
            
        Example:
            ```python
            data = client.request("GET", "contacts", params={"limit": 10})
            ```
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
            
            if status_code == 400:
                raise ValidationError(f"Validation error: {error_detail}")
            elif status_code == 401:
                raise AuthenticationError(f"Authentication failed: {error_detail}")
            elif status_code == 404:
                raise NotFoundError(f"Resource not found: {error_detail}")
            elif status_code == 429:
                raise RateLimitError(f"Rate limit exceeded: {error_detail}")
            elif 500 <= status_code < 600:
                raise ServerError(f"Server error {status_code}: {error_detail}")
            else:
                raise ActiveTrailError(f"HTTP error {status_code}: {error_detail}")
                
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}") 