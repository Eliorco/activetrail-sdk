"""
Data Transfer Objects for SMS Campaigns API.
"""

from typing import Dict, List, Optional, Any, ClassVar, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator, model_validator
import logging

logger = logging.getLogger(__name__)

class BaseDTO(BaseModel):
    """Base DTO class with helper methods for API field mapping."""
    
    class Config:
        arbitrary_types_allowed = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the DTO to a dictionary with proper API field mappings."""
        data = self.model_dump(exclude_none=True)
        
        # Apply field mappings if available
        api_field_mapping = getattr(self, "_api_field_mapping", {})
        
        if api_field_mapping:
            # Map field names to API field names
            for field_name, api_field_name in api_field_mapping.items():
                if field_name in data:
                    data[api_field_name] = data.pop(field_name)
        
        # Handle nested DTOs
        for key, value in list(data.items()):
            if isinstance(value, BaseDTO):
                data[key] = value.to_dict()
            elif isinstance(value, list) and value and isinstance(value[0], BaseDTO):
                data[key] = [item.to_dict() for item in value]
        
        return data


class ApiSmsCampaignSegment(BaseDTO):
    """
    SMS campaign segmentation and sending restrictions data transfer object.
    
    Fields:
        group_ids: List of group IDs that will receive the campaign
        restricated_group_ids: Do not send the SMS to users that are in these groups
        restricated_campaign_ids: Do not send the SMS to users that got these campaigns
        mailing_list_id: The mailing list the SMS is going to be sent to
        limit_amount: Limit the number of SMS to send
        sms_sending_profile_id: SMS sending profile ID (required if "from_name" is not used)
    """
    group_ids: Optional[List[int]] = None
    restricated_group_ids: Optional[List[int]] = None
    restricated_campaign_ids: Optional[List[int]] = None
    mailing_list_id: Optional[int] = None
    limit_amount: Optional[int] = None
    sms_sending_profile_id: Optional[int] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'group_ids': 'groupIds',
        'restricated_group_ids': 'restricatedGroupIds',
        'restricated_campaign_ids': 'restricatedCampaignIds', 
        'mailing_list_id': 'mailingListId',
        'limit_amount': 'limitAmount',
        'sms_sending_profile_id': 'smsSendingProfileId'
    }


class SMSCampaignSchedulingDTO(BaseDTO):
    """
    SMS campaign time zone scheduling data transfer object.
    """
    scheduled_date: datetime
    scheduled_time_zone: str = "Israel"
    is_sent: bool = False
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'scheduled_date': 'scheduledDate',
        'scheduled_time_zone': 'scheduledTimeZone',
        'is_sent': 'isSent'
    }


class SMSCampaignDTO(BaseDTO):
    """
    SMS campaign data transfer object for creation and updates.
    
    Fields:
        name: SMS campaign name (internal use only)
        content: SMS content
        unsubscribe_text: Unsubscribe text (required even if unsubscription link is not used)
        segment: Campaign segmentation and sending restrictions (can be dict or ApiSmsCampaignSegment)
        scheduling: Scheduling the SMS campaign (can be dict or SMSCampaignSchedulingDTO)
        from_name: From name (sender name, up to 11 English letters without special characters or spaces)
        can_unsubscribe: If true, an unsubscription link will be added
        is_link_tracking: Whether links are tracked
        sms_sending_profile_id: SMS sending profile ID (alternative to from_name)
        id: SMS campaign ID (required for updates, not for creation)
    """
    name: str
    content: str
    unsubscribe_text: str
    segment: Union[Dict[str, Any], ApiSmsCampaignSegment]
    scheduling: Union[Dict[str, Any], SMSCampaignSchedulingDTO]
    from_name: Optional[str] = None
    can_unsubscribe: Optional[bool] = None
    is_link_tracking: Optional[bool] = None
    sms_sending_profile_id: Optional[int] = None
    id: Optional[int] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'from_name': 'fromName',
        'unsubscribe_text': 'unsubscribeText',
        'can_unsubscribe': 'canUnsubscribe',
        'is_link_tracking': 'isLinkTracking',
        'sms_sending_profile_id': 'smsSendingProfileId'
    }
    
    @validator('from_name')
    def validate_from_name(cls, v, values):
        if v is not None and not (v.isalpha() and len(v) <= 11):
            raise ValueError("from_name must be up to 11 English letters without special characters or spaces")
        return v
    
    @model_validator(mode='after')
    def validate_sender_info(self):
        if not self.from_name and not self.sms_sending_profile_id:
            raise ValueError("Either from_name or sms_sending_profile_id must be provided")
        return self


class ApiSmsCampaignInfoCampaign(BaseDTO):
    """
    SMS campaign information response object.
    """
    id: int
    name: str
    content: str
    from_name: str
    unsubscribe_text: str
    can_unsubscribe: bool
    is_link_tracking: bool
    segment: Union[Dict[str, Any], ApiSmsCampaignSegment]
    scheduling: Union[Dict[str, Any], SMSCampaignSchedulingDTO]
    send_type: str
    send_type_name: str
    status_id: int
    status_name: str
    total_sent: int
    status_date: datetime
    handled_date: datetime
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'id': 'id',
        'name': 'name',
        'content': 'content',
        'from_name': 'fromName',
        'unsubscribe_text': 'unsubscribeText',
        'can_unsubscribe': 'canUnsubscribe',
        'is_link_tracking': 'isLinkTracking',
        'segment': 'segment',
        'scheduling': 'scheduling',
        'send_type': 'sendType',
        'send_type_name': 'sendTypeName',
        'status_id': 'statusId',
        'status_name': 'statusName',
        'total_sent': 'totalSent',
        'status_date': 'statusDate',
        'handled_date': 'handledDate'
    }


class ApiSmsCampaignInfoCampaignList(BaseDTO):
    """
    List of SMS campaigns response object.
    """
    sms_campaign: List[Union[Dict[str, Any], ApiSmsCampaignInfoCampaign]]
    total_items: int
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'sms_campaign': 'sms_campaign',
        'total_items': 'total_items'
    }


class CampaignScheduleBaseDTO(BaseDTO):
    """
    Base data transfer object for campaign scheduling.
    """
    campaign_id: int
    scheduled_time: str
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'campaign_id': 'campaignId',
        'scheduled_time': 'scheduledTime'
    }


class SMSCampaignScheduleDTO(CampaignScheduleBaseDTO):
    """
    SMS campaign schedule data transfer object.
    """
    pass


class SMSCampaignTestDTO(BaseDTO):
    """
    SMS campaign test data transfer object.
    """
    campaign_id: int
    recipients: List[str]
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'campaign_id': 'campaignId'
    }
    
    @validator('recipients')
    def validate_recipients(cls, v):
        if not v:
            raise ValueError("At least one recipient is required")
        return v


class SMSCampaignSendDTO(BaseDTO):
    """
    SMS campaign send data transfer object.
    """
    campaign_id: int
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'campaign_id': 'campaignId'
    }


class SMSCampaignStatisticsDTO(BaseDTO):
    """
    SMS campaign statistics data transfer object.
    """
    campaign_id: int
    recipients: int
    delivered: int
    failed: int
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'campaign_id': 'campaignId'
    }


class SMSCampaignRecipientsRequestDTO(BaseDTO):
    """
    Request parameters for retrieving SMS campaign recipients.
    """
    campaign_id: int
    status: Optional[str] = None
    limit: Optional[int] = Field(None, gt=0, le=100)
    offset: Optional[int] = Field(None, ge=0)
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'campaign_id': 'campaignId'
    }


# SMS Operational Message DTOs

class ApiSMSMobileDTO(BaseDTO):
    """
    Mobile phone number data transfer object.
    """
    phone_number: str
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'phone_number': 'phone_number'
    }
    
    @model_validator(mode='after')
    def validate_phone_number(self):
        # Basic validation - could be enhanced further
        if not self.phone_number or not self.phone_number.startswith('+'):
            raise ValueError("Phone number must start with '+' and include country code")
        return self


class ApiSMSCampaignDetailsDTO(BaseDTO):
    """
    SMS campaign details data transfer object for operational messages.
    """
    name: str
    content: str
    unsubscribe_text: str = "Reply STOP to unsubscribe"
    from_name: Optional[str] = None
    can_unsubscribe: Optional[bool] = False
    sms_sending_profile_id: Optional[int] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'from_name': 'from_name',
        'unsubscribe_text': 'unsubscribe_text',
        'can_unsubscribe': 'can_unsubscribe',
        'sms_sending_profile_id': 'sms_sending_profile_id'
    }
    
    @validator('from_name')
    def validate_from_name(cls, v):
        if v is not None and not (v.isalpha() and len(v) <= 11):
            raise ValueError("from_name must be up to 11 English letters without special characters or spaces")
        return v
    
    @model_validator(mode='after')
    def validate_sender_info(self):
        if not self.from_name and not self.sms_sending_profile_id:
            raise ValueError("Either from_name or sms_sending_profile_id must be provided")
        return self


class ApiSmsCampaignSchedulingDTO(BaseDTO):
    """
    SMS campaign scheduling data transfer object for operational messages.
    """
    scheduled_date_utc: Optional[datetime] = None
    send_now: bool = True
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'scheduled_date_utc': 'scheduled_date_utc',
        'send_now': 'send_now'
    }
    
    @model_validator(mode='after')
    def validate_scheduling(self):
        if not self.send_now and not self.scheduled_date_utc:
            raise ValueError("If send_now is False, scheduled_date_utc must be provided")
        return self


class SMSOperationalMessageDTO(BaseDTO):
    """
    SMS operational message data transfer object for creation.
    """
    details: Union[Dict[str, Any], ApiSMSCampaignDetailsDTO]
    scheduling: Union[Dict[str, Any], ApiSmsCampaignSchedulingDTO]
    mobiles: Union[List[Dict[str, Any]], List[ApiSMSMobileDTO]]
    
    @model_validator(mode='after')
    def validate_mobiles(self):
        if not self.mobiles:
            raise ValueError("At least one mobile number must be provided")
            
        # Validate each mobile number if they are dictionaries
        if isinstance(self.mobiles, list) and self.mobiles and isinstance(self.mobiles[0], dict):
            for mobile in self.mobiles:
                if not mobile.get('phone_number', '').startswith('+'):
                    raise ValueError("Phone number must start with '+' and include country code")
        return self


class SMSOperationalMessageResponseDTO(BaseDTO):
    """
    SMS operational message response data transfer object.
    """
    id: int
    name: str
    content: str
    from_name: Optional[str] = None
    sms_sending_profile_id: Optional[int] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'from_name': 'from_name',
        'sms_sending_profile_id': 'sms_sending_profile_id'
    }


class SMSCampaignReportDTO(BaseDTO):
    """
    SMS campaign report data transfer object.
    
    Fields:
        sent: Number of messages sent
        delivered: Number of messages successfully delivered
        errors: Number of messages with delivery errors
        unsubscribed: Number of recipients who unsubscribed
        error_rate: Error rate as a percentage
        sum_clicks: Total number of link clicks
        clickers: Number of unique clickers
        click_rate: Click rate as a percentage
    """
    sent: int
    delivered: int
    errors: int
    unsubscribed: int
    error_rate: float = Field(..., ge=0, le=100)
    sum_clicks: int
    clickers: int
    click_rate: float = Field(..., ge=0, le=100)
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'error_rate': 'error_rate',
        'sum_clicks': 'sum_clicks',
        'click_rate': 'click_rate'
    }


class ApiSmsCampaignOverviewInfo(BaseDTO):
    """
    API response data transfer object for SMS campaign reports.
    
    This class matches the exact structure returned by the ActiveTrail API
    for SMS campaign reports.
    
    Fields:
        sent: Number of messages sent
        delivered: Number of messages successfully delivered
        errors: Number of messages with delivery errors
        unsubscribed: Number of recipients who unsubscribed
        error_rate: Error rate as a percentage
        sum_clicks: Total number of link clicks
        clickers: Number of unique clickers
        click_rate: Click rate as a percentage
    """
    sent: int
    delivered: int
    errors: int
    unsubscribed: int
    error_rate: float = Field(..., ge=0, le=100)
    sum_clicks: int
    clickers: int
    click_rate: float = Field(..., ge=0, le=100)
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'error_rate': 'error_rate',
        'sum_clicks': 'sum_clicks',
        'click_rate': 'click_rate'
    } 