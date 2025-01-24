import grpc
import json
import requests
from chirpstack_api import api
from google.protobuf.json_format import ParseDict

class ChirpStackClient:
    def __init__(self, server_address, api_token):
        print(f"Token being used: {api_token}")  # Add this line
        self.server_address = server_address
        self.api_token = api_token
        self.base_url = f"http://{server_address.split(':')[0]}:8090"
        self.headers = {
            'Grpc-Metadata-Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }


    # # Device creation parameters
    # new_device = {
    #     "name": "new-device-1",
    #     "description": "Test LoRaWAN device created via API",
    #     "dev_eui": "a8610a35392c6606",
    #     "application_id": config['application_id'],
    #     "device_profile_id": "34b2ec28-04a4-46cc-b9f5-ff0efc83e4c3"  # Your provided profile ID
    # }


    def create_device(self, application_id, device_profile_id, name, dev_eui, description=""):
        """Create a new device using REST API"""
        try:
            url = f"{self.base_url}/api/devices"
            
            payload = {
                "device": {
                    "applicationId": application_id,
                    "deviceProfileId": device_profile_id,
                    "name": name,
                    "description": description,
                    "devEui": dev_eui,
                    "isDisabled": False,
                    "skipFcntCheck": False
                }
            }
            
            print("\nCreating device with payload:")
            print(json.dumps(payload, indent=2))
            
            response = requests.post(url, json=payload, headers=self.headers)
            
            if response.status_code == 200:
                return {
                    "status": "success", 
                    "message": f"Device {name} created successfully"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to create device: {response.text}",
                    "code": response.status_code
                }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create device: {str(e)}",
                "error": str(e)
            }
        
    def delete_device(self, dev_eui):
        url = f"{self.base_url}/api/devices/{dev_eui}"

        print("Deleting device\n")
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 200:
                return {
                    "status": "success", 
                    "message": f"Device {dev_eui} deleted successfully"
                }
        else:
            return {
                "status": "error",
                "message": f"Failed to delete device: {response.text}",
                "code": response.status_code
            }
    
    def get_device_metrics(self, dev_eui, start_time=None, end_time=None, aggregation=None):
        # Get metrics for a specific device within a time range.
        
        # Args:
        #     dev_eui (str): Device EUI to get metrics for
        #     start_time (str, optional): Start time in ISO format (e.g., "2023-01-01T00:00:00Z")
        #     end_time (str, optional): End time in ISO format (e.g., "2023-12-31T23:59:59Z")
            
        # Returns:
        #     dict: Response containing metrics data or error information
        try:
            # Construct base URL
            url = f"{self.base_url}/api/devices/{dev_eui}/link-metrics"
            
            # Add query parameters if time range is specified
            params = {}
            if start_time:
                params['start'] = start_time
            if end_time:
                params['end'] = end_time
            if aggregation:
                params["aggregation"] = aggregation
                
            print(f"\nGetting metrics for device {dev_eui}")
            print(f"Time range: {start_time} to {end_time}")
            
            # Make the request
            response = requests.get(
                url,
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                metrics_data = response.json()
                return {
                    "status": "success",
                    "metrics": metrics_data,
                    "message": "Metrics retrieved successfully"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to get metrics: {response.text}",
                    "code": response.status_code
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get metrics: {str(e)}",
                "error": str(e)
            }

    def get_devices(self):
        url = f"{self.base_url}/api/tenants"  # Try listing tenants first
        response = requests.get(url, headers=self.headers)
        print(f"Response: {response.text}")  # Add this to see full response
        
        if response.status_code == 200:
            return {
                "status": "success",
                "devices": response.json(),
                "message": "Devices retrieved successfully"
            }
        return {
            "status": "error",
            "message": f"Failed to get devices: {response.text}",
            "code": response.status_code
        }


def load_config(config_file):
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        raise

if __name__ == "__main__":
    # Load configuration
    try:
        config = load_config('chirpstack_config.json')
        print("Configuration loaded successfully")
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        exit(1)
    
    # Initialize client
    client = ChirpStackClient(config['server_address'], config['api_token'])
    

    
    channel = grpc.insecure_channel(config['server_address'])
    client = api.DeviceServiceStub(channel)  # Changed from GatewayServiceStub

    # Set up auth metadata
    metadata = [("authorization", f"Bearer {config['api_token']}")]

    # Create and send request
    req = api.ListDevicesRequest()
    req.application_id = config["application_id"]
    req.limit = 1000

    resp = client.List(req, metadata=metadata)

    print(resp)

