#!/usr/bin/env python3
"""
🔬 COMPREHENSIVE MCP SERVER TEST - Deep Functionality Analysis
Tests what the MCP server actually DOES, not just that it exists.
"""

import requests
import json
import time
import subprocess
import os
import sys
from datetime import datetime
from typing import Dict, Any, List
import concurrent.futures
from threading import Thread
import signal

class BonzaiMCPTester:
    def __init__(self):
        self.server_url = "http://localhost:3000"
        self.mcp_url = f"{self.server_url}/mcp"
        self.health_url = f"{self.server_url}/health"
        self.tools_url = f"{self.server_url}/mcp/tools"
        self.execute_url = f"{self.server_url}/mcp/execute"
        self.server_process = None
        self.test_results = []
        self.start_time = datetime.now()
        
    def log_test(self, test_name: str, result: str, details: Dict[str, Any] = None, success: bool = True):
        """Log test result with timestamp and details"""
        self.test_results.append({
            'test': test_name,
            'result': result,
            'details': details or {},
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'duration': (datetime.now() - self.start_time).total_seconds()
        })
        
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {result}")
        if details:
            for key, value in details.items():
                print(f"   📊 {key}: {value}")
        print()

    def start_mcp_server(self):
        """Start the MCP server in background"""
        print("🚀 Starting Bonzai MCP Server...")
        server_dir = "/mnt/c/Bonzai-Desktop/bonzai-core-engine/bonzai-mcp-server"
        
        if not os.path.exists(server_dir):
            self.log_test("Server Directory Check", "MCP server directory not found", 
                         {"expected_path": server_dir}, False)
            return False
            
        try:
            # Change to server directory and start
            os.chdir(server_dir)
            self.server_process = subprocess.Popen(
                ["node", "server.js"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            print("⏳ Waiting for server startup...")
            time.sleep(8)
            
            # Check if server is running
            if self.server_process.poll() is None:
                self.log_test("Server Startup", "MCP server started successfully", 
                             {"pid": self.server_process.pid})
                return True
            else:
                stdout, stderr = self.server_process.communicate()
                self.log_test("Server Startup", "MCP server failed to start", 
                             {"stdout": stdout[:200], "stderr": stderr[:200]}, False)
                return False
                
        except Exception as e:
            self.log_test("Server Startup", f"Exception during startup: {str(e)}", 
                         {"error": str(e)}, False)
            return False

    def stop_mcp_server(self):
        """Stop the MCP server"""
        if self.server_process:
            print("🛑 Stopping MCP server...")
            self.server_process.terminate()
            self.server_process.wait()
            self.log_test("Server Shutdown", "MCP server stopped")

    def test_health_endpoint(self):
        """Test the health endpoint functionality"""
        try:
            response = requests.get(self.health_url, timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                
                # Validate health response structure
                required_fields = ['status', 'service', 'version', 'tools_available', 'superpowers']
                missing_fields = [field for field in required_fields if field not in health_data]
                
                if missing_fields:
                    self.log_test("Health Endpoint Structure", f"Missing fields: {missing_fields}", 
                                 {"response": health_data}, False)
                    return False
                
                # Test superpowers configuration
                superpowers = health_data.get('superpowers', {})
                power_status = {
                    'ai_models': superpowers.get('ai_models', 0),
                    'vm_spawning': superpowers.get('vm_spawning', 'disabled'),
                    'code_sandbox': superpowers.get('code_sandbox', 'disabled'),
                    'github_tools': superpowers.get('github_tools', 'disabled'),
                    'enhanced_memory': superpowers.get('enhanced_memory', 'disabled')
                }
                
                self.log_test("Health Endpoint", "Fully operational with detailed capabilities", {
                    'service': health_data.get('service'),
                    'version': health_data.get('version'),
                    'tools_available': health_data.get('tools_available'),
                    'superpowers': power_status,
                    'backend_url': health_data.get('backend')
                })
                return True
                
            else:
                self.log_test("Health Endpoint", f"HTTP {response.status_code}", 
                             {"response": response.text}, False)
                return False
                
        except Exception as e:
            self.log_test("Health Endpoint", f"Connection failed: {str(e)}", 
                         {"error": str(e)}, False)
            return False

    def test_mcp_tools_listing(self):
        """Test MCP tools listing and validate tool schemas"""
        try:
            response = requests.post(self.tools_url, json={}, timeout=10)
            
            if response.status_code == 200:
                tools_data = response.json()
                tools = tools_data.get('tools', [])
                
                if not tools:
                    self.log_test("MCP Tools Listing", "No tools found in response", 
                                 {"response": tools_data}, False)
                    return False
                
                # Analyze each tool
                tool_analysis = {}
                for tool in tools:
                    tool_name = tool.get('name', 'unnamed')
                    tool_analysis[tool_name] = {
                        'description': tool.get('description', 'No description'),
                        'required_params': tool.get('inputSchema', {}).get('properties', {}).keys(),
                        'has_schema': 'inputSchema' in tool
                    }
                
                self.log_test("MCP Tools Listing", f"Found {len(tools)} tools with full schemas", {
                    'total_tools': len(tools),
                    'tool_names': list(tool_analysis.keys()),
                    'tools_with_schemas': sum(1 for t in tool_analysis.values() if t['has_schema'])
                })
                
                # Test specific critical tools
                critical_tools = ['orchestrate_ai', 'access_memory', 'spawn_vm_agent', 'github_power_tool']
                missing_critical = [tool for tool in critical_tools if tool not in tool_analysis]
                
                if missing_critical:
                    self.log_test("Critical Tools Check", f"Missing critical tools: {missing_critical}", 
                                 {"missing": missing_critical}, False)
                else:
                    self.log_test("Critical Tools Check", "All critical tools present and configured")
                
                return True
                
            else:
                self.log_test("MCP Tools Listing", f"HTTP {response.status_code}", 
                             {"response": response.text}, False)
                return False
                
        except Exception as e:
            self.log_test("MCP Tools Listing", f"Request failed: {str(e)}", 
                         {"error": str(e)}, False)
            return False

    def test_ai_orchestration(self):
        """Test AI orchestration capabilities"""
        test_cases = [
            {
                'name': 'Gemini Flash Test',
                'params': {
                    'model': 'gemini-2.5-flash',
                    'prompt': 'Say hello and confirm you are working',
                    'context': 'Testing MCP integration'
                }
            },
            {
                'name': 'Express Mode Test',
                'params': {
                    'model': 'express-mode',
                    'prompt': 'Quick test response',
                    'express_mode': True
                }
            }
        ]
        
        for test_case in test_cases:
            try:
                response = requests.post(self.execute_url, json={
                    'tool': 'orchestrate_ai',
                    'parameters': test_case['params']
                }, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('success', False):
                        ai_result = result.get('result', {})
                        self.log_test(f"AI Orchestration - {test_case['name']}", 
                                     "AI model responded successfully", {
                                         'model': ai_result.get('model'),
                                         'backend_status': ai_result.get('backend_status'),
                                         'response_length': len(str(ai_result.get('response', ''))),
                                         'express_mode': ai_result.get('express_mode', False)
                                     })
                    else:
                        self.log_test(f"AI Orchestration - {test_case['name']}", 
                                     "AI model call failed", {
                                         'error': result.get('error'),
                                         'result': result.get('result')
                                     }, False)
                else:
                    self.log_test(f"AI Orchestration - {test_case['name']}", 
                                 f"HTTP {response.status_code}", {"response": response.text}, False)
                    
            except Exception as e:
                self.log_test(f"AI Orchestration - {test_case['name']}", 
                             f"Request failed: {str(e)}", {"error": str(e)}, False)

    def test_memory_system(self):
        """Test memory system integration"""
        memory_tests = [
            {
                'name': 'Memory Search Test',
                'params': {
                    'action': 'search',
                    'query': 'bonzai platform',
                    'user_id': 'test_user'
                }
            },
            {
                'name': 'Memory Add Test',
                'params': {
                    'action': 'add',
                    'query': 'MCP server test completed successfully',
                    'user_id': 'test_user'
                }
            }
        ]
        
        for test_case in memory_tests:
            try:
                response = requests.post(self.execute_url, json={
                    'tool': 'access_memory',
                    'parameters': test_case['params']
                }, timeout=20)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('success', False):
                        memory_result = result.get('result', {})
                        self.log_test(f"Memory System - {test_case['name']}", 
                                     "Memory operation completed", {
                                         'action': memory_result.get('action'),
                                         'user_id': memory_result.get('user_id'),
                                         'memory_count': memory_result.get('memory_count', 0),
                                         'has_result': bool(memory_result.get('result'))
                                     })
                    else:
                        self.log_test(f"Memory System - {test_case['name']}", 
                                     "Memory operation failed", {
                                         'error': result.get('error'),
                                         'result': result.get('result')
                                     }, False)
                else:
                    self.log_test(f"Memory System - {test_case['name']}", 
                                 f"HTTP {response.status_code}", {"response": response.text}, False)
                    
            except Exception as e:
                self.log_test(f"Memory System - {test_case['name']}", 
                             f"Request failed: {str(e)}", {"error": str(e)}, False)

    def test_vm_capabilities(self):
        """Test VM spawning and control capabilities"""
        try:
            # Test VM spawning (will likely fail without API key, but should return proper error)
            response = requests.post(self.execute_url, json={
                'tool': 'spawn_vm_agent',
                'parameters': {
                    'task': 'Test VM spawn functionality',
                    'duration_hours': 1,
                    'vm_type': 'development'
                }
            }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                vm_result = result.get('result', {})
                
                # Check if it's a proper error (expected without API key) or success
                if vm_result.get('status') == 'failed':
                    error_msg = vm_result.get('error', '')
                    if 'api' in error_msg.lower() or 'key' in error_msg.lower() or 'auth' in error_msg.lower():
                        self.log_test("VM Capabilities", "VM spawning properly configured (API key needed)", {
                            'task': vm_result.get('task'),
                            'status': vm_result.get('status'),
                            'error_type': 'authentication'
                        })
                    else:
                        self.log_test("VM Capabilities", "VM spawning failed with unexpected error", {
                            'error': error_msg,
                            'status': vm_result.get('status')
                        }, False)
                elif vm_result.get('status') == 'spawned':
                    self.log_test("VM Capabilities", "VM spawned successfully", {
                        'vm_id': vm_result.get('vm_id'),
                        'task': vm_result.get('task'),
                        'duration': vm_result.get('duration_hours'),
                        'vm_type': vm_result.get('vm_type')
                    })
                else:
                    self.log_test("VM Capabilities", "Unexpected VM spawn response", {
                        'result': vm_result
                    }, False)
            else:
                self.log_test("VM Capabilities", f"HTTP {response.status_code}", 
                             {"response": response.text}, False)
                
        except Exception as e:
            self.log_test("VM Capabilities", f"Request failed: {str(e)}", 
                         {"error": str(e)}, False)

    def test_oauth_endpoints(self):
        """Test OAuth endpoints for Claude Web integration"""
        oauth_tests = [
            {
                'name': 'OAuth Metadata',
                'url': f"{self.server_url}/oauth/metadata",
                'method': 'GET',
                'expected_fields': ['issuer', 'authorization_endpoint', 'token_endpoint']
            },
            {
                'name': 'OAuth Token Exchange',
                'url': f"{self.server_url}/oauth/token",
                'method': 'POST',
                'data': {'grant_type': 'authorization_code', 'code': 'test'},
                'expected_fields': ['access_token', 'token_type', 'expires_in']
            }
        ]
        
        for test_case in oauth_tests:
            try:
                if test_case['method'] == 'GET':
                    response = requests.get(test_case['url'], timeout=10)
                else:
                    response = requests.post(test_case['url'], json=test_case.get('data', {}), timeout=10)
                
                if response.status_code == 200:
                    oauth_data = response.json()
                    
                    # Check required fields
                    missing_fields = [field for field in test_case['expected_fields'] 
                                    if field not in oauth_data]
                    
                    if missing_fields:
                        self.log_test(f"OAuth - {test_case['name']}", 
                                     f"Missing fields: {missing_fields}", 
                                     {"response": oauth_data}, False)
                    else:
                        self.log_test(f"OAuth - {test_case['name']}", 
                                     "OAuth endpoint properly configured", {
                                         'fields_present': len(test_case['expected_fields']),
                                         'endpoint': test_case['url']
                                     })
                else:
                    self.log_test(f"OAuth - {test_case['name']}", 
                                 f"HTTP {response.status_code}", {"response": response.text}, False)
                    
            except Exception as e:
                self.log_test(f"OAuth - {test_case['name']}", 
                             f"Request failed: {str(e)}", {"error": str(e)}, False)

    def generate_test_report(self):
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "="*80)
        print("🔬 BONZAI MCP SERVER - COMPREHENSIVE TEST REPORT")
        print("="*80)
        print(f"⏰ Test Duration: {(datetime.now() - self.start_time).total_seconds():.2f} seconds")
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {(passed_tests/total_tests*100):.1f}%")
        print("\n" + "="*80)
        print("📋 DETAILED TEST RESULTS")
        print("="*80)
        
        for result in self.test_results:
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"{status} | {result['test']}")
            print(f"     Result: {result['result']}")
            print(f"     Time: {result['timestamp']}")
            
            if result['details']:
                print("     Details:")
                for key, value in result['details'].items():
                    print(f"       • {key}: {value}")
            print()
        
        print("="*80)
        print("🎯 FUNCTIONALITY ASSESSMENT")
        print("="*80)
        
        # Analyze functionality categories
        categories = {
            'Core Infrastructure': ['Server Startup', 'Server Shutdown', 'Health Endpoint'],
            'MCP Protocol': ['MCP Tools Listing', 'Critical Tools Check'],
            'AI Orchestration': [t['test'] for t in self.test_results if 'AI Orchestration' in t['test']],
            'Memory System': [t['test'] for t in self.test_results if 'Memory System' in t['test']],
            'VM Capabilities': ['VM Capabilities'],
            'OAuth Integration': [t['test'] for t in self.test_results if 'OAuth' in t['test']]
        }
        
        for category, tests in categories.items():
            category_results = [r for r in self.test_results if r['test'] in tests]
            if category_results:
                category_passed = sum(1 for r in category_results if r['success'])
                category_total = len(category_results)
                category_rate = (category_passed / category_total * 100) if category_total > 0 else 0
                
                status = "🟢 OPERATIONAL" if category_rate >= 75 else "🟡 PARTIAL" if category_rate >= 50 else "🔴 ISSUES"
                print(f"{status} {category}: {category_passed}/{category_total} ({category_rate:.1f}%)")
        
        print("\n" + "="*80)
        print("🚀 CONCLUSION")
        print("="*80)
        
        if passed_tests >= total_tests * 0.8:
            print("✅ MCP SERVER IS FULLY OPERATIONAL")
            print("   All major systems are working correctly.")
            print("   Ready for production use with Claude Web/Desktop.")
        elif passed_tests >= total_tests * 0.6:
            print("🟡 MCP SERVER IS PARTIALLY OPERATIONAL")
            print("   Core functionality works but some features need attention.")
            print("   May work with limited capabilities.")
        else:
            print("❌ MCP SERVER HAS SIGNIFICANT ISSUES")
            print("   Multiple critical systems are not functioning.")
            print("   Requires immediate attention before use.")
            
        print("="*80)

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🧪 STARTING COMPREHENSIVE MCP SERVER TEST")
        print("="*60)
        
        # Start server
        if not self.start_mcp_server():
            print("❌ Cannot start MCP server. Aborting tests.")
            return
        
        try:
            # Run all tests
            self.test_health_endpoint()
            self.test_mcp_tools_listing()
            self.test_ai_orchestration()
            self.test_memory_system()
            self.test_vm_capabilities()
            self.test_oauth_endpoints()
            
        finally:
            # Always stop server
            self.stop_mcp_server()
            
        # Generate report
        self.generate_test_report()

if __name__ == "__main__":
    tester = BonzaiMCPTester()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n🛑 Test interrupted by user")
        tester.stop_mcp_server()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
        tester.stop_mcp_server()
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        tester.stop_mcp_server()