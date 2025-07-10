"""
Quick Ultimate Mem0 Tester for Mama Bear
Tests if the deployment is working after Claude Code's crash
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "https://mofy.ai"
API_KEY = "bz_ultimate_enterprise_123"

print("🔥 ULTIMATE MEM0 QUICK TEST")
print("Testing deployment after Claude Code crash")
print(f"Time: {datetime.now()}")
print("=" * 60)

# Test 1: Health Check
print("\n1. Health Check (no auth):")
try:
    response = requests.get(f"{BASE_URL}/api/health", timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("   ✅ SUCCESS - JSON works!")
        print(f"   Service: {data.get('service', 'Unknown')}")
        print(f"   Family System: {data.get('family_system', {}).get('family_system', 'Unknown')}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 2: Root endpoint
print("\n2. Root Endpoint:")
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("   ✅ SUCCESS")
        print(f"   Endpoints: {data.get('endpoints', 0)}")
        print(f"   Optimization: {data.get('optimization_level', 'Unknown')}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 3: Validate API Key
print("\n3. API Key Validation:")
try:
    response = requests.post(
        f"{BASE_URL}/api/keys/validate",
        json={"key": API_KEY},
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("   ✅ API Key Valid!")
        print(f"   User: {data.get('key_data', {}).get('user_id', 'Unknown')}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 4: Add Memory (with auth)
print("\n4. Add Memory Test:")
try:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(
        f"{BASE_URL}/api/memory/add",
        headers=headers,
        json={
            "content": "Test from Mama Bear after Claude Code crash",
            "category": "recovery_test"
        },
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Memory Added Successfully!")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE!")
print("\nIf you see SUCCESS messages, the Ultimate Mem0 is working!")
print("If you see ERRORS, check Railway deployment status.")
