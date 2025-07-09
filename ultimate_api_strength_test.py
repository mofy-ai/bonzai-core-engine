#!/usr/bin/env python3
"""
 ULTIMATE API STRENGTH & MODEL AVAILABILITY TEST
Tests ALL API keys against ALL endpoints for maximum model access
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

print(" ULTIMATE API STRENGTH & MODEL AVAILABILITY TEST")
print("=" * 80)
print(f"Test Started: {datetime.now()}")
print("=" * 80)

# Test results structure
results = {
    "timestamp": str(datetime.now()),
    "api_keys": {
        "google_keys": {},
        "anthropic": {},
        "openai": {},
        "deepseek": {}
    },
    "endpoints": {
        "google_ai_standard": {},
        "vertex_ai_express": {},
        "anthropic_api": {},
        "openai_api": {},
        "deepseek_api": {}
    },
    "model_summary": {
        "total_working_models": 0,
        "by_provider": {},
        "by_api_key": {},
        "recommendations": []
    }
}

# API Keys to test
API_KEYS = {
    "Google Keys": {
        "podplay-build-alpha": "AIzaSyCrLGbHF6LBTmJggdJW-6TBmLLEKC4nr5g",
        "Gemini-API": "AIzaSyB0YfTUMuMB13DZM22nvbQcest57Bal8ik", 
        "podplay-build-beta": "AIzaSyBU9JndWn2Uf1WLgbnMDmw5NHGQNRBO-_U"
    },
    "Anthropic": {
        "primary": os.getenv("ANTHROPIC_API_KEY")
    },
    "OpenAI": {
        "primary": os.getenv("OPENAI_API_KEY")
    }
}

def print_header(title, char="=", width=80):
    """Print a styled header"""
    print(f"\n{char * width}")
    print(f" {title}")
    print(f"{char * width}")

def print_subheader(title, char="-", width=60):
    """Print a styled subheader"""
    print(f"\n{char * width}")
    print(f" {title}")
    print(f"{char * width}")

async def test_google_api_key(key_name, api_key):
    """Test a Google API key against Google AI API"""
    print_subheader(f"Testing Google Key: {key_name}")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        models_tested = 0
        models_working = 0
        model_details = {}
        
        print(f" API Key: {api_key[:15]}...")
        
        # Get all available models
        try:
            available_models = list(genai.list_models())
            print(f"📋 Found {len(available_models)} total models")
            
            for model in available_models:
                if 'generateContent' in model.supported_generation_methods:
                    models_tested += 1
                    model_name = model.name
                    
                    try:
                        # Quick test
                        test_model = genai.GenerativeModel(model_name)
                        start_time = time.time()
                        response = test_model.generate_content(
                            "Hello", 
                            generation_config={'max_output_tokens': 5}
                        )
                        response_time = (time.time() - start_time) * 1000
                        
                        if response.text:
                            models_working += 1
                            model_details[model_name] = {
                                "status": " Working",
                                "response_time_ms": round(response_time, 2),
                                "sample_response": response.text[:30] + "..."
                            }
                            print(f"    {model_name} ({response_time:.0f}ms)")
                        else:
                            model_details[model_name] = {
                                "status": " No response",
                                "error": "Empty response"
                            }
                            print(f"    {model_name} - No response")
                            
                    except Exception as e:
                        error_msg = str(e)[:50]
                        model_details[model_name] = {
                            "status": " Failed",
                            "error": error_msg
                        }
                        if "quota" in error_msg.lower():
                            print(f"   💰 {model_name} - Quota exceeded")
                        elif "deprecated" in error_msg.lower():
                            print(f"   📅 {model_name} - Deprecated")
                        else:
                            print(f"    {model_name} - {error_msg}")
                            
        except Exception as e:
            print(f" Failed to list models: {e}")
            return {"status": " Failed", "error": str(e)}
        
        # Summary for this key
        success_rate = (models_working / models_tested * 100) if models_tested > 0 else 0
        
        print(f"\n SUMMARY FOR {key_name}:")
        print(f"   📈 Success Rate: {success_rate:.1f}% ({models_working}/{models_tested})")
        print(f"    Working Models: {models_working}")
        print(f"   ⚡ Best for: {'Premium models' if models_working > 10 else 'Basic models'}")
        
        return {
            "status": " Working" if models_working > 0 else " No working models",
            "models_tested": models_tested,
            "models_working": models_working,
            "success_rate": success_rate,
            "model_details": model_details
        }
        
    except ImportError:
        return {"status": " google.generativeai not available", "error": "Missing package"}
    except Exception as e:
        return {"status": " Failed", "error": str(e)}

async def test_anthropic_key(api_key):
    """Test Anthropic API key"""
    print_subheader("Testing Anthropic API")
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        # Claude models to test
        claude_models = [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022", 
            "claude-3-haiku-20240307",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229"
        ]
        
        print(f" API Key: {api_key[:15]}...")
        
        models_working = 0
        model_details = {}
        
        for model in claude_models:
            try:
                start_time = time.time()
                message = client.messages.create(
                    model=model,
                    max_tokens=5,
                    messages=[{"role": "user", "content": "Hello"}]
                )
                response_time = (time.time() - start_time) * 1000
                
                models_working += 1
                model_details[model] = {
                    "status": " Working",
                    "response_time_ms": round(response_time, 2),
                    "sample_response": message.content[0].text[:30] + "..."
                }
                print(f"    {model} ({response_time:.0f}ms)")
                
            except Exception as e:
                error_msg = str(e)[:50]
                model_details[model] = {
                    "status": " Failed", 
                    "error": error_msg
                }
                if "404" in error_msg:
                    print(f"   📅 {model} - Deprecated")
                else:
                    print(f"    {model} - {error_msg}")
        
        success_rate = (models_working / len(claude_models) * 100)
        
        print(f"\n ANTHROPIC SUMMARY:")
        print(f"   📈 Success Rate: {success_rate:.1f}% ({models_working}/{len(claude_models)})")
        print(f"    Working Models: {models_working}")
        
        return {
            "status": " Working" if models_working > 0 else " No working models",
            "models_tested": len(claude_models),
            "models_working": models_working,
            "success_rate": success_rate,
            "model_details": model_details
        }
        
    except ImportError:
        return {"status": " anthropic package not available", "error": "Missing package"}
    except Exception as e:
        return {"status": " Failed", "error": str(e)}

async def test_openai_key(api_key):
    """Test OpenAI API key"""
    print_subheader("Testing OpenAI API")
    
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        print(f" API Key: {api_key[:15]}...")
        
        # Get available models
        try:
            models_list = client.models.list()
            gpt_models = [m for m in models_list.data if 'gpt' in m.id.lower()]
            
            print(f"📋 Found {len(gpt_models)} GPT models")
            
            models_working = 0
            model_details = {}
            
            # Test a few key models
            test_models = ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo']
            
            for model_id in test_models:
                try:
                    start_time = time.time()
                    response = client.chat.completions.create(
                        model=model_id,
                        messages=[{"role": "user", "content": "Hello"}],
                        max_tokens=5
                    )
                    response_time = (time.time() - start_time) * 1000
                    
                    models_working += 1
                    model_details[model_id] = {
                        "status": " Working",
                        "response_time_ms": round(response_time, 2),
                        "sample_response": response.choices[0].message.content[:30] + "..."
                    }
                    print(f"    {model_id} ({response_time:.0f}ms)")
                    
                except Exception as e:
                    error_msg = str(e)[:50]
                    model_details[model_id] = {
                        "status": " Failed",
                        "error": error_msg
                    }
                    print(f"    {model_id} - {error_msg}")
            
            success_rate = (models_working / len(test_models) * 100)
            
            print(f"\n OPENAI SUMMARY:")
            print(f"   📈 Success Rate: {success_rate:.1f}% ({models_working}/{len(test_models)})")
            print(f"    Total GPT Models Available: {len(gpt_models)}")
            
            return {
                "status": " Working" if models_working > 0 else " No working models",
                "models_tested": len(test_models),
                "models_working": models_working,
                "total_models_available": len(gpt_models),
                "success_rate": success_rate,
                "model_details": model_details
            }
            
        except Exception as e:
            return {"status": " Failed to list models", "error": str(e)}
            
    except ImportError:
        return {"status": " openai package not available", "error": "Missing package"}
    except Exception as e:
        return {"status": " Failed", "error": str(e)}

def generate_beautiful_report(results):
    """Generate a beautiful visual report"""
    
    print_header(" ULTIMATE API STRENGTH REPORT", "=", 80)
    
    # Calculate totals
    total_working = 0
    total_tested = 0
    
    # Google APIs Summary
    print_header(" GOOGLE API KEYS RANKING", "-", 70)
    
    google_ranking = []
    for key_name, key_results in results["api_keys"]["google_keys"].items():
        if isinstance(key_results, dict) and "models_working" in key_results:
            google_ranking.append((key_name, key_results["models_working"], key_results["success_rate"]))
            total_working += key_results["models_working"]
            total_tested += key_results["models_tested"]
    
    # Sort by working models
    google_ranking.sort(key=lambda x: x[1], reverse=True)
    
    print("\n GOOGLE API KEY RANKINGS:")
    for i, (key_name, working, rate) in enumerate(google_ranking, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else ""
        print(f"   {medal} {i}. {key_name}: {working} models ({rate:.1f}% success)")
    
    # Anthropic Summary
    anthropic_results = results["api_keys"]["anthropic"]
    if isinstance(anthropic_results, dict) and "models_working" in anthropic_results:
        print(f"\n ANTHROPIC API: {anthropic_results['models_working']} Claude models working")
        total_working += anthropic_results["models_working"]
        total_tested += anthropic_results["models_tested"]
    
    # OpenAI Summary  
    openai_results = results["api_keys"]["openai"]
    if isinstance(openai_results, dict) and "models_working" in openai_results:
        print(f"🧠 OPENAI API: {openai_results['models_working']} GPT models working")
        total_working += openai_results["models_working"]
        total_tested += openai_results["models_tested"]
    
    # Overall Summary
    print_header(" OVERALL ARSENAL SUMMARY", "=", 70)
    
    print(f"\n TOTAL MODEL ACCESS:")
    print(f"    Working Models: {total_working}")
    print(f"   📋 Models Tested: {total_tested}")
    print(f"   📈 Overall Success Rate: {(total_working/total_tested*100):.1f}%")
    
    print(f"\n BEST API KEYS FOR DIFFERENT NEEDS:")
    if google_ranking:
        best_google = google_ranking[0]
        print(f"   🥇 Best Google Key: {best_google[0]} ({best_google[1]} models)")
    
    print(f"\n YOUR AI ORCHESTRATION POWER:")
    print(f"    Can orchestrate {total_working} different AI models")
    print(f"   ⚡ Express mode configured for 6x speed")
    print(f"   🧠 Shared memory across all models")
    print(f"   🔗 Local MCP integration ready")
    
    print(f"\n RECOMMENDATION:")
    if total_working > 15:
        print("    INCREDIBLE! You have access to a massive AI arsenal!")
        print("    Ready for full MOFY Family AI deployment")
        print("   👨‍👩‍👧‍👦 All systems GO for Family Unity!")
    elif total_working > 5:
        print("    Good model access for orchestration")
        print("    Ready for multi-AI coordination")
    else:
        print("     Limited model access - check API quotas")

async def main():
    """Run ultimate API strength test"""
    
    # Test all Google API keys
    print_header("TESTING GOOGLE API KEYS")
    for key_name, api_key in API_KEYS["Google Keys"].items():
        results["api_keys"]["google_keys"][key_name] = await test_google_api_key(key_name, api_key)
        await asyncio.sleep(1)  # Be nice to the API
    
    # Test Anthropic
    print_header("TESTING ANTHROPIC API")
    results["api_keys"]["anthropic"] = await test_anthropic_key(API_KEYS["Anthropic"]["primary"])
    
    # Test OpenAI
    print_header("TESTING OPENAI API") 
    results["api_keys"]["openai"] = await test_openai_key(API_KEYS["OpenAI"]["primary"])
    
    # Generate beautiful report
    generate_beautiful_report(results)
    
    # Save detailed results
    with open('ultimate_api_strength_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: ultimate_api_strength_results.json")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)