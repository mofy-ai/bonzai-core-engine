"""
🚀 GitHub AI Integration Test
Test the new GitHub AI models integration in Bonzai Core Engine
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Test configuration
BASE_URL = "http://localhost:5001"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def test_github_ai_endpoints():
    """Test all GitHub AI endpoints"""
    
    print("🚀 Testing GitHub AI Integration in Bonzai Core Engine")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/github-ai/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test 2: Get available models
    print("\n2. Testing available models...")
    try:
        response = requests.get(f"{BASE_URL}/api/github-ai/models")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Available models: {data.get('count', 0)}")
        for model_key, model_name in data.get('models', {}).items():
            print(f"  - {model_key}: {model_name}")
    except Exception as e:
        print(f"Models test failed: {e}")
    
    # Test 3: Connection test
    print("\n3. Testing connection...")
    try:
        response = requests.get(f"{BASE_URL}/api/github-ai/test")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Connection test failed: {e}")
    
    # Test 4: Simple completion
    print("\n4. Testing simple completion...")
    try:
        payload = {
            "prompt": "Hello! Please respond with 'GitHub AI integration successful'",
            "model": "gpt-4o-mini"
        }
        response = requests.post(f"{BASE_URL}/api/github-ai/simple", json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {data.get('response', 'No response')}")
    except Exception as e:
        print(f"Simple completion test failed: {e}")
    
    # Test 5: Chat completion
    print("\n5. Testing chat completion...")
    try:
        payload = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France?"}
            ],
            "model": "gpt-4o-mini",
            "temperature": 0.7
        }
        response = requests.post(f"{BASE_URL}/api/github-ai/chat", json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {data.get('response', 'No response')}")
    except Exception as e:
        print(f"Chat completion test failed: {e}")
    
    # Test 6: Code assistance
    print("\n6. Testing code assistance...")
    try:
        payload = {
            "code_context": "def calculate_sum(a, b):",
            "request": "Complete this function to add two numbers and return the result",
            "model": "gpt-4o-mini"
        }
        response = requests.post(f"{BASE_URL}/api/github-ai/code-assist", json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {data.get('response', 'No response')[:200]}...")
    except Exception as e:
        print(f"Code assistance test failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ GitHub AI Integration Test Complete!")

if __name__ == "__main__":
    test_github_ai_endpoints()