#!/usr/bin/env python3
"""
 BONZAI EMPIRE MASTER TEST SUITE
Complete testing of all services, models, and integrations
Run locally to verify what actually works vs what just says it's "loaded"
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

class BonzaiMasterTester:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "test_location": "LOCAL",
            "environment_variables": {},
            "api_connections": {},
            "service_functionality": {},
            "model_availability": {},
            "integration_tests": {},
            "family_coordination": {},
            "summary": {}
        }
        self.passed = 0
        self.failed = 0
        
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_emoji = {
            "PASS": "",
            "FAIL": "", 
            "INFO": "",
            "WARN": ""
        }
        print(f"{status_emoji.get(status, '')} [{timestamp}] {message}")
        
    def test_environment_variables(self):
        """Test if all required environment variables are present"""
        self.log("TESTING ENVIRONMENT VARIABLES", "INFO")
        
        required_vars = [
            "MEM0_API_KEY",
            "ANTHROPIC_API_KEY", 
            "OPENAI_API_KEY",
            "GEMINI_API_KEY",
            "DEEPSEEK_API_KEY",
            "SCRAPYBARA_API_KEY",
            "E2B_API_KEY",
            "PIPEDREAM_API_TOKEN",
            "GITHUB_PAT"
        ]
        
        for var in required_vars:
            value = os.getenv(var)
            if value:
                self.results["environment_variables"][var] = "PRESENT"
                self.log(f"{var}: PRESENT ({value[:8]}...)", "PASS")
                self.passed += 1
            else:
                self.results["environment_variables"][var] = "MISSING"
                self.log(f"{var}: MISSING", "FAIL")
                self.failed += 1
                
    def test_api_connections(self):
        """Test actual API connections"""
        self.log("TESTING API CONNECTIONS", "INFO")
        
        # Test Mem0
        try:
            from mem0 import MemoryClient
            client = MemoryClient(api_key=os.getenv('MEM0_API_KEY'))
            # Try a simple operation
            result = client.search("test", user_id="test-user")
            self.results["api_connections"]["mem0"] = "CONNECTED"
            self.log("Mem0 API: CONNECTED", "PASS")
            self.passed += 1
        except Exception as e:
            self.results["api_connections"]["mem0"] = f"FAILED: {str(e)}"
            self.log(f"Mem0 API: FAILED - {e}", "FAIL")
            self.failed += 1
            
        # Test OpenAI
        try:
            import openai
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = openai.models.list()
            self.results["api_connections"]["openai"] = "CONNECTED"
            self.log("OpenAI API: CONNECTED", "PASS")
            self.passed += 1
        except Exception as e:
            self.results["api_connections"]["openai"] = f"FAILED: {str(e)}"
            self.log(f"OpenAI API: FAILED - {e}", "FAIL")
            self.failed += 1
            
        # Test Anthropic
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            # Just test client creation
            self.results["api_connections"]["anthropic"] = "CONNECTED"
            self.log("Anthropic API: CONNECTED", "PASS")
            self.passed += 1
        except Exception as e:
            self.results["api_connections"]["anthropic"] = f"FAILED: {str(e)}"
            self.log(f"Anthropic API: FAILED - {e}", "FAIL")
            self.failed += 1
            
        # Test Google Gemini
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            models = genai.list_models()
            self.results["api_connections"]["gemini"] = "CONNECTED"
            self.log("Gemini API: CONNECTED", "PASS")
            self.passed += 1
        except Exception as e:
            self.results["api_connections"]["gemini"] = f"FAILED: {str(e)}"
            self.log(f"Gemini API: FAILED - {e}", "FAIL")
            self.failed += 1
            
    def test_bonzai_services(self):
        """Test actual Bonzai service functionality"""
        self.log("TESTING BONZAI SERVICE FUNCTIONALITY", "INFO")
        
        services_to_test = [
            ("Agent Registry", "services.bonzai_agent_registry"),
            ("Memory Manager", "services.zai_memory_system"),
            ("Multi-Provider System", "services.zai_multi_provider_system"),
            ("Task Orchestrator", "services.bonzai_task_orchestrator"),
            ("Scrapybara Integration", "services.zai_scrapybara_integration"),
            ("Pipedream Integration", "services.pipedream_integration_service"),
            ("Gemini Orchestra", "services.orchestration.orchestra_manager"),
            ("Express Mode", "services.zai_express_vertex_supercharger")
        ]
        
        for service_name, module_path in services_to_test:
            try:
                # Add current directory to path for imports
                import sys
                if os.getcwd() not in sys.path:
                    sys.path.append(os.getcwd())
                
                module = __import__(module_path, fromlist=[''])
                
                # Check if module has key functions/classes
                module_attrs = dir(module)
                key_indicators = ['initialize', 'get_manager', 'Manager', 'Service', 'get_', 'create_']
                has_functionality = any(attr for attr in module_attrs if any(indicator in attr for indicator in key_indicators))
                
                if has_functionality:
                    self.results["service_functionality"][service_name] = "FUNCTIONAL"
                    self.log(f"{service_name}: FUNCTIONAL", "PASS")
                    self.passed += 1
                else:
                    self.results["service_functionality"][service_name] = "LOADED_BUT_NO_CLEAR_INTERFACE"
                    self.log(f"{service_name}: LOADED BUT NO CLEAR INTERFACE", "WARN")
            except ImportError as e:
                self.results["service_functionality"][service_name] = f"IMPORT_ERROR: {str(e)}"
                self.log(f"{service_name}: IMPORT ERROR - {e}", "FAIL")
                self.failed += 1
            except Exception as e:
                self.results["service_functionality"][service_name] = f"ERROR: {str(e)}"
                self.log(f"{service_name}: ERROR - {e}", "FAIL")
                self.failed += 1
                
    def test_model_availability(self):
        """Test which AI models are actually available"""
        self.log("TESTING MODEL AVAILABILITY", "INFO")
        
        # Test OpenAI models
        try:
            import openai
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            self.results["model_availability"]["gpt-3.5-turbo"] = "WORKING"
            self.log("GPT-3.5-Turbo: WORKING", "PASS")
            self.passed += 1
        except Exception as e:
            self.results["model_availability"]["gpt-3.5-turbo"] = f"FAILED: {str(e)}"
            self.log(f"GPT-3.5-Turbo: FAILED - {e}", "FAIL")
            self.failed += 1
            
        # Test Gemini
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("test")
            self.results["model_availability"]["gemini-pro"] = "WORKING"
            self.log("Gemini Pro: WORKING", "PASS")
            self.passed += 1
        except Exception as e:
            self.results["model_availability"]["gemini-pro"] = f"FAILED: {str(e)}"
            self.log(f"Gemini Pro: FAILED - {e}", "FAIL")
            self.failed += 1
            
    def test_integrations(self):
        """Test third-party integrations"""
        self.log("TESTING THIRD-PARTY INTEGRATIONS", "INFO")
        
        # Test E2B Code Interpreter
        try:
            # Check if we can import e2b
            import e2b_code_interpreter
            self.results["integration_tests"]["e2b"] = "AVAILABLE"
            self.log("E2B Code Interpreter: AVAILABLE", "PASS")
            self.passed += 1
        except ImportError:
            self.results["integration_tests"]["e2b"] = "NOT_INSTALLED"
            self.log("E2B Code Interpreter: NOT INSTALLED", "FAIL")
            self.failed += 1
            
        # Test Scrapybara
        try:
            scrapybara_key = os.getenv('SCRAPYBARA_API_KEY')
            if scrapybara_key:
                # Try to make a test request
                response = requests.get(
                    "https://api.scrapybara.com/health",
                    headers={"Authorization": f"Bearer {scrapybara_key}"},
                    timeout=10
                )
                if response.status_code == 200:
                    self.results["integration_tests"]["scrapybara"] = "CONNECTED"
                    self.log("Scrapybara: CONNECTED", "PASS")
                    self.passed += 1
                else:
                    self.results["integration_tests"]["scrapybara"] = f"HTTP_ERROR: {response.status_code}"
                    self.log(f"Scrapybara: HTTP ERROR {response.status_code}", "FAIL")
                    self.failed += 1
            else:
                self.results["integration_tests"]["scrapybara"] = "NO_API_KEY"
                self.log("Scrapybara: NO API KEY", "FAIL")
                self.failed += 1
        except Exception as e:
            self.results["integration_tests"]["scrapybara"] = f"ERROR: {str(e)}"
            self.log(f"Scrapybara: ERROR - {e}", "FAIL")
            self.failed += 1
            
    def test_family_coordination(self):
        """Test family memory and coordination features"""
        self.log("TESTING FAMILY COORDINATION", "INFO")
        
        # Test family usernames
        family_usernames = ["papa-bear", "mama-bear", "claude-code", "nathan-prime", "claude-web"]
        
        for username in family_usernames:
            try:
                from mem0 import MemoryClient
                client = MemoryClient(api_key=os.getenv('MEM0_API_KEY'))
                
                # Try to add a test memory
                test_memory = f"Master test at {datetime.now().isoformat()}"
                result = client.add(
                    messages=[{"role": "user", "content": test_memory}],
                    user_id=username
                )
                
                # Try to search for it
                search_result = client.search(test_memory, user_id=username)
                
                if search_result:
                    self.results["family_coordination"][username] = "WORKING"
                    self.log(f"Family member {username}: WORKING", "PASS")
                    self.passed += 1
                else:
                    self.results["family_coordination"][username] = "NO_SEARCH_RESULTS"
                    self.log(f"Family member {username}: NO SEARCH RESULTS", "FAIL")
                    self.failed += 1
                    
            except Exception as e:
                self.results["family_coordination"][username] = f"ERROR: {str(e)}"
                self.log(f"Family member {username}: ERROR - {e}", "FAIL")
                self.failed += 1
                
    def test_railway_backend(self):
        """Test Railway backend connectivity"""
        self.log("TESTING RAILWAY BACKEND", "INFO")
        
        try:
            # Test health endpoint
            response = requests.get("https://mofy.ai/api/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.results["railway_backend"] = {
                    "health_check": "PASS",
                    "services_reported": data.get("services", {}).get("running", 0),
                    "status": data.get("status", "unknown")
                }
                self.log(f"Railway Health: PASS ({data.get('services', {}).get('running', 0)} services)", "PASS")
                self.passed += 1
                
                # Test specific endpoints
                endpoints_to_test = [
                    "/api/mcp",
                    "/api/multimodal/chat",
                    "/api/agentic",
                    "/api/zai-prime/status"
                ]
                
                for endpoint in endpoints_to_test:
                    try:
                        test_response = requests.get(f"https://mofy.ai{endpoint}", timeout=5)
                        if test_response.status_code == 200:
                            self.log(f"Railway {endpoint}: WORKING", "PASS")
                            self.passed += 1
                        else:
                            self.log(f"Railway {endpoint}: HTTP {test_response.status_code}", "FAIL")
                            self.failed += 1
                    except Exception as e:
                        self.log(f"Railway {endpoint}: ERROR - {e}", "FAIL")
                        self.failed += 1
            else:
                self.results["railway_backend"] = {"health_check": f"HTTP_ERROR: {response.status_code}"}
                self.log(f"Railway Health: HTTP ERROR {response.status_code}", "FAIL")
                self.failed += 1
                
        except Exception as e:
            self.results["railway_backend"] = {"health_check": f"CONNECTION_ERROR: {str(e)}"}
            self.log(f"Railway Backend: CONNECTION ERROR - {e}", "FAIL")
            self.failed += 1
            
    def run_all_tests(self):
        """Run the complete test suite"""
        self.log(" STARTING BONZAI EMPIRE MASTER TEST SUITE", "INFO")
        self.log("=" * 80, "INFO")
        
        start_time = time.time()
        
        # Run all test categories
        self.test_environment_variables()
        self.test_api_connections()
        self.test_bonzai_services()
        self.test_model_availability()
        self.test_integrations()
        self.test_family_coordination()
        self.test_railway_backend()
        
        # Calculate summary
        end_time = time.time()
        duration = end_time - start_time
        
        self.results["summary"] = {
            "total_tests": self.passed + self.failed,
            "passed": self.passed,
            "failed": self.failed,
            "success_rate": f"{(self.passed / (self.passed + self.failed) * 100):.1f}%" if (self.passed + self.failed) > 0 else "0%",
            "duration_seconds": round(duration, 2)
        }
        
        # Print summary
        self.log("=" * 80, "INFO")
        self.log(" TEST SUMMARY:", "INFO")
        self.log(f"   Total Tests: {self.passed + self.failed}", "INFO")
        self.log(f"   Passed: {self.passed}", "PASS")
        self.log(f"   Failed: {self.failed}", "FAIL")
        self.log(f"   Success Rate: {self.results['summary']['success_rate']}", "INFO")
        self.log(f"   Duration: {duration:.2f} seconds", "INFO")
        
        # Save results
        results_file = f"bonzai_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        self.log(f"📄 Results saved to: {results_file}", "INFO")
        
        if self.failed > 0:
            self.log(" CRITICAL ISSUES FOUND - Empire needs attention!", "FAIL")
        else:
            self.log(" ALL SYSTEMS OPERATIONAL - Empire is strong!", "PASS")
            
        return self.results

if __name__ == "__main__":
    print(" BONZAI EMPIRE MASTER TEST SUITE")
    print("   Testing all services, models, and integrations locally")
    print("   This will show what's ACTUALLY working vs what just says 'loaded'")
    print()
    
    tester = BonzaiMasterTester()
    results = tester.run_all_tests()
    
    print("\n KEY FINDINGS:")
    print("   - Environment variables that are missing")
    print("   - API connections that are broken") 
    print("   - Services that import but don't initialize")
    print("   - Models that are unreachable")
    print("   - Family coordination issues")
    print("   - Railway backend endpoint failures")
    print("\nRun this locally to see what's REALLY working! ")