import requests
import json

# Test the deployment
base_url = "https://mofy.ai"

print("Testing Ultimate Mem0 deployment...")
print("=" * 60)

# Test health endpoint
try:
    response = requests.get(f"{base_url}/api/health", timeout=10)
    print(f"Health Check: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Response successful - JSON parsing works!")
        print(f"Service: {data.get('service', 'Unknown')}")
        print(f"Status: {data.get('status', 'Unknown')}")
        print(f"Message: {data.get('message', 'Unknown')}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error testing health endpoint: {e}")

print("\n" + "=" * 60)

# Test root endpoint
try:
    response = requests.get(f"{base_url}/", timeout=10)
    print(f"Root Endpoint: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Response successful - JSON parsing works!")
        print(f"Service: {data.get('service', 'Unknown')}")
        print(f"Endpoints: {data.get('endpoints', 0)}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error testing root endpoint: {e}")
