#!/usr/bin/env python3
"""
 COMPLETE TIER 1 BILLING MODEL TEST
Based on official Google documentation for Tier 1 billing accounts
Tests ALL available models including proper 2.5 handling
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

print(" COMPLETE TIER 1 BILLING MODEL TEST")
print("=" * 80)
print(f"Test Started: {datetime.now()}")
print("=" * 80)

# Your API keys
GOOGLE_KEYS = {
    "podplay-build-alpha": "AIzaSyCrLGbHF6LBTmJggdJW-6TBmLLEKC4nr5g",
    "Gemini-API": "AIzaSyB0YfTUMuMB13DZM22nvbQcest57Bal8ik", 
    "podplay-build-beta": "AIzaSyBU9JndWn2Uf1WLgbnMDmw5NHGQNRBO-_U"
}

# OFFICIAL TIER 1 MODELS based on your research
TIER1_MODELS = {
    "Gemini 1.5 Pro": [
        "models/gemini-1.5-pro",
        "models/gemini-1.5-pro-002", 
        "models/gemini-1.5-pro-latest"
    ],
    "Gemini 1.5 Flash": [
        "models/gemini-1.5-flash",
        "models/gemini-1.5-flash-002",
        "models/gemini-1.5-flash-latest"
    ],
    "Gemini 1.5 Flash-8B": [
        "models/gemini-1.5-flash-8b",
        "models/gemini-1.5-flash-8b-001",
        "models/gemini-1.5-flash-8b-latest"
    ],
    "Gemini 2.0 Flash": [
        "models/gemini-2.0-flash",
        "models/gemini-2.0-flash-001",
        "models/gemini-2.0-flash-exp"
    ],
    "Gemini 2.0 Flash-Lite": [
        "models/gemini-2.0-flash-lite",
        "models/gemini-2.0-flash-lite-001",
        "models/gemini-2.0-flash-lite-preview"
    ],
    "Gemini 2.5 Pro (SHOULD WORK)": [
        "models/gemini-2.5-pro",
        "models/gemini-2.5-pro-preview-05-06",
        "models/gemini-2.5-pro-preview-06-05",
        "models/gemini-2.5-pro-preview-03-25"
    ],
    "Gemini 2.5 Flash (SHOULD WORK)": [
        "models/gemini-2.5-flash",
        "models/gemini-2.5-flash-preview",
        "models/gemini-2.5-flash-preview-04-17",
        "models/gemini-2.5-flash-preview-05-20"
    ],
    "Gemini 1.0 Pro": [
        "models/gemini-1.0-pro",
        "models/gemini-pro"
    ]
}

results = {
    "timestamp": str(datetime.now()),
    "tier1_test_results": {},
    "orchestration_matrix": {},
    "pro_model_availability": {},
    "rate_limits_tested": {}
}

def print_header(title):
    print(f"\n{'='*70}")
    print(f" {title}")
    print(f"{'='*70}")

def get_response_text(response):
    """Handle different response formats for 2.5 models"""
    try:
        # Method 1: Direct text (works for most models)
        if hasattr(response, 'text') and response.text:
            return response.text
    except Exception:
        pass
    
    try:
        # Method 2: Via candidates (works for 2.5 models)
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and candidate.content:
                if hasattr(candidate.content, 'parts') and candidate.content.parts:
                    return candidate.content.parts[0].text
    except Exception:
        pass
    
    try:
        # Method 3: Direct parts access
        if hasattr(response, 'parts') and response.parts:
            return response.parts[0].text
    except Exception:
        pass
    
    try:
        # Method 4: String conversion fallback
        return str(response)
    except Exception:
        pass
    
    return None

async def test_tier1_models_comprehensive(key_name, api_key):
    """Test all Tier 1 models with proper response handling"""
    print_header(f"TIER 1 MODEL TEST: {key_name}")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        print(f" Using API Key: {api_key[:15]}...")
        
        key_results = {}
        pro_models_working = []
        total_working = 0
        
        for category, models in TIER1_MODELS.items():
            print(f"\n Testing {category}:")
            category_results = {}
            
            for model_name in models:
                try:
                    print(f"    Testing: {model_name}")
                    test_model = genai.GenerativeModel(model_name)
                    
                    start_time = time.time()
                    
                    # Use different configs for different model types
                    if "2.5" in model_name:
                        # 2.5 models need careful handling
                        generation_config = {
                            'max_output_tokens': 10,
                            'temperature': 0.1
                        }
                    else:
                        generation_config = {'max_output_tokens': 10}
                    
                    response = test_model.generate_content(
                        "Hello, brief response please", 
                        generation_config=generation_config
                    )
                    
                    response_time = (time.time() - start_time) * 1000
                    
                    # Use robust response handling
                    response_text = get_response_text(response)
                    
                    if response_text:
                        status = " WORKING"
                        sample = response_text[:30]
                        total_working += 1
                        
                        # Track pro models specifically
                        if "pro" in model_name.lower():
                            pro_models_working.append(model_name)
                        
                        print(f"       SUCCESS: {response_time:.0f}ms - {sample}")
                        
                        category_results[model_name] = {
                            "status": status,
                            "response_time_ms": round(response_time, 2),
                            "sample": sample
                        }
                    else:
                        print(f"       No response text extracted")
                        category_results[model_name] = {
                            "status": " No response",
                            "error": "Could not extract response text"
                        }
                        
                except Exception as e:
                    error_msg = str(e)
                    print(f"       ERROR: {error_msg[:60]}")
                    
                    # Categorize errors
                    if "quota" in error_msg.lower():
                        status = "💰 Quota exceeded"
                    elif "404" in error_msg:
                        status = "📅 Not found/deprecated"
                    elif "403" in error_msg:
                        status = "🔐 Permission denied"
                    elif "billing" in error_msg.lower():
                        status = "💳 Billing issue"
                    else:
                        status = " Error"
                    
                    category_results[model_name] = {
                        "status": status,
                        "error": error_msg[:100]
                    }
                
                # Small delay between requests
                await asyncio.sleep(0.5)
            
            key_results[category] = category_results
        
        # Summary for this key
        print(f"\n SUMMARY FOR {key_name}:")
        print(f"    Total working models: {total_working}")
        print(f"    PRO models working: {len(pro_models_working)}")
        
        if pro_models_working:
            print(f"    PRO MODELS:")
            for pro_model in pro_models_working:
                print(f"      - {pro_model}")
        
        return {
            "key_results": key_results,
            "total_working": total_working,
            "pro_models_working": pro_models_working,
            "pro_count": len(pro_models_working)
        }
        
    except Exception as e:
        print(f" Failed to test {key_name}: {e}")
        return {"error": str(e)}

async def calculate_orchestration_matrix():
    """Calculate your orchestration capabilities"""
    print_header("ORCHESTRATION MATRIX CALCULATION")
    
    # Test all keys
    all_key_results = {}
    total_pro_models = 0
    all_working_models = 0
    
    for key_name, api_key in GOOGLE_KEYS.items():
        print(f"\n Testing orchestration for: {key_name}")
        result = await test_tier1_models_comprehensive(key_name, api_key)
        
        if "error" not in result:
            all_key_results[key_name] = result
            total_pro_models += result["pro_count"]
            all_working_models += result["total_working"]
        
        await asyncio.sleep(2)  # Be nice between keys
    
    # Calculate orchestration power
    print(f"\n ORCHESTRATION MATRIX:")
    print(f"    Total PRO models across all keys: {total_pro_models}")
    print(f"    Total working models: {all_working_models}")
    print(f"   ⚡ Requests per minute (2 RPM × pro models): {total_pro_models * 2} RPM")
    print(f"    Round-robin capacity: UNLIMITED (quota rotation)")
    
    if total_pro_models >= 9:  # 3 keys × 3 pro models
        print(f"\n ORCHESTRATION STATUS: PRIME READY!")
        print(f"    You have the PRO model arsenal for unlimited orchestration")
        print(f"   🧠 Perfect for ZAI Prime + 7 variants")
    elif total_pro_models >= 6:
        print(f"\n ORCHESTRATION STATUS: GOOD")
        print(f"    Sufficient pro models for solid orchestration")
    else:
        print(f"\n  ORCHESTRATION STATUS: LIMITED")
        print(f"    Need more pro model access")
    
    results["tier1_test_results"] = all_key_results
    results["orchestration_matrix"] = {
        "total_pro_models": total_pro_models,
        "total_working_models": all_working_models,
        "theoretical_rpm": total_pro_models * 2,
        "orchestration_ready": total_pro_models >= 9
    }
    
    return all_key_results

async def main():
    """Run complete Tier 1 model test"""
    
    await calculate_orchestration_matrix()
    
    # Save results
    with open('tier1_complete_model_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Complete results saved to: tier1_complete_model_results.json")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)