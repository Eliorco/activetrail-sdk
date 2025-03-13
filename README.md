# ActiveTrail SDK for Python

An unofficial Python SDK for the [ActiveTrail](https://www.activetrail.com/) email marketing and automation platform.

## Features

- Synchronous and asynchronous API clients
- Complete coverage of ActiveTrail API endpoints:
  - Contacts management
  - Campaigns 
  - Transactional emails
  - SMS messages
  - Webhooks
- Proper error handling
- Type hints for better IDE support
- Comprehensive test suite

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
contacts = client.contacts.list(params={"limit": 10})
print(contacts)

# Create a contact
new_contact = client.contacts.create({
    "email": "example@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "0512345678"  # Israeli phone format
})

# Send a transactional email
response = client.messages.send_email({
    "subject": "Welcome!",
    "html_content": "<p>Thank you for signing up!</p>",
    "recipients": [{"email": "recipient@example.com", "name": "Recipient Name"}],
    "sender": {
        "email": "sender@example.com",
        "name": "Sender Name"
    }
})
```

## Async Usage

```python
import asyncio
from active_trail.client import AsyncActiveTrailClient

async def main():
    # Initialize the async client
    client = AsyncActiveTrailClient(api_key="your_api_key")
    
    try:
        # Setup the client
        await client.setup()
        
        # Get contacts
        contacts = await client.get("contacts")
        print(contacts)
    finally:
        # Always close the client
        await client.close()

# Run the async function
asyncio.run(main())
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

Contributions are more then welcome! Please feel free to join the effort, by sending a pull request. 