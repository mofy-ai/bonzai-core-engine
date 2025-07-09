#!/usr/bin/env python3
"""
🧪 NATHAN'S REAL AI TESTER - NO BULLSHIT VERSION
Test actual AI responses from your running backend
ZERO tolerance for mock responses!
"""
import requests
import json
import time
from datetime import datetime

class RealShitTester:
    def __init__(self):
        self.base_url = "http://localhost:5001"
        self.results = []
        
    def test_actual_ai_call(self, endpoint, payload, test_name):
        """Test real AI endpoint and detect mocks"""
        print(f"\n🧪 TESTING: {test_name}")
        print(f"Endpoint: {endpoint}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        print("-" * 50)
        
        try:
            start_time = time.time()
            response = requests.post(f"{self.base_url}{endpoint}", json=payload, timeout=30)
            duration = time.time() - start_time
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Time: {duration:.2f}s")
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", data.get("message", ""))
                
                # DETECT FAKE/MOCK RESPONSES
                mock_indicators = [
                    "Chat response for:",
                    "Backend ready", 
                    "Mock",
                    "Test response",
                    "Backend mapping test",
                    "Multi-model orchestration ready",
                    "AI orchestration for",
                    "Backend ready"
                ]
                
                is_mock = any(indicator in str(response_text) for indicator in mock_indicators)
                is_echo = response_text.strip() == payload.get("message", "").strip()
                is_empty = len(response_text.strip()) < 5
                
                if is_mock:
                    print("🚨 MOCK DETECTED! This is fake!")
                    print(f"Response: {response_text}")
                    result = "MOCK"
                elif is_echo:
                    print("🚨 ECHO DETECTED! Just repeating input!")
                    print(f"Response: {response_text}")
                    result = "ECHO"
                elif is_empty:
                    print("🚨 EMPTY RESPONSE!")
                    result = "EMPTY"
                else:
                    print("✅ REAL AI RESPONSE!")
                    print(f"Response: {response_text[:200]}...")
                    result = "REAL"
                
                # Show full response data
                print(f"\nFull Response Data:")
                print(json.dumps(data, indent=2))
                
            else:
                print(f"❌ HTTP ERROR: {response.status_code}")
                print(f"Error: {response.text}")
                result = "ERROR"
                
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
            result = "EXCEPTION"
        
        self.results.append({
            "test": test_name,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return result
    
    def run_hardcore_ai_tests(self):
        """Run hardcore tests on actual AI functionality"""
        print("🔥 NATHAN'S HARDCORE AI TESTING - NO BULLSHIT!")
        print("=" * 60)
        print(f"Backend URL: {self.base_url}")
        print(f"Time: {datetime.now()}")
        print()
        
        # Test 1: Simple Chat 
        self.test_actual_ai_call(
            "/api/chat/simple",
            {
                "model": "gemini-2.0-flash-exp",
                "message": "Say exactly 'BONZAI AI IS REAL' and nothing else",
                "user_id": "hardcore_test"
            },
            "Simple Gemini Chat Test"
        )
        
        # Test 2: Different Model
        self.test_actual_ai_call(
            "/api/chat/simple", 
            {
                "model": "claude-3-5-sonnet",
                "message": "Count from 1 to 5 and add 'CLAUDE WORKS' at the end",
                "user_id": "hardcore_test"
            },
            "Claude Model Test"
        )
        
        # Test 3: Multi-Model Orchestrator
        self.test_actual_ai_call(
            "/api/multi-model/chat",
            {
                "message": "What is 2 + 2? Answer only with the number.",
                "user_id": "hardcore_test",
                "auto_route": True
            },
            "Multi-Model Orchestrator Test"
        )
        
        # Test 4: ZAI Prime
        self.test_actual_ai_call(
            "/api/zai/chat",
            {
                "message": "Tell me the current time and say 'ZAI PRIME ACTIVE'",
                "user_id": "hardcore_test"
            },
            "ZAI Prime Chat Test"
        )
        
        # Test 5: Agent Orchestration
        self.test_actual_ai_call(
            "/api/agents/orchestrate",
            {
                "agent_type": "general",
                "message": "Generate a random 3-word phrase",
                "user_id": "hardcore_test"
            },
            "Agent Orchestration Test"
        )
        
        print("\n" + "=" * 60)
        print("🎯 HARDCORE TEST RESULTS SUMMARY")
        print("=" * 60)
        
        real_count = sum(1 for r in self.results if r["result"] == "REAL")
        mock_count = sum(1 for r in self.results if r["result"] == "MOCK")
        error_count = sum(1 for r in self.results if r["result"] in ["ERROR", "EXCEPTION", "EMPTY", "ECHO"])
        
        print(f"✅ REAL AI RESPONSES: {real_count}")
        print(f"🚨 MOCK/FAKE RESPONSES: {mock_count}")
        print(f"❌ ERRORS/ISSUES: {error_count}")
        print()
        
        if real_count > 0:
            print("🎉 SUCCESS! Your system has REAL AI!")
        elif mock_count > 0:
            print("⚠️ MOCKS DETECTED! Still some fake responses")
        else:
            print("🚨 NO AI WORKING! Need to fix connections")
        
        # Save results
        with open("HARDCORE_AI_TEST_RESULTS.json", "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Results saved to: HARDCORE_AI_TEST_RESULTS.json")

def main():
    """Run the hardcore test"""
    tester = RealShitTester()
    tester.run_hardcore_ai_tests()

if __name__ == "__main__":
    main()
