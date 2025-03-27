# ActiveTrail SDK for Python

An unofficial Python SDK for the [ActiveTrail](https://www.activetrail.com/) email marketing and automation platform.

## Features

- Complete coverage of ActiveTrail API endpoints:
  - Contacts management
  - Email campaigns
  - SMS campaigns 
  - Operational emails
  - Operational SMS messages
  - Webhooks
  - Templates
- Proper error handling with specific exception types
- Type hints for better IDE support
- Comprehensive documentation
- Clean, Pythonic API

## Installation

```bash
pip install activetrail-sdk
```

## Quick Start

```python
from active_trail import ActiveTrailClient

# Initialize the client
client = ActiveTrailClient(api_key="your_api_key")

# Get contacts
contacts = client.contacts.list(limit=10)
print(contacts)

# Create a contact
new_contact = client.contacts.create({
    "email": "example@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "0512345678"  # Israeli phone format
})

# Send an operational email
response = client.operational_messages.send_email(
    subject="Welcome!",
    html_content="<p>Thank you for signing up!</p>",
    recipients=[{"email": "recipient@example.com", "name": "Recipient Name"}],
    sender_email="sender@example.com",
    sender_name="Sender Name"
)

# Send an SMS message
response = client.operational_messages.send_sms(
    message="Your verification code is 123456",
    recipients=["0512345678"],
    sender_id="YourBrand"
)

# Create and schedule an email campaign
campaign = client.email_campaigns.create({
    "name": "Monthly Newsletter",
    "subject": "Our Latest Updates",
    "html_content": "<h1>Monthly Newsletter</h1><p>Hello from our team!</p>",
    "groups": ["group_id_1", "group_id_2"],
    "from_email": "newsletter@example.com",
    "from_name": "Your Brand"
})

# Schedule the campaign for tomorrow
import datetime
tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
client.email_campaigns.schedule(campaign["id"], {
    "send_time": tomorrow.isoformat(),
    "time_zone": "Asia/Jerusalem"
})
```

## Module Structure

The SDK is organized into specialized modules:

- `contacts.py` - Manage contacts and their properties
- `email_campaigns.py` - Create and manage email campaigns
- `sms_campaigns.py` - Create and manage SMS campaigns 
- `operational_messages.py` - Send transactional emails and SMS
- `webhooks.py` - Manage webhook subscriptions
- `campaigns.py` - Base campaign functionality and templates
- `messages.py` - Base message functionality

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from active_trail import ActiveTrailClient
from active_trail.exceptions import (
    ActiveTrailError,  # Base exception
    AuthenticationError,  # Authentication issues
    RateLimitError,  # API rate limit exceeded
    ValidationError,  # Invalid request data
    NotFoundError,  # Resource not found
    ServerError  # Server-side errors
)

client = ActiveTrailClient(api_key="your_api_key")

try:
    contacts = client.contacts.list()
except AuthenticationError:
    print("Check your API key")
except RateLimitError:
    print("Rate limit exceeded, try again later")
except ValidationError as e:
    print(f"Invalid request: {e}")
except ActiveTrailError as e:
    print(f"An error occurred: {e}")
```

## Documentation

For detailed documentation, see [docs/](docs/).

## Development

### Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements-dev.txt`

### Running Tests

```bash
pytest
```

## License

MIT

## Contributing

Contributions are more than welcome! Please feel free to join the effort by sending a pull request. 