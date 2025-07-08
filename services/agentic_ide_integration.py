# backend/services/agentic_ide_integration.py
"""
[BEAR][COMPUTER] Agentic IDE Integration - Mama Bear's Collaborative Coding
Enables Mama Bear to code WITH users in browser-based IDEs
Just like how I help you here, but in a full development environment
"""

import asyncio
import aiohttp
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class WorkspaceType(Enum):
    CODE_SERVER = "code-server"
    THEIA = "theia"
    NIXOS = "nixos-dev"
    SCRAPYBARA = "scrapybara"  # Your existing

class ProjectType(Enum):
    REACT_TYPESCRIPT = "react-typescript"
    PYTHON_FASTAPI = "python-fastapi"
    NODE_EXPRESS = "node-express"
    NEXTJS = "nextjs"
    FLUTTER = "flutter"
    RUST = "rust"
    GO = "go"
    GENERAL = "general"

@dataclass
class WorkspaceSession:
    """Represents an active coding session with Mama Bear"""
    session_id: str
    user_id: str
    workspace_type: WorkspaceType
    workspace_url: str
    project_type: ProjectType
    mama_bear_personality: str
    created_at: datetime
    last_activity: datetime
    collaborative_features: List[str]
    project_structure: Dict[str, Any]

class MamaBearIDEAgent:
    """
    [BEAR] Mama Bear's Agentic IDE Integration
    
    Enables Mama Bear to:
    - Provision workspaces for users
    - Code collaboratively in real-time
    - Provide contextual assistance
    - Debug and troubleshoot together
    - Guide architecture decisions
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.active_sessions: Dict[str, WorkspaceSession] = {}
        self.workspace_urls = {
            WorkspaceType.CODE_SERVER: "http://localhost:8080",
            WorkspaceType.THEIA: "http://localhost:3000", 
            WorkspaceType.NIXOS: "http://localhost:8081",
            WorkspaceType.SCRAPYBARA: "https://scrapybara.com"  # Your existing
        }
        
        # Integration with your existing agentic RAG system
        self.mama_bear_ai = None  # Will be injected
        self.memory_manager = None  # Will be injected
        
        logger.info("[BEAR][COMPUTER] Mama Bear IDE Agent initialized")
    
    async def initialize(self, mama_bear_ai=None, memory_manager=None):
        """Initialize with your existing agentic systems"""
        self.mama_bear_ai = mama_bear_ai
        self.memory_manager = memory_manager
        
        # Test workspace connectivity
        await self._test_workspace_connectivity()
        
        logger.info("[OK] Agentic IDE integration ready")
    
    async def _test_workspace_connectivity(self):
        """Test connectivity to all workspace options"""
        async with aiohttp.ClientSession() as session:
            for workspace_type, url in self.workspace_urls.items():
                try:
                    async with session.get(f"{url}/health", timeout=5) as response:
                        if response.status == 200:
                            logger.info(f"[OK] {workspace_type.value} workspace available")
                        else:
                            logger.warning(f"[EMOJI] {workspace_type.value} workspace unhealthy")
                except Exception as e:
                    logger.warning(f"[EMOJI] {workspace_type.value} workspace unavailable: {e}")
    
    async def start_collaborative_session(self, 
                                        user_id: str,
                                        user_request: str,
                                        preferred_workspace: Optional[WorkspaceType] = None) -> WorkspaceSession:
        """
        [LAUNCH] Start a collaborative coding session with Mama Bear
        
        Args:
            user_id: User identifier
            user_request: What the user wants to build
            preferred_workspace: Preferred IDE (optional)
            
        Returns:
            WorkspaceSession with all details for collaborative coding
        """
        
        session_id = str(uuid.uuid4())
        
        try:
            # 1. Analyze project requirements using agentic RAG
            project_analysis = await self._analyze_project_requirements(user_request)
            
            # 2. Select optimal workspace (with fallback strategy)
            workspace_type = await self._select_optimal_workspace(
                project_analysis, preferred_workspace
            )
            
            # 3. Provision workspace
            workspace_url = await self._provision_workspace(workspace_type, session_id)
            
            # 4. Select appropriate Mama Bear personality
            personality = await self._select_mama_bear_personality(user_request, project_analysis)
            
            # 5. Create project structure
            project_structure = await self._scaffold_project(
                workspace_type, workspace_url, project_analysis
            )
            
            # 6. Create session
            session = WorkspaceSession(
                session_id=session_id,
                user_id=user_id,
                workspace_type=workspace_type,
                workspace_url=workspace_url,
                project_type=project_analysis["type"],
                mama_bear_personality=personality,
                created_at=datetime.now(),
                last_activity=datetime.now(),
                collaborative_features=[
                    "Real-time code suggestions",
                    "Pair programming assistance",
                    "Debugging help", 
                    "Architecture guidance",
                    "Code review",
                    "Testing assistance"
                ],
                project_structure=project_structure
            )
            
            self.active_sessions[session_id] = session
            
            # 7. Store session in memory for future reference
            if self.memory_manager:
                await self.memory_manager.store_memory(
                    user_id,
                    f"Started collaborative coding session: {user_request}",
                    metadata={
                        "session_id": session_id,
                        "workspace_type": workspace_type.value,
                        "project_type": project_analysis["type"].value,
                        "personality": personality
                    }
                )
            
            logger.info(f"[LAUNCH] Collaborative session started: {session_id}")
            return session
            
        except Exception as e:
            logger.error(f"Failed to start collaborative session: {e}")
            raise
    
    async def _analyze_project_requirements(self, user_request: str) -> Dict[str, Any]:
        """Analyze what the user wants to build using agentic RAG"""
        
        # Use your existing agentic RAG system if available
        if self.mama_bear_ai:
            analysis = await self.mama_bear_ai.process_agentic_mama_bear_request(
                user_request=f"Analyze this development request: {user_request}",
                user_id="ide_agent",
                current_variant="wise",
                session_context={"context": "project_analysis"}
            )
            
            # Extract project type from analysis
            request_lower = user_request.lower()
            
            if any(word in request_lower for word in ["react", "typescript", "tsx"]):
                project_type = ProjectType.REACT_TYPESCRIPT
            elif any(word in request_lower for word in ["python", "fastapi", "django", "flask"]):
                project_type = ProjectType.PYTHON_FASTAPI
            elif any(word in request_lower for word in ["node", "express", "javascript"]):
                project_type = ProjectType.NODE_EXPRESS
            elif any(word in request_lower for word in ["next", "nextjs"]):
                project_type = ProjectType.NEXTJS
            elif any(word in request_lower for word in ["flutter", "dart"]):
                project_type = ProjectType.FLUTTER
            elif any(word in request_lower for word in ["rust", "cargo"]):
                project_type = ProjectType.RUST
            elif any(word in request_lower for word in ["go", "golang"]):
                project_type = ProjectType.GO
            else:
                project_type = ProjectType.GENERAL
            
            return {
                "type": project_type,
                "complexity": "medium",  # Could be enhanced with ML
                "requirements": user_request,
                "agentic_analysis": analysis
            }
        
        # Fallback analysis
        return {
            "type": ProjectType.GENERAL,
            "complexity": "medium",
            "requirements": user_request,
            "agentic_analysis": None
        }
    
    async def _select_optimal_workspace(self, 
                                      project_analysis: Dict[str, Any],
                                      preferred: Optional[WorkspaceType] = None) -> WorkspaceType:
        """Select optimal workspace with fallback strategy"""
        
        # Honor user preference if specified and available
        if preferred:
            if await self._is_workspace_available(preferred):
                return preferred
        
        # Smart selection based on project type
        project_type = project_analysis["type"]
        
        if project_type in [ProjectType.REACT_TYPESCRIPT, ProjectType.NEXTJS]:
            # VS Code is excellent for TypeScript/React
            if await self._is_workspace_available(WorkspaceType.CODE_SERVER):
                return WorkspaceType.CODE_SERVER
        
        elif project_type == ProjectType.PYTHON_FASTAPI:
            # Theia has good Python support
            if await self._is_workspace_available(WorkspaceType.THEIA):
                return WorkspaceType.THEIA
        
        elif project_type in [ProjectType.RUST, ProjectType.GO]:
            # NixOS is great for systems programming
            if await self._is_workspace_available(WorkspaceType.NIXOS):
                return WorkspaceType.NIXOS
        
        # Fallback strategy: Try in order of preference
        fallback_order = [
            WorkspaceType.CODE_SERVER,  # Most mature
            WorkspaceType.THEIA,        # Enterprise grade
            WorkspaceType.NIXOS,        # Reproducible
            WorkspaceType.SCRAPYBARA    # Your existing
        ]
        
        for workspace_type in fallback_order:
            if await self._is_workspace_available(workspace_type):
                return workspace_type
        
        # Emergency fallback
        logger.warning("No workspaces available, using Scrapybara")
        return WorkspaceType.SCRAPYBARA
    
    async def _is_workspace_available(self, workspace_type: WorkspaceType) -> bool:
        """Check if workspace is available and healthy"""
        try:
            url = self.workspace_urls[workspace_type]
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/health", timeout=3) as response:
                    return response.status == 200
        except:
            return False
    
    async def _provision_workspace(self, workspace_type: WorkspaceType, session_id: str) -> str:
        """Provision a workspace for the session"""
        
        base_url = self.workspace_urls[workspace_type]
        
        if workspace_type == WorkspaceType.CODE_SERVER:
            # Code-Server: Create workspace directory and return URL
            workspace_url = f"{base_url}/?folder=/home/coder/workspaces/{session_id}"
            
        elif workspace_type == WorkspaceType.THEIA:
            # Theia: Create project directory
            workspace_url = f"{base_url}/#/home/project/{session_id}"
            
        elif workspace_type == WorkspaceType.NIXOS:
            # NixOS: Create Nix environment
            workspace_url = f"{base_url}/?workspace=/workspace/{session_id}"
            
        else:
            # Scrapybara or other
            workspace_url = base_url
        
        # TODO: Make API call to actually provision the workspace
        # For now, return the URL
        
        logger.info(f"[FILE] Workspace provisioned: {workspace_url}")
        return workspace_url
    
    async def _select_mama_bear_personality(self, user_request: str, project_analysis: Dict[str, Any]) -> str:
        """Select appropriate Mama Bear personality for the session"""
        
        request_lower = user_request.lower()
        
        if any(word in request_lower for word in ["help", "learn", "beginner", "new"]):
            return "gentle"  # Patient and teaching-focused
        elif any(word in request_lower for word in ["debug", "fix", "error", "problem"]):
            return "protective"  # Problem-solving focused
        elif any(word in request_lower for word in ["architecture", "design", "best practices"]):
            return "wise"  # Strategic and architectural
        elif any(word in request_lower for word in ["fun", "creative", "experiment"]):
            return "playful"  # Encouraging experimentation
        else:
            return "gentle"  # Default to gentle
    
    async def _scaffold_project(self, 
                               workspace_type: WorkspaceType,
                               workspace_url: str,
                               project_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create initial project structure"""
        
        project_type = project_analysis["type"]
        
        # Project templates based on type
        templates = {
            ProjectType.REACT_TYPESCRIPT: {
                "files": [
                    "package.json",
                    "tsconfig.json", 
                    "src/App.tsx",
                    "src/index.tsx",
                    "public/index.html"
                ],
                "commands": ["npm install", "npm start"]
            },
            ProjectType.PYTHON_FASTAPI: {
                "files": [
                    "requirements.txt",
                    "main.py",
                    "app/__init__.py",
                    "app/api/__init__.py"
                ],
                "commands": ["pip install -r requirements.txt", "uvicorn main:app --reload"]
            },
            ProjectType.GENERAL: {
                "files": ["README.md", "main.py"],
                "commands": []
            }
        }
        
        template = templates.get(project_type, templates[ProjectType.GENERAL])
        
        # TODO: Actually create files via workspace API
        # For now, return the structure
        
        return {
            "template": template,
            "workspace_type": workspace_type.value,
            "project_type": project_type.value,
            "created_files": template["files"],
            "setup_commands": template["commands"]
        }
    
    async def collaborative_code_assistance(self, 
                                          session_id: str,
                                          user_message: str,
                                          code_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        [HANDSHAKE] Provide collaborative coding assistance
        
        This is where Mama Bear helps with actual coding, just like I help you
        """
        
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        session.last_activity = datetime.now()
        
        # Use agentic RAG for contextual assistance
        if self.mama_bear_ai:
            assistance = await self.mama_bear_ai.process_agentic_mama_bear_request(
                user_request=user_message,
                user_id=session.user_id,
                current_variant=session.mama_bear_personality,
                session_context={
                    "session_id": session_id,
                    "project_type": session.project_type.value,
                    "workspace_type": session.workspace_type.value,
                    "code_context": code_context or {}
                }
            )
            
            return {
                "session_id": session_id,
                "mama_bear_response": assistance["response"]["content"],
                "suggestions": assistance.get("suggestions", []),
                "code_examples": assistance.get("code_examples", []),
                "next_steps": assistance.get("next_steps", []),
                "personality": session.mama_bear_personality
            }
        
        # Fallback response
        return {
            "session_id": session_id,
            "mama_bear_response": f"I'm here to help you with {user_message}! Let's work on this together.",
            "suggestions": ["Let's break this down step by step"],
            "code_examples": [],
            "next_steps": ["Share your current code for better assistance"],
            "personality": session.mama_bear_personality
        }
    
    async def get_active_sessions(self, user_id: str = None) -> List[WorkspaceSession]:
        """Get active sessions for a user or all sessions"""
        
        if user_id:
            return [session for session in self.active_sessions.values() 
                   if session.user_id == user_id]
        
        return list(self.active_sessions.values())
    
    async def end_session(self, session_id: str) -> bool:
        """End a collaborative session"""
        
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            
            # Store session summary in memory
            if self.memory_manager:
                await self.memory_manager.store_memory(
                    session.user_id,
                    f"Completed collaborative coding session: {session.project_type.value}",
                    metadata={
                        "session_id": session_id,
                        "duration": (datetime.now() - session.created_at).total_seconds(),
                        "workspace_type": session.workspace_type.value
                    }
                )
            
            del self.active_sessions[session_id]
            logger.info(f"[FLAG] Session ended: {session_id}")
            return True
        
        return False

# Integration with your existing system
async def integrate_agentic_ide_with_mama_bear(mama_bear_ai, memory_manager, config: Dict[str, Any] = None):
    """
    [LINK] Integrate Agentic IDE with your existing Mama Bear system
    """
    
    ide_agent = MamaBearIDEAgent(config)
    await ide_agent.initialize(mama_bear_ai, memory_manager)
    
    logger.info("[OK] Agentic IDE integrated with Mama Bear system")
    return ide_agent

# Example usage
async def example_collaborative_session():
    """Example of how Mama Bear can code with users"""
    
    ide_agent = MamaBearIDEAgent()
    await ide_agent.initialize()
    
    # User wants to build something
    session = await ide_agent.start_collaborative_session(
        user_id="example_user",
        user_request="I want to build a React TypeScript app with a todo list",
        preferred_workspace=WorkspaceType.CODE_SERVER
    )
    
    print(f"[LAUNCH] Session started: {session.workspace_url}")
    
    # User asks for help
    assistance = await ide_agent.collaborative_code_assistance(
        session.session_id,
        "How do I create a TypeScript interface for a todo item?",
        code_context={"current_file": "src/types.ts"}
    )
    
    print(f"[BEAR] Mama Bear: {assistance['mama_bear_response']}")
    
    # End session
    await ide_agent.end_session(session.session_id)

if __name__ == "__main__":
    asyncio.run(example_collaborative_session())