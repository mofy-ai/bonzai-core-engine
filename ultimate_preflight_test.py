#!/usr/bin/env python3
"""
🚀 ULTIMATE PRE-FLIGHT TEST SUITE
Testing all AI endpoints, models, and orchestration capabilities
For Nathan's BONZAI Family Unity System
"""

import os
import sys
import json
import asyncio
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv('../.env')

class UltimatePreflightTester:
    def __init__(self):
        self.results = {
            "test_start": datetime.now().isoformat(),
            "google_standard_api": {},
            "google_vertex_express": {},
            "claude_models": {},
            "mcp_integration": {},
            "orchestration_test": {},
            "family_coordination": {},
            "model_inventory": []
        }
        
        # API Keys
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.google_key = os.getenv('GOOGLE_API_KEY') 
        self.mem0_key = os.getenv('MEM0_API_KEY')
        
        print("🚀 ULTIMATE PRE-FLIGHT TEST SUITE")
        print("=" * 70)
        print(f"Test Started: {datetime.now()}")
        print("=" * 70)

    async def test_google_standard_endpoints(self):
        """Test standard Gemini API endpoints"""
        print("\n🔥 TESTING GOOGLE STANDARD API ENDPOINTS")
        print("-" * 50)
        
        # Standard endpoint
        base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        # Test models endpoint
        try:
            models_url = f"{base_url}/models?key={self.gemini_key}"
            response = requests.get(models_url, timeout=10)
            
            if response.status_code == 200:
                models_data = response.json()
                models = [model['name'] for model in models_data.get('models', [])]
                
                print(f"✅ Standard API Connected")
                print(f"📊 Available Models: {len(models)}")
                
                # Extract Gemini models
                gemini_models = [m for m in models if 'gemini' in m.lower()]
                for model in gemini_models:
                    print(f"   🤖 {model}")
                    self.results["model_inventory"].append({
                        "name": model,
                        "endpoint": "standard",
                        "status": "available"
                    })
                
                self.results["google_standard_api"] = {
                    "status": "success",
                    "models_count": len(models),
                    "gemini_models": gemini_models
                }
            else:
                print(f"❌ Standard API Error: {response.status_code}")
                self.results["google_standard_api"] = {
                    "status": "failed",
                    "error": f"HTTP {response.