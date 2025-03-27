"""
Data Transfer Objects for the ActiveTrail API.

This package contains all DTOs (Data Transfer Objects) used for
request and response parameters across the ActiveTrail API.

Each module contains DTOs for a specific API section.
"""

# Base DTO
from .base import BaseDTO

# Contacts
from .contacts import (
    ContactDTO,
    ContactListRequestDTO,
    ContactActivityDTO,
    ContactActivityRequestDTO,
    ContactUnsubscribeDTO,
    ContactMultipleUnsubscribeDTO,
    ContactResubscribeDTO,
    ContactMultipleResubscribeDTO,
)

# Campaigns (needed for SMS campaigns)
from .campaigns import (
    CampaignListRequestDTO,
    CampaignDuplicateRequestDTO,
)

# SMS Campaigns
from .sms_campaigns import (
    SMSCampaignDTO,
    SMSCampaignResponseDTO,
    SMSCampaignScheduleDTO,
    SMSCampaignTestDTO,
    SMSCampaignSendDTO,
    SMSCampaignStatisticsDTO,
    SMSCampaignRecipientsRequestDTO,
    ApiSmsCampaignSegment,
    SMSCampaignSchedulingDTO,
    CampaignScheduleBaseDTO
)

# Groups
from .groups import (
    GroupDTO,
    GroupResponseDTO,
    GroupListRequestDTO,
    GroupContactDTO,
    GroupContactsRequestDTO,
    GroupAddContactDTO,
    GroupAddMultipleContactsDTO,
    GroupRemoveContactDTO,
    GroupRemoveMultipleContactsDTO,
)
