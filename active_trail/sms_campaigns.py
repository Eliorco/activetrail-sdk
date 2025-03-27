"""
ActiveTrail SMS Campaigns API implementation.
"""

from typing import Dict, Any, Optional, List, Union
from .base_api import CampaignBaseAPI
from .dto.sms_campaigns import (
    SMSCampaignDTO,
    SMSCampaignResponseDTO,
    SMSCampaignScheduleDTO,
    SMSCampaignTestDTO,
    SMSCampaignSendDTO,
    SMSCampaignStatisticsDTO,
    SMSCampaignRecipientsRequestDTO,
    SMSCampaignSchedulingDTO,
    ApiSMSMobileDTO,
    ApiSMSCampaignDetailsDTO,
    ApiSmsCampaignSchedulingDTO,
    SMSOperationalMessageDTO,
    SMSOperationalMessageResponseDTO,
    SMSCampaignReportDTO,
    ApiSmsCampaignOverviewInfo
)
from .dto.campaigns import (
    CampaignListRequestDTO,
    CampaignDuplicateRequestDTO
)


class SMSCampaignsAPI(CampaignBaseAPI):
    """SMS Campaigns API handling for ActiveTrail."""

    def __init__(self, client):
        """
        Initialize the SMS Campaigns API.
        
        Args:
            client: The ActiveTrail client instance
        
        Example:
            ```python
            from active_trail import ActiveTrailClient
            
            client = ActiveTrailClient(api_key="your_api_key")
            sms_campaigns = client.sms_campaigns
            ```
        """
        super().__init__(client, "smscampaign")
    
    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None,
        campaign_type: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get a list of SMS campaigns.
        
        Args:
            limit: Maximum number of campaigns to retrieve
            offset: Offset for pagination
            status: Filter by campaign status
            campaign_type: Filter by campaign type
            from_date: Filter by creation date (from) in ISO format
            to_date: Filter by creation date (to) in ISO format
            
        Returns:
            Dictionary containing SMS campaigns data
            
        Example:
            ```python
            # Get a list of SMS campaigns
            campaigns = client.sms_campaigns.list(limit=20)
            for campaign in campaigns.get('campaigns', []):
                print(f"Campaign: {campaign['name']}")
            ```
        """
        request = CampaignListRequestDTO(
            limit=limit,
            offset=offset,
            status=status,
            campaign_type=campaign_type,
            from_date=from_date,
            to_date=to_date
        )
        
        return self.client.get(f"{self.resource_path}", params=request.to_dict())
    
    def get(self, campaign_id: int) -> Dict[str, Any]:
        """
        Get information about a specific SMS campaign.
        
        Args:
            campaign_id: The ID of the SMS campaign
            
        Returns:
            SMS campaign data
            
        Example:
            ```python
            # Get a specific SMS campaign
            campaign = client.sms_campaigns.get(123)
            print(f"Campaign name: {campaign['name']}")
            ```
        """
        return self.client.get(f"{self.resource_path}/Campaign/{campaign_id}")
    
    def create(self, campaign: Union[SMSCampaignDTO, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a new SMS campaign.
        
        Args:
            campaign: SMSCampaignDTO object or dictionary with campaign data
                Required fields: 
                  - name: SMS campaign name (internal use only)
                  - content: SMS content
                  - unsubscribe_text: Unsubscribe text
                  - segment: Campaign segmentation (groups, exclude_groups)
                  - scheduling: Campaign scheduling information
                Optional fields:
                  - from_name: From name (sender name, up to 11 English letters, no special chars)
                  - can_unsubscribe: If true, adds unsubscription link
                  - is_link_tracking: Whether links are tracked
                  - sms_sending_profile_id: Alternative to from_name
                
        Returns:
            Created SMS campaign data
            
        Example:
            ```python
            # Create a new SMS campaign using a DTO
            from active_trail.dto.sms_campaigns import SMSCampaignDTO, SMSCampaignSegmentDTO, SMSCampaignSchedulingDTO
            from datetime import datetime, timedelta
            
            # Schedule for tomorrow
            tomorrow = datetime.now() + timedelta(days=1)
            
            # Create segment and scheduling objects
            segment = SMSCampaignSegmentDTO(
                groups=[123, 456],
                exclude_groups=[789]
            )
            
            scheduling = SMSCampaignSchedulingDTO(
                scheduled_date=tomorrow,
                scheduled_time_zone="50",
                is_sent=False
            )
            
            # Create the campaign
            campaign = SMSCampaignDTO(
                name="Summer Sale SMS",
                content="Get 20% off with code SUMMER20",
                unsubscribe_text="Reply STOP to unsubscribe",
                segment=segment,
                scheduling=scheduling,
                from_name="YourBrand",
                can_unsubscribe=True,
                is_link_tracking=True
            )
            
            new_campaign = client.sms_campaigns.create(campaign)
            print(f"Created campaign with ID: {new_campaign['id']}")
            ```
        """
        if isinstance(campaign, SMSCampaignDTO):
            campaign_data = campaign.to_dict()
        else:
            campaign_data = campaign
            
        return self.client.post(f"{self.resource_path}/Campaign", json=campaign_data)
    
    def update(
        self,
        campaign_id: int,
        campaign: Union[SMSCampaignDTO, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Update an existing SMS campaign.
        
        Args:
            campaign_id: The ID of the SMS campaign to update
            campaign: SMSCampaignDTO object or dictionary with updated campaign data
                Required fields: name, content, unsubscribe_text, segment, scheduling
                Optional fields: from_name, can_unsubscribe, is_link_tracking, sms_sending_profile_id
                
        Returns:
            Updated SMS campaign data
            
        Example:
            ```python
            # Update an SMS campaign using a DTO
            from active_trail.dto.sms_campaigns import SMSCampaignDTO, SMSCampaignSegmentDTO, SMSCampaignSchedulingDTO
            from datetime import datetime
            
            # Create segment and scheduling objects
            segment = SMSCampaignSegmentDTO(
                groups=[123, 456]
            )
            
            scheduling = SMSCampaignSchedulingDTO(
                scheduled_date=datetime(2023, 12, 1, 10, 0, 0),
                scheduled_time_zone="50",
                is_sent=False
            )
            
            campaign = SMSCampaignDTO(
                name="Updated Campaign Name",
                content="New message content",
                unsubscribe_text="Text STOP to opt out",
                segment=segment,
                scheduling=scheduling,
                from_name="YourBrand",
                can_unsubscribe=True,
                is_link_tracking=True
            )
            
            result = client.sms_campaigns.update(123, campaign)
            ```
        """
        if isinstance(campaign, SMSCampaignDTO):
            campaign_data = campaign.to_dict()
        else:
            campaign_data = campaign
            
        return self.client.put(f"{self.resource_path}/{campaign_id}", json=campaign_data)
    
    def delete(self, campaign_id: int) -> Dict[str, Any]:
        """
        Delete an SMS campaign.
        
        Args:
            campaign_id: The ID of the SMS campaign to delete
            
        Returns:
            Response data
            
        Example:
            ```python
            # Delete an SMS campaign
            client.sms_campaigns.delete(123)
            ```
        """
        return self.client.delete(f"{self.resource_path}/{campaign_id}")
    
    def schedule(self, campaign_id: int, scheduled_time: str) -> Dict[str, Any]:
        """
        Schedule an SMS campaign for delivery.
        
        Args:
            campaign_id: The ID of the SMS campaign to schedule
            scheduled_time: ISO format datetime string for when to send the campaign
                
        Returns:
            Scheduling confirmation data
            
        Example:
            ```python
            # Schedule an SMS campaign for tomorrow
            import datetime
            
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            result = client.sms_campaigns.schedule(123, tomorrow.isoformat())
            ```
        """
        schedule = SMSCampaignScheduleDTO(
            campaign_id=campaign_id,
            scheduled_time=scheduled_time
        )
            
        return self.client.post(
            f"{self.resource_path}/{campaign_id}/schedule", 
            json=schedule.to_dict()
        )
    
    def send_now(self, campaign_id: int) -> Dict[str, Any]:
        """
        Send an SMS campaign immediately.
        
        Args:
            campaign_id: The ID of the SMS campaign to send
                
        Returns:
            Response data
            
        Example:
            ```python
            # Send an SMS campaign immediately
            result = client.sms_campaigns.send_now(123)
            ```
        """
        send_request = SMSCampaignSendDTO(campaign_id=campaign_id)
        return self.client.post(
            f"{self.resource_path}/{campaign_id}/send",
            json=send_request.to_dict()
        )
    
    def test(self, campaign_id: int, recipients: List[str]) -> Dict[str, Any]:
        """
        Send a test SMS campaign to specified recipients.
        
        Args:
            campaign_id: The ID of the SMS campaign to test
            recipients: List of phone numbers to send the test to
                
        Returns:
            Test results
            
        Example:
            ```python
            # Send a test SMS
            result = client.sms_campaigns.test(123, ["1234567890", "9876543210"])
            ```
        """
        test_request = SMSCampaignTestDTO(
            campaign_id=campaign_id,
            recipients=recipients
        )
            
        return self.client.post(
            f"{self.resource_path}/{campaign_id}/test",
            json=test_request.to_dict()
        )
    
    def get_statistics(self, campaign_id: int) -> Dict[str, Any]:
        """
        Get statistics for a specific SMS campaign.
        
        Args:
            campaign_id: The ID of the SMS campaign
                
        Returns:
            SMS campaign statistics
            
        Example:
            ```python
            # Get statistics for an SMS campaign
            stats = client.sms_campaigns.get_statistics(123)
            print(f"Sent: {stats['recipients']}, Delivered: {stats['delivered']}")
            ```
        """
        return self.client.get(f"{self.resource_path}/{campaign_id}/statistics")
    
    def get_recipients(
        self,
        campaign_id: int,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get recipients for a specific SMS campaign with their status.
        
        Args:
            campaign_id: The ID of the SMS campaign
            status: Filter by delivery status (e.g. 'delivered', 'failed')
            limit: Maximum number of records to retrieve
            offset: Offset for pagination
                
        Returns:
            Campaign recipients data
            
        Example:
            ```python
            # Get all recipients with 'delivered' status
            recipients = client.sms_campaigns.get_recipients(123, status='delivered')
            ```
        """
        request = SMSCampaignRecipientsRequestDTO(
            campaign_id=campaign_id,
            status=status,
            limit=limit,
            offset=offset
        )
            
        return self.client.get(
            f"{self.resource_path}/{campaign_id}/recipients", 
            params=request.to_dict()
        )
    
    def get_delivery_status(
        self,
        campaign_id: int,
        contact_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get delivery status for an SMS campaign.
        
        Args:
            campaign_id: The ID of the SMS campaign
            contact_id: Optional contact ID to filter results
                
        Returns:
            Delivery status information
            
        Example:
            ```python
            # Get delivery status for an SMS campaign
            status = client.sms_campaigns.get_delivery_status(123)
            
            # Get delivery status for a specific contact
            contact_status = client.sms_campaigns.get_delivery_status(123, 456)
            ```
        """
        params = {}
        if contact_id is not None:
            params["contact_id"] = contact_id
            
        return self.client.get(f"{self.resource_path}/Campaign/{campaign_id}/delivery-status", params=params)
    
    def get_report(self, campaign_id: int, get_contacts: bool = False) -> Dict[str, Any]:
        """
        Get a summary report for a specific SMS campaign.
        
        This endpoint provides comprehensive metrics about the campaign performance,
        including delivery rates, errors, and engagement statistics.
        
        Args:
            campaign_id: The ID of the SMS campaign
            get_contacts: If True, get contacts report for the campaign
        Returns:
            Dictionary of ApiSmsCampaignOverviewInfo: SMS campaign report with performance metrics including:
                - sent: Number of messages sent
                - delivered: Number of messages successfully delivered
                - errors: Number of messages with delivery errors
                - unsubscribed: Number of recipients who unsubscribed
                - error_rate: Error rate as a percentage
                - sum_clicks: Total number of link clicks
                - clickers: Number of unique clickers
                - click_rate: Click rate as a percentage
            
        Example:
            ```python
            # Get report for an SMS campaign
            report = client.sms_campaigns.get_report(123)
            print(f"Delivered: {report['delivered']}, Errors: {report['errors']}")
            print(f"Click rate: {report['click_rate']}%")
            ```
        """
        if get_contacts:
            return self.client.get(f"smscampaignreport/{campaign_id}/Delivered", params={"id": campaign_id})
        return self.client.get(f"smscampaignreport/{campaign_id}")
    
    # region Operational Messages
    def send_operational_message(
        self, 
        message: Union[SMSOperationalMessageDTO, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Send an operational SMS message to specific mobile numbers.
        
        Unlike SMS campaigns that are sent to groups, operational messages are 
        sent to individual recipients defined by their mobile numbers.
        
        Args:
            message: SMSOperationalMessageDTO object or dictionary with message data
                Required fields:
                    - details: SMS message details (name, content, unsubscribe_text, etc.)
                    - scheduling: Message scheduling information
                    - mobiles: List of mobile phone numbers to receive the message
                
        Returns:
            Created SMS operational message data
            
        Example:
            ```python
            # Send an operational SMS message
            from active_trail.dto.sms_campaigns import (
                ApiSMSMobileDTO, 
                ApiSMSCampaignDetailsDTO, 
                ApiSmsCampaignSchedulingDTO,
                SMSOperationalMessageDTO
            )
            
            # Create details object
            details = ApiSMSCampaignDetailsDTO(
                name="Password Reset",
                content="Your verification code is 123456",
                unsubscribe_text="Reply STOP to unsubscribe",
                from_name="MyCompany",
                can_unsubscribe=True
            )
            
            # Create scheduling object - send immediately
            scheduling = ApiSmsCampaignSchedulingDTO(
                send_now=True
            )
            
            # Create mobile numbers list
            mobiles = [
                ApiSMSMobileDTO(phone_number="+1234567890"),
                ApiSMSMobileDTO(phone_number="+9876543210")
            ]
            
            # Create the operational message
            message = SMSOperationalMessageDTO(
                details=details,
                scheduling=scheduling,
                mobiles=mobiles
            )
            
            # Send the message
            response = client.sms_campaigns.send_operational_message(message)
            print(f"Sent message with ID: {response['id']}")
            ```
        """
        if isinstance(message, SMSOperationalMessageDTO):
            message_data = message.to_dict()
        else:
            message_data = message
            
        return self.client.post(f"{self.resource_path}/OperationalMessage", json=message_data)
    
    def get_operational_message(self, message_id: int) -> Dict[str, Any]:
        """
        Get information about a specific SMS operational message.
        
        Args:
            message_id: The ID of the SMS operational message
            
        Returns:
            SMS operational message data
            
        Example:
            ```python
            # Get a specific SMS operational message
            message = client.sms_campaigns.get_operational_message(123)
            print(f"Message content: {message['content']}")
            ```
        """
        return self.client.get(f"{self.resource_path}/OperationalMessage/{message_id}")
    
    def update_operational_message(
        self,
        message_id: int,
        message: Union[SMSOperationalMessageDTO, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Update an existing SMS operational message that has not been sent yet.
        
        Args:
            message_id: The ID of the SMS operational message to update
            message: SMSOperationalMessageDTO object or dictionary with updated message data
                
        Returns:
            Updated SMS operational message data
            
        Example:
            ```python
            # Update an SMS operational message
            from active_trail.dto.sms_campaigns import (
                ApiSMSMobileDTO, 
                ApiSMSCampaignDetailsDTO, 
                ApiSmsCampaignSchedulingDTO,
                SMSOperationalMessageDTO
            )
            
            # Create the updated message
            details = ApiSMSCampaignDetailsDTO(
                name="Updated Password Reset",
                content="Your new verification code is 654321",
                unsubscribe_text="Reply STOP to unsubscribe",
                from_name="MyCompany",
                can_unsubscribe=True
            )
            
            scheduling = ApiSmsCampaignSchedulingDTO(
                send_now=True
            )
            
            mobiles = [
                ApiSMSMobileDTO(phone_number="+1234567890")
            ]
            
            message = SMSOperationalMessageDTO(
                details=details,
                scheduling=scheduling,
                mobiles=mobiles
            )
            
            # Update the message
            result = client.sms_campaigns.update_operational_message(123, message)
            ```
        """
        if isinstance(message, SMSOperationalMessageDTO):
            message_data = message.to_dict()
        else:
            message_data = message
            
        return self.client.put(f"{self.resource_path}/OperationalMessage/{message_id}", json=message_data) 
    # endregion Operational Messages
