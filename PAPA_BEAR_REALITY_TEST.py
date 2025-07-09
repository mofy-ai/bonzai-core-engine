#!/usr/bin/env python3
"""
🔥 PAPA BEAR'S BRUTAL REALITY TEST 🔥
Tests EVERYTHING on localhost:5001 - Built by Papa Bear, Run by Nathan
"""

import requests
import json
import time
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:5001"

def brutal_test():
    print("🔥" * 60)
    print("🔥 PAPA BEAR'S BRUTAL BACKEND REALITY CHECK 🔥")
    print("🔥" * 60)
    print(f"Testing: {BACKEND_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    passed = 0
    failed = 0
    critical_failures = []
    
    def test_endpoint(name, url, method='GET', data=None, critical=False):
        nonlocal passed, failed, critical_failures
        
        print(f"\n🧪 {name}")
        try:
            start = time.time()
            
            if method == 'GET':
                resp = requests.get(url, timeout=5)
            else:
                resp = requests.post(url, json=data, timeout=5)
            
            duration = (time.time() - start) * 1000
            
            if resp.status_code in [200, 201]:
                print(f"   ✅ PASS - {resp.status_code} ({duration:.0f}ms)")
                passed += 1
                
                # Show response preview
                try:
                    data = resp.json()
                    if isinstance(data, dict):
                        keys = list(data.keys())[:3]
                        print(f"   📋 Keys: {keys}")
                except:
                    text = resp.text[:100]
                    print(f"   📋 Response: {text}...")
                    
            else:
                print(f"   ❌ FAIL - {resp.status_code} ({duration:.0f}ms)")
                failed += 1
                if critical:
                    critical_failures.append(f"{name}: {resp.status_code}")
                    
        except Exception as e:
            print(f"   💥 ERROR - {str(e)}")
            failed += 1
            if critical:
                critical_failures.append(f"{name}: {str(e)}")
    
    # CRITICAL TESTS
    print("\n🚨 CRITICAL CORE TESTS")
    print("=" * 30)
    test_endpoint("Root Endpoint", f"{BACKEND_URL}/", critical=True)
    test_endpoint("Health Check", f"{BACKEND_URL}/api/health", critical=True)
    
    # SERVICE TESTS  
    print("\n📊 SERVICE STATUS TESTS")
    print("=" * 30)
    test_endpoint("ZAI Prime Status", f"{BACKEND_URL}/api/zai-prime/status")
    test_endpoint("Agents List", f"{BACKEND_URL}/api/zai-prime/agents")
    test_endpoint("Global Context", f"{BACKEND_URL}/api/zai-prime/context")
    
    # MCP TESTS
    print("\n🔌 MCP INTEGRATION TESTS") 
    print("=" * 30)
    test_endpoint("MCP Tools", f"{BACKEND_URL}/api/mcp/tools")
    test_endpoint("MCP Execute", f"{BACKEND_URL}/api/mcp/execute", "POST", {
        "tool": "orchestrate_ai",
        "parameters": {"model": "test", "prompt": "Reality check"}
    })
    
    # MEMORY TESTS
    print("\n🧠 MEMORY SYSTEM TESTS")
    print("=" * 30)
    test_endpoint("Memory Health", f"{BACKEND_URL}/api/memory/health")
    test_endpoint("Memory Search", f"{BACKEND_URL}/api/memory/search", "POST", {
        "query": "test",
        "user_id": "papa_bear_test"
    })
    
    # AI TESTS
    print("\n🤖 AI ORCHESTRATION TESTS")
    print("=" * 30)
    test_endpoint("Simple Chat", f"{BACKEND_URL}/api/chat/simple", "POST", {
        "message": "Are you working?",
        "model": "gemini"
    })
    test_endpoint("Multi-Model", f"{BACKEND_URL}/api/multi-model/status")
    
    # ADVANCED TESTS
    print("\n⚡ ADVANCED FEATURE TESTS")
    print("=" * 30)
    test_endpoint("Agent Registry", f"{BACKEND_URL}/api/agent-registry/status")
    test_endpoint("Task Orchestrator", f"{BACKEND_URL}/api/task-orchestrator/status") 
    test_endpoint("WebSocket Coordinator", f"{BACKEND_URL}/api/websocket-coordinator/status")
    test_endpoint("Scrapybara Status", f"{BACKEND_URL}/api/scrape/status")
    
    # FINAL REPORT
    print("\n" + "🔥" * 60)
    print("🔥 PAPA BEAR'S BRUTAL REALITY REPORT 🔥")
    print("🔥" * 60)
    
    total = passed + failed
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"📊 RESULTS:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success Rate: {success_rate:.1f}%")
    
    if critical_failures:
        print(f"\n🚨 CRITICAL FAILURES:")
        for failure in critical_failures:
            print(f"   💥 {failure}")
    else:
        print(f"\n🎉 NO CRITICAL FAILURES!")
    
    if success_rate >= 80:
        print(f"\n🏆 VERDICT: BACKEND IS SOLID! Give Claude Code the good news!")
    elif success_rate >= 60:
        print(f"\n⚠️ VERDICT: BACKEND MOSTLY WORKING - Some issues to fix")
    else:
        print(f"\n💥 VERDICT: BACKEND NEEDS SERIOUS WORK")
    
    print(f"\nTest completed: {datetime.now().strftime('%H:%M:%S')}")
    print("🔥" * 60)

if __name__ == "__main__":
    brutal_test()
