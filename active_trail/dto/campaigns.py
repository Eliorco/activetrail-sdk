"""
Data Transfer Objects for Campaigns API.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, ClassVar
from .base import BaseDTO


@dataclass
class CampaignListRequestDTO(BaseDTO):
    """
    Request parameters for listing campaigns.
    """
    limit: Optional[int] = None
    offset: Optional[int] = None
    status: Optional[str] = None
    campaign_type: Optional[int] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'campaign_type': 'campaignType',
        'from_date': 'fromDate',
        'to_date': 'toDate'
    }
    
    _optional_fields: ClassVar[List[str]] = [
        'limit', 'offset', 'status', 'campaign_type', 'from_date', 'to_date'
    ]


@dataclass
class CampaignDuplicateRequestDTO(BaseDTO):
    """
    Request parameters for duplicating a campaign.
    """
    campaign_id: int
    new_name: str
    
    _api_field_mapping: ClassVar[Dict[str, str]] = {
        'campaign_id': 'campaignId',
        'new_name': 'newName'
    }
    