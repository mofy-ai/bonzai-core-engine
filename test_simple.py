#!/usr/bin/env python3
"""Simple test to check what's working"""

import requests
import json

BASE_URL = "https://mofy.ai"

# Test 1: Basic health check
print("1. Testing /api/health...")
try:
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Debug endpoint
print("\n2. Testing /api/debug...")
try:
    response = requests.get(f"{BASE_URL}/api/debug")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Family System: {data.get('family_system_status')}")
    print(f"   API Key Manager: {data.get('api_key_manager_status')}")
    print(f"   Mem0 Test: {data.get('mem0_test_initialization')}")
    if 'mem0_test_operation' in data:
        print(f"   Mem0 Operation: {data.get('mem0_test_operation')}")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Simple chat without fancy characters
print("\n3. Testing /api/chat with simple message...")
try:
    headers = {
        "Authorization": "Bearer bz_ultimate_enterprise_123",
        "Content-Type": "application/json"
    }
    data = {
        "message": "Hello test",  # Simple ASCII message
        "model": "claude"
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
    else:
        print(f"   Error: {response.text[:200]}...")
except Exception as e:
    print(f"   Error: {e}")

print("\n4. Testing root endpoint...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Endpoints: {data.get('endpoints', 0)}")
    print(f"   Family System: {data.get('family_system', 'unknown')}")
except Exception as e:
    print(f"   Error: {e}")
