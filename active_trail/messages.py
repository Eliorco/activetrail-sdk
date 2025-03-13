"""
ActiveTrail Messages API implementation.
"""

from typing import Dict, Any, Optional, List


class MessagesAPI:
    """Messages API handling for ActiveTrail."""

    def __init__(self, client):
        """
        Initialize the Messages API.
        
        Args:
            client: The ActiveTrail client instance
        """
        self.client = client
    
    def send_email(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send an email.
        
        Args:
            data: Email data including subject, content, recipients, and sender info
            
        Returns:
            Response data
        """
        return self.client.post("messages/email", json=data)
    
    def send_sms(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send an SMS message.
        
        Args:
            data: SMS data including message, recipients, and sender ID
            
        Returns:
            Response data
        """
        return self.client.post("messages/sms", json=data)
    
    def get_status(self, message_id: str) -> Dict[str, Any]:
        """
        Check the status of a sent message.
        
        Args:
            message_id: The ID of the message
            
        Returns:
            Message status information
        """
        return self.client.get(f"messages/{message_id}/status")
    
    def get_statistics(self, message_id: str) -> Dict[str, Any]:
        """
        Get statistics for a specific message.
        
        Args:
            message_id: The ID of the message
            
        Returns:
            Message statistics
        """
        return self.client.get(f"messages/{message_id}/statistics") 