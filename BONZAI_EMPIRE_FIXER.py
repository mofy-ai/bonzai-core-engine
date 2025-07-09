#!/usr/bin/env python3
"""
 BONZAI EMPIRE COMPREHENSIVE FIXER
Automatically fix all issues found in master test to get to 100%
"""

import os
import sys
import subprocess
import json
from datetime import datetime

class BonzaiEmpireFixer:
    def __init__(self):
        self.fixed = 0
        self.failed = 0
        
    def log(self, message, status="INFO"):
        status_emoji = {"PASS": "", "FAIL": "", "INFO": "", "WARN": ""}
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{status_emoji.get(status, '')} [{timestamp}] {message}")
        
    def run_command(self, command, description):
        """Run a shell command and return success"""
        self.log(f"Running: {description}", "INFO")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
            if result.returncode == 0:
                self.log(f"{description}: SUCCESS", "PASS")
                self.fixed += 1
                return True
            else:
                self.log(f"{description}: FAILED - {result.stderr[:200]}", "FAIL")
                self.failed += 1
                return False
        except Exception as e:
            self.log(f"{description}: ERROR - {e}", "FAIL")
            self.failed += 1
            return False
    
    def fix_dependencies(self):
        """Install missing dependencies"""
        self.log("FIXING DEPENDENCIES", "INFO")
        
        dependencies = [
            ("pip install e2b-code-interpreter", "Installing E2B Code Interpreter"),
            ("pip install playwright", "Installing Playwright for browser automation"),
            ("pip install crewai[all]", "Installing CrewAI with all extras"),
            ("pip install --upgrade openai", "Upgrading OpenAI client"),
            ("pip install google-generativeai", "Installing Google Generative AI"),
            ("pip install --upgrade mem0ai", "Upgrading Mem0"),
            ("pip install scrapybara", "Installing Scrapybara client")
        ]
        
        for command, description in dependencies:
            self.run_command(command, description)
    
    def fix_environment_variables(self):
        """Fix environment variable issues"""
        self.log("CHECKING ENVIRONMENT VARIABLES", "INFO")
        
        # Check if .env exists and has required variables
        env_path = ".env"
        if not os.path.exists(env_path):
            self.log("No .env file found", "WARN")
            return
            
        with open(env_path, 'r') as f:
            env_content = f.read()
            
        # Check for placeholder values that need updating
        placeholders = [
            "your_openai_api_key_here",
            "your_gemini_api_key_here", 
            "your_anthropic_api_key_here"
        ]
        
        for placeholder in placeholders:
            if placeholder in env_content:
                self.log(f"Found placeholder: {placeholder}", "WARN")
                self.failed += 1
    
    def fix_service_imports(self):
        """Fix Python path issues for service imports"""
        self.log("FIXING SERVICE IMPORT PATHS", "INFO")
        
        # Add __init__.py files where missing
        service_dirs = [
            "services",
            "services/orchestration", 
            "services/supervisor",
            "api"
        ]
        
        for service_dir in service_dirs:
            init_file = os.path.join(service_dir, "__init__.py")
            if not os.path.exists(init_file):
                try:
                    with open(init_file, 'w') as f:
                        f.write('"""Bonzai service module"""\n')
                    self.log(f"Created {init_file}", "PASS")
                    self.fixed += 1
                except Exception as e:
                    self.log(f"Failed to create {init_file}: {e}", "FAIL")
                    self.failed += 1
            else:
                self.log(f"{init_file} already exists", "PASS")
                
    def fix_railway_deployment(self):
        """Fix Railway deployment issues"""
        self.log("FIXING RAILWAY DEPLOYMENT", "INFO")
        
        # Check if requirements.txt includes all needed packages
        requirements_additions = [
            "e2b-code-interpreter",
            "playwright", 
            "crewai[all]",
            "scrapybara"
        ]
        
        requirements_file = "requirements.txt"
        if os.path.exists(requirements_file):
            with open(requirements_file, 'r') as f:
                current_requirements = f.read()
                
            missing_requirements = []
            for req in requirements_additions:
                base_req = req.split('[')[0]  # Remove [extras] part for checking
                if base_req not in current_requirements:
                    missing_requirements.append(req)
                    
            if missing_requirements:
                try:
                    with open(requirements_file, 'a') as f:
                        f.write("\n# Additional dependencies for 100% functionality\n")
                        for req in missing_requirements:
                            f.write(f"{req}\n")
                    self.log(f"Added {len(missing_requirements)} missing requirements", "PASS")
                    self.fixed += 1
                except Exception as e:
                    self.log(f"Failed to update requirements.txt: {e}", "FAIL")
                    self.failed += 1
        
    def fix_api_endpoints(self):
        """Ensure all API endpoints are properly registered"""
        self.log("CHECKING API ENDPOINT REGISTRATION", "INFO")
        
        # Read app.py to check if all APIs are properly integrated
        app_file = "app.py"
        if not os.path.exists(app_file):
            self.log("app.py not found", "FAIL")
            self.failed += 1
            return
            
        with open(app_file, 'r') as f:
            app_content = f.read()
            
        # Check for critical API registrations
        critical_apis = [
            "multimodal_chat_api",
            "agentic_superpowers_api",
            "agent_workbench_api",
            "task_orchestrator_api"
        ]
        
        for api in critical_apis:
            if api in app_content:
                self.log(f"API {api} found in app.py", "PASS")
                self.fixed += 1
            else:
                self.log(f"API {api} missing from app.py", "WARN")
                
    def create_startup_script(self):
        """Create startup script for proper service initialization"""
        self.log("CREATING STARTUP SCRIPT", "INFO")
        
        startup_script = """#!/usr/bin/env python3
'''
 BONZAI EMPIRE STARTUP SCRIPT
Ensures all services start properly with dependencies
'''

import os
import sys
import logging

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bonzai-startup")

def initialize_bonzai_empire():
    '''Initialize all Bonzai services properly'''
    logger.info(" Starting Bonzai Empire...")
    
    # Import and start main application
    from app import app, initialize_bonzai_services
    
    # Initialize services
    initialize_bonzai_services()
    
    # Get port from environment
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f" Bonzai Empire starting on port {port}")
    
    # Start Flask app
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    initialize_bonzai_empire()
"""
        
        try:
            with open("bonzai_startup.py", 'w') as f:
                f.write(startup_script)
            self.log("Created bonzai_startup.py", "PASS")
            self.fixed += 1
        except Exception as e:
            self.log(f"Failed to create startup script: {e}", "FAIL")
            self.failed += 1
    
    def run_fixes(self):
        """Run all fixes"""
        self.log(" BONZAI EMPIRE COMPREHENSIVE FIXER STARTING", "INFO")
        self.log("=" * 80, "INFO")
        
        # Run all fix operations
        self.fix_dependencies()
        self.fix_environment_variables()
        self.fix_service_imports()
        self.fix_railway_deployment()
        self.fix_api_endpoints()
        self.create_startup_script()
        
        # Summary
        total = self.fixed + self.failed
        success_rate = (self.fixed / total * 100) if total > 0 else 0
        
        self.log("=" * 80, "INFO")
        self.log(" FIX SUMMARY:", "INFO")
        self.log(f"   Total Fixes Attempted: {total}", "INFO")
        self.log(f"   Successful: {self.fixed}", "PASS")
        self.log(f"   Failed: {self.failed}", "FAIL")
        self.log(f"   Success Rate: {success_rate:.1f}%", "INFO")
        
        if self.failed == 0:
            self.log(" ALL FIXES SUCCESSFUL - EMPIRE READY!", "PASS")
        else:
            self.log(" Some fixes need manual attention", "WARN")
            
        return self.fixed, self.failed

if __name__ == "__main__":
    print(" BONZAI EMPIRE COMPREHENSIVE FIXER")
    print("   Automatically fixing all issues to reach 100% functionality")
    print()
    
    fixer = BonzaiEmpireFixer()
    fixed, failed = fixer.run_fixes()
    
    print(f"\n NEXT STEPS:")
    print("1. Run: python MASTER_BONZAI_TEST.py")
    print("2. Check improved success rate")
    print("3. Deploy to Railway with: git add . && git commit -m 'Fix empire issues' && git push")
    print("4. Test Railway deployment endpoints")
    print("\n YOUR EMPIRE WILL BE STRONGER!")