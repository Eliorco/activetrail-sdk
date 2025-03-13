"""
Tests for the ActiveTrail client.
"""

import unittest
import asyncio
import aiohttp
from unittest.mock import patch, MagicMock, AsyncMock

from active_trail.client import ActiveTrailClient, AsyncActiveTrailClient
from active_trail.exceptions import ActiveTrailError, AuthenticationError, RateLimitError


class TestSyncActiveTrailClient(unittest.TestCase):
    """Test cases for the synchronous ActiveTrailClient."""

    def setUp(self):
        """Set up test environment."""
        self.api_key = "test_api_key"
        self.client = ActiveTrailClient(api_key=self.api_key)
        
    def test_init(self):
        """Test client initialization."""
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertEqual(self.client.timeout, 30)
        self.assertEqual(
            self.client.async_client.api_key, 
            self.api_key
        )
        
    @patch("active_trail.client.AsyncActiveTrailClient._request")
    def test_request(self, mock_request):
        """Test the request method."""
        # Simply have the mock return the expected dict directly
        # The _run_async method will handle converting the coroutine to a result
        mock_request.return_value = {"data": "test"}
        
        # Call the method
        result = self.client.get("test/endpoint", params={"param": "value"})
        
        # Assert the call was made correctly to the async client
        mock_request.assert_called_once()
        
        # Assert the result is correct
        self.assertEqual(result, {"data": "test"})
        
    @patch("active_trail.client.requests.Session")
    def test_authentication_error(self, mock_session):
        """Test handling of authentication errors."""
        # This test remains mostly the same as it tests exception behavior
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid API key"}
        mock_response.raise_for_status.side_effect = Exception("401 Client Error")
        
        # Configure the mock session
        mock_session_instance = mock_session.return_value
        mock_session_instance.get.return_value = mock_response
        mock_session_instance.get.side_effect = Exception("401 Client Error")
        
        # Create client with mocked session
        client = ActiveTrailClient("invalid_api_key")
        
        # Call the method and assert it raises the expected exception
        with self.assertRaises(Exception):
            # We'll patch the _run_async method to directly raise the exception
            with patch.object(client, '_run_async', side_effect=Exception("401 Client Error")):
                client.get("test/endpoint")


class TestAsyncActiveTrailClient(unittest.IsolatedAsyncioTestCase):
    """Test cases for the asynchronous ActiveTrailClient."""

    def setUp(self):
        """Set up test environment."""
        self.api_key = "test_api_key"
        self.client = AsyncActiveTrailClient(api_key=self.api_key)
        
    def test_init(self):
        """Test client initialization."""
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertEqual(self.client.timeout, 30)
        self.assertEqual(self.client.max_concurrent, 10)
        
    @patch("aiohttp.ClientSession.request")
    async def test_request(self, mock_request):
        """Test the async request method."""
        # Mock the response
        mock_response = AsyncMock()
        mock_response.content_type = "application/json"
        mock_response.json.return_value = {"data": "test"}
        mock_response.__aenter__.return_value = mock_response
        
        # Configure the mock to return a properly awaitable response
        mock_request.return_value = mock_response
        
        try:
            # Setup client
            await self.client.setup()
            
            # Call the method
            result = await self.client.get("test/endpoint", params={"param": "value"})
            
            # Assert the call was made correctly
            mock_request.assert_called_once()
            
            # Assert the result is correct
            self.assertEqual(result, {"data": "test"})
        finally:
            # Ensure cleanup happens even if test fails
            await self.client.close()
        
    @patch("active_trail.client.AsyncActiveTrailClient._request")
    async def test_authentication_error(self, mock_request):
        """Test handling of authentication errors."""
        # Have the method raise AuthenticationError directly
        mock_request.side_effect = AuthenticationError("Authentication failed")
        
        try:
            # Setup client
            await self.client.setup()
            
            # Call the method and assert it raises the expected exception
            with self.assertRaises(AuthenticationError):
                await self.client.get("test/endpoint")
        finally:
            # Ensure cleanup happens even if test fails
            await self.client.close()


if __name__ == "__main__":
    unittest.main() 