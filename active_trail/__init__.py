"""
ActiveTrail SDK - Unofficial SDK for ActiveTrail service.

This package provides a simple, Pythonic interface to the ActiveTrail API.
"""

__version__ = "0.1.0"

from .client import ActiveTrailClient
from .contacts import ContactsAPI
from .campaigns import CampaignsAPI
from .messages import MessagesAPI
from .webhooks import WebhooksAPI
from .exceptions import ActiveTrailError, AuthenticationError, RateLimitError 