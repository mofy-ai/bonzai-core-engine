#!/usr/bin/env python3
"""
🔬 DIRECT MEM0 API TEST - Prove what's actually working
Tests Nathan's actual Mem0 deployment with real API calls
"""

import requests
import json
import os
from datetime import datetime

# Your actual Mem0 API configuration
MEM0_API_KEY = "m0-tBwWs1ygkxcbEiVvX6iXdwiJ42epw8a3wyoEUlpg"
MEM0_USER_ID = "nathan_sanctuary"
MEM0_BASE_URL = "https://api.mem0.ai/v1"

def test_mem0_api():
    """Test direct Mem0 API calls"""
    
    headers = {
        "Authorization": f"Bearer {MEM0_API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("🔬 TESTING DIRECT MEM0 API ACCESS")
    print("="*50)
    
    # Test 1: Add a memory
    print("🧠 Test 1: Adding memory to Mem0...")
    add_payload = {
        "messages": [
            {
                "role": "user",
                "content": "MCP server test completed at " + datetime.now().isoformat()
            }
        ],
        "user_id": MEM0_USER_ID
    }
    
    try:
        response = requests.post(
            f"{MEM0_BASE_URL}/memories",
            headers=headers,
            json=add_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Memory added successfully!")
            print(f"   📊 Response: {result}")
        else:
            print(f"❌ Failed to add memory: {response.status_code}")
            print(f"   📊 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception adding memory: {e}")
    
    print()
    
    # Test 2: Search memories
    print("🔍 Test 2: Searching memories...")
    search_payload = {
        "query": "bonzai",
        "user_id": MEM0_USER_ID
    }
    
    try:
        response = requests.post(
            f"{MEM0_BASE_URL}/memories/search",
            headers=headers,
            json=search_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            memories = result.get("memories", [])
            print(f"✅ Search successful!")
            print(f"   📊 Found {len(memories)} memories")
            
            for i, memory in enumerate(memories[:3]):  # Show first 3
                print(f"   🧠 Memory {i+1}: {memory.get('text', 'No text')[:100]}...")
                
        else:
            print(f"❌ Failed to search memories: {response.status_code}")
            print(f"   📊 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception searching memories: {e}")
    
    print()
    
    # Test 3: Get all memories
    print("📋 Test 3: Getting all memories...")
    
    try:
        response = requests.get(
            f"{MEM0_BASE_URL}/memories",
            headers=headers,
            params={"user_id": MEM0_USER_ID},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            memories = result.get("memories", [])
            print(f"✅ Retrieved all memories!")
            print(f"   📊 Total memories: {len(memories)}")
            
            # Group by categories if available
            categories = {}
            for memory in memories:
                category = memory.get("category", "uncategorized")
                if category not in categories:
                    categories[category] = 0
                categories[category] += 1
            
            print("   📊 Memory categories:")
            for cat, count in categories.items():
                print(f"       • {cat}: {count}")
                
        else:
            print(f"❌ Failed to get memories: {response.status_code}")
            print(f"   📊 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception getting memories: {e}")
    
    print()
    
    # Test 4: Test Railway backend memory endpoint
    print("🚀 Test 4: Testing Railway backend memory endpoint...")
    
    try:
        response = requests.get(
            "https://bonzai-backend.railway.app/api/memory/status",
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Railway backend memory endpoint works!")
            print(f"   📊 Response: {result}")
        else:
            print(f"❌ Railway backend memory endpoint failed: {response.status_code}")
            print(f"   📊 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception testing Railway backend: {e}")

if __name__ == "__main__":
    test_mem0_api()