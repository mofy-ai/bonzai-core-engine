#!/usr/bin/env python3
"""
REAL FUNCTIONAL TEST - No Bullshit Edition
Tests what actually WORKS, not what just exists.
Nathan's kids' future depends on getting this right.
"""

import requests
import time
import json
import os
from datetime import datetime

class RealFunctionalTest:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'total_failures': 0,
            'critical_failures': [],
            'working_systems': [],
            'broken_systems': [],
            'partially_working': []
        }
    
    def test_railway_deployment(self):
        """Test if Railway deployment actually works"""
        print("🔍 TESTING RAILWAY DEPLOYMENT...")
        
        # Test health endpoint
        try:
            response = requests.get('https://bonzai-backend.railway.app/health', timeout=10)
            if response.status_code == 200:
                print("✅ Railway health endpoint responds")
                self.results['working_systems'].append("Railway health endpoint")
            else:
                print(f"❌ Railway health endpoint broken: {response.status_code}")
                self.results['broken_systems'].append(f"Railway health endpoint: {response.status_code}")
                self.results['total_failures'] += 1
        except Exception as e:
            print(f"❌ Railway deployment completely broken: {e}")
            self.results['critical_failures'].append(f"Railway deployment: {e}")
            self.results['total_failures'] += 1
            return False
        
        # Test MCP endpoints
        try:
            response = requests.get('https://bonzai-backend.railway.app/api/mcp/tools', timeout=10)
            if response.status_code == 200:
                tools = response.json()
                if 'tools' in tools and len(tools['tools']) > 0:
                    print(f"✅ MCP tools endpoint works: {len(tools['tools'])} tools")
                    self.results['working_systems'].append(f"MCP tools endpoint: {len(tools['tools'])} tools")
                else:
                    print("❌ MCP tools endpoint returns empty")
                    self.results['broken_systems'].append("MCP tools endpoint: empty response")
                    self.results['total_failures'] += 1
            else:
                print(f"❌ MCP tools endpoint broken: {response.status_code}")
                self.results['broken_systems'].append(f"MCP tools endpoint: {response.status_code}")
                self.results['total_failures'] += 1
        except Exception as e:
            print(f"❌ MCP tools endpoint broken: {e}")
            self.results['broken_systems'].append(f"MCP tools endpoint: {e}")
            self.results['total_failures'] += 1
        
        return True
    
    def test_memory_system(self):
        """Test if memory system actually works"""
        print("🔍 TESTING MEMORY SYSTEM...")
        
        # Try to actually add and retrieve a memory
        test_memory = f"Functional test at {datetime.now().isoformat()}"
        
        # Test add memory
        try:
            response = requests.post(
                'https://bonzai-backend.railway.app/api/memory/add',
                json={'content': test_memory, 'user_id': 'test_user'},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("✅ Memory add works")
                    memory_id = result.get('memory_id')
                    
                    # Test search memory
                    search_response = requests.post(
                        'https://bonzai-backend.railway.app/api/memory/search',
                        json={'query': 'Functional test', 'user_id': 'test_user'},
                        timeout=10
                    )
                    
                    if search_response.status_code == 200:
                        search_result = search_response.json()
                        if search_result.get('results') and len(search_result['results']) > 0:
                            print("✅ Memory search works")
                            self.results['working_systems'].append("Complete memory system: add + search")
                        else:
                            print("❌ Memory search returns no results")
                            self.results['partially_working'].append("Memory: add works, search broken")
                            self.results['total_failures'] += 1
                    else:
                        print(f"❌ Memory search broken: {search_response.status_code}")
                        self.results['partially_working'].append("Memory: add works, search broken")
                        self.results['total_failures'] += 1
                else:
                    print("❌ Memory add fails")
                    self.results['broken_systems'].append("Memory add: API error")
                    self.results['total_failures'] += 1
            else:
                print(f"❌ Memory add broken: {response.status_code}")
                self.results['broken_systems'].append(f"Memory add: {response.status_code}")
                self.results['total_failures'] += 1
                
        except Exception as e:
            print(f"❌ Memory system completely broken: {e}")
            self.results['critical_failures'].append(f"Memory system: {e}")
            self.results['total_failures'] += 1
    
    def test_ai_orchestration(self):
        """Test if AI orchestration actually works"""
        print("🔍 TESTING AI ORCHESTRATION...")
        
        # Test if we can actually call an AI model
        try:
            response = requests.post(
                'https://bonzai-backend.railway.app/api/mcp/execute',
                json={
                    'tool': 'orchestrate_ai',
                    'parameters': {
                        'model': 'gemini-2.5-flash',
                        'prompt': 'Say hello and confirm you are working'
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success') and 'response' in result.get('result', {}):
                    ai_response = result['result']['response']
                    if len(ai_response) > 10:  # Actual response, not just status
                        print(f"✅ AI orchestration works: {ai_response[:50]}...")
                        self.results['working_systems'].append("AI orchestration: real AI responses")
                    else:
                        print("❌ AI orchestration returns fake responses")
                        self.results['broken_systems'].append("AI orchestration: fake responses")
                        self.results['total_failures'] += 1
                else:
                    print("❌ AI orchestration fails")
                    self.results['broken_systems'].append("AI orchestration: API error")
                    self.results['total_failures'] += 1
            else:
                print(f"❌ AI orchestration broken: {response.status_code}")
                self.results['broken_systems'].append(f"AI orchestration: {response.status_code}")
                self.results['total_failures'] += 1
                
        except Exception as e:
            print(f"❌ AI orchestration completely broken: {e}")
            self.results['critical_failures'].append(f"AI orchestration: {e}")
            self.results['total_failures'] += 1
    
    def test_local_backend(self):
        """Test if local backend actually starts without crashes"""
        print("🔍 TESTING LOCAL BACKEND...")
        
        # Try to start the backend and see if it crashes
        import subprocess
        
        try:
            # Try to import the main app to see if it has syntax errors
            import sys
            sys.path.append('/mnt/c/Bonzai-Desktop/bonzai-core-engine')
            
            # This will fail if there are import errors
            from app import app
            
            print("✅ Backend code imports without errors")
            self.results['working_systems'].append("Backend code: clean imports")
            
        except ImportError as e:
            print(f"❌ Backend has import errors: {e}")
            self.results['critical_failures'].append(f"Backend imports: {e}")
            self.results['total_failures'] += 1
        except Exception as e:
            print(f"❌ Backend completely broken: {e}")
            self.results['critical_failures'].append(f"Backend code: {e}")
            self.results['total_failures'] += 1
    
    def generate_honest_report(self):
        """Generate brutally honest report"""
        print("\n" + "="*60)
        print("🔍 REAL FUNCTIONAL TEST REPORT - NO BULLSHIT")
        print("="*60)
        
        print(f"⏰ Test Time: {self.results['timestamp']}")
        print(f"❌ Total Failures: {self.results['total_failures']}")
        
        if self.results['critical_failures']:
            print(f"\n🚨 CRITICAL FAILURES ({len(self.results['critical_failures'])}):")
            for failure in self.results['critical_failures']:
                print(f"   💥 {failure}")
        
        if self.results['broken_systems']:
            print(f"\n❌ BROKEN SYSTEMS ({len(self.results['broken_systems'])}):")
            for system in self.results['broken_systems']:
                print(f"   🔴 {system}")
        
        if self.results['partially_working']:
            print(f"\n🟡 PARTIALLY WORKING ({len(self.results['partially_working'])}):")
            for system in self.results['partially_working']:
                print(f"   🟡 {system}")
        
        if self.results['working_systems']:
            print(f"\n✅ ACTUALLY WORKING ({len(self.results['working_systems'])}):")
            for system in self.results['working_systems']:
                print(f"   🟢 {system}")
        
        print("\n" + "="*60)
        print("🎯 BRUTAL HONESTY ASSESSMENT")
        print("="*60)
        
        total_systems = (len(self.results['working_systems']) + 
                        len(self.results['partially_working']) + 
                        len(self.results['broken_systems']) + 
                        len(self.results['critical_failures']))
        
        working_percentage = (len(self.results['working_systems']) / total_systems * 100) if total_systems > 0 else 0
        
        if working_percentage >= 80:
            verdict = "🟢 ACTUALLY WORKING - Ready for Nathan's kids' future"
        elif working_percentage >= 60:
            verdict = "🟡 PARTIALLY WORKING - Needs fixes before deployment"
        elif working_percentage >= 40:
            verdict = "🔴 MOSTLY BROKEN - Major fixes needed"
        else:
            verdict = "💥 COMPLETELY FUCKED - Start over"
        
        print(f"Working Systems: {working_percentage:.1f}%")
        print(f"Verdict: {verdict}")
        
        if self.results['total_failures'] > 0:
            print(f"\n⚠️  WARNING: {self.results['total_failures']} systems are not working")
            print("   This affects Nathan's investment and his kids' future")
            print("   IMMEDIATE ACTION REQUIRED")
        
        print("\n" + "="*60)
        
        # Save results to file
        with open('/mnt/c/Bonzai-Desktop/bonzai-core-engine/HONEST_TEST_RESULTS.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return working_percentage >= 70
    
    def run_all_tests(self):
        """Run all tests and be brutally honest"""
        print("🔍 STARTING REAL FUNCTIONAL TESTS")
        print("No more bullshit. Testing what actually works.")
        print("="*60)
        
        self.test_railway_deployment()
        self.test_memory_system()
        self.test_ai_orchestration()
        self.test_local_backend()
        
        return self.generate_honest_report()

if __name__ == "__main__":
    tester = RealFunctionalTest()
    success = tester.run_all_tests()
    
    if not success:
        print("\n💥 SYSTEM IS NOT READY")
        print("Nathan's investment is at risk")
        print("IMMEDIATE FIXES REQUIRED")
        exit(1)
    else:
        print("\n✅ SYSTEM IS ACTUALLY WORKING")
        print("Ready for Nathan's family")
        exit(0)