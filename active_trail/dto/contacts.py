"""
Data Transfer Objects for Contacts API.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, ClassVar
from datetime import datetime
from .base import BaseDTO


@dataclass
class ContactDTO(BaseDTO):
    """
    Contact Data Transfer Object for creating and retrieving contacts.
    """
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    company: Optional[str] = None
    birthday: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    
    # API field mapping (snake_case to camelCase where needed)
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'first_name': 'firstName',
        'last_name': 'lastName',
        'mobile_phone': 'mobilePhone',
        'zip_code': 'zip',
        'custom_fields': 'customFields'
    }
    
    # Fields that can be safely omitted when sending to API
    _optional_fields: ClassVar[List[str]] = [
        'first_name', 'last_name', 'phone', 'mobile_phone', 
        'address', 'city', 'state', 'zip_code', 'country',
        'company', 'birthday', 'custom_fields'
    ]


@dataclass
class ContactListRequestDTO(BaseDTO):
    """
    Request parameters for listing contacts.
    """
    limit: Optional[int] = None
    offset: Optional[int] = None
    status: Optional[str] = None
    email: Optional[str] = None
    created_from: Optional[str] = None
    created_to: Optional[str] = None
    only_active: Optional[bool] = None
    only_bounced: Optional[bool] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'created_from': 'createdFrom',
        'created_to': 'createdTo',
        'only_active': 'onlyActive',
        'only_bounced': 'onlyBounced'
    }
    
    _optional_fields: ClassVar[List[str]] = [
        'limit', 'offset', 'status', 'email', 
        'created_from', 'created_to', 'only_active', 'only_bounced'
    ]


@dataclass
class ContactActivityDTO(BaseDTO):
    """
    Contact activity data transfer object.
    """
    activity_id: int
    contact_id: int
    activity_type: str
    activity_time: str
    campaign_id: Optional[int] = None
    campaign_name: Optional[str] = None
    subject: Optional[str] = None
    ip: Optional[str] = None
    operating_system: Optional[str] = None
    browser: Optional[str] = None
    url: Optional[str] = None
    message_id: Optional[str] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'activity_id': 'activityId',
        'contact_id': 'contactId',
        'activity_type': 'activityType',
        'activity_time': 'activityTime',
        'campaign_id': 'campaignId',
        'campaign_name': 'campaignName',
        'operating_system': 'operatingSystem',
        'message_id': 'messageId'
    }


@dataclass
class ContactActivityRequestDTO(BaseDTO):
    """
    Request parameters for retrieving contact activities.
    """
    contact_id: int
    limit: Optional[int] = None
    offset: Optional[int] = None
    activity_type: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'contact_id': 'contactId',
        'activity_type': 'activityType',
        'from_date': 'fromDate',
        'to_date': 'toDate'
    }
    
    _optional_fields: ClassVar[List[str]] = [
        'limit', 'offset', 'activity_type', 'from_date', 'to_date'
    ]


@dataclass
class ContactUnsubscribeDTO(BaseDTO):
    """
    Data transfer object for unsubscribing a contact.
    """
    email: str
    reason: Optional[str] = None
    
    _optional_fields: ClassVar[List[str]] = ['reason']


@dataclass
class ContactMultipleUnsubscribeDTO(BaseDTO):
    """
    Data transfer object for unsubscribing multiple contacts.
    """
    emails: List[str]
    reason: Optional[str] = None
    
    _optional_fields: ClassVar[List[str]] = ['reason']


@dataclass
class ContactResubscribeDTO(BaseDTO):
    """
    Data transfer object for resubscribing a contact.
    """
    email: str


@dataclass
class ContactMultipleResubscribeDTO(BaseDTO):
    """
    Data transfer object for resubscribing multiple contacts.
    """
    emails: List[str] 