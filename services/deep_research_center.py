"""
[BUILDING] Deep Research Center - Collaborative AI Research System
Combines Claude 3.5 models with Gemini Deep Research for mind-blowing collaborative research
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum
import json
import anthropic
import google.generativeai as genai

logger = logging.getLogger(__name__)

class ResearchMode(Enum):
    CLAUDE_ONLY = "claude_only"
    GEMINI_ONLY = "gemini_only"
    COLLABORATIVE = "collaborative"
    CONSENSUS = "consensus"
    DEBATE = "debate"

class ResearchDepth(Enum):
    QUICK = "quick"  # 5-10 minutes
    STANDARD = "standard"  # 15-30 minutes
    DEEP = "deep"  # 30-60 minutes
    EXHAUSTIVE = "exhaustive"  # 1-2 hours

class DeepResearchCenter:
    """
    [BUILDING] The Library - A collaborative deep research center
    Where Claude and Gemini work together to produce extraordinary research
    """
    
    def __init__(self, anthropic_api_key: str, gemini_api_key: str):
        # Initialize Claude models
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.claude_models = {
            "opus": "claude-3-opus-20240229",      # Most capable, best for complex research
            "sonnet": "claude-3-5-sonnet-20241022", # Balanced, great for most research
            "haiku": "claude-3-haiku-20240307"     # Fast, good for quick lookups
        }
        
        # Initialize Gemini with Deep Research
        genai.configure(api_key=gemini_api_key)
        self.gemini_models = {
            "deep_research": "gemini-1.5-pro",  # Has Deep Research capability
            "deep_think": "gemini-1.5-pro",     # Enhanced reasoning
            "fast": "gemini-1.5-flash"          # Quick responses
        }
        
        # Research session storage
        self.active_sessions = {}
        
        logger.info("[BUILDING] Deep Research Center initialized with Claude & Gemini models")
    
    async def start_research_session(
        self, 
        query: str, 
        mode: ResearchMode, 
        depth: ResearchDepth,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Start a new research session"""
        if not session_id:
            session_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = {
            "id": session_id,
            "query": query,
            "mode": mode.value,
            "depth": depth.value,
            "started_at": datetime.now().isoformat(),
            "status": "active",
            "results": [],
            "metadata": {
                "estimated_duration": self._get_estimated_duration(depth),
                "models_used": self._get_models_for_mode(mode)
            }
        }
        
        self.active_sessions[session_id] = session
        logger.info(f"[BUILDING] Started research session {session_id} in {mode.value} mode")
        
        # Start the research process
        try:
            if mode == ResearchMode.CLAUDE_ONLY:
                result = await self._claude_research(query, depth)
            elif mode == ResearchMode.GEMINI_ONLY:
                result = await self._gemini_research(query, depth)
            elif mode == ResearchMode.COLLABORATIVE:
                result = await self._collaborative_research(query, depth)
            elif mode == ResearchMode.CONSENSUS:
                result = await self._consensus_research(query, depth)
            elif mode == ResearchMode.DEBATE:
                result = await self._debate_research(query, depth)
            
            session["results"].append(result)
            session["status"] = "completed"
            session["completed_at"] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Research session {session_id} failed: {e}")
            session["status"] = "failed"
            session["error"] = str(e)
            session["failed_at"] = datetime.now().isoformat()
        
        return session
    
    async def _claude_research(self, query: str, depth: ResearchDepth) -> Dict[str, Any]:
        """Pure Claude research"""
        model = self._select_claude_model(depth)
        
        # Craft research prompt based on depth
        system_prompt = self._get_claude_research_prompt(depth)
        
        try:
            response = await asyncio.to_thread(
                self.anthropic_client.messages.create,
                model=model,
                max_tokens=4000,
                system=system_prompt,
                messages=[{"role": "user", "content": query}]
            )
            
            return {
                "type": "claude_research",
                "model": model,
                "content": response.content[0].text,
                "timestamp": datetime.now().isoformat(),
                "token_usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
        except Exception as e:
            logger.error(f"Claude research failed: {e}")
            raise
    
    async def _gemini_research(self, query: str, depth: ResearchDepth) -> Dict[str, Any]:
        """Pure Gemini research with Deep Research capability"""
        model_name = self._select_gemini_model(depth)
        
        try:
            # Use Gemini's deep research capabilities
            model = genai.GenerativeModel(model_name)
            
            # Enhanced prompt for deep research
            research_prompt = self._get_gemini_research_prompt(query, depth)
            
            response = await asyncio.to_thread(
                model.generate_content,
                research_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=4000,
                    temperature=0.3
                )
            )
            
            return {
                "type": "gemini_research", 
                "model": model_name,
                "content": response.text,
                "timestamp": datetime.now().isoformat(),
                "safety_ratings": [
                    {"category": rating.category.name, "probability": rating.probability.name}
                    for rating in response.candidates[0].safety_ratings
                ] if response.candidates else []
            }
        except Exception as e:
            logger.error(f"Gemini research failed: {e}")
            raise
    
    async def _collaborative_research(self, query: str, depth: ResearchDepth) -> Dict[str, Any]:
        """Collaborative research - Claude and Gemini work together"""
        logger.info("[HANDSHAKE] Starting collaborative research...")
        
        # Phase 1: Initial research by both models
        claude_task = self._claude_research(query, depth)
        gemini_task = self._gemini_research(query, depth)
        
        claude_result, gemini_result = await asyncio.gather(claude_task, gemini_task)
        
        # Phase 2: Cross-pollination - each model reviews the other's work
        synthesis_prompt = f"""
        Research Query: {query}
        
        Claude's Research:
        {claude_result['content']}
        
        Gemini's Research:
        {gemini_result['content']}
        
        Please synthesize these two research approaches into a comprehensive, unified analysis.
        Identify complementary insights, resolve any contradictions, and create a more complete picture.
        """
        
        # Get synthesis from both models
        claude_synthesis = await self._claude_research(synthesis_prompt, ResearchDepth.STANDARD)
        gemini_synthesis = await self._gemini_research(synthesis_prompt, ResearchDepth.STANDARD)
        
        return {
            "type": "collaborative_research",
            "phases": {
                "initial_research": {
                    "claude": claude_result,
                    "gemini": gemini_result
                },
                "synthesis": {
                    "claude_synthesis": claude_synthesis,
                    "gemini_synthesis": gemini_synthesis
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    
    async def _consensus_research(self, query: str, depth: ResearchDepth) -> Dict[str, Any]:
        """Consensus research - models work toward agreement"""
        logger.info("[HANDSHAKE] Starting consensus research...")
        
        # Initial positions
        claude_result = await self._claude_research(query, depth)
        gemini_result = await self._gemini_research(query, depth)
        
        # Consensus building rounds
        consensus_rounds = []
        current_claude = claude_result['content']
        current_gemini = gemini_result['content']
        
        for round_num in range(3):  # Max 3 consensus rounds
            # Claude reviews Gemini's position
            claude_consensus_prompt = f"""
            Original query: {query}
            
            Your initial position: {current_claude}
            
            Gemini's position: {current_gemini}
            
            Please refine your position considering Gemini's insights. Focus on finding common ground 
            while maintaining accuracy. What aspects can you agree on? Where might you need to adjust your view?
            """
            
            # Gemini reviews Claude's position  
            gemini_consensus_prompt = f"""
            Original query: {query}
            
            Your initial position: {current_gemini}
            
            Claude's position: {current_claude}
            
            Please refine your position considering Claude's insights. Focus on finding common ground
            while maintaining accuracy. What aspects can you agree on? Where might you need to adjust your view?
            """
            
            claude_refined = await self._claude_research(claude_consensus_prompt, ResearchDepth.QUICK)
            gemini_refined = await self._gemini_research(gemini_consensus_prompt, ResearchDepth.QUICK)
            
            consensus_rounds.append({
                "round": round_num + 1,
                "claude_refined": claude_refined,
                "gemini_refined": gemini_refined
            })
            
            current_claude = claude_refined['content']
            current_gemini = gemini_refined['content']
        
        return {
            "type": "consensus_research",
            "initial_positions": {
                "claude": claude_result,
                "gemini": gemini_result  
            },
            "consensus_rounds": consensus_rounds,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _debate_research(self, query: str, depth: ResearchDepth) -> Dict[str, Any]:
        """Debate research - models argue different positions"""
        logger.info("[SWORD] Starting debate research...")
        
        # Assign debate positions
        claude_position_prompt = f"""
        Research query: {query}
        
        You are participating in an academic debate. Please take a position on this query and argue for it
        with evidence and reasoning. Be thorough but also be prepared to defend your position against counterarguments.
        Focus on {depth.value} level analysis.
        """
        
        gemini_position_prompt = f"""
        Research query: {query}
        
        You are participating in an academic debate. Please take a position on this query, specifically looking
        for angles that might differ from or challenge conventional wisdom. Argue your position with evidence
        and reasoning. Focus on {depth.value} level analysis.
        """
        
        # Initial positions
        claude_position = await self._claude_research(claude_position_prompt, depth)
        gemini_position = await self._gemini_research(gemini_position_prompt, depth)
        
        # Debate rounds
        debate_rounds = []
        
        for round_num in range(2):  # 2 rounds of rebuttals
            # Claude's rebuttal to Gemini
            claude_rebuttal_prompt = f"""
            Debate topic: {query}
            
            Your position: {claude_position['content']}
            
            Opponent's position: {gemini_position['content']}
            
            Please provide a respectful but strong rebuttal to your opponent's position. 
            Point out weaknesses in their argument while reinforcing your own position with additional evidence.
            """
            
            # Gemini's rebuttal to Claude
            gemini_rebuttal_prompt = f"""
            Debate topic: {query}
            
            Your position: {gemini_position['content']}
            
            Opponent's position: {claude_position['content']}
            
            Please provide a respectful but strong rebuttal to your opponent's position.
            Point out weaknesses in their argument while reinforcing your own position with additional evidence.
            """
            
            claude_rebuttal = await self._claude_research(claude_rebuttal_prompt, ResearchDepth.STANDARD)
            gemini_rebuttal = await self._gemini_research(gemini_rebuttal_prompt, ResearchDepth.STANDARD)
            
            debate_rounds.append({
                "round": round_num + 1,
                "claude_rebuttal": claude_rebuttal,
                "gemini_rebuttal": gemini_rebuttal
            })
        
        # Final synthesis - neutral perspective
        synthesis_prompt = f"""
        Debate topic: {query}
        
        Claude's position: {claude_position['content']}
        Gemini's position: {gemini_position['content']}
        
        Debate exchanges have occurred. As a neutral observer, please synthesize the strongest points
        from both sides and provide a balanced analysis of the topic that acknowledges the merits
        of different perspectives.
        """
        
        final_synthesis = await self._claude_research(synthesis_prompt, ResearchDepth.STANDARD)
        
        return {
            "type": "debate_research",
            "initial_positions": {
                "claude": claude_position,
                "gemini": gemini_position
            },
            "debate_rounds": debate_rounds,
            "final_synthesis": final_synthesis,
            "timestamp": datetime.now().isoformat()
        }
    
    def _select_claude_model(self, depth: ResearchDepth) -> str:
        """Select appropriate Claude model based on research depth"""
        if depth == ResearchDepth.EXHAUSTIVE:
            return self.claude_models["opus"]
        elif depth in [ResearchDepth.DEEP, ResearchDepth.STANDARD]:
            return self.claude_models["sonnet"]
        else:
            return self.claude_models["haiku"]
    
    def _select_gemini_model(self, depth: ResearchDepth) -> str:
        """Select appropriate Gemini model based on research depth"""
        if depth in [ResearchDepth.EXHAUSTIVE, ResearchDepth.DEEP]:
            return self.gemini_models["deep_research"]
        elif depth == ResearchDepth.STANDARD:
            return self.gemini_models["deep_think"]
        else:
            return self.gemini_models["fast"]
    
    def _get_claude_research_prompt(self, depth: ResearchDepth) -> str:
        """Get Claude research system prompt based on depth"""
        base_prompt = """You are a world-class researcher with access to vast knowledge. 
        Your task is to provide comprehensive, accurate, and insightful research."""
        
        depth_instructions = {
            ResearchDepth.QUICK: "Provide a focused, concise analysis hitting the key points.",
            ResearchDepth.STANDARD: "Provide a thorough analysis with multiple perspectives and evidence.",
            ResearchDepth.DEEP: "Provide an extensive analysis with deep insights, multiple sources, and nuanced understanding.",
            ResearchDepth.EXHAUSTIVE: "Provide the most comprehensive analysis possible, exploring all angles, implications, and expert perspectives."
        }
        
        return f"{base_prompt}\n\n{depth_instructions[depth]}"
    
    def _get_gemini_research_prompt(self, query: str, depth: ResearchDepth) -> str:
        """Get Gemini research prompt with deep research instructions"""
        depth_instructions = {
            ResearchDepth.QUICK: "Provide a focused analysis with key insights.",
            ResearchDepth.STANDARD: "Conduct thorough research with multiple angles and evidence.",
            ResearchDepth.DEEP: "Perform deep research with comprehensive analysis and expert-level insights.",
            ResearchDepth.EXHAUSTIVE: "Conduct exhaustive research exploring every angle, implication, and expert perspective."
        }
        
        return f"""
        Research Query: {query}
        
        Instructions: {depth_instructions[depth]}
        
        Please provide a comprehensive research response that leverages your deep research capabilities.
        Include multiple perspectives, evidence-based analysis, and actionable insights.
        """
    
    def _get_estimated_duration(self, depth: ResearchDepth) -> str:
        """Get estimated duration for research depth"""
        durations = {
            ResearchDepth.QUICK: "5-10 minutes",
            ResearchDepth.STANDARD: "15-30 minutes", 
            ResearchDepth.DEEP: "30-60 minutes",
            ResearchDepth.EXHAUSTIVE: "1-2 hours"
        }
        return durations[depth]
    
    def _get_models_for_mode(self, mode: ResearchMode) -> List[str]:
        """Get list of models used for research mode"""
        if mode == ResearchMode.CLAUDE_ONLY:
            return ["claude-3.5-sonnet"]
        elif mode == ResearchMode.GEMINI_ONLY:
            return ["gemini-1.5-pro"]
        else:
            return ["claude-3.5-sonnet", "gemini-1.5-pro"]
    
    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a research session"""
        return self.active_sessions.get(session_id)
    
    def list_active_sessions(self) -> List[Dict[str, Any]]:
        """List all active research sessions"""
        return list(self.active_sessions.values())
    
    def cancel_session(self, session_id: str) -> bool:
        """Cancel an active research session"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]["status"] = "cancelled"
            self.active_sessions[session_id]["cancelled_at"] = datetime.now().isoformat()
            return True
        return False


class LibrarySection:
    """
    [BUILDING] Library Section - Wrapper for the Deep Research Center
    Provides the main interface for the Podplay Sanctuary
    """
    
    def __init__(self, anthropic_api_key: str, gemini_api_key: str):
        self.research_center = DeepResearchCenter(anthropic_api_key, gemini_api_key)
        self.initialized_at = datetime.now()
        logger.info("[BUILDING] Library Section initialized and ready for research")
    
    async def conduct_research(
        self, 
        query: str, 
        mode: str = "collaborative", 
        depth: str = "standard",
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Main research interface"""
        try:
            research_mode = ResearchMode(mode)
            research_depth = ResearchDepth(depth)
            
            return await self.research_center.start_research_session(
                query, research_mode, research_depth, session_id
            )
        except ValueError as e:
            logger.error(f"Invalid research parameters: {e}")
            raise ValueError(f"Invalid research parameters: {e}")
    
    def get_available_modes(self) -> List[Dict[str, str]]:
        """Get list of available research modes"""
        return [
            {"value": mode.value, "name": mode.value.replace("_", " ").title()}
            for mode in ResearchMode
        ]
    
    def get_available_depths(self) -> List[Dict[str, str]]:
        """Get list of available research depths"""
        return [
            {"value": depth.value, "name": depth.value.title()}
            for depth in ResearchDepth
        ]
    
    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get research session status"""
        return self.research_center.get_session_status(session_id)
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all research sessions"""
        return self.research_center.list_active_sessions()
