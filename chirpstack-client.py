import grpc
import json
from chirpstack_api import api
from google.protobuf.json_format import ParseDict

class ChirpStackClient:
    def __init__(self, server_address, api_token):
        options = [
            ('grpc.max_receive_message_length', 10 * 1024 * 1024),
            ('grpc.keepalive_time_ms', 30000),
            ('grpc.keepalive_timeout_ms', 10000)
        ]
        
        print(f"Initializing connection to {server_address}")
        self.channel = grpc.insecure_channel(server_address, options=options)
        
        self.metadata = [
            ('authorization', f'Bearer {api_token}')
        ]
        print("Using metadata:", self.metadata)
        
        # Initialize service stubs
        self.tenant_service = api.TenantServiceStub(self.channel)
        self.application_service = api.ApplicationServiceStub(self.channel)
        self.device_service = api.DeviceServiceStub(self.channel)

    def get_device(self, dev_eui):
        """Get details of a specific device"""
        try:
            request = api.GetDeviceRequest(
                dev_eui=dev_eui
            )
            
            print(f"Getting device with EUI: {dev_eui}")
            response = self.device_service.Get(
                request,
                metadata=self.metadata
            )
            
            return {"status": "success", "device": response}
            
        except grpc.RpcError as e:
            error_details = {
                "status": "error",
                "message": f"Failed to get device: {e.details()}",
                "code": e.code(),
                "debug_info": str(e)
            }
            print("Error details:", error_details)
            return error_details

    def list_devices(self, application_id, limit=10, offset=0):
        """List devices for a specific application"""
        try:
            request = api.ListDevicesRequest(
                limit=limit,
                offset=offset,
                applicationId=application_id
            )
            
            print(f"Listing devices for application {application_id}...")
            response = self.device_service.List(
                request,
                metadata=self.metadata
            )
            
            return {"status": "success", "devices": response}
            
        except grpc.RpcError as e:
            error_details = {
                "status": "error",
                "message": f"Failed to list devices: {e.details()}",
                "code": e.code(),
                "debug_info": str(e)
            }
            print("Error details:", error_details)
            return error_details

    def create_device(self, application_id, name, description, dev_eui):
        """Create a new device"""
        try:
            request = api.CreateDeviceRequest(
                device={
                    "applicationId": application_id,
                    "name": name,
                    "description": description,
                    "devEui": dev_eui
                }
            )
            
            print(f"Creating device '{name}' with EUI {dev_eui}...")
            response = self.device_service.Create(
                request,
                metadata=self.metadata
            )
            
            return {"status": "success", "device": response}
            
        except grpc.RpcError as e:
            error_details = {
                "status": "error",
                "message": f"Failed to create device: {e.details()}",
                "code": e.code(),
                "debug_info": str(e)
            }
            print("Error details:", error_details)
            return error_details

def load_config(config_file):
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        raise

if __name__ == "__main__":
    # Load configuration from JSON file
    try:
        config = load_config('chirpstack_config.json')
        print("Configuration loaded successfully")
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        exit(1)
    
    # Initialize client with config values
    client = ChirpStackClient(config['server_address'], config['api_token'])
    
    # Get specific device information
    print("\nGetting device information...")
    device_result = client.get_device(config['device_eui'])
    print("Device result:", device_result)
    
    # List all devices in the application
    print("\nListing all devices in application...")
    devices_result = client.list_devices(config['application_id'])
    print("Devices list:", devices_result)