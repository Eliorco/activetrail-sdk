"""
Simple usage example for the ActiveTrail SDK.

This module demonstrates the usage of the ActiveTrail SDK through examples
that can be run individually or all together.
"""

import os
import logging
import datetime
import argparse
import sys
from typing import Optional, Dict, List, Any

from active_trail import ActiveTrailClient
from active_trail.dto.sms_campaigns import ApiSmsCampaignSegment
from active_trail.utils import configure_logging
from active_trail.exceptions import ActiveTrailError, ValidationError, NotFoundError
from active_trail.dto import (
    ContactDTO,
    SMSCampaignDTO,
    GroupDTO,
    SMSCampaignSchedulingDTO
)


def get_client() -> Optional[ActiveTrailClient]:
    """
    Get the ActiveTrail client instance.
    
    Returns:
        ActiveTrailClient: The client instance or None if API key is not set.
    """
    # Get API key from environment variable
    api_key = os.environ.get("ACTIVETRAIL_API_KEY")
    if not api_key:
        print("Error: ACTIVETRAIL_API_KEY environment variable is required")
        return None
    
    # Initialize the client
    return ActiveTrailClient(api_key=api_key)


def example_get_contacts(client: ActiveTrailClient) -> bool:
    """
    Example 1: Get a list of contacts.
    
    Args:
        client: The ActiveTrail client instance.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print("\n=== Getting contacts ===")
        contacts = client.contacts.list(limit=5)
        print(f"Found {len(contacts.get('contacts', []))} contacts")
        return True
    except ActiveTrailError as e:
        print(f"Error getting contacts: {e}")
        return False


def example_create_contact(client: ActiveTrailClient) -> bool:
    """
    Example 2: Create a new contact.
    
    Args:
        client: The ActiveTrail client instance.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print("\n=== Creating a contact ===")
        # Create contact using DTO
        contact = ContactDTO(
            email=f"example_{datetime.datetime.now().timestamp()}@example.com",
            first_name="John",
            last_name="Doe",
            phone="1234567890"
        )
        new_contact = client.contacts.create(contact)
        print(f"Created contact: {new_contact.get('id')}")
        return True
    except ActiveTrailError as e:
        print(f"Error creating contact: {e}")
        return False


def example_send_operational_email(client: ActiveTrailClient) -> bool:
    """
    Example 3: Send an operational email.
    
    Args:
        client: The ActiveTrail client instance.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print("\n=== Sending an operational email ===")
        # Create sender using DTO
        sender = EmailMessageSenderDTO(
            name="Test Sender",
            email="sender@example.com"
        )
        
        # Create email message using DTO
        email = EmailMessageDTO(
            subject="Test Email from SDK",
            html_content="<p>Hello from the ActiveTrail SDK!</p>",
            recipients=["recipient@example.com"],
            sender=sender,
            track_opens=True,
            track_clicks=True
        )
        
        # Send using the DTO
        email_result = client.operational_messages.send_email(
            subject=email.subject,
            html_content=email.html_content,
            recipients=email.recipients,
            sender_name=email.sender.name,
            sender_email=email.sender.email,
            track_opens=email.track_opens,
            track_clicks=email.track_clicks
        )
        
        print(f"Email sent: {email_result}")
        return True
    except ActiveTrailError as e:
        print(f"Error sending operational email: {e}")
        return False


def example_send_operational_sms(client: ActiveTrailClient) -> bool:
    """
    Example 4: Send an operational SMS.
    
    Args:
        client: The ActiveTrail client instance.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print("\n=== Sending an operational SMS ===")
        # Create SMS message using DTO
        sms = SMSMessageDTO(
            message="Hello from ActiveTrail SDK!",
            recipients=["1234567890", "0987654321"],
            sender_id="TestSender"
        )
        
        # Send using the DTO
        sms_result = client.operational_messages.send_sms(
            message=sms.message,
            recipients=sms.recipients,
            sender_id=sms.sender_id
        )
        
        print(f"SMS sent: {sms_result}")
        return True
    except ActiveTrailError as e:
        print(f"Error sending operational SMS: {e}")
        return False


def example_create_and_schedule_email_campaign(client: ActiveTrailClient) -> bool:
    """
    Example 5: Create and schedule an email campaign.
    
    Args:
        client: The ActiveTrail client instance.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print("\n=== Creating an email campaign ===")
        # Create sender using DTO
        sender = EmailCampaignSenderDTO(
            name="Test Sender",
            email="sender@example.com"
        )
        
        # Create campaign using DTO
        campaign = EmailCampaignDTO(
            name=f"Test Campaign {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            subject="Test Email Campaign",
            html_content="<p>This is a test email campaign</p>",
            sender=sender,
            groups=[1, 2]  # Example group IDs
        )
        
        campaign_result = client.email_campaigns.create(campaign)
        campaign_id = campaign_result.get("id")
        print(f"Created campaign: {campaign_id}")
        
        # Schedule the campaign
        print("\n=== Scheduling the campaign ===")
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        scheduled_time = tomorrow.isoformat()
        
        schedule_result = client.email_campaigns.schedule(campaign_id, scheduled_time)
        print(f"Scheduled campaign: {schedule_result}")
        
        # Get campaign statistics (would normally be done after sending)
        try:
            print("\n=== Getting campaign statistics ===")
            stats = client.email_campaigns.get_statistics(campaign_id)
            print(f"Campaign stats: {stats}")
        except NotFoundError:
            print("Campaign statistics not available yet (campaign not sent)")
        
        return True
    except ActiveTrailError as e:
        print(f"Error working with email campaign: {e}")
        return False


def example_create_sms_campaign(client: ActiveTrailClient) -> bool:
    """
    Example 6: Create an SMS campaign.
    
    Args:
        client: The ActiveTrail client instance.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print("\n=== Creating an SMS campaign ===")
        
        # Create tomorrow's date for scheduling
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        
        # Create segment and scheduling objects
        segment = ApiSmsCampaignSegment(
            group_ids=[1, 2]  # Example group IDs
        )
        
        scheduling = SMSCampaignSchedulingDTO(
            scheduled_date=tomorrow,
            scheduled_time_zone="50",  # Default time zone
            is_sent=False
        )
        
        # Create SMS campaign using DTO
        sms_campaign = SMSCampaignDTO(
            name=f"Test SMS Campaign {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            content="This is a test SMS campaign",
            unsubscribe_text="Reply STOP to unsubscribe",
            segment=segment,
            scheduling=scheduling,
            from_name="TestSender",
            can_unsubscribe=True,
            is_link_tracking=True
        )
        
        sms_campaign_result = client.sms_campaigns.create(sms_campaign)
        sms_campaign_id = sms_campaign_result.get("id")
        print(f"Created SMS campaign: {sms_campaign_id}")
        return True
    except ActiveTrailError as e:
        print(f"Error creating SMS campaign: {e}")
        return False


def example_manage_webhooks(client: ActiveTrailClient) -> bool:
    """
    Example 7: Manage webhooks (list, create, test, delete).
    
    Args:
        client: The ActiveTrail client instance.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print("\n=== Managing webhooks ===")
        webhooks = client.webhooks.list()
        print(f"Found {len(webhooks.get('webhooks', []))} webhooks")
        
        # Create a webhook using DTO
        webhook = WebhookDTO(
            event_type="contact.created",
            url="https://example.com/webhook",
            state_type="active"
        )
        
        # Create the webhook
        print("\n=== Creating a webhook ===")
        webhook_data = client.webhooks.create(webhook)
        webhook_id = webhook_data.get("id")
        print(f"Created webhook: {webhook_id}")
        
        # Test the webhook
        print("\n=== Testing the webhook ===")
        test_result = client.webhooks.test(webhook_id)
        print(f"Webhook test result: {test_result}")
        
        # Delete the webhook
        print("\n=== Deleting the webhook ===")
        client.webhooks.delete(webhook_id)
        print(f"Deleted webhook: {webhook_id}")
        return True
    except ActiveTrailError as e:
        print(f"Error managing webhooks: {e}")
        return False


def example_work_with_groups(client: ActiveTrailClient) -> bool:
    """
    Example 8: Work with contact groups.
    
    Args:
        client: The ActiveTrail client instance.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print("\n=== Working with groups ===")
        
        # List groups
        groups = client.groups.list(limit=5)
        print(f"Found {len(groups.get('groups', []))} groups")
        
        # Create a group using DTO
        group_name = f"Test Group {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        group = GroupDTO(
            name=group_name,
            description="A test group created by the SDK"
        )
        
        new_group = client.groups.create(group)
        group_id = new_group.get("id")
        print(f"Created group: {group_id}")
        
        # Get contacts in the group
        group_contacts = client.groups.get_contacts(group_id)
        print(f"Group has {len(group_contacts.get('contacts', []))} contacts")
        
        # Add a contact to the group
        contact_email = f"example_{datetime.datetime.now().timestamp()}@example.com"
        contact = ContactDTO(email=contact_email)
        client.contacts.create(contact)
        client.groups.add_contact(group_id, contact_email)
        print(f"Added contact {contact_email} to group")
        
        # Delete the group
        client.groups.delete(group_id)
        print(f"Deleted group: {group_id}")
        
        return True
    except ActiveTrailError as e:
        print(f"Error working with groups: {e}")
        return False


def example_two_way_sms(client: ActiveTrailClient) -> bool:
    """
    Example 9: Work with two-way SMS.
    
    Args:
        client: The ActiveTrail client instance.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print("\n=== Working with two-way SMS ===")
        
        # List SMS replies
        replies = client.two_way_sms.list(limit=5)
        print(f"Found {len(replies.get('replies', []))} SMS replies")
        
        # If there are replies, respond to the first one
        if replies.get('replies'):
            reply_id = replies['replies'][0]['id']
            response = client.two_way_sms.respond(
                reply_id=reply_id,
                message="Thank you for your response!"
            )
            print(f"Sent response to SMS reply: {response}")
        
        return True
    except ActiveTrailError as e:
        print(f"Error working with two-way SMS: {e}")
        return False


def example_sms_reports(client: ActiveTrailClient) -> bool:
    """
    Example 10: Work with SMS reports.
    
    Args:
        client: The ActiveTrail client instance.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print("\n=== Working with SMS reports ===")
        
        # List SMS reports
        reports = client.sms_reports.list(limit=5)
        print(f"Found {len(reports.get('reports', []))} SMS reports")
        
        # If there are reports, get details for the first one
        if reports.get('reports'):
            report_id = reports['reports'][0]['id']
            details = client.sms_reports.get_details(report_id)
            print(f"SMS report details: {details}")
        
        return True
    except ActiveTrailError as e:
        print(f"Error working with SMS reports: {e}")
        return False


def run_examples(examples_to_run: List[str], client: ActiveTrailClient) -> Dict[str, bool]:
    """
    Run the specified examples.
    
    Args:
        examples_to_run: List of example names to run.
        client: The ActiveTrail client instance.
        
    Returns:
        Dict[str, bool]: Dictionary with example names as keys and success status as values.
    """
    # Map of available examples
    examples = {
        "contacts": example_get_contacts,
        "create_contact": example_create_contact,
        "email": example_send_operational_email,
        "sms": example_send_operational_sms,
        "email_campaign": example_create_and_schedule_email_campaign,
        "sms_campaign": example_create_sms_campaign,
        "webhooks": example_manage_webhooks,
        "groups": example_work_with_groups,
        "two_way_sms": example_two_way_sms,
        "sms_reports": example_sms_reports
    }
    
    # If "all" is in the list, run all examples
    if "all" in examples_to_run:
        examples_to_run = list(examples.keys())
    
    # Run the specified examples and collect results
    results = {}
    for example_name in examples_to_run:
        if example_name in examples:
            print(f"\n\n{'=' * 40}\nRunning example: {example_name}\n{'=' * 40}")
            results[example_name] = examples[example_name](client)
        else:
            print(f"Unknown example: {example_name}")
            results[example_name] = False
    
    return results


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="ActiveTrail SDK usage examples")
    
    parser.add_argument(
        "--examples", 
        nargs="+", 
        default=["all"],
        help="Examples to run. Options: contacts, create_contact, email, sms, email_campaign, " + 
             "sms_campaign, webhooks, groups, two_way_sms, sms_reports, all"
    )
    
    return parser.parse_args()


def main():
    """Run the examples."""
    # Parse command line arguments
    args = parse_args()
    
    # Configure logging
    configure_logging(level=logging.INFO)
    
    # Get client
    client = get_client()
    if not client:
        return 1
    
    # Run examples
    results = run_examples(args.examples, client)
    
    # Print summary
    print("\n\n" + "=" * 40)
    print("EXECUTION SUMMARY")
    print("=" * 40)
    
    for example, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{example}: {status}")
    
    # Return non-zero exit code if any example failed
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main()) 