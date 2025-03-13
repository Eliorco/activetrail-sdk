"""
Tests for the Contacts API module.
"""

import unittest
from unittest.mock import MagicMock, AsyncMock, patch

from active_trail.contacts import ContactsAPI


class TestSyncContactsAPI(unittest.TestCase):
    """Test cases for the synchronous ContactsAPI."""

    def setUp(self):
        """Set up test environment."""
        self.mock_client = MagicMock()
        self.contacts_api = ContactsAPI(self.mock_client)
    
    def test_list(self):
        """Test getting contacts."""
        # Setup mock return value
        expected_result = {"contacts": [{"id": "1", "email": "test@example.com"}]}
        self.mock_client.get.return_value = expected_result
        
        # Call the method
        result = self.contacts_api.list(params={"limit": 10, "offset": 5})
        
        # Verify the client was called correctly
        self.mock_client.get.assert_called_once_with(
            "contacts", params={"limit": 10, "offset": 5}
        )
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_get(self):
        """Test getting a single contact."""
        # Setup mock return value
        expected_result = {"id": "123", "email": "contact@example.com"}
        self.mock_client.get.return_value = expected_result
        
        # Call the method
        result = self.contacts_api.get("123")
        
        # Verify the client was called correctly
        self.mock_client.get.assert_called_once_with("contacts/123")
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_create(self):
        """Test creating a contact."""
        # Setup mock return value
        expected_result = {"id": "123", "email": "new@example.com"}
        self.mock_client.post.return_value = expected_result
        
        # Contact data
        contact_data = {"email": "new@example.com", "first_name": "Test"}
        
        # Call the method
        result = self.contacts_api.create(contact_data)
        
        # Verify the client was called correctly
        self.mock_client.post.assert_called_once_with(
            "contacts", json=contact_data
        )
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_update(self):
        """Test updating a contact."""
        # Setup mock return value
        expected_result = {"id": "123", "email": "updated@example.com"}
        self.mock_client.put.return_value = expected_result
        
        # Contact data
        contact_data = {"email": "updated@example.com"}
        
        # Call the method
        result = self.contacts_api.update("123", contact_data)
        
        # Verify the client was called correctly
        self.mock_client.put.assert_called_once_with(
            "contacts/123", json=contact_data
        )
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_delete(self):
        """Test deleting a contact."""
        # Setup mock return value
        expected_result = {}
        self.mock_client.delete.return_value = expected_result
        
        # Call the method
        result = self.contacts_api.delete("123")
        
        # Verify the client was called correctly
        self.mock_client.delete.assert_called_once_with("contacts/123")
        
        # Verify the result
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main() 