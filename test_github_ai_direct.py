"""
🚀 Direct GitHub AI Client Test
Test the GitHub AI client functionality directly
"""

import os
import sys
from dotenv import load_dotenv

# Add services to path
sys.path.append('/mnt/c/vscodium/bonzai-core-engine')
sys.path.append('/mnt/c/vscodium/bonzai-core-engine/services')

load_dotenv()

def test_github_ai_client():
    """Test GitHub AI client directly"""
    
    print("🚀 Testing GitHub AI Client Direct Integration")
    print("=" * 60)
    
    try:
        from services.github_ai_client import GitHubAIClient, create_github_ai_client
        
        print("✅ Successfully imported GitHub AI client")
        
        # Test 1: Create client
        print("\n1. Creating GitHub AI client...")
        client = create_github_ai_client()
        print(f"✅ Client created with endpoint: {client.endpoint}")
        
        # Test 2: Get available models
        print("\n2. Getting available models...")
        models = client.get_available_models()
        print(f"✅ Found {len(models)} models:")
        for key, value in models.items():
            print(f"  - {key}: {value}")
        
        # Test 3: Test connection
        print("\n3. Testing connection...")
        is_connected = client.test_connection()
        print(f"✅ Connection test: {'PASSED' if is_connected else 'FAILED'}")
        
        # Test 4: Simple completion
        if is_connected:
            print("\n4. Testing simple completion...")
            response = client.simple_completion(
                "Hello! Please respond with 'GitHub AI working perfectly'",
                model="gpt-4o-mini"
            )
            print(f"✅ Response: {response}")
            
            # Test 5: Chat completion
            print("\n5. Testing chat completion...")
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is 2+2?"}
            ]
            response = client.chat(messages, model="gpt-4o-mini")
            print(f"✅ Chat response: {response}")
            
            # Test 6: Code completion
            print("\n6. Testing code completion...")
            response = client.code_completion(
                "def add_numbers(a, b):",
                "Complete this Python function to add two numbers",
                model="gpt-4o-mini"
            )
            print(f"✅ Code response: {response[:200]}...")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ Direct GitHub AI Client Test Complete!")

if __name__ == "__main__":
    test_github_ai_client()