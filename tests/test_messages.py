"""
Tests for the Messages API module.
"""

import unittest
from unittest.mock import MagicMock, AsyncMock, patch

from active_trail.messages import MessagesAPI


class TestSyncMessagesAPI(unittest.TestCase):
    """Test cases for the synchronous MessagesAPI."""

    def setUp(self):
        """Set up test environment."""
        self.mock_client = MagicMock()
        self.messages_api = MessagesAPI(self.mock_client)
    
    def test_send_email(self):
        """Test sending a transactional email."""
        # Setup mock return value
        expected_result = {"status": "sent", "message_id": "abc123"}
        self.mock_client.post.return_value = expected_result
        
        # Email data
        email_data = {
            "subject": "Test Subject",
            "html_content": "<p>Test content</p>",
            "recipients": [{"email": "recipient@example.com", "name": "Test Recipient"}],
            "sender": {
                "email": "sender@example.com",
                "name": "Test Sender"
            }
        }
        
        # Call the method
        result = self.messages_api.send_email(email_data)
        
        # Verify the client was called correctly
        self.mock_client.post.assert_called_once_with("messages/email", json=email_data)
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_send_sms(self):
        """Test sending an SMS."""
        # Setup mock return value
        expected_result = {"status": "sent", "message_id": "sms123"}
        self.mock_client.post.return_value = expected_result
        
        # SMS data
        sms_data = {
            "message": "Test SMS message",
            "recipients": ["+1234567890", "+9876543210"],
            "sender_id": "TestCompany"
        }
        
        # Call the method
        result = self.messages_api.send_sms(sms_data)
        
        # Verify the client was called correctly
        self.mock_client.post.assert_called_once_with("messages/sms", json=sms_data)
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_get_status(self):
        """Test getting message status."""
        # Setup mock return value
        expected_result = {
            "status": "delivered",
            "delivery_time": "2023-07-15T14:30:00Z"
        }
        self.mock_client.get.return_value = expected_result
        
        # Call the method
        result = self.messages_api.get_status("msg123")
        
        # Verify the client was called correctly
        self.mock_client.get.assert_called_once_with("messages/msg123/status")
        
        # Verify the result
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main() 