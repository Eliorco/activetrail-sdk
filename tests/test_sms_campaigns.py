"""
Tests for the SMS Campaigns API module.
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from pydantic import ValidationError

from active_trail.sms_campaigns import SMSCampaignsAPI
from active_trail.dto.sms_campaigns import (
    SMSCampaignDTO, 
    ApiSmsCampaignSegment, 
    SMSCampaignSchedulingDTO,
    SMSOperationalMessageDTO,
    ApiSMSCampaignDetailsDTO,
    ApiSmsCampaignSchedulingDTO,
    ApiSMSMobileDTO
)


class TestSMSCampaignsAPI(unittest.TestCase):
    """Test cases for the SMS Campaigns API."""

    def setUp(self):
        """Set up test environment."""
        self.mock_client = MagicMock()
        self.sms_campaigns_api = SMSCampaignsAPI(self.mock_client)
        
        # Common test data
        self.tomorrow = datetime.now() + timedelta(days=1)
        self.campaign_data = {
            "name": "Test Campaign",
            "content": "Test content with a code: TEST123",
            "unsubscribe_text": "Reply STOP to unsubscribe",
            "segment": {
                "group_ids": [123, 456]
            },
            "scheduling": {
                "scheduled_date": self.tomorrow.isoformat(),
                "scheduled_time_zone": "Israel",
                "is_sent": False
            },
            "from_name": "TestBrand",
            "can_unsubscribe": True,
            "is_link_tracking": True
        }
        
        self.operational_message_data = {
            "details": {
                "name": "Test Operational",
                "content": "Your code is 123456",
                "from_name": "TestApp"
            },
            "scheduling": {
                "send_now": True
            },
            "mobiles": [
                {"phone_number": "+1234567890"}
            ]
        }
    
    def test_get_campaigns(self):
        """Test getting SMS campaigns."""
        # Setup mock return value
        expected_result = {
            "sms_campaign": [
                {"id": 1, "name": "Campaign 1"},
                {"id": 2, "name": "Campaign 2"}
            ],
            "total_items": 2
        }
        self.mock_client.get.return_value = expected_result
        
        # Call the method
        from_date = datetime(2023, 1, 1)
        to_date = datetime(2023, 12, 31)
        result = self.sms_campaigns_api.get_campaigns(
            is_include_not_sent=True,
            from_date=from_date,
            to_date=to_date,
            search_term="Test",
            filter_type=1,
            page=1,
            limit=10
        )
        
        # Verify the client was called correctly
        self.mock_client.get.assert_called_once()
        call_args = self.mock_client.get.call_args
        self.assertEqual(call_args[0][0], "smscampaign/Campaign")
        
        # Check params
        params = call_args[1]["params"]
        self.assertEqual(params["IsIncludeNotSent"], True)
        self.assertEqual(params["FromDate"], from_date.isoformat())
        self.assertEqual(params["ToDate"], to_date.isoformat())
        self.assertEqual(params["SearchTerm"], "Test")
        self.assertEqual(params["FilterType"], 1)
        self.assertEqual(params["Page"], 1)
        self.assertEqual(params["Limit"], 10)
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_get_campaign(self):
        """Test getting a single SMS campaign."""
        # Setup mock return value
        expected_result = {
            "id": 123, 
            "name": "Test Campaign",
            "content": "Test content",
            "status_name": "Scheduled"
        }
        self.mock_client.get.return_value = expected_result
        
        # Call the method
        result = self.sms_campaigns_api.get_campaign(123)
        
        # Verify the client was called correctly
        self.mock_client.get.assert_called_once_with("smscampaign/Campaign/123")
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_create_with_dict(self):
        """Test creating an SMS campaign with dictionary input."""
        # Setup mock return value
        expected_result = {"id": 123, "name": "Test Campaign"}
        self.mock_client.post.return_value = expected_result
        
        # Call the method
        result = self.sms_campaigns_api.create(self.campaign_data)
        
        # Verify the client was called correctly
        self.mock_client.post.assert_called_once()
        call_args = self.mock_client.post.call_args
        self.assertEqual(call_args[0][0], "smscampaign/Campaign")
        
        # Verify request data has been transformed correctly
        json_data = call_args[1]["json"]
        self.assertEqual(json_data["name"], "Test Campaign")
        self.assertEqual(json_data["fromName"], "TestBrand")
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_create_with_pydantic_model(self):
        """Test creating an SMS campaign with Pydantic model input."""
        # Setup mock return value
        expected_result = {"id": 123, "name": "Test Campaign"}
        self.mock_client.post.return_value = expected_result
        
        # Create Pydantic models
        segment = ApiSmsCampaignSegment(group_ids=[123, 456])
        scheduling = SMSCampaignSchedulingDTO(
            scheduled_date=self.tomorrow,
            scheduled_time_zone="Israel",
            is_sent=False
        )
        campaign = SMSCampaignDTO(
            name="Test Campaign",
            content="Test content with a code: TEST123",
            unsubscribe_text="Reply STOP to unsubscribe",
            segment=segment,
            scheduling=scheduling,
            from_name="TestBrand",
            can_unsubscribe=True,
            is_link_tracking=True
        )
        
        # Call the method
        result = self.sms_campaigns_api.create(campaign)
        
        # Verify the client was called correctly
        self.mock_client.post.assert_called_once()
        call_args = self.mock_client.post.call_args
        self.assertEqual(call_args[0][0], "smscampaign/Campaign")
        
        # Verify request data has been transformed correctly
        json_data = call_args[1]["json"]
        self.assertEqual(json_data["name"], "Test Campaign")
        self.assertEqual(json_data["fromName"], "TestBrand")
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_update(self):
        """Test updating an SMS campaign."""
        # Setup mock return value
        expected_result = {"id": 123, "name": "Updated Campaign"}
        self.mock_client.put.return_value = expected_result
        
        # Update data
        update_data = self.campaign_data.copy()
        update_data["id"] = 123
        update_data["name"] = "Updated Campaign"
        
        # Call the method
        result = self.sms_campaigns_api.update(update_data)
        
        # Verify the client was called correctly
        self.mock_client.put.assert_called_once()
        call_args = self.mock_client.put.call_args
        self.assertEqual(call_args[0][0], "smscampaign/Campaign/123")
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_update_missing_id(self):
        """Test updating an SMS campaign without ID raises error."""
        # Update data without ID
        update_data = self.campaign_data.copy()  # No ID set
        
        # Call the method and expect ValueError
        with self.assertRaises(ValueError):
            self.sms_campaigns_api.update(update_data)
    
    def test_get_estimate(self):
        """Test getting campaign estimate."""
        # Setup mock return value
        expected_result = 1500  # 1500 messages estimated
        self.mock_client.get.return_value = expected_result
        
        # Call the method
        result = self.sms_campaigns_api.get_estimate(123)
        
        # Verify the client was called correctly
        self.mock_client.get.assert_called_once_with("smscampaign/Campaign/123/estimate")
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_send_operational_message_with_dict(self):
        """Test sending an operational message with dictionary input."""
        # Setup mock return value
        expected_result = {"id": 456, "name": "Test Operational"}
        self.mock_client.post.return_value = expected_result
        
        # Call the method
        result = self.sms_campaigns_api.send_operational_message(self.operational_message_data)
        
        # Verify the client was called correctly
        self.mock_client.post.assert_called_once()
        call_args = self.mock_client.post.call_args
        self.assertEqual(call_args[0][0], "smscampaign/OperationalMessage")
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_send_operational_message_with_pydantic_model(self):
        """Test sending an operational message with Pydantic model input."""
        # Setup mock return value
        expected_result = {"id": 456, "name": "Test Operational"}
        self.mock_client.post.return_value = expected_result
        
        # Create Pydantic models
        details = ApiSMSCampaignDetailsDTO(
            name="Test Operational",
            content="Your code is 123456",
            from_name="TestApp"
        )
        scheduling = ApiSmsCampaignSchedulingDTO(send_now=True)
        mobiles = [ApiSMSMobileDTO(phone_number="+1234567890")]
        
        message = SMSOperationalMessageDTO(
            details=details,
            scheduling=scheduling,
            mobiles=mobiles
        )
        
        # Call the method
        result = self.sms_campaigns_api.send_operational_message(message)
        
        # Verify the client was called correctly
        self.mock_client.post.assert_called_once()
        call_args = self.mock_client.post.call_args
        self.assertEqual(call_args[0][0], "smscampaign/OperationalMessage")
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_get_operational_message(self):
        """Test getting an operational message."""
        # Setup mock return value
        expected_result = {
            "id": 456, 
            "name": "Test Operational",
            "content": "Your code is 123456"
        }
        self.mock_client.get.return_value = expected_result
        
        # Call the method
        result = self.sms_campaigns_api.get_operational_message(456)
        
        # Verify the client was called correctly
        self.mock_client.get.assert_called_once_with("smscampaign/OperationalMessage/456")
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_update_operational_message(self):
        """Test updating an operational message."""
        # Setup mock return value
        expected_result = {
            "id": 456, 
            "name": "Updated Operational",
            "content": "Your updated code is 654321"
        }
        self.mock_client.put.return_value = expected_result
        
        # Update data
        update_data = self.operational_message_data.copy()
        update_data["details"]["name"] = "Updated Operational"
        update_data["details"]["content"] = "Your updated code is 654321"
        
        # Call the method
        result = self.sms_campaigns_api.update_operational_message(456, update_data)
        
        # Verify the client was called correctly
        self.mock_client.put.assert_called_once()
        call_args = self.mock_client.put.call_args
        self.assertEqual(call_args[0][0], "smscampaign/OperationalMessage/456")
        
        # Verify the result
        self.assertEqual(result, expected_result)
    
    def test_validation_error_campaign(self):
        """Test validation error for invalid campaign data."""
        # Campaign data with invalid from_name
        invalid_campaign = self.campaign_data.copy()
        invalid_campaign["from_name"] = "Invalid Name with Spaces"  # Contains spaces
        
        # Call the method and expect ValidationError
        with self.assertRaises(ValidationError):
            self.sms_campaigns_api.create(invalid_campaign)
    
    def test_validation_error_missing_required(self):
        """Test validation error for missing required fields."""
        # Campaign data missing required fields
        invalid_campaign = {
            "name": "Test Campaign",
            # Missing content, unsubscribe_text, segment, scheduling
            "from_name": "TestBrand"
        }
        
        # Call the method and expect ValidationError
        with self.assertRaises(ValidationError):
            self.sms_campaigns_api.create(invalid_campaign)
    
    def test_validation_error_phone_number(self):
        """Test validation error for invalid phone number."""
        # Message with invalid phone number
        invalid_message = self.operational_message_data.copy()
        invalid_message["mobiles"] = [{"phone_number": "1234567890"}]  # Missing + prefix
        
        # Call the method and expect ValidationError
        with self.assertRaises(ValidationError):
            self.sms_campaigns_api.send_operational_message(invalid_message)
    
    def test_validate_and_convert_type_error(self):
        """Test _validate_and_convert with wrong input type."""
        # Try to pass a string instead of dict/model
        with self.assertRaises(TypeError):
            self.sms_campaigns_api._validate_and_convert("not a dict or model", SMSCampaignDTO)


if __name__ == "__main__":
    unittest.main() 