"""
Tests for the Groups API module.
"""

import unittest
from unittest.mock import MagicMock

from active_trail.groups import GroupsAPI
from active_trail.dto.groups import GroupDTO


class TestGroupsAPI(unittest.TestCase):
    """Test cases for the GroupsAPI class."""

    #region Setup
    def setUp(self):
        """Set up test environment."""
        self.mock_client = MagicMock()
        self.groups_api = GroupsAPI(self.mock_client)
    #endregion
    
    #region List Operations
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
    #endregion
    
    #region Get Operations
    def test_get(self):
        """Test get method."""
        # Set up mock return value based on the API documentation
        expected_result = {
            "id": 123,
            "name": "Test Group",
            "active_counter": 3,
            "counter": 4,
            "created": "2016-12-24T14:12:12",
            "last_generated": "2016-12-24T14:12:12"
        }
        self.mock_client.get.return_value = expected_result
        
        # Call the method
        result = self.groups_api.get(123)
        
        # Verify method called correctly
        self.mock_client.get.assert_called_once_with("groups/123")
        
        # Verify result
        self.assertEqual(result, expected_result)
    #endregion
    
    #region Create Operations
    def test_create_with_name_only(self):
        """Test create method with name only."""
        # Set up mock return value
        expected_result = {"id": 123, "name": "New Group"}
        self.mock_client.post.return_value = expected_result
        
        # Create GroupDTO object
        group = GroupDTO(name="New Group")
        
        # Call the method
        result = self.groups_api.create(group)
        
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
        expected_result = {"id": 123, "name": "New Group", "description": "A test group"}
        self.mock_client.post.return_value = expected_result
        
        # Create GroupDTO object
        group = GroupDTO(name="New Group", description="A test group")
        
        # Call the method
        result = self.groups_api.create(group)
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            "groups", 
            json={"name": "New Group", "description": "A test group"}
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
    #endregion
    
    #region Update Operations
    def test_update_name_only(self):
        """Test update method with name only."""
        # Set up mock return value
        expected_result = {"id": 123, "name": "Updated Group"}
        self.mock_client.put.return_value = expected_result
        
        # Create GroupDTO object
        group = GroupDTO(name="Updated Group")
        
        # Call the method
        result = self.groups_api.update(123, group)
        
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
        expected_result = {"id": 123, "description": "Updated description"}
        self.mock_client.put.return_value = expected_result
        
        # Create GroupDTO object with only description
        group = GroupDTO(name="", description="Updated description")
        
        # Call the method
        result = self.groups_api.update(123, group)
        
        # Verify method called correctly
        self.mock_client.put.assert_called_once_with(
            "groups/123", 
            json={"name": "", "description": "Updated description"}
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
    #endregion
    
    #region Delete Operations
    def test_delete(self):
        """Test delete method."""
        # Set up mock return value
        expected_result = {}
        self.mock_client.delete.return_value = expected_result
        
        # Call the method
        result = self.groups_api.delete(123)
        
        # Verify method called correctly
        self.mock_client.delete.assert_called_once_with("groups/123")
        
        # Verify result
        self.assertEqual(result, expected_result)
    #endregion
    
    #region Contact Operations
    def test_get_members(self):
        """Test get_members method."""
        # Set up mock return value according to API docs
        expected_result = {
            "count": 2,
            "contacts": [
                {
                    "id": 1, 
                    "state": "Active", 
                    "is_optined": True, 
                    "sms": "+972501234567",
                    "first_name": "John", 
                    "last_name": "Doe"
                },
                {
                    "id": 2, 
                    "state": "Unsubscribed", 
                    "is_optined": False, 
                    "sms": "+972541234567",
                    "first_name": "Jane", 
                    "last_name": "Smith"
                }
            ]
        }
        self.mock_client.get.return_value = expected_result
        
        # Call the method with available filter parameters according to docs
        result = self.groups_api.get_members(
            123,
            customer_states=["Active", "Unsubscribed"],
            search_term="+97250",
            from_date="2023-01-01",
            to_date="2023-12-31",
            page=1,
            limit=10
        )
        
        # Verify method called correctly with the right endpoint and parameters
        self.mock_client.get.assert_called_once_with(
            "groups/123/members", 
            params={
                "CustomerStates": ["Active", "Unsubscribed"],
                "SearchTerm": "+97250",
                "FromDate": "2023-01-01",
                "ToDate": "2023-12-31",
                "Page": 1,
                "Limit": 10
            }
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
    
    def test_get_contacts(self):
        """Test get_contacts method."""
        # Set up mock return value
        expected_result = {"contacts": [{"id": 1, "sms": "+972501234567"}, {"id": 2, "sms": "+972541234567"}]}
        self.mock_client.get.return_value = expected_result
        
        # Call the method
        result = self.groups_api.get_contacts(123, limit=10, offset=5)
        
        # Verify method called correctly
        self.mock_client.get.assert_called_once_with(
            "groups/123/contacts", 
            params={"groupId": 123, "limit": 10, "offset": 5}
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
    
    def test_add_contact(self):
        """Test add_contact method."""
        # Set up mock return value
        expected_result = {
            "id": 1,
            "state": "Active",
            "is_optined": True,
            "sms": "+972501234567",
            "first_name": "John",
            "last_name": "Doe"
        }
        self.mock_client.post.return_value = expected_result
        
        # Call the method with default status
        result = self.groups_api.add_contact(
            group_id=123,
            sms="+972501234567",
            first_name="John",
            last_name="Doe",
            status="Active"
        )
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            "groups/123/members",
            json={
                "sms": "+972501234567",
                "first_name": "John",
                "last_name": "Doe",
                "status": "Active"
            }
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
        
        # Reset mock
        self.mock_client.post.reset_mock()
        
        # Call the method with custom status
        result = self.groups_api.add_contact(
            group_id=123,
            sms="+972501234567",
            first_name="John",
            last_name="Doe",
            status="Unsubscribed"
        )
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            "groups/123/members",
            json={
                "sms": "+972501234567",
                "first_name": "John",
                "last_name": "Doe",
                "status": "Unsubscribed"
            }
        )
    
    def test_remove_contact(self):
        """Test remove_contact_from_group method."""
        # Set up mock return value
        expected_result = {}
        self.mock_client.delete.return_value = expected_result
        
        # Call the method
        result = self.groups_api.remove_contact_from_group(123, 456)
        
        # Verify method called correctly
        self.mock_client.delete.assert_called_once_with("groups/123/members/456")
        
        # Verify result
        self.assertEqual(result, expected_result)
    #endregion
    
    #region Batch Contact Operations
    def test_add_multiple_contacts(self):
        """Test add_multiple_contacts method."""
        # Set up mock return value
        expected_result = {
            "id": 1,
            "state": "Active",
            "is_optined": True,
            "sms": "+972501234567",
            "first_name": "John",
            "last_name": "Doe"
        }
        self.mock_client.post.return_value = expected_result
        
        # Contact numbers to add
        contacts = [
            {
                "sms": "+972501234567",
                "first_name": "John",
                "last_name": "Doe"
            },
            {
                "sms": "+972541234567",
                "first_name": "Jane",
                "last_name": "Smith"
            }
        ]
        
        # Call the method with default status
        result = self.groups_api.add_multiple_contacts(123, contacts)
        
        # Verify method called correctly for each contact
        self.assertEqual(self.mock_client.post.call_count, 2)
        
        # Verify first call
        self.mock_client.post.assert_any_call(
            "groups/123/members",
            json={
                "sms": "+972501234567",
                "first_name": "John",
                "last_name": "Doe",
                "status": "active"
            }
        )
        
        # Verify second call
        self.mock_client.post.assert_any_call(
            "groups/123/members",
            json={
                "sms": "+972541234567",
                "first_name": "Jane",
                "last_name": "Smith",
                "status": "active"
            }
        )
        
        # Verify result
        self.assertTrue(result)
        
        # Reset mock
        self.mock_client.post.reset_mock()
        
        # Call the method with custom status
        result = self.groups_api.add_multiple_contacts(123, contacts, status="unsubscribed")
        
        # Verify method called correctly for each contact
        self.assertEqual(self.mock_client.post.call_count, 2)
        
        # Verify first call
        self.mock_client.post.assert_any_call(
            "groups/123/members",
            json={
                "sms": "+972501234567",
                "first_name": "John",
                "last_name": "Doe",
                "status": "unsubscribed"
            }
        )
        
        # Verify second call
        self.mock_client.post.assert_any_call(
            "groups/123/members",
            json={
                "sms": "+972541234567",
                "first_name": "Jane",
                "last_name": "Smith",
                "status": "unsubscribed"
            }
        )
    
    def test_remove_multiple_contacts(self):
        """Test remove_multiple_contacts method."""
        # Set up mock return value
        expected_result = {}
        self.mock_client.delete.return_value = expected_result
        
        # Contact IDs to remove
        contacts = [
            {"id": 456, "sms": "+972501234567"},
            {"id": 789, "sms": "+972541234567"}
        ]
        
        # Call the method
        result = self.groups_api.remove_multiple_contacts(123, contacts)
        
        # Verify method called correctly for each contact
        self.assertEqual(self.mock_client.delete.call_count, 2)
        
        # Verify first call
        self.mock_client.delete.assert_any_call("groups/123/members/456")
        
        # Verify second call
        self.mock_client.delete.assert_any_call("groups/123/members/789")
        
        # Verify result
        self.assertTrue(result)
    #endregion


if __name__ == "__main__":
    unittest.main() 