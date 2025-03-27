"""
Base API implementation for ActiveTrail SDK.

This module provides base classes that implement common API patterns
to promote code reuse and consistency across the SDK.
"""

from typing import Dict, Any, Optional, List, Union, TypeVar, Generic, Callable

T = TypeVar('T')


class BaseAPI:
    """Base class for all API implementations."""

    def __init__(self, client):
        """
        Initialize the API with a client.
        
        Args:
            client: The ActiveTrail client instance
        """
        self.client = client


class CrudAPI(BaseAPI):
    """
    Base class implementing CRUD operations for a resource.
    
    This class provides standard Create, Read, Update, Delete operations
    that are common across many API endpoints.
    """
    
    def __init__(self, client, resource_path: str):
        """
        Initialize the CRUD API with a client and resource path.
        
        Args:
            client: The ActiveTrail client instance
            resource_path: The base path for the resource (e.g., "contacts")
        """
        super().__init__(client)
        self.resource_path = resource_path
    
    def list(self, limit: int = 100, offset: int = 0, **kwargs) -> Dict[str, Any]:
        """
        Get a list of resources.
        
        Args:
            limit: Maximum number of resources to retrieve (default: 100)
            offset: Offset for pagination (default: 0)
            **kwargs: Additional filter parameters
            
        Returns:
            Dictionary containing resource data
        """
        params = {
            "limit": limit,
            "offset": offset,
            **kwargs
        }
        
        return self.client.get(self.resource_path, params=params)
    
    def get(self, resource_id: str) -> Dict[str, Any]:
        """
        Get information about a specific resource.
        
        Args:
            resource_id: The ID of the resource to retrieve
            
        Returns:
            Resource data
        """
        return self.client.get(f"{self.resource_path}/{resource_id}")
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new resource.
        
        Args:
            data: Resource data
            
        Returns:
            Created resource data
        """
        return self.client.post(self.resource_path, json=data)
    
    def update(self, resource_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing resource.
        
        Args:
            resource_id: The ID of the resource to update
            data: Updated resource data
            
        Returns:
            Updated resource data
        """
        return self.client.put(f"{self.resource_path}/{resource_id}", json=data)
    
    def delete(self, resource_id: str) -> Any:
        """
        Delete a resource.
        
        Args:
            resource_id: The ID of the resource to delete
            
        Returns:
            Response data
        """
        return self.client.delete(f"{self.resource_path}/{resource_id}")


class NestedResourceAPI(BaseAPI):
    """
    Base class for APIs that operate on nested resources.
    
    This is useful for resources that exist under a parent resource,
    such as contact groups or campaign events.
    """
    
    def __init__(self, client, parent_path: str, resource_path: str):
        """
        Initialize the nested resource API.
        
        Args:
            client: The ActiveTrail client instance
            parent_path: The parent resource path (e.g., "contacts")
            resource_path: The nested resource path (e.g., "groups")
        """
        super().__init__(client)
        self.parent_path = parent_path
        self.resource_path = resource_path
    
    def list(self, parent_id: str, limit: int = 100, offset: int = 0, **kwargs) -> Dict[str, Any]:
        """
        Get a list of nested resources for a parent.
        
        Args:
            parent_id: The ID of the parent resource
            limit: Maximum number of resources to retrieve (default: 100)
            offset: Offset for pagination (default: 0)
            **kwargs: Additional filter parameters
            
        Returns:
            Dictionary containing resource data
        """
        params = {
            "limit": limit,
            "offset": offset,
            **kwargs
        }
        
        return self.client.get(
            f"{self.parent_path}/{parent_id}/{self.resource_path}", 
            params=params
        )
    
    def get(self, parent_id: str, resource_id: str) -> Dict[str, Any]:
        """
        Get information about a specific nested resource.
        
        Args:
            parent_id: The ID of the parent resource
            resource_id: The ID of the nested resource to retrieve
            
        Returns:
            Resource data
        """
        return self.client.get(
            f"{self.parent_path}/{parent_id}/{self.resource_path}/{resource_id}"
        )
    
    def create(self, parent_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new nested resource.
        
        Args:
            parent_id: The ID of the parent resource
            data: Resource data
            
        Returns:
            Created resource data
        """
        return self.client.post(
            f"{self.parent_path}/{parent_id}/{self.resource_path}", 
            json=data
        )
    
    def update(self, parent_id: str, resource_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing nested resource.
        
        Args:
            parent_id: The ID of the parent resource
            resource_id: The ID of the nested resource to update
            data: Updated resource data
            
        Returns:
            Updated resource data
        """
        return self.client.put(
            f"{self.parent_path}/{parent_id}/{self.resource_path}/{resource_id}", 
            json=data
        )
    
    def delete(self, parent_id: str, resource_id: str) -> Any:
        """
        Delete a nested resource.
        
        Args:
            parent_id: The ID of the parent resource
            resource_id: The ID of the nested resource to delete
            
        Returns:
            Response data
        """
        return self.client.delete(
            f"{self.parent_path}/{parent_id}/{self.resource_path}/{resource_id}"
        )


class CampaignBaseAPI(CrudAPI):
    """
    Base class for campaign APIs.
    
    This class extends CrudAPI with additional operations specific to
    campaign management like scheduling, sending, and reporting.
    """
    
    def __init__(self, client, resource_path: str):
        """
        Initialize the Campaign API with a client and resource path.
        
        Args:
            client: The ActiveTrail client instance
            resource_path: The base path for the campaign resource
        """
        super().__init__(client, resource_path)
    
    def schedule(self, campaign_id: str, schedule_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule a campaign for delivery.
        
        Args:
            campaign_id: The ID of the campaign to schedule
            schedule_data: Scheduling information including:
                - send_time: Datetime for sending the campaign (ISO format)
                - time_zone: Time zone for the send_time
                
        Returns:
            Scheduling confirmation data
        """
        return self.client.post(
            f"{self.resource_path}/{campaign_id}/schedule", 
            json=schedule_data
        )
    
    def send_now(self, campaign_id: str) -> Dict[str, Any]:
        """
        Send a campaign immediately.
        
        Args:
            campaign_id: The ID of the campaign to send
                
        Returns:
            Response data
        """
        return self.client.post(f"{self.resource_path}/{campaign_id}/send")
    
    def get_statistics(self, campaign_id: str) -> Dict[str, Any]:
        """
        Get statistics for a specific campaign.
        
        Args:
            campaign_id: The ID of the campaign
                
        Returns:
            Campaign statistics
        """
        return self.client.get(f"{self.resource_path}/{campaign_id}/statistics")
    
    def clone(self, campaign_id: str, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a clone of an existing campaign.
        
        Args:
            campaign_id: The ID of the campaign to clone
            name: Optional new name for the cloned campaign
                
        Returns:
            Cloned campaign data
        """
        data = {}
        if name:
            data["name"] = name
            
        return self.client.post(f"{self.resource_path}/{campaign_id}/clone", json=data)