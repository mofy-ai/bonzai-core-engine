#!/usr/bin/env python3
"""
🚀 ULTIMATE MEM0 API COMPREHENSIVE TEST SUITE
Tests all new Ultimate Mem0 endpoints on Railway deployment
For Nathan's Doctor Demo - July 10, 2025
"""

import requests
import json
import time
import os
from datetime import datetime

# Railway deployment URL
BASE_URL = "https://mofy.ai"

def log_test(test_name, result, details=""):
    """Log test results with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"[{timestamp}] {status} - {test_name}")
    if details:
        print(f"    Details: {details}")
    return result

def test_health_endpoint():
    """Test basic health check"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        data = response.json()
        
        # Check basic health
        basic_health = response.status_code == 200 and data.get("success") == True
        
        # Check family system
        family_system = data.get("family_system", {})
        family_operational = family_system.get("family_system") == "operational"
        redis_connected = family_system.get("redis_connected") == True
        mem0_connected = family_system.get("mem0_connected") == True
        
        # Check enterprise features
        advanced_features = family_system.get("advanced_features", [])
        required_features = ["graph_memory", "group_chat", "custom_categories", "advanced_retrieval"]
        features_present = all(feature in advanced_features for feature in required_features)
        
        # Check family members
        family_members = family_system.get("family_members", [])
        required_members = ["claude_desktop", "claude_code", "mama_bear", "papa_bear"]
        members_present = all(member in family_members for member in required_members)
        
        overall_health = all([basic_health, family_operational, redis_connected, 
                            mem0_connected, features_present, members_present])
        
        details = f"Status: {data.get('status')}, Service: {data.get('service')}, " \
                 f"Features: {len(advanced_features)}, Members: {len(family_members)}"
        
        return log_test("Health Endpoint - Ultimate Mem0", overall_health, details)
        
    except Exception as e:
        return log_test("Health Endpoint - Ultimate Mem0", False, f"Error: {str(e)}")

def test_oauth_endpoints():
    """Test OAuth authorization server endpoints"""
    try:
        response = requests.get(f"{BASE_URL}/.well-known/oauth-authorization-server", timeout=10)
        oauth_config = response.json()
        
        # Check required OAuth fields
        required_fields = ["issuer", "authorization_endpoint", "token_endpoint"]
        oauth_valid = all(field in oauth_config for field in required_fields)
        
        details = f"Issuer: {oauth_config.get('issuer', 'None')}"
        return log_test("OAuth Authorization Server", oauth_valid, details)
        
    except Exception as e:
        return log_test("OAuth Authorization Server", False, f"Error: {str(e)}")

def test_mcp_endpoint():
    """Test MCP endpoint availability"""
    try:
        response = requests.get(f"{BASE_URL}/mcp", timeout=10)
        mcp_available = response.status_code in [200, 405]  # 405 = Method not allowed (expected for GET)
        
        details = f"Status Code: {response.status_code}"
        return log_test("MCP Endpoint", mcp_available, details)
        
    except Exception as e:
        return log_test("MCP Endpoint", False, f"Error: {str(e)}")

def test_mem0_enterprise_features():
    """Test Mem0 enterprise features integration"""
    try:
        # Test health endpoint for enterprise feature info
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        data = response.json()
        
        family_system = data.get("family_system", {})
        advanced_features = family_system.get("advanced_features", [])
        
        # Check all enterprise features are active
        enterprise_features = [
            "graph_memory", "group_chat", "custom_categories", 
            "advanced_retrieval", "criteria_retrieval", "memory_export",
            "direct_import", "contextual_add_v2", "expiration_dates",
            "selective_storage", "custom_instructions", "webhooks"
        ]
        
        features_active = all(feature in advanced_features for feature in enterprise_features)
        
        # Check optimization status
        optimization = data.get("optimization_status") == "maximum_utilization"
        mem0_integration = data.get("mem0_integration") == "full_enterprise_features"
        
        enterprise_ready = all([features_active, optimization, mem0_integration])
        
        details = f"Features Active: {len(advanced_features)}/{len(enterprise_features)}, " \
                 f"Optimization: {data.get('optimization_status')}"
        
        return log_test("Mem0 Enterprise Features", enterprise_ready, details)
        
    except Exception as e:
        return log_test("Mem0 Enterprise Features", False, f"Error: {str(e)}")

def test_claude_ai_integration():
    """Test Claude AI integration readiness"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        data = response.json()
        
        claude_integration = data.get("claude_ai_integration") == "oauth_endpoints_active"
        
        details = f"Integration Status: {data.get('claude_ai_integration')}"
        return log_test("Claude AI Integration", claude_integration, details)
        
    except Exception as e:
        return log_test("Claude AI Integration", False, f"Error: {str(e)}")

def test_response_times():
    """Test API response times for demo readiness"""
    endpoints = [
        "/api/health",
        "/.well-known/oauth-authorization-server",
        "/mcp"
    ]
    
    response_times = []
    
    for endpoint in endpoints:
        try:
            start_time = time.time()
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            response_times.append(response_time)
            
        except Exception as e:
            response_times.append(float('inf'))
    
    avg_response_time = sum(response_times) / len(response_times)
    fast_responses = avg_response_time < 2000  # Less than 2 seconds average
    
    details = f"Average: {avg_response_time:.2f}ms, Max: {max(response_times):.2f}ms"
    return log_test("Response Times (Demo Ready)", fast_responses, details)

def run_comprehensive_test():
    """Run all tests and generate report"""
    print("🚀 BONZAI ULTIMATE MEM0 API TEST SUITE")
    print(f"🎯 Testing Railway Deployment: {BASE_URL}")
    print(f"⏰ Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        test_health_endpoint,
        test_oauth_endpoints,
        test_mcp_endpoint,
        test_mem0_enterprise_features,
        test_claude_ai_integration,
        test_response_times
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        time.sleep(1)  # Brief pause between tests
    
    print("=" * 60)
    print(f"📊 TEST SUMMARY:")
    print(f"✅ Passed: {sum(results)}/{len(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}/{len(results)}")
    print(f"📈 Success Rate: {(sum(results)/len(results)*100):.1f}%")
    
    if all(results):
        print("🎉 ALL SYSTEMS READY FOR DOCTOR DEMO!")
    else:
        print("⚠️  Some tests failed - check details above")
    
    print(f"⏰ Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return all(results)

if __name__ == "__main__":
    success = run_comprehensive_test()
    exit(0 if success else 1)
