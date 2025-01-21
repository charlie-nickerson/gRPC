import grpc
import json
import requests
from chirpstack_api import api
from google.protobuf.json_format import ParseDict

class ChirpStackClient:
    def __init__(self, server_address, api_token):
        self.server_address = server_address
        self.api_token = api_token
        self.base_url = f"http://{server_address.split(':')[0]}:8090"
        
        print(f"Initializing connection to {server_address}")
        
        # Set up the headers we'll use for REST API calls
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

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
    
    # # Device creation parameters
    # new_device = {
    #     "name": "new-device-1",
    #     "description": "Test LoRaWAN device created via API",
    #     "dev_eui": "a8610a35392c6606",
    #     "application_id": config['application_id'],
    #     "device_profile_id": "34b2ec28-04a4-46cc-b9f5-ff0efc83e4c3"  # Your provided profile ID
    # }
    
    dev_eui = "a8610a35392c6606"
    # Create the device
    print("\nAttempting to delete device...")
    result = client.delete_device(dev_eui)
    print("\nDeletion result:", result)