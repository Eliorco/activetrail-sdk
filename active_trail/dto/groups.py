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
    email: str


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


@dataclass
class GroupAddContactDTO(BaseDTO):
    """
    Data transfer object for adding a contact to a group.
    """
    group_id: int
    email: str
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'group_id': 'groupId'
    }


@dataclass
class GroupAddMultipleContactsDTO(BaseDTO):
    """
    Data transfer object for adding multiple contacts to a group.
    """
    group_id: int
    emails: List[str]
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'group_id': 'groupId'
    }


@dataclass
class GroupRemoveContactDTO(BaseDTO):
    """
    Data transfer object for removing a contact from a group.
    """
    group_id: int
    email: str
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'group_id': 'groupId'
    }


@dataclass
class GroupRemoveMultipleContactsDTO(BaseDTO):
    """
    Data transfer object for removing multiple contacts from a group.
    """
    group_id: int
    emails: List[str]
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'group_id': 'groupId'
    } 