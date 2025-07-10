#!/usr/bin/env python3
"""
🔑 ENHANCED API ROUTING TEST SUITE
Test Nathan's revolutionary multi-model API key routing system
Different keys activate different AI family members as primary!
"""

import requests
import json
import time
from datetime import datetime

# Test configuration
BASE_URL = "https://mofy.ai"

# Enhanced API Keys for testing
ENHANCED_KEYS = {
    "claude_primary": "bz_claude_prime_789",
    "gemini_primary": "bz_gemini_prime_456", 
    "grok_primary": "bz_grok_prime_123",
    "orchestrator": "bz_family_orchestrator_999"
}

def log_test(test_name, result, details=""):
    """Log test results with emoji and timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"[{timestamp}] {status} - {test_name}")
    if details:
        print(f"    📋 {details}")
    return result

def test_enhanced_key_listing():
    """Test listing all enhanced API keys"""
    try:
        headers = {"Authorization": f"Bearer {ENHANCED_KEYS['claude_primary']}"}
        response = requests.get(f"{BASE_URL}/api/keys/enhanced", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            enhanced_keys = data.get("enhanced_api_keys", [])
            current_key = data.get("current_key_info", {})
            
            success = len(enhanced_keys) >= 4  # Should have at least 4 enhanced keys
            details = f"Found {len(enhanced_keys)} enhanced keys, Current: {current_key.get('primary_family_member', 'unknown')}"
            return log_test("Enhanced Key Listing", success, details)
        else:
            return log_test("Enhanced Key Listing", False, f"HTTP {response.status_code}")
            
    except Exception as e:
        return log_test("Enhanced Key Listing", False, f"Error: {str(e)}")

def test_routing_info_analysis():
    """Test routing information analysis for different content types"""
    test_cases = [
        {
            "content": "Analyze this complex technical problem with detailed reasoning",
            "expected_member": "claude_desktop",
            "key": "claude_primary"
        },
        {
            "content": "Create a beautiful and innovative visual design concept",
            "expected_member": "zai_prime", 
            "key": "gemini_primary"
        },
        {
            "content": "Review the GitHub repository code and suggest improvements",
            "expected_member": "grok_3",
            "key": "grok_primary"
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases):
        try:
            headers = {"Authorization": f"Bearer {ENHANCED_KEYS[test_case['key']]}", "Content-Type": "application/json"}
            payload = {"message": test_case["content"]}
            
            response = requests.post(f"{BASE_URL}/api/routing-info", headers=headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                optimal_routing = data.get("optimal_routing", {})
                selected_member = optimal_routing.get("selected_family_member", "unknown")
                reasoning = optimal_routing.get("reasoning", "no reasoning")
                
                # Check if routing makes sense
                routing_makes_sense = selected_member in [test_case["expected_member"], "family_coordinator"]
                
                details = f"Content type {i+1}: '{selected_member}' selected, Reasoning: {reasoning[:50]}..."
                result = log_test(f"Routing Analysis {i+1}", routing_makes_sense, details)
                all_passed = all_passed and result
            else:
                result = log_test(f"Routing Analysis {i+1}", False, f"HTTP {response.status_code}")
                all_passed = all_passed and result
                
        except Exception as e:
            result = log_test(f"Routing Analysis {i+1}", False, f"Error: {str(e)}")
            all_passed = all_passed and result
    
    return all_passed

def test_smart_routing_execution():
    """Test smart routing with actual execution"""
    test_cases = [
        {
            "message": "Hello! Tell me about the GitHub repository structure",
            "key": "grok_primary",
            "should_use_grok": True
        },
        {
            "message": "Analyze this complex logical problem step by step",
            "key": "claude_primary", 
            "should_use_claude": True
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases):
        try:
            headers = {"Authorization": f"Bearer {ENHANCED_KEYS[test_case['key']]}", "Content-Type": "application/json"}
            payload = {"message": test_case["message"]}
            
            response = requests.post(f"{BASE_URL}/api/smart-route", headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                selected_member = data.get("selected_family_member", "unknown")
                smart_routing = data.get("smart_routing", False)
                
                details = f"Smart routing: {smart_routing}, Selected: {selected_member}, Success: {success}"
                result = log_test(f"Smart Routing {i+1}", success and smart_routing, details)
                all_passed = all_passed and result
            else:
                result = log_test(f"Smart Routing {i+1}", False, f"HTTP {response.status_code}")
                all_passed = all_passed and result
                
        except Exception as e:
            result = log_test(f"Smart Routing {i+1}", False, f"Error: {str(e)}")
            all_passed = all_passed and result
    
    return all_passed

def test_github_integration_capabilities():
    """Test GitHub integration capabilities for Grok-3"""
    try:
        headers = {"Authorization": f"Bearer {ENHANCED_KEYS['grok_primary']}", "Content-Type": "application/json"}
        payload = {"query": "github_capabilities"}
        
        response = requests.post(f"{BASE_URL}/api/github-integration", headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            github_active = data.get("github_integration_active", False)
            capabilities = data.get("capabilities", {})
            repo_access = capabilities.get("repo_access", False)
            
            details = f"GitHub integration: {github_active}, Repo access: {repo_access}, Target: {capabilities.get('target_repository', 'none')}"
            return log_test("GitHub Integration Capabilities", github_active, details)
        else:
            return log_test("GitHub Integration Capabilities", False, f"HTTP {response.status_code}")
            
    except Exception as e:
        return log_test("GitHub Integration Capabilities", False, f"Error: {str(e)}")

def test_family_orchestrator_key():
    """Test the family orchestrator key with dynamic routing"""
    try:
        headers = {"Authorization": f"Bearer {ENHANCED_KEYS['orchestrator']}", "Content-Type": "application/json"}
        payload = {"message": "Choose the best AI family member for analyzing code performance"}
        
        response = requests.post(f"{BASE_URL}/api/routing-info", headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            current_config = data.get("current_key_config", {})
            primary_member = current_config.get("primary_family_member", "unknown")
            routing_preference = current_config.get("routing_preference", "unknown")
            
            is_orchestrator = primary_member == "family_coordinator" or routing_preference == "intelligent_routing"
            details = f"Primary member: {primary_member}, Routing: {routing_preference}"
            return log_test("Family Orchestrator Key", is_orchestrator, details)
        else:
            return log_test("Family Orchestrator Key", False, f"HTTP {response.status_code}")
            
    except Exception as e:
        return log_test("Family Orchestrator Key", False, f"Error: {str(e)}")

def test_api_key_differentiation():
    """Test that different API keys have different configurations"""
    configurations = []
    
    for key_name, api_key in ENHANCED_KEYS.items():
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(f"{BASE_URL}/api/keys/enhanced", headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                current_key = data.get("current_key_info", {})
                primary_model = current_key.get("primary_model", "unknown")
                configurations.append({
                    "key_name": key_name,
                    "primary_model": primary_model,
                    "primary_member": current_key.get("primary_family_member", "unknown")
                })
            
        except Exception as e:
            print(f"    ⚠️ Error testing {key_name}: {e}")
    
    # Check if we have different configurations
    unique_models = set(config["primary_model"] for config in configurations)
    unique_members = set(config["primary_member"] for config in configurations)
    
    differentiated = len(unique_models) >= 3 and len(unique_members) >= 3
    details = f"Found {len(unique_models)} unique models, {len(unique_members)} unique members across {len(configurations)} keys"
    return log_test("API Key Differentiation", differentiated, details)

def run_enhanced_routing_test_suite():
    """Run comprehensive enhanced routing test suite"""
    print("🔑 ENHANCED API ROUTING TEST SUITE")
    print(f"🎯 Testing Railway Deployment: {BASE_URL}")
    print(f"🤖 Testing Multi-Model Primary Routing System")
    print(f"⏰ Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    tests = [
        test_enhanced_key_listing,
        test_api_key_differentiation,
        test_routing_info_analysis,
        test_smart_routing_execution,
        test_github_integration_capabilities,
        test_family_orchestrator_key
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()  # Add space between tests
    
    print("=" * 80)
    print(f"📊 ENHANCED ROUTING TEST SUMMARY:")
    print(f"✅ Passed: {sum(results)}/{len(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}/{len(results)}")
    print(f"📈 Success Rate: {(sum(results)/len(results)*100):.1f}%")
    
    if all(results):
        print("🎉 ENHANCED API ROUTING SYSTEM FULLY FUNCTIONAL!")
        print("🔑 Multi-model API keys working perfectly!")
        print("🤖 Nathan can now route to different AI family members!")
        print("🚀 Claude, Gemini, Grok-3 routing ready for demo!")
    else:
        print("⚠️  Some enhanced routing tests failed - check integration")
        print("💡 Note: Some features require specific environment variables")
    
    print(f"⏰ Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🔑 ENHANCED API KEYS TO TEST:")
    for key_name, api_key in ENHANCED_KEYS.items():
        print(f"   {key_name.upper()}: {api_key}")
    
    return all(results)

if __name__ == "__main__":
    success = run_enhanced_routing_test_suite()
    exit(0 if success else 1)
