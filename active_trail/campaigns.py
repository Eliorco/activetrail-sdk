"""
ActiveTrail Campaigns API implementation.
"""

from typing import Dict, Any, Optional, List


class CampaignsAPI:
    """Campaigns API handling for ActiveTrail."""

    def __init__(self, client):
        """
        Initialize the Campaigns API.
        
        Args:
            client: The ActiveTrail client instance
        """
        self.client = client
    
    def get_campaigns(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Get a list of campaigns.
        
        Args:
            limit: Maximum number of campaigns to retrieve
            offset: Offset for pagination
            
        Returns:
            Campaigns data
        """
        return self.client.request("GET", "campaigns", params={"limit": limit, "offset": offset})
    
    def get_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """
        Get information about a specific campaign.
        
        Args:
            campaign_id: The ID of the campaign
            
        Returns:
            Campaign data
        """
        return self.client.request("GET", f"campaigns/{campaign_id}")
    
    def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new campaign.
        
        Args:
            campaign_data: Campaign configuration
            
        Returns:
            Created campaign data
        """
        return self.client.request("POST", "campaigns", data=campaign_data)
    
    def update_campaign(self, campaign_id: str, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing campaign.
        
        Args:
            campaign_id: The ID of the campaign to update
            campaign_data: Updated campaign configuration
            
        Returns:
            Updated campaign data
        """
        return self.client.request("PUT", f"campaigns/{campaign_id}", data=campaign_data)
    
    def delete_campaign(self, campaign_id: str) -> None:
        """
        Delete a campaign.
        
        Args:
            campaign_id: The ID of the campaign to delete
        """
        return self.client.request("DELETE", f"campaigns/{campaign_id}")
    
    def schedule_campaign(self, campaign_id: str, schedule_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule a campaign for delivery.
        
        Args:
            campaign_id: The ID of the campaign to schedule
            schedule_data: Scheduling information including date/time
            
        Returns:
            Scheduling confirmation
        """
        return self.client.request("POST", f"campaigns/{campaign_id}/schedule", data=schedule_data)
    
    def get_campaign_statistics(self, campaign_id: str) -> Dict[str, Any]:
        """
        Get statistics for a specific campaign.
        
        Args:
            campaign_id: The ID of the campaign
            
        Returns:
            Campaign statistics
        """
        return self.client.request("GET", f"campaigns/{campaign_id}/statistics") 