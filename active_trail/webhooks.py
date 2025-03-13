"""
ActiveTrail Webhooks API implementation.
"""

from typing import Dict, Any, Optional, List


class WebhooksAPI:
    """Webhooks API handling for ActiveTrail."""

    def __init__(self, client):
        """
        Initialize the Webhooks API.
        
        Args:
            client: The ActiveTrail client instance
        """
        self.client = client
    
    def get_webhooks(self) -> List[Dict[str, Any]]:
        """
        Get all registered webhooks.
        
        Returns:
            List of webhooks
        """
        return self.client.request("GET", "webhooks")
    
    def get_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """
        Get information about a specific webhook.
        
        Args:
            webhook_id: The ID of the webhook
            
        Returns:
            Webhook data
        """
        return self.client.request("GET", f"webhooks/{webhook_id}")
    
    def create_webhook(
        self,
        url: str,
        events: List[str],
        description: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new webhook.
        
        Args:
            url: The URL that will receive webhook events
            events: List of event types to subscribe to (e.g., ["contact.created", "email.sent"])
            description: Description of the webhook (optional)
            headers: Custom HTTP headers to include with webhook requests (optional)
            
        Returns:
            Created webhook data
        """
        data = {
            "url": url,
            "events": events
        }
        
        if description:
            data["description"] = description
            
        if headers:
            data["headers"] = headers
            
        return self.client.request("POST", "webhooks", data=data)
    
    def update_webhook(
        self,
        webhook_id: str,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        description: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing webhook.
        
        Args:
            webhook_id: The ID of the webhook to update
            url: New URL (optional)
            events: New list of event types (optional)
            description: New description (optional)
            headers: New custom HTTP headers (optional)
            
        Returns:
            Updated webhook data
        """
        data = {}
        
        if url:
            data["url"] = url
            
        if events:
            data["events"] = events
            
        if description:
            data["description"] = description
            
        if headers:
            data["headers"] = headers
            
        return self.client.request("PUT", f"webhooks/{webhook_id}", data=data)
    
    def delete_webhook(self, webhook_id: str) -> None:
        """
        Delete a webhook.
        
        Args:
            webhook_id: The ID of the webhook to delete
        """
        return self.client.request("DELETE", f"webhooks/{webhook_id}")
    
    def test_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """
        Test a webhook by sending a test event.
        
        Args:
            webhook_id: The ID of the webhook to test
            
        Returns:
            Test result
        """
        return self.client.request("POST", f"webhooks/{webhook_id}/test") 