#!/usr/bin/env python3
"""
🧪 BONZAI REAL SYSTEM TESTER
Test Nathan's actual sophisticated AI orchestration system
NO MORE MOCK RESPONSES - REAL AI CALLS ONLY!
"""
import requests
import json
import time
import asyncio
from datetime import datetime
from typing import Dict, Any
import os

class BonzaiRealTester:
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.results = []
        self.start_time = datetime.now()
        
    def log_result(self, test_name: str, success: bool, details: Dict[str, Any]):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if not success and "error" in details:
            print(f"    Error: {details['error']}")
    
    def test_basic_health(self):
        """Test basic health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            success = response.status_code == 200
            details = {
                "status_code": response.status_code,
                "response": response.json() if success else response.text
            }
        except Exception as e:
            success = False
            details = {"error": str(e)}
        
        self.log_result("Basic Health Check", success, details)
        return success
    
    def test_real_ai_orchestration(self):
        """Test REAL AI orchestration - no mocks!"""
        test_prompts = [
            {
                "name": "Simple Chat Test",
                "model": "gemini-2.0-flash-exp",
                "message": "Say 'Hello from Bonzai AI' and nothing else",
                "expect_real_response": True
            },
            {
                "name": "Multi-Model Routing Test", 
                "model": "auto",
                "message": "Test function calling capability",
                "expect_real_response": True
            },
            {
                "name": "Claude Computer Use Test",
                "model": "claude-3-5-sonnet",
                "message": "Use computer tools to list current directory",
                "expect_tools": True
            }
        ]
        
        for test in test_prompts:
            try:
                payload = {
                    "model": test["model"],
                    "message": test["message"],
                    "user_id": "real_test_user"
                }
                
                response = requests.post(
                    f"{self.base_url}/api/chat/simple", 
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "")
                    
                    # Check if this is a REAL AI response or mock
                    is_mock = (
                        "Chat response for:" in response_text or
                        "Backend ready" in response_text or
                        "Mock" in response_text or
                        response_text == test["message"]  # Exact echo = mock
                    )
                    
                    success = not is_mock and len(response_text) > 10
                    
                    details = {
                        "status_code": response.status_code,
                        "response_text": response_text,
                        "is_mock_detected": is_mock,
                        "model_used": data.get("model"),
                        "response_length": len(response_text)
                    }
                else:
                    success = False
                    details = {
                        "status_code": response.status_code,
                        "error": response.text
                    }
                    
            except Exception as e:
                success = False
                details = {"error": str(e)}
            
            self.log_result(f"REAL AI Test: {test['name']}", success, details)
    
    def test_multi_model_orchestrator(self):
        """Test the sophisticated multi-model orchestrator"""
        try:
            response = requests.get(f"{self.base_url}/api/multi-model/status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                details = {
                    "status": data.get("status"),
                    "available_models": data.get("available_models", 0),
                    "service_status": data.get("message")
                }
            else:
                success = False
                details = {"status_code": response.status_code, "error": response.text}
                
        except Exception as e:
            success = False
            details = {"error": str(e)}
        
        self.log_result("Multi-Model Orchestrator", success, details)
    
    def test_zai_prime_supervisor(self):
        """Test ZAI Prime Supervisor system"""
        endpoints = [
            "/api/zai-prime/status",
            "/api/zai-prime/agents", 
            "/api/zai-prime/context"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                success = response.status_code == 200
                
                if success:
                    data = response.json()
                    details = {
                        "status": data.get("success", False),
                        "zai_prime_data": data
                    }
                else:
                    details = {"status_code": response.status_code, "error": response.text}
                    
            except Exception as e:
                success = False
                details = {"error": str(e)}
            
            self.log_result(f"ZAI Prime: {endpoint}", success, details)
    
    def test_memory_systems(self):
        """Test memory systems (Neo4j, Qdrant, Redis)"""
        memory_tests = [
            {
                "endpoint": "/api/memory/search",
                "method": "POST",
                "data": {"query": "test memory search", "user_id": "test_user"}
            },
            {
                "endpoint": "/api/memory/add",
                "method": "POST", 
                "data": {"content": "Test memory content", "user_id": "test_user"}
            }
        ]
        
        for test in memory_tests:
            try:
                if test["method"] == "POST":
                    response = requests.post(
                        f"{self.base_url}{test['endpoint']}", 
                        json=test["data"],
                        timeout=10
                    )
                else:
                    response = requests.get(f"{self.base_url}{test['endpoint']}", timeout=10)
                
                success = response.status_code == 200
                details = {
                    "status_code": response.status_code,
                    "response": response.json() if success else response.text
                }
                
            except Exception as e:
                success = False
                details = {"error": str(e)}
            
            self.log_result(f"Memory System: {test['endpoint']}", success, details)
    
    def test_agent_spawning(self):
        """Test the agent spawning service (up to 8000 agents!)"""
        try:
            payload = {
                "agent_type": "general",
                "purpose": "Test agent spawning system",
                "page_context": "real_test",
                "config": {"test_mode": True}
            }
            
            response = requests.post(
                f"{self.base_url}/api/zai-prime/agents/spawn",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                details = {
                    "agent_spawned": data.get("success", False),
                    "agent_id": data.get("agent_id"),
                    "response": data
                }
            else:
                details = {"status_code": response.status_code, "error": response.text}
                
        except Exception as e:
            success = False
            details = {"error": str(e)}
        
        self.log_result("Agent Spawning Service", success, details)
    
    def test_computer_use_api(self):
        """Test Claude Computer Use API integration"""
        try:
            payload = {
                "model": "claude-3-5-sonnet",
                "message": "Use the computer tools to check system status",
                "enable_computer_use": True,
                "user_id": "computer_test_user"
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat/computer-use",
                json=payload,
                timeout=30
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                has_tools = "tool_calls" in data or "tools_used" in data
                details = {
                    "computer_use_active": has_tools,
                    "response": data.get("response", ""),
                    "tools_detected": has_tools
                }
            else:
                details = {"status_code": response.status_code, "error": response.text}
                
        except Exception as e:
            success = False
            details = {"error": str(e)}
        
        self.log_result("Computer Use API", success, details)
    
    def run_comprehensive_test(self):
        """Run all tests and generate report"""
        print("🧪 BONZAI REAL SYSTEM COMPREHENSIVE TEST")
        print("=" * 60)
        print(f"Testing backend at: {self.base_url}")
        print(f"Started at: {self.start_time}")
        print()
        
        # Run all tests
        self.test_basic_health()
        self.test_real_ai_orchestration() 
        self.test_multi_model_orchestrator()
        self.test_zai_prime_supervisor()
        self.test_memory_systems()
        self.test_agent_spawning()
        self.test_computer_use_api()
        
        # Generate final report
        self.generate_final_report()
    
    def generate_final_report(self):
        """Generate final test report"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "=" * 60)
        print("🎯 BONZAI REAL SYSTEM TEST REPORT")
        print("=" * 60)
        print(f"Duration: {duration:.2f} seconds")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if success_rate >= 80:
            print("🎉 EXCELLENT! Nathan's sophisticated system is working!")
        elif success_rate >= 60:
            print("🔧 GOOD PROGRESS! Some components need fixes")
        else:
            print("🚨 NEEDS ATTENTION! Multiple systems require fixing")
        
        # Save detailed results
        report_filename = f"BONZAI_REAL_TEST_RESULTS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump({
                "summary": {
                    "total_tests": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "success_rate": success_rate,
                    "duration_seconds": duration,
                    "test_url": self.base_url
                },
                "detailed_results": self.results
            }, f, indent=2)
        
        print(f"📄 Detailed results saved to: {report_filename}")

def main():
    """Run the real system test"""
    # Test both local and Railway
    urls_to_test = [
        "http://localhost:5001",
        # Add your Railway URL here: "https://your-app.railway.app"
    ]
    
    for url in urls_to_test:
        print(f"\n🌐 Testing: {url}")
        tester = BonzaiRealTester(url)
        tester.run_comprehensive_test()
        print()

if __name__ == "__main__":
    main()
