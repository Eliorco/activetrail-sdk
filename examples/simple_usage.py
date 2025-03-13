"""
Simple usage example for the ActiveTrail SDK.
"""

import os
import logging

from active_trail import ActiveTrailClient
from active_trail.utils import configure_logging, prepare_contact_payload
from active_trail.exceptions import ActiveTrailError


def main():
    """Run the example."""
    # Configure logging
    configure_logging(level=logging.INFO)
    
    # Get API key from environment variable
    api_key = os.environ.get("ACTIVETRAIL_API_KEY")
    if not api_key:
        print("Error: ACTIVETRAIL_API_KEY environment variable is required")
        return
    
    # Initialize the client
    client = ActiveTrailClient(api_key=api_key)
    
    try:
        # Example 1: Get contacts
        print("\n=== Getting contacts ===")
        contacts = client.contacts.get_contacts(limit=5)
        print(f"Found {len(contacts.get('contacts', []))} contacts")
        
        # Example 2: Create a contact
        print("\n=== Creating a contact ===")
        contact_data = prepare_contact_payload(
            email="example@example.com",
            first_name="John",
            last_name="Doe",
            phone="1234567890"
        )
        new_contact = client.contacts.create_contact(contact_data)
        print(f"Created contact: {new_contact.get('id')}")
        
        # Example 3: Send transactional email
        print("\n=== Sending a transactional email ===")
        email_result = client.messages.send_transactional_email(
            subject="Test Email from SDK",
            html_content="<p>Hello from the ActiveTrail SDK!</p>",
            recipients=[{"email": "recipient@example.com", "name": "Test Recipient"}],
            sender_email="sender@example.com",
            sender_name="Test Sender"
        )
        print(f"Email sent: {email_result}")
        
        # Example 4: Work with campaigns
        print("\n=== Getting campaigns ===")
        campaigns = client.campaigns.get_campaigns(limit=3)
        print(f"Found {len(campaigns.get('campaigns', []))} campaigns")
        
        # Example 5: Working with webhooks
        print("\n=== Managing webhooks ===")
        webhooks = client.webhooks.get_webhooks()
        print(f"Found {len(webhooks)} webhooks")
        
    except ActiveTrailError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 