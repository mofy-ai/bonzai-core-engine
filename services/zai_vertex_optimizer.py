#!/usr/bin/env python3
"""
🧠 ZAI VERTEX AI MODEL OPTIMIZER
Advanced intelligent model selection with fallback to brilliant quota rotation
"""

import os
import sys
import json
import asyncio
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

load_dotenv('../.env')

class OptimizationMode(Enum):
    COST = "cost"
    QUALITY = "quality" 
    BALANCE = "balance"
    SPEED = "speed"

@dataclass
class ModelPerformance:
    name: str
    avg_response_time: float
    success_rate: float
    cost_per_token: float
    quality_score: float
    last_used: datetime
    quota_status: str

class ZaiVertexOptimizer:
    """
    Intelligent model selection with Nathan's quota rotation as fallback
    """
    
    def __init__(self):
        self.google_keys = {
            "podplay-build-alpha": os.getenv("GOOGLE_AI_API_KEY_1", "AIzaSyCrLGbHF6LBTmJggdJW-6TBmLLEKC4nr5g"),
            "Gemini-API": os.getenv("GOOGLE_AI_API_KEY_2", "AIzaSyB0YfTUMuMB13DZM22nvbQcest57Bal8ik"), 
            "podplay-build-beta": os.getenv("GOOGLE_AI_API_KEY_3", "AIzaSyBU9JndWn2Uf1WLgbnMDmw5NHGQNRBO-_U")
        }
        
        # Pro models confirmed working from today's testing
        self.pro_models = {
            "podplay-build-alpha": [
                "models/gemini-1.5-pro",
                "models/gemini-1.5-pro-002", 
                "models/gemini-1.5-pro-latest",
                "models/gemini-2.5-pro",
                "models/gemini-2.5-pro-preview-05-06",
                "models/gemini-2.5-pro-preview-06-05",
                "models/gemini-2.5-pro-preview-03-25"
            ],
            "Gemini-API": [
                "models/gemini-1.5-pro",
                "models/gemini-1.5-pro-002",
                "models/gemini-1.5-pro-latest", 
                "models/gemini-2.5-pro",
                "models/gemini-2.5-pro-preview-05-06",
                "models/gemini-2.5-pro-preview-06-05",
                "models/gemini-2.5-pro-preview-03-25"
            ],
            "podplay-build-beta": [
                "models/gemini-2.5-pro"
            ]
        }
        
        # Model performance tracking
        self.model_performance: Dict[str, ModelPerformance] = {}
        self.load_performance_data()
        
        # Quota rotation state (Nathan's brilliant strategy)
        self.quota_rotation_index = 0
        self.last_rotation_time = datetime.now()
        
        # Vertex AI setup
        self.vertex_available = False
        self.setup_vertex_ai()
        
    def setup_vertex_ai(self):
        """Setup Vertex AI if available"""
        try:
            import vertexai
            from vertexai.generative_models import GenerativeModel
            
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
            region = os.getenv('VERTEX_AI_REGION', 'us-central1')
            
            if project_id and region:
                vertexai.init(project=project_id, location=region)
                self.vertex_available = True
                print(f" Vertex AI initialized: {project_id} in {region}")
            else:
                print("  Vertex AI config missing - using standard API with quota rotation")
                
        except ImportError:
            print("  Vertex AI SDK not available - using standard API with quota rotation")
            
    def load_performance_data(self):
        """Load model performance data"""
        try:
            with open('/mnt/c/Bonzai-Desktop/zai-backend/model_performance.json', 'r') as f:
                data = json.load(f)
                for model_name, perf_data in data.items():
                    self.model_performance[model_name] = ModelPerformance(
                        name=model_name,
                        avg_response_time=perf_data.get('avg_response_time', 1000),
                        success_rate=perf_data.get('success_rate', 0.9),
                        cost_per_token=perf_data.get('cost_per_token', 0.001),
                        quality_score=perf_data.get('quality_score', 0.8),
                        last_used=datetime.fromisoformat(perf_data.get('last_used', datetime.now().isoformat())),
                        quota_status=perf_data.get('quota_status', 'available')
                    )
        except FileNotFoundError:
            print(" Initializing performance tracking...")
            
    def save_performance_data(self):
        """Save model performance data"""
        data = {}
        for model_name, perf in self.model_performance.items():
            data[model_name] = {
                'avg_response_time': perf.avg_response_time,
                'success_rate': perf.success_rate,
                'cost_per_token': perf.cost_per_token,
                'quality_score': perf.quality_score,
                'last_used': perf.last_used.isoformat(),
                'quota_status': perf.quota_status
            }
            
        with open('/mnt/c/Bonzai-Desktop/zai-backend/model_performance.json', 'w') as f:
            json.dump(data, f, indent=2)
            
    def get_next_quota_rotation_model(self) -> Tuple[str, str]:
        """
        Nathan's brilliant quota rotation strategy
        15 PRO models across 3 keys = unlimited capacity
        """
        all_models = []
        for key_name, models in self.pro_models.items():
            for model in models:
                all_models.append((key_name, model))
        
        # Rotate through all 15 models
        key_name, model_name = all_models[self.quota_rotation_index % len(all_models)]
        self.quota_rotation_index += 1
        
        print(f" Quota rotation: {key_name} -> {model_name}")
        return key_name, model_name
        
    def intelligent_model_selection(self, task_type: str, optimization_mode: OptimizationMode) -> Tuple[str, str]:
        """
        Intelligent model selection based on task and optimization mode
        Falls back to quota rotation if needed
        """
        if not self.vertex_available:
            print(" Using quota rotation (Vertex AI not available)")
            return self.get_next_quota_rotation_model()
            
        # Get available models with good performance
        available_models = []
        for key_name, models in self.pro_models.items():
            for model in models:
                perf = self.model_performance.get(model)
                if not perf:
                    # New model - add to tracking
                    perf = ModelPerformance(
                        name=model,
                        avg_response_time=1000 if "2.5" in model else 500,
                        success_rate=0.9,
                        cost_per_token=0.002 if "2.5" in model else 0.001,
                        quality_score=0.95 if "2.5" in model else 0.85,
                        last_used=datetime.now() - timedelta(hours=1),
                        quota_status='available'
                    )
                    self.model_performance[model] = perf
                    
                # Check if model is available (not recently quota-limited)
                if perf.quota_status == 'available' or \
                   (perf.quota_status == 'quota_exceeded' and 
                    datetime.now() - perf.last_used > timedelta(minutes=60)):
                    available_models.append((key_name, model, perf))
        
        if not available_models:
            print("  No available models - using quota rotation fallback")
            return self.get_next_quota_rotation_model()
            
        # Select based on optimization mode
        if optimization_mode == OptimizationMode.SPEED:
            # Fastest response time
            selected = min(available_models, key=lambda x: x[2].avg_response_time)
        elif optimization_mode == OptimizationMode.QUALITY:
            # Highest quality score (prioritize 2.5 models)
            selected = max(available_models, key=lambda x: x[2].quality_score)
        elif optimization_mode == OptimizationMode.COST:
            # Lowest cost per token
            selected = min(available_models, key=lambda x: x[2].cost_per_token)
        else:  # BALANCE
            # Balanced score
            def balance_score(model_data):
                key, model, perf = model_data
                return (perf.quality_score * 0.4 + 
                       (1 - perf.cost_per_token) * 0.3 + 
                       (1000 / perf.avg_response_time) * 0.3)
            selected = max(available_models, key=balance_score)
            
        key_name, model_name, perf = selected
        print(f"🧠 Intelligent selection ({optimization_mode.value}): {key_name} -> {model_name}")
        return key_name, model_name
        
    async def generate_content(self, 
                             prompt: str, 
                             task_type: str = "general",
                             optimization_mode: OptimizationMode = OptimizationMode.BALANCE,
                             **kwargs) -> Dict:
        """
        Generate content with intelligent model selection
        """
        try:
            import google.generativeai as genai
            
            # Select optimal model
            key_name, model_name = self.intelligent_model_selection(task_type, optimization_mode)
            api_key = self.google_keys[key_name]
            
            # Configure and generate
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            
            start_time = time.time()
            
            generation_config = kwargs.get('generation_config', {})
            if not generation_config:
                generation_config = {'max_output_tokens': 1000}
                
            response = model.generate_content(prompt, generation_config=generation_config)
            response_time = (time.time() - start_time) * 1000
            
            # Extract response text (handle 2.5 models)
            response_text = self.extract_response_text(response)
            
            if response_text:
                # Update performance tracking
                self.update_model_performance(model_name, response_time, True)
                
                return {
                    "success": True,
                    "content": response_text,
                    "model_used": model_name,
                    "key_used": key_name,
                    "response_time_ms": round(response_time, 2),
                    "optimization_mode": optimization_mode.value
                }
            else:
                raise Exception("No response text extracted")
                
        except Exception as e:
            error_msg = str(e)
            
            # Update performance tracking for failures
            if 'model_name' in locals():
                self.update_model_performance(model_name, 0, False, error_msg)
            
            # If quota exceeded, try quota rotation fallback
            if "quota" in error_msg.lower() or "429" in error_msg:
                print(f"💰 Quota exceeded on {model_name}, trying rotation...")
                return await self.quota_rotation_fallback(prompt, **kwargs)
            
            return {
                "success": False,
                "error": error_msg,
                "model_attempted": model_name if 'model_name' in locals() else "unknown"
            }
            
    async def quota_rotation_fallback(self, prompt: str, **kwargs) -> Dict:
        """
        Fallback to Nathan's quota rotation when intelligent selection fails
        """
        max_attempts = 5
        
        for attempt in range(max_attempts):
            try:
                import google.generativeai as genai
                
                key_name, model_name = self.get_next_quota_rotation_model()
                api_key = self.google_keys[key_name]
                
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                
                start_time = time.time()
                generation_config = kwargs.get('generation_config', {'max_output_tokens': 1000})
                
                response = model.generate_content(prompt, generation_config=generation_config)
                response_time = (time.time() - start_time) * 1000
                
                response_text = self.extract_response_text(response)
                
                if response_text:
                    self.update_model_performance(model_name, response_time, True)
                    
                    return {
                        "success": True,
                        "content": response_text,
                        "model_used": model_name,
                        "key_used": key_name,
                        "response_time_ms": round(response_time, 2),
                        "optimization_mode": "quota_rotation_fallback"
                    }
                    
            except Exception as e:
                if 'model_name' in locals():
                    self.update_model_performance(model_name, 0, False, str(e))
                print(f" Attempt {attempt + 1} failed: {str(e)[:50]}")
                await asyncio.sleep(1)
                
        return {
            "success": False,
            "error": "All quota rotation attempts failed",
            "attempts": max_attempts
        }
        
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
        
        return None
        
    def update_model_performance(self, model_name: str, response_time: float, success: bool, error: str = ""):
        """Update model performance tracking"""
        if model_name not in self.model_performance:
            self.model_performance[model_name] = ModelPerformance(
                name=model_name,
                avg_response_time=response_time or 1000,
                success_rate=1.0 if success else 0.0,
                cost_per_token=0.002 if "2.5" in model_name else 0.001,
                quality_score=0.95 if "2.5" in model_name else 0.85,
                last_used=datetime.now(),
                quota_status='available'
            )
        else:
            perf = self.model_performance[model_name]
            if response_time > 0:
                perf.avg_response_time = (perf.avg_response_time * 0.8 + response_time * 0.2)
            perf.success_rate = perf.success_rate * 0.9 + (1.0 if success else 0.0) * 0.1
            perf.last_used = datetime.now()
            
            if "quota" in error.lower():
                perf.quota_status = 'quota_exceeded'
            elif success:
                perf.quota_status = 'available'
                
        self.save_performance_data()
        
    def get_orchestration_status(self) -> Dict:
        """Get current orchestration status"""
        total_models = sum(len(models) for models in self.pro_models.values())
        available_models = sum(1 for perf in self.model_performance.values() 
                             if perf.quota_status == 'available')
        
        return {
            "total_pro_models": total_models,
            "available_models": available_models,
            "vertex_ai_available": self.vertex_available,
            "quota_rotation_index": self.quota_rotation_index,
            "theoretical_rpm": total_models * 2,
            "orchestration_ready": total_models >= 9
        }

# Global optimizer instance
zai_optimizer = ZaiVertexOptimizer()

async def main():
    """Test the optimizer"""
    print("🧠 Testing ZAI Vertex Optimizer...")
    
    # Test intelligent selection
    result = await zai_optimizer.generate_content(
        "Hello, this is a test of the intelligent orchestration system",
        task_type="general",
        optimization_mode=OptimizationMode.QUALITY
    )
    
    print(f" Result: {json.dumps(result, indent=2)}")
    
    # Test status
    status = zai_optimizer.get_orchestration_status()
    print(f" Status: {json.dumps(status, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())