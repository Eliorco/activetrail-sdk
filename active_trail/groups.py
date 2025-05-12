"""
ActiveTrail Groups API implementation.
"""

from typing import Dict, Any, Optional, List, Union
from .base_api import CrudAPI
from .dto.groups import (
    GroupDTO,
    GroupResponseDTO,
    GroupListRequestDTO,
    GroupContactDTO,
    GroupContactsRequestDTO,
    GroupAddContactDTO,
    GroupAddMultipleContactsDTO,
    GroupRemoveContactDTO,
    GroupRemoveMultipleContactsDTO
)


class GroupsAPI(CrudAPI):
    """Groups API handling for ActiveTrail."""

    def __init__(self, client):
        """
        Initialize the Groups API.
        
        Args:
            client: The ActiveTrail client instance
        """
        super().__init__(client, "groups")
    
    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get a list of contact groups.
        
        Args:
            limit: Maximum number of groups to retrieve
            offset: Offset for pagination
            search: Optional search query to filter groups by name
            
        Returns:
            Dictionary containing groups data
        """
        request = GroupListRequestDTO(
            limit=limit,
            offset=offset
        )
        
        params = request.to_dict()
        if search:
            params["search"] = search
            
        return self.client.get(self.resource_path, params=params)
    
    def get(self, group_id: int) -> Dict[str, Any]:
        """
        Get information about a specific group.
        
        Args:
            group_id: The ID of the group to retrieve
            
        Returns:
            Group data including name, description, and member count
        """
        return self.client.get(f"{self.resource_path}/{group_id}")
    
    def create(self, group: Union[GroupDTO, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a new contact group.
        
        Args:
            group: GroupDTO object or dictionary with group data
                Required fields: name
                Optional fields: description
            
        Returns:
            Created group data
        """
        if isinstance(group, GroupDTO):
            group_data = group.to_dict()
        else:
            group_data = group
            
        return self.client.post(self.resource_path, json=group_data)
    
    def update(
        self,
        group_id: int,
        group: Union[GroupDTO, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Update an existing contact group.
        
        Args:
            group_id: The ID of the group to update
            group: GroupDTO object or dictionary with updated group data
                Optional fields: name, description
            
        Returns:
            Updated group data
        """
        if isinstance(group, GroupDTO):
            group_data = group.to_dict()
        else:
            group_data = group
            
        return self.client.put(f"{self.resource_path}/{group_id}", json=group_data)
    
    def delete(self, group_id: int) -> Dict[str, Any]:
        """
        Delete a contact group.
        
        Args:
            group_id: The ID of the group to delete
            
        Returns:
            Response data
        """
        return self.client.delete(f"{self.resource_path}/{group_id}")
    
    def get_contacts(
        self,
        group_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get contacts that belong to a specific group.
        
        Args:
            group_id: The ID of the group
            limit: Maximum number of contacts to retrieve
            offset: Offset for pagination
            
        Returns:
            Dictionary containing contacts data
        """
        request = GroupContactsRequestDTO(
            group_id=group_id,
            limit=limit,
            offset=offset
        )
        
        return self.client.get(
            f"{self.resource_path}/{group_id}/contacts",
            params=request.to_dict()
        )
    
    def add_contact(self, group_id: int, sms: str, status: str = "active") -> Dict[str, Any]:
        """
        Add a contact to a group.
        
        Args:
            group_id: The ID of the group
            sms: The SMS number of the contact to add
            status: The status of the contact in the group (default: "active")
            
        Returns:
            Response data
        """
        request = GroupAddContactDTO(
            group_id=group_id,
            sms=sms
        )
        
        # Status might need special handling if not part of the DTO
        data = request.to_dict()
        data["status"] = status
        
        return self.client.post(
            f"{self.resource_path}/{group_id}/contacts/{sms}",
            json=data
        )
    
    def remove_contact(self, group_id: int, sms: str) -> Dict[str, Any]:
        """
        Remove a contact from a group.
        
        Args:
            group_id: The ID of the group
            sms: The SMS number of the contact to remove
            
        Returns:
            Response data
        """
        return self.client.delete(f"{self.resource_path}/{group_id}/contacts/{sms}")
    
    def add_multiple_contacts(
        self,
        group_id: int, 
        sms_numbers: List[str],
        status: str = "active"
    ) -> Dict[str, Any]:
        """
        Add multiple contacts to a group in a single operation.
        
        Args:
            group_id: The ID of the group
            sms_numbers: List of SMS numbers to add to the group
            status: The status of the contacts in the group (default: "active")
            
        Returns:
            Response data
        """
        request = GroupAddMultipleContactsDTO(
            group_id=group_id,
            sms=sms_numbers
        )
        
        # Status might need special handling if not part of the DTO
        data = request.to_dict()
        data["status"] = status
        
        return self.client.post(
            f"{self.resource_path}/{group_id}/contacts/batch",
            json=data
        )
    
    def remove_multiple_contacts(self, group_id: int, sms_numbers: List[str]) -> Dict[str, Any]:
        """
        Remove multiple contacts from a group in a single operation.
        
        Args:
            group_id: The ID of the group
            sms_numbers: List of SMS numbers to remove from the group
            
        Returns:
            Response data
        """
        request = GroupRemoveMultipleContactsDTO(
            group_id=group_id,
            sms=sms_numbers
        )
        
        return self.client.delete(
            f"{self.resource_path}/{group_id}/contacts/batch",
            json=request.to_dict()
        )

    def get_members(
        self,
        group_id: int,
        customer_states: Optional[List[str]] = None,
        search_term: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get all group members.
        
        Args:
            group_id: The ID of the group
            customer_states: Filter by contact status (e.g., ["Active", "Unsubscribed", "Bounced"])
            search_term: Search by SMS number
            from_date: Start date for filtering (YYYY-MM-DD format)
            to_date: End date for filtering (YYYY-MM-DD format)
            page: Page number for pagination
            limit: Maximum number of results per page (1-100)
            
        Returns:
            Dictionary containing group members data
        """
        params = {}
        
        if customer_states:
            params["CustomerStates"] = customer_states
        
        if search_term:
            params["SearchTerm"] = search_term
        
        if from_date:
            params["FromDate"] = from_date
        
        if to_date:
            params["ToDate"] = to_date
        
        if page:
            params["Page"] = page
        
        if limit:
            params["Limit"] = limit
            
        return self.client.get(
            f"{self.resource_path}/{group_id}/members",
            params=params
        )