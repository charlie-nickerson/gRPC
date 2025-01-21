# ChirpStack API Client Documentation

## Overview
The `ChirpStackClient` is a Python class that provides an interface for interacting with the ChirpStack LoRaWAN Network Server API. It simplifies the process of managing devices, applications, and device profiles through both REST and gRPC interfaces.

## Installation
Required packages:
```bash
pip install grpcio chirpstack-api requests
```

## Configuration
The client requires a configuration file (`chirpstack_config.json`) with the following structure:
```json
{
    "server_address": "your.server.address:8080",
    "api_token": "your-api-token",
    "application_id": "your-application-id",
    "device_profile_id": "your-device-profile-id"
}
```

## Class: ChirpStackClient

### Constructor
```python
client = ChirpStackClient(server_address, api_token)
```

Parameters:
- `server_address` (str): The address of your ChirpStack server (e.g., "example.com:8080")
- `api_token` (str): Your ChirpStack API authentication token

### Methods

#### create_device
Creates a new device in ChirpStack.

```python
result = client.create_device(
    application_id="app-id",
    name="device-name",
    description="device-description",
    dev_eui="device-eui",
    device_profile_id="profile-id"
)
```

Parameters:
- `application_id` (str): The ID of the application to add the device to
- `name` (str): Name for the device
- `description` (str): Description of the device
- `dev_eui` (str): Device EUI (unique identifier)
- `device_profile_id` (str): The ID of the device profile to use

Returns:
- Dictionary with status and message

#### list_devices
Lists devices in an application.

```python
result = client.list_devices(application_id="app-id")
```

Parameters:
- `application_id` (str): The ID of the application to list devices from

Returns:
- Dictionary containing list of devices

## Usage Example
```python
from chirpstack_client import ChirpStackClient

# Initialize client
client = ChirpStackClient(
    server_address="server.address:8080",
    api_token="your-api-token"
)

# Create a new device
new_device = {
    "name": "test-device",
    "description": "Test LoRaWAN device",
    "dev_eui": "a8610a35392c6606",
    "application_id": "your-app-id",
    "device_profile_id": "your-profile-id"
}

result = client.create_device(**new_device)
print(result)

# List devices
devices = client.list_devices(application_id="your-app-id")
print(devices)
```

## Error Handling
The client includes error handling for common API errors. All methods return a dictionary with at least:
- `status`: "success" or "error"
- `message`: Description of the result or error

Example error handling:
```python
result = client.create_device(**device_data)
if result["status"] == "error":
    print(f"Error creating device: {result['message']}")
else:
    print(f"Success: {result['message']}")
```

## Best Practices
1. Always store sensitive information like API tokens in configuration files
2. Use error handling when calling API methods
3. Validate device EUIs are in the correct format before sending
4. Keep track of device EUIs to ensure uniqueness

## Contributing
When extending this client:
1. Maintain consistent error handling
2. Add documentation for new methods
3. Follow the existing pattern for API calls
4. Include response validation

## Security Considerations
1. Never commit API tokens to version control
2. Use environment variables or secure configuration files
3. Implement proper token rotation procedures
4. Monitor API usage and implement rate limiting if needed