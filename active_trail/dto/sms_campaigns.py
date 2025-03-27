"""
Data Transfer Objects for SMS Campaigns API.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, ClassVar, Union
from datetime import datetime
from .base import BaseDTO


@dataclass
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


@dataclass
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
    group_ids: List[int]  # Required
    restricated_group_ids: Optional[List[int]] = None
    restricated_campaign_ids: Optional[List[int]] = None
    mailing_list_id: Optional[int] = None
    limit_amount: Optional[int] = None
    sms_sending_profile_id: Optional[int] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'group_ids': 'group_ids',
        'restricated_group_ids': 'restricated_group_ids',
        'restricated_campaign_ids': 'restricated_campaign_ids', 
        'mailing_list_id': 'mailing_list_id',
        'limit_amount': 'limit_amount',
        'sms_sending_profile_id': 'sms_sending_profile_id'
    }
    
    _optional_fields: ClassVar[List[str]] = [
        'restricated_group_ids', 'restricated_campaign_ids', 
        'mailing_list_id', 'limit_amount', 'sms_sending_profile_id'
    ]


@dataclass
class SMSCampaignSchedulingDTO(BaseDTO):
    """
    SMS campaign time zone scheduling data transfer object.
    """
    scheduled_date: datetime
    scheduled_time_zone: str = "Isreal"
    is_sent: bool = False
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'scheduled_date': 'scheduledDate',
        'scheduled_time_zone': 'scheduledTimeZone',
        'is_sent': 'isSent'
    }
    
    _optional_fields: ClassVar[List[str]] = ['is_sent']


@dataclass
class SMSCampaignDTO(BaseDTO):
    """
    SMS campaign data transfer object for creation and updates.
    
    Fields:
        name: SMS campaign name (internal use only)
        content: SMS content
        from_name: From name (sender name, up to 11 English letters without special characters or spaces)
        unsubscribe_text: Unsubscribe text (required even if unsubscribed link is not used)
        segment: Campaign segmentation and sending restrictions
        scheduling: Scheduling the SMS campaign
        can_unsubscribe: If true, an unsubscription link will be added
        is_link_tracking: Whether links are tracked
        sms_sending_profile_id: SMS sending profile ID (alternative to from_name)
        campaign_id: Campaign ID for updates
    """
    name: str
    content: str
    unsubscribe_text: str
    segment: ApiSmsCampaignSegment
    scheduling: SMSCampaignSchedulingDTO
    from_name: Optional[str] = None
    can_unsubscribe: Optional[bool] = False
    is_link_tracking: Optional[bool] = None
    sms_sending_profile_id: Optional[int] = None
    campaign_id: Optional[int] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'from_name': 'fromName',
        'unsubscribe_text': 'unsubscribeText',
        'can_unsubscribe': 'canUnsubscribe',
        'is_link_tracking': 'isLinkTracking',
        'sms_sending_profile_id': 'smsSendingProfileId',
        'campaign_id': 'id'
    }
    
    _optional_fields: ClassVar[List[str]] = [
        'from_name', 'can_unsubscribe', 'is_link_tracking', 
        'sms_sending_profile_id', 'campaign_id'
    ]


@dataclass
class SMSCampaignResponseDTO(BaseDTO):
    """
    SMS campaign response data transfer object.
    """
    id: int
    name: str
    content: str
    from_name: str
    unsubscribe_text: str
    segment: Dict[str, Any]
    scheduling: Dict[str, Any]
    status: Optional[str] = None
    can_unsubscribe: Optional[bool] = None
    is_link_tracking: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    scheduled_time: Optional[str] = None
    sent_time: Optional[str] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'from_name': 'fromName',
        'unsubscribe_text': 'unsubscribeText',
        'can_unsubscribe': 'canUnsubscribe',
        'is_link_tracking': 'isLinkTracking',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'scheduled_time': 'scheduledTime',
        'sent_time': 'sentTime'
    }


@dataclass
class SMSCampaignScheduleDTO(CampaignScheduleBaseDTO):
    """
    SMS campaign schedule data transfer object.
    """
    pass


@dataclass
class SMSCampaignTestDTO(BaseDTO):
    """
    SMS campaign test data transfer object.
    """
    campaign_id: int
    recipients: List[str]
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'campaign_id': 'campaignId'
    }


@dataclass
class SMSCampaignSendDTO(BaseDTO):
    """
    SMS campaign send data transfer object.
    """
    campaign_id: int
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'campaign_id': 'campaignId'
    }


@dataclass
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


@dataclass
class SMSCampaignRecipientsRequestDTO(BaseDTO):
    """
    Request parameters for retrieving SMS campaign recipients.
    """
    campaign_id: int
    status: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'campaign_id': 'campaignId'
    }
    
    _optional_fields: ClassVar[List[str]] = ['status', 'limit', 'offset']


# SMS Operational Message DTOs

@dataclass
class ApiSMSMobileDTO(BaseDTO):
    """
    Mobile phone number data transfer object.
    """
    phone_number: str
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'phone_number': 'phone_number'
    }


@dataclass
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
    
    _optional_fields: ClassVar[List[str]] = [
        'from_name', 'can_unsubscribe', 'sms_sending_profile_id', 'unsubscribe_text'
    ]
    
    def __post_init__(self):
        # Validate that either from_name or sms_sending_profile_id is provided
        if self.from_name is None and self.sms_sending_profile_id is None:
            raise ValueError("Either from_name or sms_sending_profile_id must be provided")


@dataclass
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
    
    _optional_fields: ClassVar[List[str]] = ['scheduled_date_utc']
    
    def __post_init__(self):
        # Validate that if send_now is False, scheduled_date_utc is provided
        if not self.send_now and self.scheduled_date_utc is None:
            raise ValueError("If send_now is False, scheduled_date_utc must be provided")


@dataclass
class SMSOperationalMessageDTO(BaseDTO):
    """
    SMS operational message data transfer object for creation.
    """
    details: ApiSMSCampaignDetailsDTO
    scheduling: ApiSmsCampaignSchedulingDTO
    mobiles: List[ApiSMSMobileDTO]
    
    def __post_init__(self):
        # Validate mobiles list is not empty
        if not self.mobiles:
            raise ValueError("At least one mobile number must be provided")


@dataclass
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
    
    _optional_fields: ClassVar[List[str]] = ['from_name', 'sms_sending_profile_id']


@dataclass
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
    error_rate: float
    sum_clicks: int
    clickers: int
    click_rate: float
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'error_rate': 'error_rate',
        'sum_clicks': 'sum_clicks',
        'click_rate': 'click_rate'
    }


@dataclass
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
    error_rate: float
    sum_clicks: int
    clickers: int
    click_rate: float
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'error_rate': 'error_rate',
        'sum_clicks': 'sum_clicks',
        'click_rate': 'click_rate'
    } 