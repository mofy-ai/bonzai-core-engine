"""
[CHART] Performance Tracker
Tracks model performance and optimizes routing decisions based on real-world data
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import defaultdict, deque
import json
import statistics

logger = logging.getLogger(__name__)

class PerformanceTracker:
    """Tracks model performance and optimizes routing"""
    
    def __init__(self, max_history: int = 10000):
        self.max_history = max_history
        self.performance_data = defaultdict(lambda: {
            "success_rate": 1.0,
            "avg_latency": 0,
            "total_requests": 0,
            "failures": 0,
            "recent_latencies": deque(maxlen=100),  # Last 100 requests
            "error_types": defaultdict(int),
            "last_success": None,
            "last_failure": None,
            "cost_efficiency": 1.0,
            "user_satisfaction": 1.0
        })
        
        self.request_history = deque(maxlen=max_history)
        self.model_rankings = {}
        self.optimization_suggestions = []
        
    async def record_request_start(self, model_key: str, request_id: str, 
                                 request_data: Dict[str, Any]) -> None:
        """Record the start of a request"""
        
        timestamp = datetime.now()
        
        request_record = {
            "request_id": request_id,
            "model_key": model_key,
            "start_time": timestamp,
            "request_data": request_data,
            "status": "in_progress"
        }
        
        self.request_history.append(request_record)
        self.performance_data[model_key]["total_requests"] += 1
        
        logger.debug(f"Started tracking request {request_id} for model {model_key}")
    
    async def record_success(self, model_key: str, request_id: str, 
                           latency_ms: float, response_data: Dict[str, Any] = None) -> None:
        """Record a successful request"""
        
        timestamp = datetime.now()
        
        # Update performance data
        perf_data = self.performance_data[model_key]
        perf_data["recent_latencies"].append(latency_ms)
        perf_data["last_success"] = timestamp
        
        # Recalculate average latency
        if perf_data["recent_latencies"]:
            perf_data["avg_latency"] = statistics.mean(perf_data["recent_latencies"])
        
        # Recalculate success rate
        total_requests = perf_data["total_requests"]
        failures = perf_data["failures"]
        perf_data["success_rate"] = (total_requests - failures) / total_requests if total_requests > 0 else 1.0
        
        # Update request history
        for record in reversed(self.request_history):
            if record["request_id"] == request_id:
                record["status"] = "success"
                record["end_time"] = timestamp
                record["latency_ms"] = latency_ms
                record["response_data"] = response_data
                break
        
        logger.debug(f"Recorded success for {model_key}: {latency_ms}ms latency")
        
        # Trigger optimization analysis
        await self._analyze_performance_trends(model_key)
    
    async def record_failure(self, model_key: str, request_id: str, 
                           error_type: str, error_details: str = None) -> None:
        """Record a failed request"""
        
        timestamp = datetime.now()
        
        # Update performance data
        perf_data = self.performance_data[model_key]
        perf_data["failures"] += 1
        perf_data["error_types"][error_type] += 1
        perf_data["last_failure"] = timestamp
        
        # Recalculate success rate
        total_requests = perf_data["total_requests"]
        failures = perf_data["failures"]
        perf_data["success_rate"] = (total_requests - failures) / total_requests if total_requests > 0 else 1.0
        
        # Update request history
        for record in reversed(self.request_history):
            if record["request_id"] == request_id:
                record["status"] = "failure"
                record["end_time"] = timestamp
                record["error_type"] = error_type
                record["error_details"] = error_details
                break
        
        logger.warning(f"Recorded failure for {model_key}: {error_type}")
        
        # Trigger immediate optimization if failure rate is high
        if perf_data["success_rate"] < 0.8:
            await self._generate_optimization_suggestions(model_key)
    
    async def get_performance_adjusted_routing(self, base_routing: Dict[str, Any]) -> Dict[str, Any]:
        """Adjust routing based on recent performance data"""
        
        primary_model = base_routing["primary_model"]
        fallback_models = base_routing["fallback_models"].copy()
        
        # Check if primary model is performing poorly
        primary_perf = self.performance_data[primary_model]
        
        # If primary model has low success rate or high latency, consider alternatives
        if (primary_perf["success_rate"] < 0.8 or 
            primary_perf["avg_latency"] > 5000 or  # 5 seconds
            self._is_model_overloaded(primary_model)):
            
            # Find best performing alternative from fallbacks
            best_fallback = self._find_best_alternative(fallback_models)
            
            if best_fallback and best_fallback != primary_model:
                logger.info(f"Performance adjustment: {primary_model} → {best_fallback}")
                
                # Promote best fallback to primary
                base_routing["primary_model"] = best_fallback
                
                # Move original primary to fallbacks
                if primary_model not in fallback_models:
                    fallback_models.insert(0, primary_model)
                
                # Remove promoted model from fallbacks
                if best_fallback in fallback_models:
                    fallback_models.remove(best_fallback)
                
                base_routing["fallback_models"] = fallback_models
                base_routing["performance_adjusted"] = True
                base_routing["adjustment_reason"] = f"Poor performance: {primary_perf['success_rate']:.2f} success rate"
        
        return base_routing
    
    def _find_best_alternative(self, candidate_models: List[str]) -> Optional[str]:
        """Find the best performing model from a list of candidates"""
        
        if not candidate_models:
            return None
        
        # Score each candidate based on multiple factors
        scored_models = []
        
        for model_key in candidate_models:
            perf_data = self.performance_data[model_key]
            
            # Calculate composite score (0-1, higher is better)
            success_score = perf_data["success_rate"]
            latency_score = max(0, 1 - (perf_data["avg_latency"] / 10000))  # Normalize to 10s max
            recency_score = self._calculate_recency_score(model_key)
            
            composite_score = (success_score * 0.4 + 
                             latency_score * 0.3 + 
                             recency_score * 0.3)
            
            scored_models.append((model_key, composite_score))
        
        # Sort by score and return best
        scored_models.sort(key=lambda x: x[1], reverse=True)
        return scored_models[0][0] if scored_models else None
    
    def _calculate_recency_score(self, model_key: str) -> float:
        """Calculate score based on recent usage (prefer recently successful models)"""
        
        perf_data = self.performance_data[model_key]
        last_success = perf_data["last_success"]
        last_failure = perf_data["last_failure"]
        
        if not last_success:
            return 0.5  # Neutral score for unused models
        
        # Time since last success
        time_since_success = (datetime.now() - last_success).total_seconds()
        
        # If there was a recent failure after the last success, penalize
        if last_failure and last_failure > last_success:
            time_since_failure = (datetime.now() - last_failure).total_seconds()
            if time_since_failure < 300:  # 5 minutes
                return 0.2  # Low score for recently failed models
        
        # Score based on recency (higher for more recent successes)
        if time_since_success < 300:  # 5 minutes
            return 1.0
        elif time_since_success < 1800:  # 30 minutes
            return 0.8
        elif time_since_success < 3600:  # 1 hour
            return 0.6
        else:
            return 0.4
    
    def _is_model_overloaded(self, model_key: str) -> bool:
        """Check if a model appears to be overloaded based on recent patterns"""
        
        # Count recent requests (last 5 minutes)
        recent_requests = 0
        cutoff_time = datetime.now() - timedelta(minutes=5)
        
        for record in reversed(self.request_history):
            if (record["model_key"] == model_key and 
                record["start_time"] > cutoff_time):
                recent_requests += 1
            elif record["start_time"] <= cutoff_time:
                break
        
        # Consider overloaded if more than 50 requests in 5 minutes
        return recent_requests > 50
    
    async def _analyze_performance_trends(self, model_key: str) -> None:
        """Analyze performance trends and generate insights"""
        
        perf_data = self.performance_data[model_key]
        
        # Analyze latency trends
        if len(perf_data["recent_latencies"]) >= 10:
            recent_latencies = list(perf_data["recent_latencies"])
            
            # Check for increasing latency trend
            first_half = recent_latencies[:len(recent_latencies)//2]
            second_half = recent_latencies[len(recent_latencies)//2:]
            
            if statistics.mean(second_half) > statistics.mean(first_half) * 1.5:
                await self._generate_optimization_suggestions(
                    model_key, 
                    "Increasing latency trend detected"
                )
    
    async def _generate_optimization_suggestions(self, model_key: str, 
                                               reason: str = None) -> None:
        """Generate optimization suggestions based on performance data"""
        
        perf_data = self.performance_data[model_key]
        suggestions = []
        
        # Low success rate suggestions
        if perf_data["success_rate"] < 0.8:
            suggestions.append({
                "type": "reliability",
                "model": model_key,
                "issue": f"Low success rate: {perf_data['success_rate']:.2f}",
                "suggestion": "Consider using fallback models more frequently",
                "priority": "high"
            })
        
        # High latency suggestions
        if perf_data["avg_latency"] > 3000:  # 3 seconds
            suggestions.append({
                "type": "performance",
                "model": model_key,
                "issue": f"High latency: {perf_data['avg_latency']:.0f}ms",
                "suggestion": "Route urgent requests to faster models",
                "priority": "medium"
            })
        
        # Error pattern analysis
        if perf_data["error_types"]:
            most_common_error = max(perf_data["error_types"].items(), key=lambda x: x[1])
            suggestions.append({
                "type": "error_pattern",
                "model": model_key,
                "issue": f"Frequent {most_common_error[0]} errors: {most_common_error[1]} occurrences",
                "suggestion": "Investigate root cause and implement error handling",
                "priority": "medium"
            })
        
        # Add suggestions to global list
        for suggestion in suggestions:
            suggestion["timestamp"] = datetime.now().isoformat()
            suggestion["reason"] = reason
            self.optimization_suggestions.append(suggestion)
        
        # Keep only recent suggestions (last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.optimization_suggestions = [
            s for s in self.optimization_suggestions
            if datetime.fromisoformat(s["timestamp"]) > cutoff_time
        ]
    
    async def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_requests": len(self.request_history),
            "models_tracked": len(self.performance_data),
            "model_performance": {},
            "optimization_suggestions": self.optimization_suggestions,
            "system_health": self._calculate_system_health()
        }
        
        # Add detailed model performance
        for model_key, perf_data in self.performance_data.items():
            report["model_performance"][model_key] = {
                "success_rate": perf_data["success_rate"],
                "avg_latency_ms": perf_data["avg_latency"],
                "total_requests": perf_data["total_requests"],
                "failures": perf_data["failures"],
                "most_common_error": max(perf_data["error_types"].items(), key=lambda x: x[1])[0] if perf_data["error_types"] else None,
                "last_success": perf_data["last_success"].isoformat() if perf_data["last_success"] else None,
                "last_failure": perf_data["last_failure"].isoformat() if perf_data["last_failure"] else None
            }
        
        return report
    
    def _calculate_system_health(self) -> Dict[str, Any]:
        """Calculate overall system health metrics"""
        
        if not self.performance_data:
            return {"status": "unknown", "score": 0}
        
        # Calculate aggregate metrics
        total_requests = sum(data["total_requests"] for data in self.performance_data.values())
        total_failures = sum(data["failures"] for data in self.performance_data.values())
        
        overall_success_rate = (total_requests - total_failures) / total_requests if total_requests > 0 else 1.0
        
        # Calculate average latency across all models
        all_latencies = []
        for data in self.performance_data.values():
            if data["recent_latencies"]:
                all_latencies.extend(data["recent_latencies"])
        
        avg_latency = statistics.mean(all_latencies) if all_latencies else 0
        
        # Calculate health score (0-100)
        success_score = overall_success_rate * 50  # 50 points max
        latency_score = max(0, 50 - (avg_latency / 100))  # 50 points max, penalize high latency
        
        health_score = success_score + latency_score
        
        # Determine status
        if health_score >= 90:
            status = "excellent"
        elif health_score >= 75:
            status = "good"
        elif health_score >= 60:
            status = "fair"
        else:
            status = "poor"
        
        return {
            "status": status,
            "score": health_score,
            "overall_success_rate": overall_success_rate,
            "average_latency_ms": avg_latency,
            "total_requests": total_requests,
            "active_models": len([k for k, v in self.performance_data.items() if v["total_requests"] > 0])
        }
    
    async def export_performance_data(self) -> str:
        """Export performance data as JSON for analysis"""
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "performance_data": {},
            "request_history": [],
            "optimization_suggestions": self.optimization_suggestions
        }
        
        # Export performance data (convert deques to lists)
        for model_key, perf_data in self.performance_data.items():
            export_data["performance_data"][model_key] = {
                "success_rate": perf_data["success_rate"],
                "avg_latency": perf_data["avg_latency"],
                "total_requests": perf_data["total_requests"],
                "failures": perf_data["failures"],
                "recent_latencies": list(perf_data["recent_latencies"]),
                "error_types": dict(perf_data["error_types"]),
                "last_success": perf_data["last_success"].isoformat() if perf_data["last_success"] else None,
                "last_failure": perf_data["last_failure"].isoformat() if perf_data["last_failure"] else None
            }
        
        # Export recent request history (last 1000 requests)
        for record in list(self.request_history)[-1000:]:
            export_record = record.copy()
            # Convert datetime objects to ISO strings
            for key in ["start_time", "end_time"]:
                if key in export_record and export_record[key]:
                    export_record[key] = export_record[key].isoformat()
            export_data["request_history"].append(export_record)
        
        return json.dumps(export_data, indent=2)