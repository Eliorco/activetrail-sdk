"""
Tests for utility functions.
"""

import unittest
import logging
from active_trail.utils import validate_email, prepare_contact_payload


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_validate_email(self):
        """Test email validation."""
        # Valid emails
        self.assertTrue(validate_email("test@example.com"))
        self.assertTrue(validate_email("user.name+tag@example.co.uk"))
        self.assertTrue(validate_email("user123@sub.domain.co"))
        
        # Invalid emails
        self.assertFalse(validate_email("not_an_email"))
        self.assertFalse(validate_email("missing@domain"))
        self.assertFalse(validate_email("@domain.com"))
        self.assertFalse(validate_email("user@.com"))
        self.assertFalse(validate_email("user@domain."))
        
    def test_prepare_contact_payload(self):
        """Test contact payload preparation with Israeli phone number validation."""
        # Basic payload with email only (no phone validation)
        payload = prepare_contact_payload("test@example.com")
        self.assertEqual(payload, {"email": "test@example.com"})
        
        # Full payload with valid Israeli mobile number format (05XXXXXXXX)
        payload = prepare_contact_payload(
            email="full@example.com",
            first_name="John",
            last_name="Doe",
            phone="0512345678",  # Valid Israeli mobile format
            custom_fields={"industry": "Technology", "company_size": "50-100"}
        )
        
        expected = {
            "email": "full@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "0512345678",
            "custom_fields": {
                "industry": "Technology", 
                "company_size": "50-100"
            }
        }
        
        self.assertEqual(payload, expected)
        
        # Test with valid Israeli international number format (+972XXXXXXXXX)
        payload = prepare_contact_payload(
            email="international@example.com",
            first_name="Jane",
            last_name="Smith",
            phone="+972512345678"  # Valid Israeli international format
        )
        
        expected = {
            "email": "international@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "+972512345678"
        }
        
        self.assertEqual(payload, expected)
        
        # Test with invalid email
        with self.assertRaises(ValueError):
            prepare_contact_payload("invalid-email")
        
        # Test with invalid phone number (not in Israeli format)
        with self.assertRaises(ValueError):
            prepare_contact_payload("valid@example.com", phone="1234567890")  # Non-Israeli format


if __name__ == "__main__":
    unittest.main() 