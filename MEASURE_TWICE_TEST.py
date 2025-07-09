#!/usr/bin/env python3
"""
MEASURE TWICE, CUT ONCE - Local Testing Before Deploy
Test all the routes we just fixed to make sure they work before deploying
"""

import requests
import json
import time
from datetime import datetime

class MeasureTwiceTest:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5001"
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'tests': []
        }
    
    def test_endpoint(self, name, url, method='GET', data=None):
        """Test a single endpoint"""
        self.results['total_tests'] += 1
        
        try:
            if method == 'GET':
                response = requests.get(f"{self.base_url}{url}", timeout=5)
            else:
                response = requests.post(f"{self.base_url}{url}", json=data or {}, timeout=5)
            
            success = response.status_code == 200
            
            if success:
                self.results['passed'] += 1
                print(f"✅ {name}: PASS (200)")
            else:
                self.results['failed'] += 1
                print(f"❌ {name}: FAIL ({response.status_code})")
            
            self.results['tests'].append({
                'name': name,
                'url': url,
                'method': method,
                'status_code': response.status_code,
                'success': success,
                'response_keys': list(response.json().keys()) if success else []
            })
            
        except Exception as e:
            self.results['failed'] += 1
            print(f"❌ {name}: ERROR ({str(e)})")
            self.results['tests'].append({
                'name': name,
                'url': url,
                'method': method,
                'status_code': 0,
                'success': False,
                'error': str(e)
            })
    
    def run_tests(self):
        """Run all tests for the fixes we made"""
        print("🔧 MEASURING TWICE - Testing Fixed Routes")
        print("="*50)
        
        # Test the routes that were failing in Papa Bear's test
        self.test_endpoint("Root Endpoint", "/")
        self.test_endpoint("Health Check", "/api/health")
        self.test_endpoint("Simple Chat", "/api/chat", "POST", {"message": "hello", "model": "gemini-2.0-flash-exp"})
        self.test_endpoint("Multi-Model", "/api/multi-model", "POST", {"message": "hello", "models": ["gemini-2.0-flash-exp"]})
        self.test_endpoint("Task Orchestrator", "/api/task-orchestrator")
        self.test_endpoint("WebSocket Coordinator", "/api/websocket-coordinator")
        self.test_endpoint("Scrapybara Status", "/api/scrapybara/status")
        
        # Test MCP endpoints
        self.test_endpoint("MCP Tools", "/api/mcp/tools")
        self.test_endpoint("MCP Execute", "/api/mcp/execute", "POST", {"tool": "orchestrate_ai", "parameters": {"model": "gemini-2.0-flash-exp", "prompt": "hello"}})
        
        # Test memory endpoints
        self.test_endpoint("Memory Health", "/api/memory/health")
        self.test_endpoint("Memory Search", "/api/memory/search", "POST", {"query": "test", "user_id": "test"})
        
        print("\n" + "="*50)
        print("📊 TEST RESULTS")
        print("="*50)
        
        success_rate = (self.results['passed'] / self.results['total_tests'] * 100) if self.results['total_tests'] > 0 else 0
        
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed']}")
        print(f"Failed: {self.results['failed']}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("✅ READY TO CUT - Deploy to Railway")
            return True
        elif success_rate >= 60:
            print("🟡 PARTIALLY READY - Some issues remain")
            return False
        else:
            print("❌ NOT READY - Major issues need fixing")
            return False
        
        print("\n" + "="*50)
        print("📋 DETAILED RESULTS")
        print("="*50)
        
        for test in self.results['tests']:
            status = "✅ PASS" if test['success'] else "❌ FAIL"
            print(f"{status} {test['name']} ({test['method']} {test['url']})")
            if 'response_keys' in test and test['response_keys']:
                print(f"    Keys: {test['response_keys']}")
            if 'error' in test:
                print(f"    Error: {test['error']}")
        
        # Save results
        with open('/mnt/c/Bonzai-Desktop/bonzai-core-engine/MEASURE_TWICE_RESULTS.json', 'w') as f:
            json.dump(self.results, f, indent=2)

if __name__ == "__main__":
    print("🚀 Starting backend for testing...")
    print("Make sure to run: python run_backend.py")
    print("Waiting 10 seconds for startup...")
    time.sleep(10)
    
    tester = MeasureTwiceTest()
    ready = tester.run_tests()
    
    if ready:
        print("\n🎯 MEASUREMENT COMPLETE - Ready to deploy!")
    else:
        print("\n⚠️  MEASUREMENT INCOMPLETE - Need more fixes!")
        
    exit(0 if ready else 1)