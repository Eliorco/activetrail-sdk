"""
Utility functions for the ActiveTrail SDK.
"""

import logging
from typing import Dict, Any, Optional
import re

def configure_logging(
    level: int = logging.INFO,
    format_string: Optional[str] = None
) -> None:
    """
    Configure logging for the ActiveTrail SDK.
    
    Args:
        level: Logging level (default: INFO)
        format_string: Custom logging format
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
    logging.basicConfig(
        level=level,
        format=format_string
    )


def validate_email(email: str) -> bool:
    """
    Simple validation for email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if the email format is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_israeli_phone_number(phone: str) -> bool:
    """
    Validate Israeli phone number format.
    
    Args:
        phone: Phone number to validate
    """
    pattern = r'^(\+972|0)([5][0-9]{8})$'
    return bool(re.match(pattern, phone))

def prepare_contact_payload(
    email: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    phone: Optional[str] = None,
    custom_fields: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a standardized contact payload.
    
    Args:
        email: Contact email address
        first_name: First name
        last_name: Last name
        phone: Phone number
        custom_fields: Additional custom fields
        
    Returns:
        Formatted contact payload for API
    """
    if not validate_email(email):
        raise ValueError(f"Invalid email format: {email}")
        
    if phone and not validate_israeli_phone_number(phone):
        raise ValueError(f"Invalid Israeli phone number format: {phone}")
    
    payload = {
        "email": email
    }
    
    if first_name:
        payload["first_name"] = first_name
        
    if last_name:
        payload["last_name"] = last_name
        
    if phone:
        payload["phone"] = phone
    
    if custom_fields:
        payload["custom_fields"] = custom_fields
        
    return payload 