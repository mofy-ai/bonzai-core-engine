#!/usr/bin/env python3
"""
🧪 GROK-3 GITHUB MODELS TEST SUITE
Test the new Grok-3 family member integration
Nathan's cutting-edge AI family expansion!
"""

import requests
import json
import os
from datetime import datetime

# Test configuration
BASE_URL = "https://mofy.ai"
API_KEY = "bz_ultimate_enterprise_123"  # Default test key

def log_test(test_name, result, details=""):
    """Log test results with emoji and timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"[{timestamp}] {status} - {test_name}")
    if details:
        print(f"    📋 Details: {details}")
    return result

def test_grok_health_status():
    """Test if Grok-3 is included in family system status"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        data = response.json()
        
        family_system = data.get("family_system", {})
        family_members = family_system.get("family_members", [])
        
        grok_included = "grok_3" in family_members
        grok_connected = family_system.get("grok_3_connected", False)
        github_integration = family_system.get("github_models_integration", "unavailable")
        
        success = grok_included and github_integration != "unavailable"
        
        details = f"Grok in family: {grok_included}, Connected: {grok_connected}, Integration: {github_integration}"
        return log_test("Grok-3 Family System Integration", success, details)
        
    except Exception as e:
        return log_test("Grok-3 Family System Integration", False, f"Error: {str(e)}")

def test_grok_connection():
    """Test Grok-3 connection endpoint"""
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(f"{BASE_URL}/api/grok/test", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            test_result = data.get("test_result", {})
            success = test_result.get("success", False)
            integration_status = data.get("integration_status", "unknown")
            
            details = f"Status: {integration_status}, Model: {data.get('model', 'unknown')}"
            return log_test("Grok-3 Connection Test", success, details)
        else:
            return log_test("Grok-3 Connection Test", False, f"HTTP {response.status_code}")
            
    except Exception as e:
        return log_test("Grok-3 Connection Test", False, f"Error: {str(e)}")

def test_grok_chat():
    """Test chatting with Grok-3"""
    try:
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {
            "message": "Hello Grok! Welcome to Nathan's AI family! 🤖👨‍👩‍👧‍👦",
            "system_prompt": "You are Grok-3, now part of Nathan's AI family. Respond with enthusiasm!"
        }
        
        response = requests.post(f"{BASE_URL}/api/grok/chat", headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            success = data.get("success", False)
            family_member = data.get("family_member", "unknown")
            provider = data.get("provider", "unknown")
            
            details = f"Member: {family_member}, Provider: {provider}, Response length: {len(data.get('response', ''))}"
            return log_test("Grok-3 Chat Interaction", success, details)
        else:
            return log_test("Grok-3 Chat Interaction", False, f"HTTP {response.status_code}")
            
    except Exception as e:
        return log_test("Grok-3 Chat Interaction", False, f"Error: {str(e)}")

def test_grok_orchestration():
    """Test Grok-3 orchestration with family context"""
    try:
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {
            "prompt": "How can our AI family work together more effectively? Give me your witty insights!"
        }
        
        response = requests.post(f"{BASE_URL}/api/grok/orchestrate", headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            success = data.get("success", False)
            orchestration_type = data.get("orchestration_type", "unknown")
            context_used = data.get("family_context_used", 0)
            
            details = f"Type: {orchestration_type}, Context used: {context_used}, Features: {len(data.get('features_utilized', []))}"
            return log_test("Grok-3 Orchestration", success, details)
        else:
            return log_test("Grok-3 Orchestration", False, f"HTTP {response.status_code}")
            
    except Exception as e:
        return log_test("Grok-3 Orchestration", False, f"Error: {str(e)}")

def test_grok_mcp_integration():
    """Test Grok-3 through MCP execute endpoint"""
    try:
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {
            "tool": "ultimate_orchestrate",
            "parameters": {
                "prompt": "Nathan wants the AI family to collaborate on a new feature",
                "models": ["grok-3"],
                "advanced_retrieval": True
            }
        }
        
        response = requests.post(f"{BASE_URL}/api/mcp/execute", headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            success = data.get("success", False)
            orchestration = data.get("orchestration", "unknown")
            model = data.get("model", "unknown")
            
            details = f"Orchestration: {orchestration}, Model: {model}, Provider: {data.get('provider', 'unknown')}"
            return log_test("Grok-3 MCP Integration", success, details)
        else:
            return log_test("Grok-3 MCP Integration", False, f"HTTP {response.status_code}")
            
    except Exception as e:
        return log_test("Grok-3 MCP Integration", False, f"Error: {str(e)}")

def test_endpoint_count():
    """Test that endpoint count reflects Grok-3 additions"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        data = response.json()
        
        endpoint_count = data.get("endpoints", 0)
        expected_count = 18  # Updated for Grok-3 endpoints
        
        success = endpoint_count >= expected_count
        details = f"Found: {endpoint_count} endpoints, Expected: >= {expected_count}"
        return log_test("Endpoint Count Update", success, details)
        
    except Exception as e:
        return log_test("Endpoint Count Update", False, f"Error: {str(e)}")

def run_grok_test_suite():
    """Run comprehensive Grok-3 test suite"""
    print("🚀 GROK-3 GITHUB MODELS TEST SUITE")
    print(f"🎯 Testing Railway Deployment: {BASE_URL}")
    print(f"🤖 Testing xAI Grok-3 via GitHub Models Integration")
    print(f"⏰ Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    tests = [
        test_grok_health_status,
        test_grok_connection,
        test_grok_chat,
        test_grok_orchestration,
        test_grok_mcp_integration,
        test_endpoint_count
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()  # Add space between tests
    
    print("=" * 70)
    print(f"📊 GROK-3 TEST SUMMARY:")
    print(f"✅ Passed: {sum(results)}/{len(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}/{len(results)}")
    print(f"📈 Success Rate: {(sum(results)/len(results)*100):.1f}%")
    
    if all(results):
        print("🎉 GROK-3 FULLY INTEGRATED INTO AI FAMILY!")
        print("🚀 Enterprise GitHub Models integration successful!")
        print("🤖 Nathan's AI family now includes cutting-edge Grok-3!")
    else:
        print("⚠️  Some Grok-3 tests failed - check integration")
        print("💡 Note: Grok-3 requires GITHUB_MODELS_TOKEN environment variable")
    
    print(f"⏰ Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return all(results)

if __name__ == "__main__":
    success = run_grok_test_suite()
    exit(0 if success else 1)
