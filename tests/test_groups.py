"""
Tests for the Groups API module.
"""

import unittest
from unittest.mock import MagicMock

from active_trail.groups import GroupsAPI


class TestGroupsAPI(unittest.TestCase):
    """Test cases for the GroupsAPI class."""

    def setUp(self):
        """Set up test environment."""
        self.mock_client = MagicMock()
        self.groups_api = GroupsAPI(self.mock_client)
    
    def test_list(self):
        """Test list method."""
        # Set up mock return value
        expected_result = {"groups": [{"id": "1", "name": "Group 1"}, {"id": "2", "name": "Group 2"}]}
        self.mock_client.get.return_value = expected_result
        
        # Call the method
        result = self.groups_api.list(limit=10, offset=5, search="test")
        
        # Verify method called correctly
        self.mock_client.get.assert_called_once_with(
            "groups", 
            params={"limit": 10, "offset": 5, "search": "test"}
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
    
    def test_get(self):
        """Test get method."""
        # Set up mock return value
        expected_result = {"id": "123", "name": "Test Group", "member_count": 5}
        self.mock_client.get.return_value = expected_result
        
        # Call the method
        result = self.groups_api.get("123")
        
        # Verify method called correctly
        self.mock_client.get.assert_called_once_with("groups/123")
        
        # Verify result
        self.assertEqual(result, expected_result)
    
    def test_create_with_name_only(self):
        """Test create method with name only."""
        # Set up mock return value
        expected_result = {"id": "123", "name": "New Group"}
        self.mock_client.post.return_value = expected_result
        
        # Call the method
        result = self.groups_api.create("New Group")
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            "groups", 
            json={"name": "New Group"}
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
    
    def test_create_with_description(self):
        """Test create method with name and description."""
        # Set up mock return value
        expected_result = {"id": "123", "name": "New Group", "description": "A test group"}
        self.mock_client.post.return_value = expected_result
        
        # Call the method
        result = self.groups_api.create("New Group", "A test group")
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            "groups", 
            json={"name": "New Group", "description": "A test group"}
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
    
    def test_update_name_only(self):
        """Test update method with name only."""
        # Set up mock return value
        expected_result = {"id": "123", "name": "Updated Group"}
        self.mock_client.put.return_value = expected_result
        
        # Call the method
        result = self.groups_api.update("123", name="Updated Group")
        
        # Verify method called correctly
        self.mock_client.put.assert_called_once_with(
            "groups/123", 
            json={"name": "Updated Group"}
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
    
    def test_update_description_only(self):
        """Test update method with description only."""
        # Set up mock return value
        expected_result = {"id": "123", "description": "Updated description"}
        self.mock_client.put.return_value = expected_result
        
        # Call the method
        result = self.groups_api.update("123", description="Updated description")
        
        # Verify method called correctly
        self.mock_client.put.assert_called_once_with(
            "groups/123", 
            json={"description": "Updated description"}
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
    
    def test_delete(self):
        """Test delete method."""
        # Set up mock return value
        expected_result = {}
        self.mock_client.delete.return_value = expected_result
        
        # Call the method
        result = self.groups_api.delete("123")
        
        # Verify method called correctly
        self.mock_client.delete.assert_called_once_with("groups/123")
        
        # Verify result
        self.assertEqual(result, expected_result)
    
    def test_get_contacts(self):
        """Test get_contacts method."""
        # Set up mock return value
        expected_result = {"contacts": [{"id": "1", "email": "test1@example.com"}, {"id": "2", "email": "test2@example.com"}]}
        self.mock_client.get.return_value = expected_result
        
        # Call the method
        result = self.groups_api.get_contacts("123", limit=10, offset=5)
        
        # Verify method called correctly
        self.mock_client.get.assert_called_once_with(
            "groups/123/contacts", 
            params={"limit": 10, "offset": 5}
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
    
    def test_add_contact(self):
        """Test add_contact method."""
        # Set up mock return value
        expected_result = {"status": "success"}
        self.mock_client.post.return_value = expected_result
        
        # Call the method with default status
        result = self.groups_api.add_contact("123", "456")
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            "groups/123/contacts/456", 
            json={"status": "active"}
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
        
        # Reset mock
        self.mock_client.post.reset_mock()
        
        # Call the method with custom status
        result = self.groups_api.add_contact("123", "456", status="unsubscribed")
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            "groups/123/contacts/456", 
            json={"status": "unsubscribed"}
        )
    
    def test_remove_contact(self):
        """Test remove_contact method."""
        # Set up mock return value
        expected_result = {}
        self.mock_client.delete.return_value = expected_result
        
        # Call the method
        result = self.groups_api.remove_contact("123", "456")
        
        # Verify method called correctly
        self.mock_client.delete.assert_called_once_with("groups/123/contacts/456")
        
        # Verify result
        self.assertEqual(result, expected_result)
    
    def test_add_multiple_contacts(self):
        """Test add_multiple_contacts method."""
        # Set up mock return value
        expected_result = {"status": "success", "processed": 2}
        self.mock_client.post.return_value = expected_result
        
        # Contact IDs to add
        contact_ids = ["456", "789"]
        
        # Call the method with default status
        result = self.groups_api.add_multiple_contacts("123", contact_ids)
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            "groups/123/contacts/batch", 
            json={"contact_ids": contact_ids, "status": "active"}
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
        
        # Reset mock
        self.mock_client.post.reset_mock()
        
        # Call the method with custom status
        result = self.groups_api.add_multiple_contacts("123", contact_ids, status="unsubscribed")
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            "groups/123/contacts/batch", 
            json={"contact_ids": contact_ids, "status": "unsubscribed"}
        )
    
    def test_remove_multiple_contacts(self):
        """Test remove_multiple_contacts method."""
        # Set up mock return value
        expected_result = {"status": "success", "processed": 2}
        self.mock_client.delete.return_value = expected_result
        
        # Contact IDs to remove
        contact_ids = ["456", "789"]
        
        # Call the method
        result = self.groups_api.remove_multiple_contacts("123", contact_ids)
        
        # Verify method called correctly
        self.mock_client.delete.assert_called_once_with(
            "groups/123/contacts/batch", 
            json={"contact_ids": contact_ids}
        )
        
        # Verify result
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main() 