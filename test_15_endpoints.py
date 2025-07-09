#!/usr/bin/env python3
"""
🔥 ULTIMATE 15 ENDPOINTS TEST SUITE
Nathan's Request: "You've got 15 endpoints to make me and test"
"""

import requests
import json
import time
from datetime import datetime

# Test configuration
BASE_URL = "https://mofy.ai"  # Railway deployment
LOCAL_URL = "http://localhost:5001"  # Local testing
TEST_API_KEY = "bz_ultimate_enterprise_123"

def test_endpoint(endpoint, method="GET", data=None, headers=None, description=""):
    """Test a single endpoint"""
    print(f"\n🧪 Testing {method} {endpoint} - {description}")
    
    # Try Railway first, then local
    for base_url in [BASE_URL, LOCAL_URL]:
        try:
            url = f"{base_url}{endpoint}"
            
            if headers is None:
                headers = {}
            
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=10)
            else:
                print(f"❌ Unsupported method: {method}")
                continue
            
            if response.status_code == 200:
                print(f"✅ SUCCESS ({base_url}): {response.status_code}")
                try:
                    result = response.json()
                    if 'success' in result:
                        print(f"   Success: {result['success']}")
                    if 'message' in result:
                        print(f"   Message: {result['message']}")
                    if 'service' in result:
                        print(f"   Service: {result['service']}")
                except:
                    print(f"   Response: {response.text[:200]}...")
                return True
            else:
                print(f"❌ FAILED ({base_url}): {response.status_code}")
                print(f"   Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ ERROR ({base_url}): {e}")
    
    return False

def test_all_15_endpoints():
    """Test all 15 Ultimate Endpoints"""
    print("🚀 TESTING ALL 15 ULTIMATE ENDPOINTS")
    print("=" * 60)
    
    # Headers for authenticated requests
    auth_headers = {
        "Authorization": f"Bearer {TEST_API_KEY}",
        "Content-Type": "application/json"
    }
    
    endpoints = [
        # 1. Root endpoint (no auth)
        {
            "endpoint": "/",
            "method": "GET",
            "description": "Root system overview",
            "headers": None
        },
        
        # 2. Health check (no auth)
        {
            "endpoint": "/api/health",
            "method": "GET", 
            "description": "Health check endpoint",
            "headers": None
        },
        
        # 3. System status (auth required)
        {
            "endpoint": "/api/status",
            "method": "GET",
            "description": "System status with user tier",
            "headers": auth_headers
        },
        
        # 4. Ultimate chat (auth required)
        {
            "endpoint": "/api/chat",
            "method": "POST",
            "description": "Ultimate chat with family collaboration",
            "headers": auth_headers,
            "data": {
                "message": "Test message for Ultimate Mem0",
                "model": "claude-ultimate"
            }
        },
        
        # 5. AI orchestration (auth required)
        {
            "endpoint": "/api/orchestrate",
            "method": "POST",
            "description": "AI orchestration with family context",
            "headers": auth_headers,
            "data": {
                "prompt": "Test orchestration prompt",
                "models": ["claude-ultimate", "gemini-pro"]
            }
        },
        
        # 6. Memory addition (auth required)
        {
            "endpoint": "/api/memory/add",
            "method": "POST",
            "description": "Add memory with advanced features",
            "headers": auth_headers,
            "data": {
                "content": "Test memory for Ultimate Mem0 system",
                "category": "test_memories"
            }
        },
        
        # 7. Memory search (auth required)
        {
            "endpoint": "/api/memory/search",
            "method": "POST",
            "description": "Search memory with advanced retrieval",
            "headers": auth_headers,
            "data": {
                "query": "Test memory Ultimate Mem0",
                "advanced_retrieval": True
            }
        },
        
        # 8. Family group chat (auth required)
        {
            "endpoint": "/api/family/group-chat",
            "method": "POST",
            "description": "Family group chat with attribution",
            "headers": auth_headers,
            "data": {
                "messages": [
                    {
                        "role": "user",
                        "content": "Test family group message",
                        "family_member": "claude_code"
                    }
                ]
            }
        },
        
        # 9. Family status (auth required)
        {
            "endpoint": "/api/family/status",
            "method": "GET",
            "description": "Family status with analytics",
            "headers": auth_headers
        },
        
        # 10. Memory export (auth required)
        {
            "endpoint": "/api/memory/export",
            "method": "POST",
            "description": "Export memories with custom schemas",
            "headers": auth_headers,
            "data": {
                "export_type": "family_backup"
            }
        },
        
        # 11. Memory import (auth required)
        {
            "endpoint": "/api/memory/import",
            "method": "POST",
            "description": "Import memories with direct bypass",
            "headers": auth_headers,
            "data": {
                "knowledge_data": [
                    {
                        "content": "Test imported knowledge",
                        "family_member": "system",
                        "type": "test_knowledge",
                        "category": "imported_test"
                    }
                ]
            }
        },
        
        # 12. API key generation (auth required)
        {
            "endpoint": "/api/keys/generate",
            "method": "POST",
            "description": "Generate API key with Mem0 storage",
            "headers": auth_headers,
            "data": {
                "user_id": "test_user",
                "tier": "family"
            }
        },
        
        # 13. API key validation (no auth - validates itself)
        {
            "endpoint": "/api/keys/validate",
            "method": "POST",
            "description": "Validate API key with Mem0 lookup",
            "headers": None,
            "data": {
                "key": TEST_API_KEY
            }
        },
        
        # 14. MCP tools (auth required)
        {
            "endpoint": "/api/mcp/tools",
            "method": "GET",
            "description": "MCP tools with all capabilities",
            "headers": auth_headers
        },
        
        # 15. MCP execute (auth required)
        {
            "endpoint": "/api/mcp/execute",
            "method": "POST",
            "description": "MCP execution with all features",
            "headers": auth_headers,
            "data": {
                "tool": "ultimate_orchestrate",
                "parameters": {
                    "prompt": "Test MCP orchestration",
                    "models": ["claude-ultimate"],
                    "advanced_retrieval": True
                }
            }
        }
    ]
    
    # Test each endpoint
    passed = 0
    total = len(endpoints)
    
    for i, test_config in enumerate(endpoints, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}/{total}: {test_config['description']}")
        print(f"{'='*60}")
        
        success = test_endpoint(
            endpoint=test_config["endpoint"],
            method=test_config["method"],
            data=test_config.get("data"),
            headers=test_config.get("headers"),
            description=test_config["description"]
        )
        
        if success:
            passed += 1
            print(f"✅ ENDPOINT {i} PASSED")
        else:
            print(f"❌ ENDPOINT {i} FAILED")
        
        # Small delay between tests
        time.sleep(0.5)
    
    # Final results
    print(f"\n{'='*60}")
    print(f"🎯 FINAL RESULTS: {passed}/{total} endpoints passed")
    print(f"{'='*60}")
    
    if passed == total:
        print("🔥 ALL 15 ENDPOINTS WORKING! READY TO CELEBRATE!")
        return True
    else:
        print(f"❌ {total - passed} endpoints need fixing")
        return False

def test_sse_endpoint():
    """Test SSE streaming endpoint separately"""
    print("\n🧪 Testing SSE Streaming Endpoint")
    print("=" * 40)
    
    for base_url in [BASE_URL, LOCAL_URL]:
        try:
            url = f"{base_url}/sse"
            print(f"Testing SSE at {url}")
            
            response = requests.get(url, stream=True, timeout=10)
            
            if response.status_code == 200:
                print("✅ SSE endpoint responding")
                
                # Read first few events
                for i, line in enumerate(response.iter_lines()):
                    if i > 5:  # Just read first few lines
                        break
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data:'):
                            print(f"   📡 {line}")
                
                print("✅ SSE STREAMING WORKING!")
                return True
            else:
                print(f"❌ SSE failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ SSE error ({base_url}): {e}")
    
    return False

def main():
    """Run all endpoint tests"""
    print("🚀 ULTIMATE 15 ENDPOINTS TEST SUITE")
    print("Nathan's Request: 'You've got 15 endpoints to make me and test'")
    print("Test Key:", TEST_API_KEY)
    print("Timestamp:", datetime.now().isoformat())
    print("=" * 80)
    
    # Test all 15 endpoints
    endpoints_success = test_all_15_endpoints()
    
    # Test SSE endpoint (bonus 16th)
    sse_success = test_sse_endpoint()
    
    print(f"\n{'='*80}")
    print("🎯 COMPREHENSIVE TEST RESULTS")
    print(f"{'='*80}")
    print(f"✅ 15 Core Endpoints: {'PASSED' if endpoints_success else 'FAILED'}")
    print(f"✅ SSE Streaming: {'PASSED' if sse_success else 'FAILED'}")
    
    if endpoints_success and sse_success:
        print("\n🔥 ALL TESTS PASSED! ULTIMATE MEM0 SYSTEM FULLY OPERATIONAL!")
        print("🎉 READY TO CELEBRATE WITH NATHAN!")
    else:
        print("\n❌ Some tests failed. Need to fix and retest.")
    
    return endpoints_success and sse_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)