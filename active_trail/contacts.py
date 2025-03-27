"""
ActiveTrail Contacts API implementation.
"""

from typing import Dict, Any, Optional, List, Union, cast
from .dto.contacts import (
    ContactDTO, 
    ContactListRequestDTO, 
    ContactActivityRequestDTO,
    ContactActivityDTO,
    ContactUnsubscribeDTO,
    ContactMultipleUnsubscribeDTO,
    ContactResubscribeDTO,
    ContactMultipleResubscribeDTO
)


class ContactsAPI:
    """Contacts API handling for ActiveTrail."""

    def __init__(self, client):
        """
        Initialize the Contacts API.
        
        Args:
            client: The ActiveTrail client instance
        """
        self.client = client
    
    def list(
        self, 
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None,
        email: Optional[str] = None,
        created_from: Optional[str] = None,
        created_to: Optional[str] = None,
        only_active: Optional[bool] = None,
        only_bounced: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Get a list of contacts from ActiveTrail.
        
        Args:
            limit: Maximum number of contacts to return
            offset: Offset for pagination
            status: Filter by contact status
            email: Filter by email address
            created_from: Filter by creation date (from)
            created_to: Filter by creation date (to)
            only_active: Return only active contacts
            only_bounced: Return only bounced contacts
            
        Returns:
            Contacts data including pagination information
        """
        params = ContactListRequestDTO(
            limit=limit,
            offset=offset,
            status=status,
            email=email,
            created_from=created_from,
            created_to=created_to,
            only_active=only_active,
            only_bounced=only_bounced
        ).to_dict()
            
        return self.client.get("contacts", params=params)
    
    def get(self, contact_id: str) -> Dict[str, Any]:
        """
        Get information about a specific contact.
        
        Args:
            contact_id: The ID or email of the contact to retrieve
            
        Returns:
            Contact data
        """
        return self.client.get(f"contacts/{contact_id}")
    
    def create(self, contact: Union[ContactDTO, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a new contact.
        
        Args:
            contact: Contact information as a ContactDTO or dictionary
                    Must include 'email' and optionally other fields
                    like 'first_name', 'last_name', 'phone', etc.
            
        Returns:
            Created contact data
        """
        if isinstance(contact, ContactDTO):
            contact_data = contact.to_dict()
        else:
            contact_data = contact
            
        return self.client.post("contacts", json=contact_data)
    
    def update(self, contact_id: str, contact: Union[ContactDTO, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update an existing contact.
        
        Args:
            contact_id: The ID of the contact to update
            contact: Updated contact information as a ContactDTO or dictionary
            
        Returns:
            Updated contact data
        """
        if isinstance(contact, ContactDTO):
            contact_data = contact.to_dict()
        else:
            contact_data = contact
            
        return self.client.put(f"contacts/{contact_id}", json=contact_data)
    
    def delete(self, contact_id: str) -> Dict[str, Any]:
        """
        Delete a contact.
        
        Args:
            contact_id: The ID of the contact to delete
            
        Returns:
            Response data
        """
        return self.client.delete(f"contacts/{contact_id}")
    
    def get_groups(self, contact_id: str) -> Dict[str, Any]:
        """
        Get the groups that a contact belongs to.
        
        Args:
            contact_id: The ID of the contact
            
        Returns:
            Groups data for the contact
        """
        return self.client.get(f"contacts/{contact_id}/groups")
    
    def add_to_group(self, contact_id: str, group_id: str, status: str = "active") -> Dict[str, Any]:
        """
        Add a contact to a group.
        
        Args:
            contact_id: The ID of the contact
            group_id: The ID of the group to add the contact to
            status: The status of the contact in the group (default: "active")
            
        Returns:
            Response data
        """
        data = {
            "status": status
        }
        return self.client.post(f"contacts/{contact_id}/groups/{group_id}", json=data)
    
    def remove_from_group(self, contact_id: str, group_id: str) -> Dict[str, Any]:
        """
        Remove a contact from a group.
        
        Args:
            contact_id: The ID of the contact
            group_id: The ID of the group to remove the contact from
            
        Returns:
            Response data
        """
        return self.client.delete(f"contacts/{contact_id}/groups/{group_id}")
    
    def get_activities(
        self, 
        contact_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        activity_type: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get a contact's activity history.
        
        Args:
            contact_id: The ID of the contact
            limit: Maximum number of activities to return
            offset: Offset for pagination
            activity_type: Filter by activity type
            from_date: Filter by activity date (from)
            to_date: Filter by activity date (to)
            
        Returns:
            Contact activities data
        """
        params = ContactActivityRequestDTO(
            contact_id=contact_id,
            limit=limit,
            offset=offset,
            activity_type=activity_type,
            from_date=from_date,
            to_date=to_date
        ).to_dict()
            
        return self.client.get(f"contacts/{contact_id}/activities", params=params)
    
    def get_custom_fields(self) -> List[Dict[str, Any]]:
        """
        Get all custom fields defined in the account.
        
        Returns:
            List of custom fields
        """
        return self.client.get("contacts/custom-fields")
    
    def create_custom_field(self, field_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new custom field.
        
        Args:
            field_data: Custom field configuration including 'name', 'type', etc.
            
        Returns:
            Created custom field data
        """
        return self.client.post("contacts/custom-fields", json=field_data)
    
    def import_contacts(self, contacts: List[Union[ContactDTO, Dict[str, Any]]], 
                       update_existing: bool = True,
                       group_ids: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Import multiple contacts at once.
        
        Args:
            contacts: List of contacts to import (as ContactDTO objects or dictionaries)
            update_existing: Whether to update existing contacts (default: True)
            group_ids: Optional list of group IDs to add the contacts to
            
        Returns:
            Import results data
        """
        contact_data = []
        for contact in contacts:
            if isinstance(contact, ContactDTO):
                contact_data.append(contact.to_dict())
            else:
                contact_data.append(contact)
                
        import_data = {
            "contacts": contact_data,
            "updateExisting": update_existing
        }
        
        if group_ids:
            import_data["groupIds"] = group_ids
            
        return self.client.post("contacts/import", json=import_data)
    
    def unsubscribe(self, email: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Unsubscribe a contact.
        
        Args:
            email: The email of the contact to unsubscribe
            reason: Optional reason for unsubscribing
            
        Returns:
            Response data
        """
        data = ContactUnsubscribeDTO(email=email, reason=reason).to_dict()
        return self.client.post("contacts/unsubscribe", json=data)
    
    def unsubscribe_multiple(self, emails: List[str], reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Unsubscribe multiple contacts.
        
        Args:
            emails: List of email addresses to unsubscribe
            reason: Optional reason for unsubscribing
            
        Returns:
            Response data
        """
        data = ContactMultipleUnsubscribeDTO(emails=emails, reason=reason).to_dict()
        return self.client.post("contacts/unsubscribe-multiple", json=data)
    
    def resubscribe(self, email: str) -> Dict[str, Any]:
        """
        Resubscribe a previously unsubscribed contact.
        
        Args:
            email: The email of the contact to resubscribe
            
        Returns:
            Response data
        """
        data = ContactResubscribeDTO(email=email).to_dict()
        return self.client.post("contacts/resubscribe", json=data)
    
    def resubscribe_multiple(self, emails: List[str]) -> Dict[str, Any]:
        """
        Resubscribe multiple previously unsubscribed contacts.
        
        Args:
            emails: List of email addresses to resubscribe
            
        Returns:
            Response data
        """
        data = ContactMultipleResubscribeDTO(emails=emails).to_dict()
        return self.client.post("contacts/resubscribe-multiple", json=data) 