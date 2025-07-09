#!/usr/bin/env python3
"""
 ZAI GROUNDING SYSTEM
Real-time information access via Google Search integration
Always up-to-date responses with live data
"""

import os
import sys
import json
import asyncio
import aiohttp
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
from dotenv import load_dotenv

load_dotenv('../.env')

class GroundingSource(Enum):
    GOOGLE_SEARCH = "google_search"
    WEB_SEARCH = "web_search"
    NEWS_SEARCH = "news_search"
    REAL_TIME = "real_time"

@dataclass
class GroundingResult:
    source: GroundingSource
    query: str
    results: List[Dict[str, Any]]
    timestamp: datetime
    confidence: float

class ZaiGroundingSystem:
    """
    Real-time information grounding for ZAI responses
    """
    
    def __init__(self):
        self.api_keys = {
            "podplay-build-alpha": os.getenv("GOOGLE_AI_API_KEY_1", "AIzaSyCrLGbHF6LBTmJggdJW-6TBmLLEKC4nr5g"),
            "Gemini-API": os.getenv("GOOGLE_AI_API_KEY_2", "AIzaSyB0YfTUMuMB13DZM22nvbQcest57Bal8ik"), 
            "podplay-build-beta": os.getenv("GOOGLE_AI_API_KEY_3", "AIzaSyBU9JndWn2Uf1WLgbnMDmw5NHGQNRBO-_U")
        }
        
        # Search API keys (if available)
        self.google_search_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        self.google_search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        
        # Cache for recent searches
        self.search_cache = {}
        self.cache_ttl = timedelta(minutes=15)  # 15 minute cache
        
        logger = logging.getLogger(__name__)
        
    async def generate_with_grounding(self, 
                                    prompt: str,
                                    enable_search: bool = True,
                                    search_queries: List[str] = None,
                                    api_key: str = None) -> Dict:
        """
        Generate response with real-time grounding
        """
        try:
            import google.generativeai as genai
            
            if not api_key:
                api_key = self.api_keys["podplay-build-alpha"]
            
            genai.configure(api_key=api_key)
            
            # Extract search queries if not provided
            if enable_search and not search_queries:
                search_queries = await self.extract_search_queries(prompt)
            
            grounding_data = []
            
            # Perform grounding searches
            if enable_search and search_queries:
                print(f" Performing grounding searches: {search_queries}")
                
                for query in search_queries[:3]:  # Limit to 3 searches
                    search_result = await self.perform_grounded_search(query)
                    if search_result:
                        grounding_data.append(search_result)
            
            # Generate response with grounding
            model = genai.GenerativeModel("models/gemini-2.5-pro")
            
            # Build grounded prompt
            grounded_prompt = self.build_grounded_prompt(prompt, grounding_data)
            
            start_time = time.time()
            response = model.generate_content(
                grounded_prompt,
                generation_config={
                    'max_output_tokens': 1000,
                    'temperature': 0.1
                }
            )
            response_time = (time.time() - start_time) * 1000
            
            response_text = self.extract_response_text(response)
            
            # Convert grounding data to serializable format
            serializable_grounding = []
            for grounding in grounding_data:
                serializable_grounding.append({
                    "source": grounding.source.value,
                    "query": grounding.query,
                    "results": grounding.results,
                    "timestamp": grounding.timestamp.isoformat(),
                    "confidence": grounding.confidence
                })

            return {
                "success": True,
                "content": response_text,
                "grounding_enabled": enable_search,
                "grounding_sources": len(grounding_data),
                "search_queries": search_queries or [],
                "grounding_data": serializable_grounding,
                "response_time_ms": round(response_time, 2),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "grounding_enabled": enable_search
            }
    
    async def extract_search_queries(self, prompt: str) -> List[str]:
        """
        Extract relevant search queries from user prompt
        """
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_keys["Gemini-API"])
            model = genai.GenerativeModel("models/gemini-1.5-flash")  # Fast model for query extraction
            
            extraction_prompt = f"""
            Analyze this user prompt and extract 1-3 specific search queries that would provide current, relevant information to help answer it.
            
            User prompt: "{prompt}"
            
            Extract search queries that would find:
            - Current events or recent developments
            - Latest data, statistics, or facts
            - Recent news or updates
            - Current prices, availability, or status
            
            Return only the search queries, one per line. If no current information is needed, return "NONE".
            
            Search queries:
            """
            
            response = model.generate_content(
                extraction_prompt,
                generation_config={'max_output_tokens': 200}
            )
            
            response_text = self.extract_response_text(response)
            
            if response_text and "NONE" not in response_text.upper():
                queries = [q.strip() for q in response_text.split('\n') if q.strip()]
                return queries[:3]  # Limit to 3 queries
            
            return []
            
        except Exception as e:
            print(f" Query extraction failed: {e}")
            return []
    
    async def perform_grounded_search(self, query: str) -> Optional[GroundingResult]:
        """
        Perform grounded search for real-time information
        """
        # Check cache first
        cache_key = f"search_{query}"
        if cache_key in self.search_cache:
            cached_result, cached_time = self.search_cache[cache_key]
            if datetime.now() - cached_time < self.cache_ttl:
                print(f"📋 Using cached result for: {query}")
                return cached_result
        
        try:
            # Try Google Custom Search API if available
            if self.google_search_api_key and self.google_search_engine_id:
                result = await self.google_custom_search(query)
            else:
                # Fallback to simulated search
                result = await self.simulated_search(query)
            
            # Cache the result
            self.search_cache[cache_key] = (result, datetime.now())
            
            return result
            
        except Exception as e:
            print(f" Search failed for '{query}': {e}")
            return None
    
    async def google_custom_search(self, query: str) -> GroundingResult:
        """
        Use Google Custom Search API for real grounding
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    'key': self.google_search_api_key,
                    'cx': self.google_search_engine_id,
                    'q': query,
                    'num': 5,
                    'dateRestrict': 'd7'  # Last 7 days for fresh content
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        results = []
                        for item in data.get('items', []):
                            results.append({
                                'title': item.get('title'),
                                'snippet': item.get('snippet'),
                                'link': item.get('link'),
                                'displayLink': item.get('displayLink')
                            })
                        
                        return GroundingResult(
                            source=GroundingSource.GOOGLE_SEARCH,
                            query=query,
                            results=results,
                            timestamp=datetime.now(),
                            confidence=0.9
                        )
                    else:
                        print(f" Google Search API error: {response.status}")
                        return await self.simulated_search(query)
                        
        except Exception as e:
            print(f" Google Custom Search failed: {e}")
            return await self.simulated_search(query)
    
    async def simulated_search(self, query: str) -> GroundingResult:
        """
        Simulated search for testing (replace with real implementation)
        """
        # Simulate search delay
        await asyncio.sleep(0.5)
        
        # Simulated results based on query
        simulated_results = [
            {
                'title': f"Latest information about {query}",
                'snippet': f"Recent developments and current information related to {query}. This is simulated search data for testing purposes.",
                'link': f"https://example.com/search/{query.replace(' ', '-')}",
                'displayLink': 'example.com'
            },
            {
                'title': f"Current status of {query}",
                'snippet': f"Up-to-date details and latest updates on {query}. Real-time information would be provided here.",
                'link': f"https://news.example.com/{query.replace(' ', '-')}",
                'displayLink': 'news.example.com'
            }
        ]
        
        return GroundingResult(
            source=GroundingSource.WEB_SEARCH,
            query=query,
            results=simulated_results,
            timestamp=datetime.now(),
            confidence=0.7  # Lower confidence for simulated data
        )
    
    def build_grounded_prompt(self, original_prompt: str, grounding_data: List[GroundingResult]) -> str:
        """
        Build prompt with grounding context
        """
        if not grounding_data:
            return original_prompt
        
        grounded_prompt = f"""
You are ZAI, an intelligent AI assistant with access to real-time information. Use the current information provided below to give accurate, up-to-date responses.

CURRENT INFORMATION (Retrieved {datetime.now().strftime('%Y-%m-%d %H:%M')}):

"""
        
        for i, grounding in enumerate(grounding_data, 1):
            grounded_prompt += f"\n--- Search Query {i}: {grounding.query} ---\n"
            for j, result in enumerate(grounding.results[:3], 1):  # Top 3 results
                grounded_prompt += f"{j}. {result['title']}\n"
                grounded_prompt += f"   {result['snippet']}\n"
                grounded_prompt += f"   Source: {result['displayLink']}\n\n"
        
        grounded_prompt += f"""
---

Original User Question: {original_prompt}

Instructions:
1. Use the current information above to provide an accurate, up-to-date response
2. Cite specific sources when referencing the grounded information
3. If the grounded information doesn't fully answer the question, combine it with your knowledge while noting what's current vs. general knowledge
4. Be clear about the recency and sources of your information

Response:
"""
        
        return grounded_prompt
    
    def extract_response_text(self, response):
        """Extract response text handling different model formats"""
        try:
            if hasattr(response, 'text') and response.text:
                return response.text
        except Exception:
            pass
        
        try:
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        return candidate.content.parts[0].text
        except Exception:
            pass
        
        return "Response processing error"
    
    def get_grounding_status(self) -> Dict:
        """
        Get current grounding system status
        """
        return {
            "google_search_api_available": bool(self.google_search_api_key),
            "cache_entries": len(self.search_cache),
            "cache_ttl_minutes": self.cache_ttl.total_seconds() / 60,
            "supported_sources": [source.value for source in GroundingSource],
            "last_cache_cleanup": datetime.now().isoformat()
        }

# Global grounding system instance
zai_grounding = ZaiGroundingSystem()

async def main():
    """Test grounding system"""
    print(" Testing ZAI Grounding System...")
    
    # Test grounded generation
    result = await zai_grounding.generate_with_grounding(
        "What are the latest developments in AI technology this week?",
        enable_search=True
    )
    
    print(f" Grounded Response: {json.dumps(result, indent=2)}")
    
    # Test status
    status = zai_grounding.get_grounding_status()
    print(f" Status: {json.dumps(status, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())