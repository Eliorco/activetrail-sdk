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
    
    def add_contact(
        self,
        group_id: int,
        sms: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        status: Optional[str] = None,
        sms_status: Optional[str] = None,
        campaign_id: Optional[int] = None,
        subscribe_ip: Optional[str] = None,
        double_optin: Optional[Dict[str, str]] = None,
        is_deleted: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Add a contact to a group.
        
        Args:
            group_id: The ID of the group
            sms: The SMS number of the contact to add
            first_name: Contact's first name
            last_name: Contact's last name
            status: Contact's status
            sms_status: Contact's SMS status
            campaign_id: Campaign ID to send to the imported contact
            subscribe_ip: The Subscribe IP
            double_optin: Double opt-in configuration
            is_deleted: If true - contact will be deleted
            
        Returns:
            Response data containing the added contact information
        """
        request = GroupAddContactDTO(
            group_id=group_id,
            sms=sms,
            first_name=first_name,
            last_name=last_name,
            status=status,
            sms_status=sms_status,
            campaign_id=campaign_id,
            subscribe_ip=subscribe_ip,
            double_optin=double_optin,
            is_deleted=is_deleted
        )
        
        return self.client.post(
            f"{self.resource_path}/{group_id}/members",
            json=request.to_dict()
        )
    
    def remove_contact_from_group(self, group_id: int, contact_id: int) -> Dict[str, Any]:
        """
        Remove a contact from a group.
        
        Args:
            group_id: The ID of the group
            contact_id: The ID of the contact to remove
            
        Returns:
            Response data
        """
        return self.client.delete(f"{self.resource_path}/{group_id}/members/{contact_id}")
    def _get_contact_dict_to_add(self, contact: dict) -> dict:
        return {
            "externalId": contact["id"],
            "externalName": f"{contact['first_name']}"
        }

    def add_multiple_contacts_to_group_external(
        self,
        group_id: int,
        contacts: List[dict]
    ) -> bool:
        """
        Add multiple contacts to a group in a single operation.
        """
        contacts_to_add = [self._get_contact_dict_to_add(contact) for contact in contacts ]        
        return self.client.post(f"external/group/{group_id}", json=contacts_to_add)
            
    def add_multiple_contacts(
        self,
        group_id: int, 
        contacts: List[dict],
        status: str = "active"
    ) -> bool:
        """
        Add multiple contacts to a group in a single operation.
        
        Args:
            group_id: The ID of the group
            contacts: List of contact dictionaries with sms, first_name, and last_name keys
            status: The status of the contacts in the group (default: "active")
            
        Returns:
            True if all contacts were added successfully, False otherwise
        """
        try:
            for contact in contacts:
                self.add_contact(
                    group_id=group_id, 
                    sms=contact["sms"],
                    first_name=contact.get("first_name"),
                    last_name=contact.get("last_name"),
                    status=status
                )
            return True
        except Exception as e:
            print(f"Error adding contact: {contact} to group: {group_id}: {e}")
            return False
    
    def remove_multiple_contacts(self, group_id: int, contacts: List[dict]) -> bool:
        """
        Remove multiple contacts from a group in a single operation.
        
        Args:
            group_id: The ID of the group
            sms_numbers: List of SMS numbers to remove from the group
            
        Returns:
            Response data
        """
        try:
            for contact in contacts:
                self.remove_contact_from_group(group_id, contact["id"])
            return True
        except Exception as e:
            print(f"Error removing contact: {contact} from group: {group_id}: {e}")
            return False

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