"""
Tests for the base API implementations.
"""

import unittest
from unittest.mock import MagicMock

from active_trail.base_api import BaseAPI, CrudAPI, NestedResourceAPI, CampaignBaseAPI


class TestBaseAPI(unittest.TestCase):
    """Test cases for the BaseAPI class."""

    def setUp(self):
        """Set up test environment."""
        self.mock_client = MagicMock()
        self.base_api = BaseAPI(self.mock_client)
    
    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.base_api.client, self.mock_client)


class TestCrudAPI(unittest.TestCase):
    """Test cases for the CrudAPI class."""

    def setUp(self):
        """Set up test environment."""
        self.mock_client = MagicMock()
        self.resource_path = "test-resource"
        self.crud_api = CrudAPI(self.mock_client, self.resource_path)
    
    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.crud_api.client, self.mock_client)
        self.assertEqual(self.crud_api.resource_path, self.resource_path)
    
    def test_list(self):
        """Test list method."""
        # Set up mock return value
        self.mock_client.get.return_value = {"items": [{"id": "1"}, {"id": "2"}]}
        
        # Call the method
        result = self.crud_api.list(limit=10, offset=5, filter="test")
        
        # Verify method called correctly
        self.mock_client.get.assert_called_once_with(
            self.resource_path, 
            params={"limit": 10, "offset": 5, "filter": "test"}
        )
        
        # Verify result
        self.assertEqual(result, {"items": [{"id": "1"}, {"id": "2"}]})
    
    def test_get(self):
        """Test get method."""
        # Set up mock return value
        self.mock_client.get.return_value = {"id": "123", "name": "Test"}
        
        # Call the method
        result = self.crud_api.get("123")
        
        # Verify method called correctly
        self.mock_client.get.assert_called_once_with(f"{self.resource_path}/123")
        
        # Verify result
        self.assertEqual(result, {"id": "123", "name": "Test"})
    
    def test_create(self):
        """Test create method."""
        # Set up mock return value
        self.mock_client.post.return_value = {"id": "123", "name": "New Resource"}
        
        # Data to send
        data = {"name": "New Resource"}
        
        # Call the method
        result = self.crud_api.create(data)
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(self.resource_path, json=data)
        
        # Verify result
        self.assertEqual(result, {"id": "123", "name": "New Resource"})
    
    def test_update(self):
        """Test update method."""
        # Set up mock return value
        self.mock_client.put.return_value = {"id": "123", "name": "Updated Resource"}
        
        # Data to send
        data = {"name": "Updated Resource"}
        
        # Call the method
        result = self.crud_api.update("123", data)
        
        # Verify method called correctly
        self.mock_client.put.assert_called_once_with(f"{self.resource_path}/123", json=data)
        
        # Verify result
        self.assertEqual(result, {"id": "123", "name": "Updated Resource"})
    
    def test_delete(self):
        """Test delete method."""
        # Set up mock return value
        self.mock_client.delete.return_value = {}
        
        # Call the method
        result = self.crud_api.delete("123")
        
        # Verify method called correctly
        self.mock_client.delete.assert_called_once_with(f"{self.resource_path}/123")
        
        # Verify result
        self.assertEqual(result, {})


class TestNestedResourceAPI(unittest.TestCase):
    """Test cases for the NestedResourceAPI class."""

    def setUp(self):
        """Set up test environment."""
        self.mock_client = MagicMock()
        self.parent_path = "parent-resource"
        self.resource_path = "nested-resource"
        self.nested_api = NestedResourceAPI(
            self.mock_client, self.parent_path, self.resource_path
        )
    
    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.nested_api.client, self.mock_client)
        self.assertEqual(self.nested_api.parent_path, self.parent_path)
        self.assertEqual(self.nested_api.resource_path, self.resource_path)
    
    def test_list(self):
        """Test list method."""
        # Set up mock return value
        self.mock_client.get.return_value = {"items": [{"id": "1"}, {"id": "2"}]}
        
        # Call the method
        result = self.nested_api.list("parent-123", limit=10, offset=5, filter="test")
        
        # Verify method called correctly
        self.mock_client.get.assert_called_once_with(
            f"{self.parent_path}/parent-123/{self.resource_path}", 
            params={"limit": 10, "offset": 5, "filter": "test"}
        )
        
        # Verify result
        self.assertEqual(result, {"items": [{"id": "1"}, {"id": "2"}]})
    
    def test_get(self):
        """Test get method."""
        # Set up mock return value
        self.mock_client.get.return_value = {"id": "123", "name": "Test"}
        
        # Call the method
        result = self.nested_api.get("parent-123", "123")
        
        # Verify method called correctly
        self.mock_client.get.assert_called_once_with(
            f"{self.parent_path}/parent-123/{self.resource_path}/123"
        )
        
        # Verify result
        self.assertEqual(result, {"id": "123", "name": "Test"})
    
    def test_create(self):
        """Test create method."""
        # Set up mock return value
        self.mock_client.post.return_value = {"id": "123", "name": "New Resource"}
        
        # Data to send
        data = {"name": "New Resource"}
        
        # Call the method
        result = self.nested_api.create("parent-123", data)
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            f"{self.parent_path}/parent-123/{self.resource_path}", json=data
        )
        
        # Verify result
        self.assertEqual(result, {"id": "123", "name": "New Resource"})
    
    def test_update(self):
        """Test update method."""
        # Set up mock return value
        self.mock_client.put.return_value = {"id": "123", "name": "Updated Resource"}
        
        # Data to send
        data = {"name": "Updated Resource"}
        
        # Call the method
        result = self.nested_api.update("parent-123", "123", data)
        
        # Verify method called correctly
        self.mock_client.put.assert_called_once_with(
            f"{self.parent_path}/parent-123/{self.resource_path}/123", json=data
        )
        
        # Verify result
        self.assertEqual(result, {"id": "123", "name": "Updated Resource"})
    
    def test_delete(self):
        """Test delete method."""
        # Set up mock return value
        self.mock_client.delete.return_value = {}
        
        # Call the method
        result = self.nested_api.delete("parent-123", "123")
        
        # Verify method called correctly
        self.mock_client.delete.assert_called_once_with(
            f"{self.parent_path}/parent-123/{self.resource_path}/123"
        )
        
        # Verify result
        self.assertEqual(result, {})


class TestCampaignBaseAPI(unittest.TestCase):
    """Test cases for the CampaignBaseAPI class."""

    def setUp(self):
        """Set up test environment."""
        self.mock_client = MagicMock()
        self.resource_path = "campaigns"
        self.campaign_api = CampaignBaseAPI(self.mock_client, self.resource_path)
    
    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.campaign_api.client, self.mock_client)
        self.assertEqual(self.campaign_api.resource_path, self.resource_path)
    
    def test_schedule(self):
        """Test schedule method."""
        # Set up mock return value
        self.mock_client.post.return_value = {"status": "scheduled"}
        
        # Schedule data
        schedule_data = {
            "send_time": "2023-01-01T12:00:00Z",
            "time_zone": "UTC"
        }
        
        # Call the method
        result = self.campaign_api.schedule("123", schedule_data)
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            f"{self.resource_path}/123/schedule", json=schedule_data
        )
        
        # Verify result
        self.assertEqual(result, {"status": "scheduled"})
    
    def test_send_now(self):
        """Test send_now method."""
        # Set up mock return value
        self.mock_client.post.return_value = {"status": "sending"}
        
        # Call the method
        result = self.campaign_api.send_now("123")
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(f"{self.resource_path}/123/send")
        
        # Verify result
        self.assertEqual(result, {"status": "sending"})
    
    def test_get_statistics(self):
        """Test get_statistics method."""
        # Set up mock return value
        self.mock_client.get.return_value = {"sent": 100, "delivered": 95}
        
        # Call the method
        result = self.campaign_api.get_statistics("123")
        
        # Verify method called correctly
        self.mock_client.get.assert_called_once_with(f"{self.resource_path}/123/statistics")
        
        # Verify result
        self.assertEqual(result, {"sent": 100, "delivered": 95})
    
    def test_clone(self):
        """Test clone method."""
        # Set up mock return value
        self.mock_client.post.return_value = {"id": "456", "name": "Copy of Campaign"}
        
        # Call the method without name
        result = self.campaign_api.clone("123")
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            f"{self.resource_path}/123/clone", json={}
        )
        
        # Verify result
        self.assertEqual(result, {"id": "456", "name": "Copy of Campaign"})
        
        # Reset mock
        self.mock_client.post.reset_mock()
        
        # Call the method with name
        result = self.campaign_api.clone("123", name="New Name")
        
        # Verify method called correctly
        self.mock_client.post.assert_called_once_with(
            f"{self.resource_path}/123/clone", json={"name": "New Name"}
        )


if __name__ == "__main__":
    unittest.main() 