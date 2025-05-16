"""
ActiveTrail SMS Campaigns API implementation.
"""

from typing import Dict, Any, Optional, List, Union, Type, TypeVar
from datetime import datetime
import logging
from pydantic import ValidationError
from .base_api import CampaignBaseAPI
from .dto.sms_campaigns import (
    BaseDTO,
    SMSCampaignDTO,
    ApiSmsCampaignInfoCampaign,
    ApiSmsCampaignInfoCampaignList,
    SMSCampaignSchedulingDTO,
    ApiSmsCampaignSegment,
    ApiSMSMobileDTO,
    ApiSMSCampaignDetailsDTO,
    ApiSmsCampaignSchedulingDTO,
    SMSOperationalMessageDTO,
    SMSOperationalMessageResponseDTO
)

logger = logging.getLogger(__name__)
T = TypeVar('T', bound=BaseDTO)

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
        logger.debug("SMS Campaigns API initialized")
    
    def _validate_and_convert(self, data: Union[Dict[str, Any], T], model_class: Type[T]) -> Dict[str, Any]:
        """
        Validate the input data against the specified model class and convert it to a dictionary.
        
        Args:
            data: Input data (either a dictionary or a Pydantic model)
            model_class: The Pydantic model class to validate against
            
        Returns:
            Validated data as a dictionary ready to be sent to the API
        """
        try:
            if isinstance(data, dict):
                # Validate against the model
                validated_data = model_class(**data)
                return validated_data.to_dict()
            elif isinstance(data, model_class):
                # Already a valid model, just convert to dict
                return data.to_dict()
            else:
                raise TypeError(f"Expected dict or {model_class.__name__}, got {type(data).__name__}")
        except ValidationError as e:
            logger.error(f"Validation error for {model_class.__name__}: {e}")
            raise
    
    def get_campaigns(
        self,
        is_include_not_sent: Optional[bool] = False,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        search_term: Optional[str] = None,
        filter_type: Optional[int] = 0,
        page: Optional[int] = 1,
        limit: Optional[int] = 20
    ) -> Dict[str, Any]:
        """
        Get account's SMS campaigns (including operational SMS).
        
        Args:
            is_include_not_sent: Whether to include campaigns that weren't sent. Default is false.
            from_date: The start date the campaign was last updated
            to_date: The end date the campaign was last updated
            search_term: Search by campaign name/partial name
            filter_type: Filter by campaign's type: All types (0), Regular (1), Test (2), 
                         Transactional/Operational (3). Default is 0.
            page: Get a specific page (1-based index)
            limit: Limit the number of items in results (1-100). Default is 20.
            
        Returns:
            Dictionary containing the ApiSmsCampaignInfoCampaignList with campaigns data
            
        Example:
            ```python
            # Get campaigns from the last month
            from datetime import datetime, timedelta
            
            from_date = datetime.now() - timedelta(days=30)
            to_date = datetime.now()
            
            # Get list of SMS campaigns
            response = client.sms_campaigns.get_campaigns(
                is_include_not_sent=True,
                from_date=from_date,
                to_date=to_date,
                search_term="Promotion",
                filter_type=1,  # Regular campaigns
                page=1,
                limit=50
            )
            
            # Display the campaigns
            for campaign in response['sms_campaign']:
                print(f"ID: {campaign['id']}, Name: {campaign['name']}, Status: {campaign['status_name']}")
            ```
        """
        logger.info(f"Getting SMS campaigns from {from_date} to {to_date} with filter_type={filter_type}")
        
        params = {
            'IsIncludeNotSent': is_include_not_sent
        }
        
        if from_date:
            params['FromDate'] = from_date.isoformat()
        
        if to_date:
            params['ToDate'] = to_date.isoformat()
        
        if search_term:
            params['SearchTerm'] = search_term
        
        if filter_type is not None:
            params['FilterType'] = filter_type
        
        if page:
            params['Page'] = page
        
        if limit:
            params['Limit'] = limit
        
        logger.debug(f"Request parameters: {params}")
        
        response = self.client.get(f"{self.resource_path}/Campaign", params=params)
        logger.debug(f"Retrieved {response.get('total_items', 0)} campaigns")
        return response
    
    def get_campaign(self, campaign_id: int) -> Dict[str, Any]:
        """
        Get details of a specific SMS campaign by its ID.
        
        Args:
            campaign_id: SMS campaign ID
            
        Returns:
            SMS campaign data as ApiSmsCampaignInfoCampaign
            
        Example:
            ```python
            # Get SMS campaign details
            campaign_id = 123
            campaign = client.sms_campaigns.get_campaign(campaign_id)
            
            # Display campaign details
            print(f"Campaign Name: {campaign['name']}")
            print(f"Content: {campaign['content']}")
            print(f"From: {campaign['from_name']}")
            print(f"Status: {campaign['status_name']}")
            print(f"Total Sent: {campaign['total_sent']}")
            ```
        """
        logger.info(f"Getting SMS campaign with ID {campaign_id}")
        
        response = self.client.get(f"{self.resource_path}/Campaign/{campaign_id}")
        logger.debug(f"Retrieved campaign: {response.get('name')}")
        return response
    
    def create(self, campaign: Union[Dict[str, Any], SMSCampaignDTO]) -> Dict[str, Any]:
        """
        Create and return a new SMS campaign.
        
        Args:
            campaign: SMSCampaignDTO object or dictionary with campaign data
                Required fields: 
                  - name: SMS campaign name (internal use only)
                  - content: SMS content
                  - unsubscribe_text: Unsubscribe text
                  - segment: Campaign segmentation (group_ids, restricated_group_ids)
                    Can be a dictionary or ApiSmsCampaignSegment object
                  - scheduling: Campaign scheduling information
                    Can be a dictionary or SMSCampaignSchedulingDTO object
                Optional fields:
                  - from_name: From name (sender name, up to 11 English letters, no special chars)
                  - can_unsubscribe: If true, adds unsubscription link
                  - is_link_tracking: Whether links are tracked
                  - sms_sending_profile_id: Alternative to from_name
                
        Returns:
            Created SMS campaign data
            
        Example:
            ```python
            from active_trail import ActiveTrailClient
            from active_trail.dto.sms_campaigns import (
                SMSCampaignDTO, 
                ApiSmsCampaignSegment, 
                SMSCampaignSchedulingDTO
            )
            from datetime import datetime, timedelta
            
            # Initialize the client
            client = ActiveTrailClient(api_key="your_api_key")
            
            # Schedule for tomorrow
            tomorrow = datetime.now() + timedelta(days=1)
            
            # Create segment object
            segment = ApiSmsCampaignSegment(
                group_ids=[123, 456],
                restricated_group_ids=[789],
                mailing_list_id=None,
                limit_amount=None
            )
            
            # Create scheduling object
            scheduling = SMSCampaignSchedulingDTO(
                scheduled_date=tomorrow,
                scheduled_time_zone="Israel",
                is_sent=False
            )
            
            # Create the campaign
            campaign = SMSCampaignDTO(
                name="Summer Sale SMS",
                content="Get 20% off with code SUMMER20",
                unsubscribe_text="Reply STOP to unsubscribe",
                segment=segment,
                scheduling=scheduling,
                from_name="MyBrand",
                can_unsubscribe=True,
                is_link_tracking=True
            )
            
            # Create the campaign
            response = client.sms_campaigns.create(campaign)
            print(f"Created campaign with ID: {response['id']}")
            
            # Or you can use dictionaries directly
            campaign_dict = {
                "name": "Summer Sale SMS",
                "content": "Get 20% off with code SUMMER20",
                "unsubscribe_text": "Reply STOP to unsubscribe",
                "segment": {
                    "group_ids": [123, 456],
                    "restricated_group_ids": [789]
                },
                "scheduling": {
                    "scheduled_date": tomorrow.isoformat(),
                    "scheduled_time_zone": "Israel",
                    "is_sent": False
                },
                "from_name": "MyBrand",
                "can_unsubscribe": True,
                "is_link_tracking": True
            }
            
            response = client.sms_campaigns.create(campaign_dict)
            ```
        """
        # Get the name for logging - handle both dict and object case
        if isinstance(campaign, dict):
            campaign_name = campaign.get('name', 'unnamed')
        else:
            campaign_name = getattr(campaign, 'name', 'unnamed')
            
        logger.info(f"Creating new SMS campaign: {campaign_name}")
        
        campaign_data = self._validate_and_convert(campaign, SMSCampaignDTO)
        logger.debug(f"Validated campaign data: {campaign_data}")
        
        response = self.client.post(f"{self.resource_path}/Campaign", json=campaign_data)
        logger.info(f"Created SMS campaign with ID: {response.get('id')}")
        return response
    
    def update(self, campaign: Union[Dict[str, Any], SMSCampaignDTO]) -> Dict[str, Any]:
        """
        Update an existing SMS campaign (whether it was sent or not).
        
        Args:
            campaign: SMSCampaignDTO object or dictionary with updated campaign data
                Required fields:
                  - id: SMS campaign ID
                  - name: SMS campaign name
                  - content: SMS content
                  - unsubscribe_text: Unsubscribe text
                  - segment: Campaign segmentation and sending restrictions
                    Can be a dictionary or ApiSmsCampaignSegment object
                  - scheduling: Campaign scheduling information
                    Can be a dictionary or SMSCampaignSchedulingDTO object
                Optional fields:
                  - from_name: Sender name
                  - can_unsubscribe: Whether unsubscription link is added
                  - is_link_tracking: Whether links are tracked
                
        Returns:
            Updated SMS campaign data
            
        Example:
            ```python
            from active_trail import ActiveTrailClient
            from active_trail.dto.sms_campaigns import (
                SMSCampaignDTO, 
                ApiSmsCampaignSegment, 
                SMSCampaignSchedulingDTO
            )
            
            # Initialize the client
            client = ActiveTrailClient(api_key="your_api_key")
            
            # Get the existing campaign first
            campaign_id = 123
            existing_campaign = client.sms_campaigns.get_campaign(campaign_id)
            
            # Update the campaign content
            updated_campaign = SMSCampaignDTO(
                id=campaign_id,
                name=existing_campaign['name'],
                content="Updated content: Get 30% off with code SUMMER30",
                unsubscribe_text=existing_campaign['unsubscribe_text'],
                segment=existing_campaign['segment'],
                scheduling=existing_campaign['scheduling'],
                from_name=existing_campaign['from_name'],
                can_unsubscribe=existing_campaign['can_unsubscribe'],
                is_link_tracking=existing_campaign['is_link_tracking']
            )
            
            # Update the campaign
            client.sms_campaigns.update(updated_campaign)
            print(f"Campaign {campaign_id} has been updated.")
            
            # Or you can update using a dictionary
            updated_campaign_dict = {
                "id": campaign_id,
                "name": existing_campaign['name'],
                "content": "Updated content: Get 30% off with code SUMMER30",
                "unsubscribe_text": existing_campaign['unsubscribe_text'],
                "segment": existing_campaign['segment'],
                "scheduling": existing_campaign['scheduling'],
                "from_name": existing_campaign['from_name'],
                "can_unsubscribe": existing_campaign['can_unsubscribe'],
                "is_link_tracking": existing_campaign['is_link_tracking']
            }
            
            client.sms_campaigns.update(updated_campaign_dict)
            ```
        """
        campaign_data = self._validate_and_convert(campaign, SMSCampaignDTO)
        
        campaign_id = campaign_data.get('id')
        if not campaign_id:
            logger.error("No campaign ID provided for update operation")
            raise ValueError("Campaign ID is required for updates")
            
        logger.info(f"Updating SMS campaign with ID: {campaign_id}")
        logger.debug(f"Update data: {campaign_data}")
        
        response = self.client.put(f"{self.resource_path}/Campaign/{campaign_id}", json=campaign_data)
        logger.info(f"Successfully updated SMS campaign with ID: {campaign_id}")
        return response
    
    def get_estimate(self, campaign_id: int) -> int:
        """
        Calculate the estimated number of messages for a given campaign.
        
        Can be used only for campaigns that were not sent yet.
        
        Args:
            campaign_id: SMS campaign ID
            
        Returns:
            Estimated number of messages
            
        Example:
            ```python
            # Get campaign estimate
            campaign_id = 123
            estimate = client.sms_campaigns.get_estimate(campaign_id)
            print(f"Estimated number of messages: {estimate}")
            ```        """
        logger.info(f"Getting estimate for SMS campaign with ID: {campaign_id}")
        
        response = self.client.get(f"{self.resource_path}/Campaign/{campaign_id}/estimate")
        logger.debug(f"Estimate for campaign {campaign_id}: {response}")
        return response
        
    def send_operational_message(
        self, 
        message: Union[Dict[str, Any], SMSOperationalMessageDTO]
    ) -> Dict[str, Any]:
        """
        Send an operational SMS message to specific mobile numbers.
        
        Unlike SMS campaigns that are sent to groups, operational messages are 
        sent to individual recipients defined by their mobile numbers.
        
        Args:
            message: SMSOperationalMessageDTO object or dictionary with message data
                Required fields:
                    - details: SMS message details (name, content, unsubscribe_text, etc.)
                      Can be a dictionary or ApiSMSCampaignDetailsDTO object
                    - scheduling: Message scheduling information
                      Can be a dictionary or ApiSmsCampaignSchedulingDTO object
                    - mobiles: List of mobile phone numbers to receive the message
                      Can be a list of dictionaries or ApiSMSMobileDTO objects
                
        Returns:
            Created SMS operational message data
            
        Example:
            ```python
            # Send an operational SMS message using objects
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
            
            # Or using dictionaries
            message_dict = {
                "details": {
                    "name": "Password Reset",
                    "content": "Your verification code is 123456",
                    "unsubscribe_text": "Reply STOP to unsubscribe",
                    "from_name": "MyCompany",
                    "can_unsubscribe": True
                },
                "scheduling": {
                    "send_now": True
                },
                "mobiles": [
                    {"phone_number": "+1234567890"},
                    {"phone_number": "+9876543210"}
                ]
            }
            
            response = client.sms_campaigns.send_operational_message(message_dict)
            ```
        """
        message_data = self._validate_and_convert(message, SMSOperationalMessageDTO)
        
        message_name = (message_data.get('details', {}) or {}).get('name', 'unnamed')
        logger.info(f"Sending operational SMS message: {message_name}")
        
        num_recipients = len(message_data.get('mobiles', []))
        logger.debug(f"Sending to {num_recipients} recipients")
        
        response = self.client.post(f"{self.resource_path}/OperationalMessage", json=message_data)
        logger.info(f"Sent operational SMS message with ID: {response.get('id')}")
        return response
    
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
        logger.info(f"Getting operational SMS message with ID: {message_id}")
        
        response = self.client.get(f"{self.resource_path}/OperationalMessage/{message_id}")
        logger.debug(f"Retrieved operational message: {response.get('name')}")
        return response
    
    def update_operational_message(
        self,
        message_id: int,
        message: Union[Dict[str, Any], SMSOperationalMessageDTO]
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
            # Update an SMS operational message using objects
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
            
            # Or using a dictionary
            message_dict = {
                "details": {
                    "name": "Updated Password Reset",
                    "content": "Your new verification code is 654321",
                    "unsubscribe_text": "Reply STOP to unsubscribe",
                    "from_name": "MyCompany",
                    "can_unsubscribe": True
                },
                "scheduling": {
                    "send_now": True
                },
                "mobiles": [
                    {"phone_number": "+1234567890"}
                ]
            }
            
            result = client.sms_campaigns.update_operational_message(123, message_dict)
            ```
        """
        message_data = self._validate_and_convert(message, SMSOperationalMessageDTO)
        
        message_name = (message_data.get('details', {}) or {}).get('name', 'unnamed')
        logger.info(f"Updating operational SMS message with ID {message_id}: {message_name}")
        
        response = self.client.put(f"{self.resource_path}/OperationalMessage/{message_id}", json=message_data)
        logger.info(f"Successfully updated operational SMS message with ID: {message_id}")
        return response 

