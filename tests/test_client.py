"""
Tests for the ActiveTrail client class.
"""

import unittest
from unittest.mock import patch, MagicMock, call

import requests

from active_trail.client import ActiveTrailClient
from active_trail.exceptions import (
    ActiveTrailError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    ServerError,
    NetworkError
)


class TestActiveTrailClient(unittest.TestCase):
    """Test cases for the ActiveTrailClient class."""

    def setUp(self):
        """Set up test environment."""
        self.api_key = "test_api_key"
        self.client = ActiveTrailClient(api_key=self.api_key)
    
    def test_initialization(self):
        """Test client initialization."""
        client = ActiveTrailClient(api_key=self.api_key, timeout=60)
        
        self.assertEqual(client.api_key, self.api_key)
        self.assertEqual(client.timeout, 60)
        self.assertEqual(client.BASE_URL, "https://webapi.mymarketing.co.il/api/")
        self.assertEqual(client.session.headers["Authorization"], self.api_key)
        self.assertEqual(client.session.headers["Content-Type"], "application/json")
        self.assertEqual(client.session.headers["Accept"], "application/json")
    
    @patch("requests.Session.get")
    def test_get_request(self, mock_get):
        """Test get method."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test_data"}
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.content = b'{"data": "test_data"}'
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get("contacts", params={"limit": 10})
        
        # Verify method called correctly
        mock_get.assert_called_once_with(
            "https://webapi.mymarketing.co.il/api/contacts",
            params={"limit": 10},
            timeout=30
        )
        
        # Verify result
        self.assertEqual(result, {"data": "test_data"})
    
    @patch("requests.Session.post")
    def test_post_request(self, mock_post):
        """Test post method."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123"}
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.content = b'{"id": "123"}'
        mock_post.return_value = mock_response
        
        # Call the method
        result = self.client.post("contacts", json={"email": "test@example.com"})
        
        # Verify method called correctly
        mock_post.assert_called_once_with(
            "https://webapi.mymarketing.co.il/api/contacts",
            params=None,
            json={"email": "test@example.com"},
            timeout=30
        )
        
        # Verify result
        self.assertEqual(result, {"id": "123"})
    
    @patch("requests.Session.put")
    def test_put_request(self, mock_put):
        """Test put method."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123", "updated": True}
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.content = b'{"id": "123", "updated": true}'
        mock_put.return_value = mock_response
        
        # Call the method
        result = self.client.put("contacts/123", json={"first_name": "John"})
        
        # Verify method called correctly
        mock_put.assert_called_once_with(
            "https://webapi.mymarketing.co.il/api/contacts/123",
            params=None,
            json={"first_name": "John"},
            timeout=30
        )
        
        # Verify result
        self.assertEqual(result, {"id": "123", "updated": True})
    
    @patch("requests.Session.delete")
    def test_delete_request(self, mock_delete):
        """Test delete method."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.content = b'{"success": true}'
        mock_delete.return_value = mock_response
        
        # Call the method
        result = self.client.delete("contacts/123")
        
        # Verify method called correctly
        mock_delete.assert_called_once_with(
            "https://webapi.mymarketing.co.il/api/contacts/123",
            params=None,
            json=None,
            timeout=30
        )
        
        # Verify result
        self.assertEqual(result, {"success": True})
    
    @patch("requests.Session.get")
    def test_non_json_response(self, mock_get):
        """Test handling of non-JSON response."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.content = b"Success"
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get("export/123")
        
        # Verify result
        self.assertEqual(result, b"Success")
    
    @patch("requests.Session.get")
    def test_empty_response(self, mock_get):
        """Test handling of empty response."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.content = b""
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get("some-endpoint")
        
        # Verify result
        self.assertEqual(result, b"")
    
    @patch("requests.Session.get")
    def test_validation_error(self, mock_get):
        """Test validation error handling."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Invalid parameter"}
        mock_response.text = '{"error": "Invalid parameter"}'
        
        # Set up side effect to raise HTTPError
        http_error = requests.exceptions.HTTPError()
        http_error.response = mock_response
        mock_get.side_effect = http_error
        
        # Call the method and check for exception
        with self.assertRaises(ValidationError) as context:
            self.client.get("contacts", params={"invalid": "value"})
        
        self.assertIn("Validation error", str(context.exception))
        self.assertIn("Invalid parameter", str(context.exception))
    
    @patch("requests.Session.get")
    def test_authentication_error(self, mock_get):
        """Test authentication error handling."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid API key"}
        mock_response.text = '{"error": "Invalid API key"}'
        
        # Set up side effect to raise HTTPError
        http_error = requests.exceptions.HTTPError()
        http_error.response = mock_response
        mock_get.side_effect = http_error
        
        # Call the method and check for exception
        with self.assertRaises(AuthenticationError) as context:
            self.client.get("contacts")
        
        self.assertIn("Authentication failed", str(context.exception))
        self.assertIn("Invalid API key", str(context.exception))
    
    @patch("requests.Session.get")
    def test_not_found_error(self, mock_get):
        """Test not found error handling."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Resource not found"}
        mock_response.text = '{"error": "Resource not found"}'
        
        # Set up side effect to raise HTTPError
        http_error = requests.exceptions.HTTPError()
        http_error.response = mock_response
        mock_get.side_effect = http_error
        
        # Call the method and check for exception
        with self.assertRaises(NotFoundError) as context:
            self.client.get("contacts/999")
        
        self.assertIn("Resource not found", str(context.exception))
    
    @patch("requests.Session.get")
    def test_rate_limit_error(self, mock_get):
        """Test rate limit error handling."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"error": "Too many requests"}
        mock_response.text = '{"error": "Too many requests"}'
        
        # Set up side effect to raise HTTPError
        http_error = requests.exceptions.HTTPError()
        http_error.response = mock_response
        mock_get.side_effect = http_error
        
        # Call the method and check for exception
        with self.assertRaises(RateLimitError) as context:
            self.client.get("contacts")
        
        self.assertIn("Rate limit exceeded", str(context.exception))
        self.assertIn("Too many requests", str(context.exception))
    
    @patch("requests.Session.get")
    def test_server_error(self, mock_get):
        """Test server error handling."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal server error"}
        mock_response.text = '{"error": "Internal server error"}'
        
        # Set up side effect to raise HTTPError
        http_error = requests.exceptions.HTTPError()
        http_error.response = mock_response
        mock_get.side_effect = http_error
        
        # Call the method and check for exception
        with self.assertRaises(ServerError) as context:
            self.client.get("contacts")
        
        self.assertIn("Server error 500", str(context.exception))
        self.assertIn("Internal server error", str(context.exception))
    
    @patch("requests.Session.get")
    def test_network_error(self, mock_get):
        """Test network error handling."""
        # Set up side effect to raise ConnectionError
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        # Call the method and check for exception
        with self.assertRaises(NetworkError) as context:
            self.client.get("contacts")
        
        self.assertIn("Network error", str(context.exception))
        self.assertIn("Connection refused", str(context.exception))
    
    @patch("requests.Session.get")
    def test_http_error_with_non_json_response(self, mock_get):
        """Test HTTP error with non-JSON response."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "Invalid request"
        
        # Set up side effect to raise HTTPError
        http_error = requests.exceptions.HTTPError()
        http_error.response = mock_response
        mock_get.side_effect = http_error
        
        # Call the method and check for exception
        with self.assertRaises(ValidationError) as context:
            self.client.get("contacts")
        
        self.assertIn("Validation error", str(context.exception))
        self.assertIn("Invalid request", str(context.exception))
    
    def test_lazy_loading_contacts(self):
        """Test lazy loading of contacts API."""
        with patch("active_trail.client.ContactsAPI") as mock_contacts_api:
            # First access should initialize the module
            contacts = self.client.contacts
            mock_contacts_api.assert_called_once_with(self.client)
            
            # Second access should return the cached instance
            contacts = self.client.contacts
            # Assert it was only initialized once
            mock_contacts_api.assert_called_once()
    
    def test_lazy_loading_campaigns(self):
        """Test lazy loading of campaigns API."""
        with patch("active_trail.client.CampaignsAPI") as mock_campaigns_api:
            # First access should initialize the module
            campaigns = self.client.campaigns
            mock_campaigns_api.assert_called_once_with(self.client)
            
            # Second access should return the cached instance
            campaigns = self.client.campaigns
            # Assert it was only initialized once
            mock_campaigns_api.assert_called_once()
    
    def test_lazy_loading_messages(self):
        """Test lazy loading of messages API."""
        with patch("active_trail.client.MessagesAPI") as mock_messages_api:
            # First access should initialize the module
            messages = self.client.messages
            mock_messages_api.assert_called_once_with(self.client)
            
            # Second access should return the cached instance
            messages = self.client.messages
            # Assert it was only initialized once
            mock_messages_api.assert_called_once()
    
    def test_lazy_loading_webhooks(self):
        """Test lazy loading of webhooks API."""
        with patch("active_trail.client.WebhooksAPI") as mock_webhooks_api:
            # First access should initialize the module
            webhooks = self.client.webhooks
            mock_webhooks_api.assert_called_once_with(self.client)
            
            # Second access should return the cached instance
            webhooks = self.client.webhooks
            # Assert it was only initialized once
            mock_webhooks_api.assert_called_once()
    
    def test_lazy_loading_sms_campaigns(self):
        """Test lazy loading of SMS campaigns API."""
        with patch("active_trail.client.SMSCampaignsAPI") as mock_sms_campaigns_api:
            # First access should initialize the module
            sms_campaigns = self.client.sms_campaigns
            mock_sms_campaigns_api.assert_called_once_with(self.client)
            
            # Second access should return the cached instance
            sms_campaigns = self.client.sms_campaigns
            # Assert it was only initialized once
            mock_sms_campaigns_api.assert_called_once()
    
    def test_lazy_loading_email_campaigns(self):
        """Test lazy loading of email campaigns API."""
        with patch("active_trail.client.EmailCampaignsAPI") as mock_email_campaigns_api:
            # First access should initialize the module
            email_campaigns = self.client.email_campaigns
            mock_email_campaigns_api.assert_called_once_with(self.client)
            
            # Second access should return the cached instance
            email_campaigns = self.client.email_campaigns
            # Assert it was only initialized once
            mock_email_campaigns_api.assert_called_once()
    
    def test_lazy_loading_operational_messages(self):
        """Test lazy loading of operational messages API."""
        with patch("active_trail.client.OperationalMessagesAPI") as mock_operational_messages_api:
            # First access should initialize the module
            operational_messages = self.client.operational_messages
            mock_operational_messages_api.assert_called_once_with(self.client)
            
            # Second access should return the cached instance
            operational_messages = self.client.operational_messages
            # Assert it was only initialized once
            mock_operational_messages_api.assert_called_once()
    
    def test_lazy_loading_groups(self):
        """Test lazy loading of groups API."""
        with patch("active_trail.client.GroupsAPI") as mock_groups_api:
            # First access should initialize the module
            groups = self.client.groups
            mock_groups_api.assert_called_once_with(self.client)
            
            # Second access should return the cached instance
            groups = self.client.groups
            # Assert it was only initialized once
            mock_groups_api.assert_called_once()
    
    def test_lazy_loading_two_way_sms(self):
        """Test lazy loading of two-way SMS API."""
        with patch("active_trail.client.TwoWaySmsAPI") as mock_two_way_sms_api:
            # First access should initialize the module
            two_way_sms = self.client.two_way_sms
            mock_two_way_sms_api.assert_called_once_with(self.client)
            
            # Second access should return the cached instance
            two_way_sms = self.client.two_way_sms
            # Assert it was only initialized once
            mock_two_way_sms_api.assert_called_once()
    
    def test_lazy_loading_sms_reports(self):
        """Test lazy loading of SMS reports API."""
        with patch("active_trail.client.SmsReportsAPI") as mock_sms_reports_api:
            # First access should initialize the module
            sms_reports = self.client.sms_reports
            mock_sms_reports_api.assert_called_once_with(self.client)
            
            # Second access should return the cached instance
            sms_reports = self.client.sms_reports
            # Assert it was only initialized once
            mock_sms_reports_api.assert_called_once()


if __name__ == "__main__":
    unittest.main() 