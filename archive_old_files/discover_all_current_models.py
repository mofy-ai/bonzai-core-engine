#!/usr/bin/env python3
"""
 DISCOVER ALL CURRENT MODELS - 2025 EDITION
Research and test ALL current API model names across providers
"""

import os
import sys
import json
import asyncio
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv('../.env')

print(" DISCOVERING ALL CURRENT MODELS - 2025 EDITION")
print("=" * 80)
print(f"Discovery Started: {datetime.now()}")
print("=" * 80)

# Your API keys
GOOGLE_KEYS = {
    "podplay-build-alpha": "AIzaSyCrLGbHF6LBTmJggdJW-6TBmLLEKC4nr5g",
    "Gemini-API": "AIzaSyB0YfTUMuMB13DZM22nvbQcest57Bal8ik", 
    "podplay-build-beta": "AIzaSyBU9JndWn2Uf1WLgbnMDmw5NHGQNRBO-_U"
}

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

results = {
    "timestamp": str(datetime.now()),
    "discovery_methods": {},
    "all_models_found": {},
    "working_models": {},
    "model_capabilities": {}
}

def print_header(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

async def discover_google_models_comprehensive(api_key, key_name):
    """Comprehensive Google model discovery"""
    print_header(f"GOOGLE MODEL DISCOVERY: {key_name}")
    
    discovered_models = []
    working_models = []
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        print(f" Using API Key: {api_key[:15]}...")
        
        # Method 1: Official list_models()
        print("\n📋 Method 1: Official API Discovery")
        try:
            official_models = list(genai.list_models())
            print(f"   Found {len(official_models)} official models")
            
            for model in official_models:
                model_name = model.name
                discovered_models.append(model_name)
                
                # Test if it supports generation
                if 'generateContent' in model.supported_generation_methods:
                    print(f"    {model_name} - Generation supported")
                    
                    # Quick test
                    try:
                        test_model = genai.GenerativeModel(model_name)
                        response = test_model.generate_content(
                            "Hi", 
                            generation_config={'max_output_tokens': 3}
                        )
                        if response.text:
                            working_models.append({
                                "name": model_name,
                                "status": " Working",
                                "sample": response.text[:20]
                            })
                            print(f"       WORKING - Sample: {response.text[:20]}")
                        else:
                            print(f"       No response")
                    except Exception as e:
                        error = str(e)[:40]
                        print(f"       Error: {error}")
                        if "quota" in error.lower():
                            print(f"      💰 Quota issue")
                        elif "deprecated" in error.lower():
                            print(f"      📅 Deprecated")
                else:
                    print(f"   🚫 {model_name} - No generation support")
                    
        except Exception as e:
            print(f" Official discovery failed: {e}")
        
        # Method 2: Try known 2025 model patterns
        print("\n Method 2: Testing 2025 Model Patterns")
        
        potential_2025_models = [
            # Gemini 2.5 variants (current naming)
            "models/gemini-2.5-pro",
            "models/gemini-2.5-pro-latest", 
            "models/gemini-2.5-pro-002",
            "models/gemini-2.5-flash-001",
            "models/gemini-2.5-flash-002",
            "models/gemini-2.5-flash-latest",
            
            # Potential new naming patterns
            "gemini-2.5-pro",
            "gemini-2.5-flash", 
            "gemini-pro-2.5",
            "gemini-flash-2.5",
            
            # Gemini 3.0 speculation
            "models/gemini-3.0-pro",
            "models/gemini-3.0-flash",
            "gemini-3.0-pro",
            "gemini-3.0-flash",
            
            # Ultra variants
            "models/gemini-ultra",
            "models/gemini-2.5-ultra",
            "gemini-ultra",
            
            # Advanced variants
            "models/gemini-advanced",
            "models/gemini-pro-advanced",
            "gemini-advanced"
        ]
        
        for model_name in potential_2025_models:
            try:
                test_model = genai.GenerativeModel(model_name)
                response = test_model.generate_content(
                    "Test", 
                    generation_config={'max_output_tokens': 3}
                )
                if response.text:
                    working_models.append({
                        "name": model_name,
                        "status": " DISCOVERED NEW!",
                        "sample": response.text[:20]
                    })
                    print(f"   🆕 FOUND NEW: {model_name} - {response.text[:20]}")
                    if model_name not in discovered_models:
                        discovered_models.append(model_name)
            except Exception as e:
                # Silent fail for speculation
                pass
        
        print(f"\n GOOGLE DISCOVERY SUMMARY ({key_name}):")
        print(f"   📋 Total models discovered: {len(discovered_models)}")
        print(f"    Working models: {len(working_models)}")
        
        return {
            "discovered_count": len(discovered_models),
            "working_count": len(working_models),
            "all_discovered": discovered_models,
            "working_models": working_models
        }
        
    except Exception as e:
        print(f" Google discovery failed: {e}")
        return {"error": str(e)}

async def discover_anthropic_models_comprehensive():
    """Comprehensive Anthropic model discovery"""
    print_header("ANTHROPIC MODEL DISCOVERY")
    
    discovered_models = []
    working_models = []
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        
        print(f" Using API Key: {ANTHROPIC_KEY[:15]}...")
        
        # Method 1: Test all known Claude variants
        print("\n📋 Method 1: Testing All Claude Variants")
        
        potential_claude_models = [
            # Claude 4 speculation (based on naming patterns)
            "claude-4",
            "claude-4-opus",
            "claude-4-sonnet", 
            "claude-4-haiku",
            "claude-4-20250101",
            "claude-4-20241201",
            
            # Claude 3.7 (you mentioned this)
            "claude-3.7",
            "claude-3.7-sonnet",
            "claude-3.7-opus",
            "claude-3.7-haiku",
            
            # Current Claude 3.5 variants
            "claude-3-5-sonnet-20241022",
            "claude-3-5-sonnet-latest",
            "claude-3-5-haiku-20241022", 
            "claude-3-5-haiku-latest",
            "claude-3-5-opus-20241022",
            
            # Other current models
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229", 
            "claude-3-haiku-20240307",
            
            # Potential new variants
            "claude-instant-1.2",
            "claude-instant-latest",
            "claude-2.1",
            "claude-2.0"
        ]
        
        for model_name in potential_claude_models:
            try:
                print(f"    Testing: {model_name}")
                start_time = time.time()
                message = client.messages.create(
                    model=model_name,
                    max_tokens=5,
                    messages=[{"role": "user", "content": "Hi"}]
                )
                response_time = (time.time() - start_time) * 1000
                
                if message.content and len(message.content) > 0:
                    sample_text = message.content[0].text[:20]
                    working_models.append({
                        "name": model_name,
                        "status": " Working",
                        "response_time_ms": round(response_time, 2),
                        "sample": sample_text
                    })
                    discovered_models.append(model_name)
                    print(f"       WORKING: {model_name} ({response_time:.0f}ms) - {sample_text}")
                    
            except Exception as e:
                error = str(e)
                if "404" in error:
                    print(f"      📅 {model_name} - Not found/deprecated")
                elif "model" in error.lower():
                    print(f"      🚫 {model_name} - Invalid model")
                else:
                    print(f"       {model_name} - {error[:30]}")
        
        print(f"\n ANTHROPIC DISCOVERY SUMMARY:")
        print(f"   📋 Models tested: {len(potential_claude_models)}")
        print(f"    Working models: {len(working_models)}")
        
        return {
            "discovered_count": len(discovered_models),
            "working_count": len(working_models),
            "all_discovered": discovered_models,
            "working_models": working_models
        }
        
    except Exception as e:
        print(f" Anthropic discovery failed: {e}")
        return {"error": str(e)}

async def discover_openai_models_comprehensive():
    """Comprehensive OpenAI model discovery"""
    print_header("OPENAI MODEL DISCOVERY")
    
    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_KEY)
        
        print(f" Using API Key: {OPENAI_KEY[:15]}...")
        
        # Get all available models
        try:
            models_response = client.models.list()
            all_models = [model.id for model in models_response.data]
            
            print(f"📋 Found {len(all_models)} total models")
            
            # Filter for the latest/best models
            current_models = [m for m in all_models if any(x in m for x in [
                'gpt-4', 'gpt-3.5', 'gpt-4o', 'o1', 'o3'  # Include o1 and o3 series
            ])]
            
            print(f" Testing {len(current_models)} current GPT models...")
            
            working_models = []
            test_models = current_models[:10]  # Test top 10 to avoid quota
            
            for model_name in test_models:
                try:
                    print(f"    Testing: {model_name}")
                    start_time = time.time()
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "user", "content": "Hi"}],
                        max_tokens=3
                    )
                    response_time = (time.time() - start_time) * 1000
                    
                    if response.choices and response.choices[0].message.content:
                        sample_text = response.choices[0].message.content[:20]
                        working_models.append({
                            "name": model_name,
                            "status": " Working",
                            "response_time_ms": round(response_time, 2),
                            "sample": sample_text
                        })
                        print(f"       WORKING: {model_name} ({response_time:.0f}ms)")
                        
                except Exception as e:
                    error = str(e)[:40]
                    if "quota" in error.lower():
                        print(f"      💰 {model_name} - Quota exceeded")
                    else:
                        print(f"       {model_name} - {error}")
            
            print(f"\n OPENAI DISCOVERY SUMMARY:")
            print(f"   📋 Total models available: {len(all_models)}")
            print(f"    Current models: {len(current_models)}")
            print(f"    Working models tested: {len(working_models)}")
            
            return {
                "total_available": len(all_models),
                "current_models": current_models,
                "working_models": working_models,
                "all_models": all_models
            }
            
        except Exception as e:
            print(f" Failed to list OpenAI models: {e}")
            return {"error": str(e)}
            
    except Exception as e:
        print(f" OpenAI discovery failed: {e}")
        return {"error": str(e)}

def generate_comprehensive_report(results):
    """Generate the ultimate model discovery report"""
    print_header(" ULTIMATE MODEL DISCOVERY REPORT")
    
    total_working = 0
    
    # Google summary
    print("\n GOOGLE MODEL DISCOVERIES:")
    for key_name, data in results["all_models_found"].get("google", {}).items():
        if isinstance(data, dict) and "working_count" in data:
            working = data["working_count"]
            total_working += working
            print(f"    {key_name}: {working} working models")
            
            # Show newest discoveries
            if "working_models" in data:
                new_models = [m for m in data["working_models"] if "DISCOVERED NEW" in m.get("status", "")]
                if new_models:
                    print(f"      🆕 NEW DISCOVERIES:")
                    for model in new_models:
                        print(f"         - {model['name']}")
    
    # Anthropic summary
    anthropic_data = results["all_models_found"].get("anthropic", {})
    if isinstance(anthropic_data, dict) and "working_count" in anthropic_data:
        working = anthropic_data["working_count"]
        total_working += working
        print(f"\n ANTHROPIC DISCOVERIES: {working} working Claude models")
        
        if "working_models" in anthropic_data:
            print(f"   📋 Working Claude Models:")
            for model in anthropic_data["working_models"]:
                print(f"       {model['name']} ({model.get('response_time_ms', 'N/A')}ms)")
    
    # OpenAI summary
    openai_data = results["all_models_found"].get("openai", {})
    if isinstance(openai_data, dict) and "working_models" in openai_data:
        working = len(openai_data["working_models"])
        total_working += working
        print(f"\n🧠 OPENAI DISCOVERIES: {working} working GPT models")
        print(f"    Total available: {openai_data.get('total_available', 'Unknown')}")
    
    print(f"\n TOTAL ARSENAL:")
    print(f"    TOTAL WORKING MODELS: {total_working}")
    print(f"    Ready for orchestration across all providers")
    
    if total_working > 50:
        print(f"\n INCREDIBLE DISCOVERY!")
        print(f"    You have access to a MASSIVE AI arsenal!")
        print(f"   👨‍👩‍👧‍👦 MOFY Family AI is UNSTOPPABLE!")

async def main():
    """Run comprehensive model discovery"""
    
    # Discover Google models for all keys
    results["all_models_found"]["google"] = {}
    for key_name, api_key in GOOGLE_KEYS.items():
        results["all_models_found"]["google"][key_name] = await discover_google_models_comprehensive(api_key, key_name)
        await asyncio.sleep(2)  # Be nice to API
    
    # Discover Anthropic models
    results["all_models_found"]["anthropic"] = await discover_anthropic_models_comprehensive()
    
    # Discover OpenAI models
    results["all_models_found"]["openai"] = await discover_openai_models_comprehensive()
    
    # Generate comprehensive report
    generate_comprehensive_report(results)
    
    # Save detailed results
    with open('all_current_models_discovered.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Full discovery results saved to: all_current_models_discovered.json")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)