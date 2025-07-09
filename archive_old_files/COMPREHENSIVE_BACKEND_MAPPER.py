#!/usr/bin/env python3
"""
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
🔥 COMPREHENSIVE BONZAI BACKEND MAPPING & ANALYSIS TOOL 🔥
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥

This tool maps EVERY endpoint, response structure, data type, and capability
of our Bonzai backend so we know EXACTLY what we're working with for UI development.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Tuple
import sys

# Configuration
BACKEND_BASE = "http://127.0.0.1:5001"
OUTPUT_FILE = "BONZAI_BACKEND_MAPPING.json"

# Comprehensive endpoint configuration - FIXED WITH /api/ PREFIX!
TEST_CONFIG = {
    "CORE": [
        {"name": "Root", "url": "/", "method": "GET"},
        {"name": "Health Check", "url": "/api/health", "method": "GET"},
    ],
    "ZAI_PRIME": [
        {"name": "ZAI Prime Status", "url": "/api/zai-prime/status", "method": "GET"},
        {"name": "Agents List", "url": "/api/zai-prime/agents", "method": "GET"},
        {"name": "Global Context", "url": "/api/zai-prime/context", "method": "GET"},
    ],
    "MCP_INTEGRATION": [
        {"name": "MCP Tools", "url": "/api/mcp/tools", "method": "GET"},
        {"name": "MCP Execute", "url": "/api/mcp/execute", "method": "POST", "data": {"tool": "orchestrate_ai", "parameters": {"model": "test", "prompt": "Mapping test"}}},
    ],
    "MEMORY_SYSTEM": [
        {"name": "Memory Health", "url": "/api/memory/health", "method": "GET"},
        {"name": "Memory Search", "url": "/api/memory/search", "method": "POST", "data": {"query": "test", "user_id": "mapper_test"}},
    ],
    "AI_ORCHESTRATION": [
        {"name": "Simple Chat", "url": "/api/chat/simple", "method": "POST", "data": {"message": "Backend mapping test", "model": "gemini"}},
        {"name": "Multi-Model", "url": "/api/multi-model/status", "method": "GET"},
    ],
    "ADVANCED_FEATURES": [
        {"name": "Agent Registry", "url": "/api/agent-registry/status", "method": "GET"},
        {"name": "Task Orchestrator", "url": "/api/task-orchestrator/status", "method": "GET"},
        {"name": "WebSocket Coordinator", "url": "/api/websocket-coordinator/status", "method": "GET"},
    ],
    "SCRAPYBARA": [
        {"name": "Scrapybara Status", "url": "/api/scrape/status", "method": "GET"},
    ]
}

def analyze_data_structure(data: Any, path: str = "") -> Dict[str, Any]:
    """Deep analysis of data structure"""
    analysis = {
        "type": type(data).__name__,
        "path": path,
        "value_sample": None,
        "children": {}
    }
    
    if isinstance(data, dict):
        analysis["keys"] = list(data.keys())
        analysis["key_count"] = len(data.keys())
        for key, value in data.items():
            child_path = f"{path}.{key}" if path else key
            analysis["children"][key] = analyze_data_structure(value, child_path)
    
    elif isinstance(data, list):
        analysis["length"] = len(data)
        analysis["item_types"] = list(set(type(item).__name__ for item in data))
        if data:  # Analyze first item structure
            analysis["children"]["[0]"] = analyze_data_structure(data[0], f"{path}[0]")
    
    else:
        # Primitive types
        analysis["value_sample"] = str(data)[:100] + "..." if len(str(data)) > 100 else str(data)
    
    return analysis

def test_endpoint(category: str, endpoint: Dict[str, str]) -> Dict[str, Any]:
    """Test a single endpoint and return comprehensive results"""
    test_start = time.time()
    result = {
        "category": category,
        "name": endpoint["name"],
        "url": endpoint["url"],
        "method": endpoint["method"],
        "timestamp": datetime.now().isoformat(),
        "success": False,
        "status_code": None,
        "response_time_ms": 0,
        "raw_response": None,
        "data_structure": None,
        "error": None,
        "headers": None,
        "content_length": 0
    }
    
    try:
        full_url = f"{BACKEND_BASE}{endpoint['url']}"
        
        # Handle different HTTP methods
        if endpoint["method"] == "POST":
            response = requests.post(full_url, json=endpoint.get("data", {}), timeout=10)
        else:
            response = requests.get(full_url, timeout=10)
        
        result["status_code"] = response.status_code
        result["response_time_ms"] = round((time.time() - test_start) * 1000, 2)
        result["headers"] = dict(response.headers)
        result["content_length"] = len(response.content)
        
        if response.ok:
            try:
                json_data = response.json()
                result["success"] = True
                result["raw_response"] = json_data
                result["data_structure"] = analyze_data_structure(json_data)
            except json.JSONDecodeError:
                result["raw_response"] = response.text
                result["error"] = "Response not valid JSON"
        else:
            result["error"] = f"HTTP {response.status_code}: {response.reason}"
            try:
                result["raw_response"] = response.json()
            except:
                result["raw_response"] = response.text
                
    except requests.exceptions.RequestException as e:
        result["error"] = str(e)
        result["response_time_ms"] = round((time.time() - test_start) * 1000, 2)
    
    return result

def generate_scrapybara_analysis(scrapybara_result: Dict[str, Any]) -> Dict[str, Any]:
    """Special analysis for Scrapybara capabilities"""
    if not scrapybara_result["success"]:
        return {"error": "Scrapybara endpoint failed", "capabilities": []}
    
    data = scrapybara_result["raw_response"]
    
    analysis = {
        "service_online": scrapybara_result["success"],
        "active_jobs": data.get("active_jobs", 0),
        "service_message": data.get("message", ""),
        "service_name": data.get("service", "unknown"),
        "capabilities": [],
        "ready_for_ui": False
    }
    
    # Analyze capabilities based on response
    if data.get("service"):
        analysis["capabilities"].append("Service Status Available")
    if "active_jobs" in data:
        analysis["capabilities"].append("Job Monitoring")
    if data.get("message"):
        analysis["capabilities"].append("Status Messages")
    
    analysis["ready_for_ui"] = len(analysis["capabilities"]) > 0
    
    return analysis

def main():
    print("🔥" * 80)
    print("🔥 COMPREHENSIVE BONZAI BACKEND MAPPING & ANALYSIS TOOL 🔥")
    print("🔥" * 80)
    print(f"Testing backend at: {BACKEND_BASE}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Initialize results structure
    results = {
        "metadata": {
            "backend_url": BACKEND_BASE,
            "test_timestamp": datetime.now().isoformat(),
            "total_endpoints": sum(len(endpoints) for endpoints in TEST_CONFIG.values()),
            "categories": list(TEST_CONFIG.keys())
        },
        "summary": {
            "total_tested": 0,
            "total_successful": 0,
            "total_failed": 0,
            "success_rate": 0.0,
            "category_stats": {}
        },
        "detailed_results": {},
        "scrapybara_analysis": {},
        "ui_development_insights": {}
    }
    
    # Test all endpoints
    for category, endpoints in TEST_CONFIG.items():
        print(f"\n🔍 TESTING {category} SERVICES")
        print("=" * 40)
        
        category_results = []
        category_success = 0
        
        for endpoint in endpoints:
            print(f"   Testing: {endpoint['name']}...", end="")
            result = test_endpoint(category, endpoint)
            
            if result["success"]:
                print(f" ✅ ({result['response_time_ms']}ms)")
                category_success += 1
            else:
                print(f" ❌ ({result.get('error', 'Unknown error')})")
            
            category_results.append(result)
            results["summary"]["total_tested"] += 1
            
            # Special handling for Scrapybara
            if category == "SCRAPYBARA" and result["success"]:
                results["scrapybara_analysis"] = generate_scrapybara_analysis(result)
        
        results["detailed_results"][category] = category_results
        results["summary"]["category_stats"][category] = {
            "tested": len(endpoints),
            "successful": category_success,
            "success_rate": round((category_success / len(endpoints)) * 100, 1)
        }
        results["summary"]["total_successful"] += category_success
    
    # Calculate overall stats
    results["summary"]["total_failed"] = results["summary"]["total_tested"] - results["summary"]["total_successful"]
    results["summary"]["success_rate"] = round(
        (results["summary"]["total_successful"] / results["summary"]["total_tested"]) * 100, 1
    )
    
    # Generate UI development insights
    results["ui_development_insights"] = generate_ui_insights(results)
    
    # Print summary
    print("\n" + "🔥" * 80)
    print("🔥 COMPREHENSIVE MAPPING COMPLETE 🔥")
    print("🔥" * 80)
    print(f"\n📊 SUMMARY STATISTICS:")
    print(f"   Total Endpoints: {results['summary']['total_tested']}")
    print(f"   Successful: {results['summary']['total_successful']}")
    print(f"   Failed: {results['summary']['total_failed']}")
    print(f"   Success Rate: {results['summary']['success_rate']}%")
    
    print(f"\n📂 CATEGORY BREAKDOWN:")
    for category, stats in results["summary"]["category_stats"].items():
        print(f"   {category}: {stats['successful']}/{stats['tested']} ({stats['success_rate']}%)")
    
    # Save detailed results
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: {OUTPUT_FILE}")
    print(f"🎯 Ready for UI development planning!")
    
    return results

def generate_ui_insights(results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate insights for UI development based on backend capabilities"""
    insights = {
        "available_data_sources": [],
        "ui_components_needed": [],
        "integration_priorities": [],
        "data_visualization_opportunities": []
    }
    
    # Analyze successful endpoints for UI opportunities
    for category, endpoints in results["detailed_results"].items():
        for endpoint in endpoints:
            if endpoint["success"]:
                insights["available_data_sources"].append({
                    "name": endpoint["name"],
                    "category": category,
                    "data_keys": list(endpoint["data_structure"]["children"].keys()) if endpoint["data_structure"]["children"] else [],
                    "url": endpoint["url"]
                })
    
    # Generate component suggestions based on available data
    if results["summary"]["category_stats"].get("AI_ORCHESTRATION", {}).get("successful", 0) > 0:
        insights["ui_components_needed"].extend(["Chat Interface", "Model Selection", "Response Display"])
    
    if results["summary"]["category_stats"].get("MEMORY_SYSTEM", {}).get("successful", 0) > 0:
        insights["ui_components_needed"].extend(["Memory Search", "Context Display", "Memory Health Monitor"])
    
    if results["summary"]["category_stats"].get("SCRAPYBARA", {}).get("successful", 0) > 0:
        insights["ui_components_needed"].extend(["Job Monitor", "Scraping Controls", "Results Display"])
    
    return insights

if __name__ == "__main__":
    try:
        results = main()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n❌ Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error during testing: {e}")
        sys.exit(1)
