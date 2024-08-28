# sdxlib

**sdxlib** is a Python client library designed for interacting with the AtlanticWave-SDX L2VPN API. It provides a convenient interface for managing L2VPN services, including creation, updating, retrieval, and deletion.

## Features

- **Create L2VPN**: Create a new L2VPN service with customizable configurations.
- **Update L2VPN**: Modify attributes of an existing L2VPN service.
- **Retrieve L2VPN**: Fetch details of a specific L2VPN service using its ID.
- **List All L2VPNs**: Retrieve a list of all L2VPN services, optionally filtered by archived date.
- **Delete L2VPN**: Remove an existing L2VPN service based on its ID.

## Installation

You can install **sdxlib** using pip:

```bash
pip install sdxlib
```

## Usage

Here's a basic example of how to use **sdxlib**:

```python
from sdxlib.sdx_client import SDXClient
from sdxlib.sdx_exception import SDXException

# Initialize SDXClient with base URL and other parameters
client = SDXClient(base_url='https://example.com/sdx-api', name='example-l2vpn', endpoints=[...])

# Create a new L2VPN service
response = client.create_l2vpn()
print("L2VPN service created:", response)

# Update an existing L2VPN service
required_service_id = 'example-service-id'
new_name = 'New Name'
new_state = 'enabled'
update_response = client.update_l2vpn(service_id=required_service_id, name=new_name, state=new_state)
print("L2VPN service updated:", update_response)

# Retrieve details of a specific L2VPN service
get_response = client.get_l2vpn(service_id=required_service_id)
print("Details of L2VPN service:", get_response)

# List all active L2VPN services
all_active_l2vpns = client.get_all_l2vpns()
print("All L2VPN services:", all_active_l2vpns)

# List all archived L2VPN services
all_archived_l2vpns = client.get_all_l2vpns(archived=True)
print("All L2VPN services:", all_archived_l2vpns)

# Delete an existing L2VPN service
delete_response = client.delete_l2vpn(service_id=required_service_id)
print("L2VPN service deleted:", delete_response)
```

## Documentation

For detailed API documentation and examples, refer to the [API Documentation](https://sdx-docs.readthedocs.io/en/latest/).

## Contributing

Contributions are welcome! Please read the [Contributing Guide]() for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE]() file for details.