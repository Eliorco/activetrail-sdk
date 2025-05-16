"""
Data Transfer Objects for Contact Groups API.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, ClassVar
from datetime import datetime
from .base import BaseDTO


@dataclass
class GroupDTO(BaseDTO):
    """
    Group data transfer object for creation and updates.
    """
    name: str
    description: Optional[str] = None
    group_id: Optional[int] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'group_id': 'id'
    }
    
    _optional_fields: ClassVar[List[str]] = ['description', 'group_id']


@dataclass
class GroupResponseDTO(BaseDTO):
    """
    Group response data transfer object.
    """
    id: int
    name: str
    description: Optional[str] = None
    contact_count: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'contact_count': 'contactCount',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt'
    }


@dataclass
class GroupListRequestDTO(BaseDTO):
    """
    Request parameters for listing groups.
    """
    limit: Optional[int] = None
    offset: Optional[int] = None
    
    _optional_fields: ClassVar[List[str]] = ['limit', 'offset']


@dataclass
class GroupContactDTO(BaseDTO):
    """
    Group contact data transfer object.
    """
    sms: str


@dataclass
class GroupContactsRequestDTO(BaseDTO):
    """
    Request parameters for retrieving group contacts.
    """
    group_id: int
    limit: Optional[int] = None
    offset: Optional[int] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'group_id': 'groupId'
    }
    
    _optional_fields: ClassVar[List[str]] = ['limit', 'offset']


class GroupAddContactDTO:
    """DTO for adding a contact to a group."""
    
    def __init__(
        self,
        group_id: int,
        sms: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        status: Optional[str] = None,
        sms_status: Optional[str] = None,
        campaign_id: Optional[int] = None,
        subscribe_ip: Optional[str] = None,
        double_optin: Optional[Dict[str, str]] = None,
        is_deleted: Optional[bool] = None
    ):
        """
        Initialize the DTO.
        
        Args:
            group_id: The ID of the group
            sms: The SMS number of the contact
            first_name: Contact's first name
            last_name: Contact's last name
            status: Contact's status
            sms_status: Contact's SMS status
            campaign_id: Campaign ID to send to the imported contact
            subscribe_ip: The Subscribe IP
            double_optin: Double opt-in configuration
            is_deleted: If true - contact will be deleted
        """
        self.group_id = group_id
        self.sms = sms
        self.first_name = first_name
        self.last_name = last_name
        self.status = status
        self.sms_status = sms_status
        self.campaign_id = campaign_id
        self.subscribe_ip = subscribe_ip
        self.double_optin = double_optin
        self.is_deleted = is_deleted
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the DTO to a dictionary."""
        data = {
            "sms": self.sms
        }
        
        if self.first_name is not None:
            data["first_name"] = self.first_name
        if self.last_name is not None:
            data["last_name"] = self.last_name
        if self.status is not None:
            data["status"] = self.status
        if self.sms_status is not None:
            data["sms_status"] = self.sms_status
        if self.campaign_id is not None:
            data["campaign_id"] = self.campaign_id
        if self.subscribe_ip is not None:
            data["subscribe_ip"] = self.subscribe_ip
        if self.double_optin is not None:
            data["double_optin"] = self.double_optin
        if self.is_deleted is not None:
            data["is_deleted"] = self.is_deleted
            
        return data


@dataclass
class GroupAddMultipleContactsDTO(BaseDTO):
    """
    Data transfer object for adding multiple contacts to a group.
    """
    group_id: int
    sms: List[dict]
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'group_id': 'groupId'
    }


@dataclass
class GroupRemoveContactDTO(BaseDTO):
    """
    Data transfer object for removing a contact from a group.
    """
    group_id: int
    sms: str
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'group_id': 'groupId'
    }


@dataclass
class GroupRemoveMultipleContactsDTO(BaseDTO):
    """
    Data transfer object for removing multiple contacts from a group.
    """
    group_id: int
    sms: List[str]
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'group_id': 'groupId'
    } 