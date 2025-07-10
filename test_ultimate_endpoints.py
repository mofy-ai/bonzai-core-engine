#!/usr/bin/env python3
"""
Ultimate Mem0 Endpoint Tester
Tests all 15 endpoints to verify deployment is working
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "https://mofy.ai"
API_KEY = "bz_ultimate_enterprise_123"

def test_endpoint(name, method, path, headers=None, data=None):
    """Test a single endpoint and return results"""
    url = f"{BASE_URL}{path}"
    print(f"\nTesting: {name}")
    print(f"URL: {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ SUCCESS")
            try:
                data = response.json()
                print(f"Response preview: {json.dumps(data, indent=2)[:200]}...")
            except:
                print("Response:", response.text[:200])
        else:
            print("✗ FAILED")
            print("Error:", response.text[:200])
            
        return response.status_code == 200
        
    except Exception as e:
        print("✗ ERROR:", str(e))
        return False

def main():
    print("=" * 60)
    print("ULTIMATE MEM0 ENDPOINT TESTER")
    print("Testing all 15 endpoints")
    print("Timestamp:", datetime.now().isoformat())
    print("=" * 60)
    
    # Headers for authenticated requests
    auth_headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    tests = [
        # Public endpoints (no auth)
        ("1. Root Overview", "GET", "/", None, None),
        ("2. Health Check", "GET", "/api/health", None, None),
        
        # Authenticated endpoints
        ("3. System Status", "GET", "/api/status", auth_headers, None),
        ("4. Chat Endpoint", "POST", "/api/chat", auth_headers, {
            "message": "Test message",
            "model": "claude-ultimate"
        }),
        ("5. AI Orchestration", "POST", "/api/orchestrate", auth_headers, {
            "prompt": "Test orchestration",
            "models": ["claude-ultimate"]
        }),
        ("6. Add Memory", "POST", "/api/memory/add", auth_headers, {
            "content": "Test memory from endpoint tester",
            "category": "test"
        }),
        ("7. Search Memory", "POST", "/api/memory/search", auth_headers, {
            "query": "test",
            "advanced_retrieval": True
        }),
        ("8. Group Chat", "POST", "/api/family/group-chat", auth_headers, {
            "messages": [{"role": "user", "content": "Test", "family_member": "claude_desktop"}],
            "session_id": "test_session"
        }),
        ("9. Family Status", "GET", "/api/family/status", auth_headers, None),
        ("10. Export Memory", "POST", "/api/memory/export", auth_headers, {
            "export_type": "family_backup"
        }),
        ("11. Import Memory", "POST", "/api/memory/import", auth_headers, {
            "knowledge_data": [{"content": "Test import", "family_member": "system", "category": "test"}]
        }),
        ("12. Generate Key", "POST", "/api/keys/generate", auth_headers, {
            "user_id": "test_user",
            "tier": "family"
        }),
        ("13. Validate Key", "POST", "/api/keys/validate", None, {
            "key": API_KEY
        }),
        ("14. MCP Tools", "GET", "/api/mcp/tools", auth_headers, None),
        ("15. MCP Execute", "POST", "/api/mcp/execute", auth_headers, {
            "tool": "ultimate_family_memory",
            "parameters": {"action": "analytics"}
        })
    ]
    
    # Run all tests
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test_endpoint(*test):
            passed += 1
        time.sleep(0.5)  # Be nice to the server
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL ENDPOINTS WORKING! ULTIMATE MEM0 FULLY OPERATIONAL!")
    else:
        print(f"\n⚠️  {total - passed} endpoints need attention")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
