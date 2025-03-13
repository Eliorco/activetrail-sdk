"""
ActiveTrail Contacts API implementation.
"""

from typing import Dict, Any, Optional


class ContactsAPI:
    """Contacts API handling for ActiveTrail."""

    def __init__(self, client):
        """
        Initialize the Contacts API.
        
        Args:
            client: The ActiveTrail client instance
        """
        self.client = client
    
    def list(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get a list of contacts from ActiveTrail.
        
        Args:
            params: Query parameters for filtering results
            
        Returns:
            Contacts data
        """
        return self.client.get("contacts", params=params)
    
    def get(self, contact_id: str) -> Dict[str, Any]:
        """
        Get information about a specific contact.
        
        Args:
            contact_id: The ID of the contact to retrieve
            
        Returns:
            Contact data
        """
        return self.client.get(f"contacts/{contact_id}")
    
    def create(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new contact.
        
        Args:
            contact_data: Contact information including at least 'email'
            
        Returns:
            Created contact data
        """
        return self.client.post("contacts", json=contact_data)
    
    def update(self, contact_id: str, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing contact.
        
        Args:
            contact_id: The ID of the contact to update
            contact_data: Updated contact information
            
        Returns:
            Updated contact data
        """
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