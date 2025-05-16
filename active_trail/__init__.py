"""
ActiveTrail SDK - Unofficial SDK for ActiveTrail service.

This package provides a simple, Pythonic interface to the ActiveTrail API.
"""

__version__ = "0.2.2"

from .client import ActiveTrailClient
from .contacts import ContactsAPI
from .sms_campaigns import SMSCampaignsAPI
from .groups import GroupsAPI
from .base_api import BaseAPI, CrudAPI, NestedResourceAPI, CampaignBaseAPI
from .exceptions import (
    ActiveTrailError, 
    AuthenticationError, 
    RateLimitError, 
    ValidationError, 
    NotFoundError,
    ServerError,
    NetworkError
) 