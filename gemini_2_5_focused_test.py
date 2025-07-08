#!/usr/bin/env python3
"""
🔥 FOCUSED GEMINI 2.5 & EXPRESS MODE TEST
Test both standard API and Vertex AI Express endpoints for 2.5 models
"""

import os
import sys
import json
import asyncio
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv('../.env')

print("🚀 FOCUSED GEMINI 2.5 & EXPRESS MODE TESTING")
print("=" * 80)
print(f"Test Started: {datetime.now()}")
print("=" * 80)

# Your API keys
GOOGLE_KEYS = {
    "podplay-build-alpha": "AIzaSyCrLGbHF6LBTmJggdJW-6TBmLLEKC4nr5g",
    "Gemini-API": "AIzaSyB0YfTUMuMB13DZM22nvbQcest57Bal8ik", 
    "podplay-build-beta": "AIzaSyBU9JndWn2Uf1WLgbnMDmw5NHGQNRBO-_U"
}

results = {
    "timestamp": str(datetime.now()),
    "standard_api_results": {},
    "vertex_ai_results": {},
    "express_mode_results": {},
    "gemini_2_5_models_found": [],
    "comparison": {}
}

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔥 {title}")
    print(f"{'='*60}")

async def test_standard_google_ai_comprehensive(key_name, api_key):
    """Test standard Google AI API with focus on 2.5 models"""
    print_header(f"STANDARD GOOGLE AI API: {key_name}")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        print(f"🔑 Using API Key: {api_key[:15]}...")
        
        # Get ALL available models
        all_models = []
        gemini_2_5_models = []
        working_models = []
        
        try:
            models_list = list(genai.list_models())
            print(f"📋 Found {len(models_list)} total models")
            
            for model in models_list:
                model_name = model.name
                all_models.append(model_name)
                
                # Focus on 2.5 models
                if "2.5" in model_name:
                    gemini_2_5_models.append(model_name)
                    print(f"   🎯 FOUND 2.5 MODEL: {model_name}")
                    
                    # Test this 2.5 model specifically
                    if 'generateContent' in model.supported_generation_methods:
                        try:
                            test_model = genai.GenerativeModel(model_name)
                            
                            # Different generation methods for 2.5
                            configs_to_try = [
                                {'max_output_tokens': 10},
                                {'max_output_tokens': 10, 'temperature': 0.1},
                                {}  # Default config
                            ]
                            
                            for i, config in enumerate(configs_to_try):
                                try:
                                    print(f"      🔍 Testing config {i+1}: {config}")
                                    response = test_model.generate_content(
                                        "Hello, please respond briefly", 
                                        generation_config=config
                                    )
                                    
                                    # Try different ways to get response
                                    response_text = None
                                    if hasattr(response, 'text') and response.text:
                                        response_text = response.text
                                    elif hasattr(response, 'parts') and response.parts:
                                        response_text = str(response.parts[0])
                                    elif hasattr(response, 'candidates') and response.candidates:
                                        response_text = str(response.candidates[0].content.parts[0].text)
                                    
                                    if response_text:
                                        working_models.append({
                                            "name": model_name,
                                            "config": config,
                                            "status": "✅ WORKING",
                                            "sample": response_text[:30]
                                        })
                                        print(f"         ✅ SUCCESS: {response_text[:30]}")
                                        break
                                    else:
                                        print(f"         ❌ No response text")
                                        
                                except Exception as e:
                                    error_msg = str(e)
                                    print(f"         ❌ Config {i+1} failed: {error_msg[:50]}")
                                    if "quota" in error_msg.lower():
                                        print(f"         💰 Quota issue")
                                        break
                                    elif "thinking" in error_msg.lower():
                                        print(f"         🤔 Thinking mode issue - trying standard mode")
                                        continue
                                    elif "text" in error_msg.lower() and "quick" in error_msg.lower():
                                        print(f"         🔄 Text access issue - trying alternative")
                                        continue
                                        
                        except Exception as e:
                            print(f"      ❌ Model setup failed: {str(e)[:50]}")
                            
        except Exception as e:
            print(f"❌ Failed to list models: {e}")
            
        print(f"\n📊 STANDARD API SUMMARY ({key_name}):")
        print(f"   📋 Total models: {len(all_models)}")
        print(f"   🎯 Gemini 2.5 models found: {len(gemini_2_5_models)}")
        print(f"   ✅ Working 2.5 models: {len(working_models)}")
        
        if gemini_2_5_models:
            print(f"\n🎯 ALL 2.5 MODELS FOUND:")
            for model in gemini_2_5_models:
                print(f"      - {model}")
        
        return {
            "total_models": len(all_models),
            "gemini_2_5_models": gemini_2_5_models,
            "working_2_5_models": working_models,
            "all_models": all_models
        }
        
    except Exception as e:
        print(f"❌ Standard API test failed: {e}")
        return {"error": str(e)}

async def test_vertex_ai_express_mode():
    """Test Vertex AI Express mode endpoints"""
    print_header("VERTEX AI EXPRESS MODE TESTING")
    
    # Express mode configuration from env
    express_config = {
        "VERTEX_AI_ENABLED": os.getenv('VERTEX_AI_ENABLED'),
        "VERTEX_AI_REGION": os.getenv('VERTEX_AI_REGION'),
        "EXPRESS_ENDPOINT_ID": os.getenv('EXPRESS_ENDPOINT_ID'),
        "EXPRESS_MODE_ENABLED": os.getenv('EXPRESS_MODE_ENABLED'),
        "EXPRESS_TARGET_RESPONSE_TIME_MS": os.getenv('EXPRESS_TARGET_RESPONSE_TIME_MS'),
        "GOOGLE_CLOUD_PROJECT": os.getenv('GOOGLE_CLOUD_PROJECT')
    }
    
    print("📋 Express Configuration:")
    for key, value in express_config.items():
        status = "✅" if value else "❌"
        print(f"   {status} {key}: {value}")
    
    # Try Vertex AI SDK if available
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        project_id = express_config["GOOGLE_CLOUD_PROJECT"]
        region = express_config["VERTEX_AI_REGION"]
        
        if project_id and region:
            print(f"\n🔍 Testing Vertex AI with project: {project_id}")
            
            try:
                vertexai.init(project=project_id, location=region)
                
                # Test specific 2.5 models on Vertex AI
                vertex_2_5_models = [
                    "gemini-2.5-pro-001",
                    "gemini-2.5-pro-002", 
                    "gemini-2.5-flash-001",
                    "gemini-2.5-flash-002",
                    "gemini-2.5-pro",
                    "gemini-2.5-flash",
                    "gemini-2.5-pro-latest",
                    "gemini-2.5-flash-latest",
                    "gemini-2.5-pro-experimental",
                    "gemini-2.5-flash-experimental"
                ]
                
                working_vertex_models = []
                
                for model_name in vertex_2_5_models:
                    try:
                        print(f"   🔍 Testing Vertex model: {model_name}")
                        model = GenerativeModel(model_name)
                        
                        start_time = time.time()
                        response = model.generate_content(
                            "Hello, brief response please",
                            generation_config={"max_output_tokens": 10}
                        )
                        response_time = (time.time() - start_time) * 1000
                        
                        if response.text:
                            working_vertex_models.append({
                                "name": model_name,
                                "status": "✅ WORKING",
                                "response_time_ms": round(response_time, 2),
                                "sample": response.text[:30]
                            })
                            print(f"      ✅ VERTEX SUCCESS: {model_name} ({response_time:.0f}ms)")
                        else:
                            print(f"      ❌ No response text")
                            
                    except Exception as e:
                        error_msg = str(e)
                        print(f"      ❌ {model_name}: {error_msg[:50]}")
                        if "404" in error_msg:
                            print(f"         📅 Model not available on Vertex")
                        elif "403" in error_msg:
                            print(f"         🔐 Permission issue")
                        elif "quota" in error_msg.lower():
                            print(f"         💰 Quota exceeded")
                
                print(f"\n📊 VERTEX AI RESULTS:")
                print(f"   ✅ Working Vertex 2.5 models: {len(working_vertex_models)}")
                
                return {
                    "vertex_models_tested": vertex_2_5_models,
                    "working_vertex_models": working_vertex_models,
                    "express_config": express_config
                }
                
            except Exception as e:
                print(f"❌ Vertex AI initialization failed: {e}")
                return {"error": f"Vertex init failed: {e}"}
        else:
            print("⚠️  Missing project ID or region for Vertex AI")
            return {"error": "Missing Vertex AI configuration"}
            
    except ImportError:
        print("❌ Vertex AI SDK not available")
        return {"error": "Vertex AI SDK not installed"}

async def compare_endpoints():
    """Compare what's available on different endpoints"""
    print_header("ENDPOINT COMPARISON & ANALYSIS")
    
    # Test all keys on standard API
    standard_results = {}
    for key_name, api_key in GOOGLE_KEYS.items():
        standard_results[key_name] = await test_standard_google_ai_comprehensive(key_name, api_key)
        await asyncio.sleep(1)  # Be nice to API
    
    # Test Vertex AI
    vertex_results = await test_vertex_ai_express_mode()
    
    # Analyze differences
    all_2_5_models = set()
    for key_name, data in standard_results.items():
        if isinstance(data, dict) and "gemini_2_5_models" in data:
            all_2_5_models.update(data["gemini_2_5_models"])
    
    print(f"\n🎯 COMPREHENSIVE 2.5 MODEL ANALYSIS:")
    print(f"   📋 Unique 2.5 models found across all keys: {len(all_2_5_models)}")
    
    if all_2_5_models:
        print(f"\n📝 ALL DISCOVERED 2.5 MODELS:")
        for model in sorted(all_2_5_models):
            print(f"      - {model}")
    
    # Check what's working vs not working
    working_2_5 = []
    not_working_2_5 = []
    
    for key_name, data in standard_results.items():
        if isinstance(data, dict) and "working_2_5_models" in data:
            for model_data in data["working_2_5_models"]:
                working_2_5.append(f"{model_data['name']} (via {key_name})")
            
            # Find non-working ones
            all_2_5_for_key = data.get("gemini_2_5_models", [])
            working_2_5_for_key = [m["name"] for m in data["working_2_5_models"]]
            not_working_for_key = [m for m in all_2_5_for_key if m not in working_2_5_for_key]
            for model in not_working_for_key:
                not_working_2_5.append(f"{model} (via {key_name})")
    
    print(f"\n✅ WORKING 2.5 MODELS ({len(working_2_5)}):")
    for model in working_2_5:
        print(f"      ✅ {model}")
    
    print(f"\n❌ NOT WORKING 2.5 MODELS ({len(not_working_2_5)}):")
    for model in not_working_2_5:
        print(f"      ❌ {model}")
    
    results["standard_api_results"] = standard_results
    results["vertex_ai_results"] = vertex_results
    results["gemini_2_5_models_found"] = list(all_2_5_models)
    results["comparison"] = {
        "working_2_5_count": len(working_2_5),
        "not_working_2_5_count": len(not_working_2_5),
        "total_2_5_discovered": len(all_2_5_models)
    }
    
    return True

async def main():
    """Run focused 2.5 testing"""
    
    success = await compare_endpoints()
    
    # Save results
    with open('gemini_2_5_focused_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: gemini_2_5_focused_results.json")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)