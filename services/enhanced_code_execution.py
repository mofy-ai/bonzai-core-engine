# Enhanced Mama Bear Code Execution with E2B Integration
import asyncio
from typing import Dict, Any, Optional, List
import logging
from e2b_code_interpreter import Sandbox
import os
from dataclasses import dataclass

@dataclass
class CodeExecutionResult:
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float = 0.0
    logs: Optional[List[str]] = None

class EnhancedMamaBearCodeExecution:
    """[BEAR] Enhanced Mama Bear Code Execution with E2B Secure Sandboxing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # E2B API key should be set in environment
        self.api_key = os.getenv('E2B_API_KEY')
        if not self.api_key:
            self.logger.warning("E2B_API_KEY not found, code execution will be limited")
        
        # Track execution sessions for better performance
        self.active_sessions = {}
        
    async def execute_code_safely(self, 
                                code: str, 
                                user_id: str, 
                                language: str = "python",
                                timeout: int = 30) -> CodeExecutionResult:
        """
        Execute code in a secure E2B sandbox with enhanced Mama Bear features
        """
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Get or create sandbox session for user
            sandbox = await self._get_or_create_sandbox(user_id, language)
            
            # Execute the code with E2B v1.5+ API
            try:
                execution = sandbox.run_code(code)
                # Use asyncio.wait_for on the execution result, not the execution object
                result = await asyncio.wait_for(execution.wait(), timeout=timeout)
                
                execution_time = asyncio.get_event_loop().time() - start_time
                
                return CodeExecutionResult(
                    success=True,
                    output=result.text if hasattr(result, 'text') else str(result),
                    execution_time=execution_time,
                    logs=result.logs if hasattr(result, 'logs') else []
                )
            except asyncio.TimeoutError:
                return CodeExecutionResult(
                    success=False,
                    output="",
                    error=f"Code execution timed out after {timeout} seconds",
                    execution_time=timeout
                )
        except Exception as e:
            self.logger.error(f"Code execution failed for user {user_id}: {str(e)}")
            return CodeExecutionResult(
                success=False,
                output="",
                error=str(e),
                execution_time=asyncio.get_event_loop().time() - start_time
            )
    
    async def _get_or_create_sandbox(self, user_id: str, language: str) -> Sandbox:
        """Get existing sandbox or create new one for user session"""
        session_key = f"{user_id}_{language}"
        
        if session_key not in self.active_sessions:
            try:
                # Create new E2B sandbox using v1.5+ API
                sandbox = await Sandbox.create(
                    template="python",  # or "node", "bash", etc.
                    api_key=self.api_key
                )
                # No need to call start() in v1.5+, sandbox is ready after create()
                self.active_sessions[session_key] = sandbox
                self.logger.info(f"Created new E2B sandbox for session {session_key}")
                
            except Exception as e:
                self.logger.error(f"Failed to create E2B sandbox: {str(e)}")
                raise e
        
        return self.active_sessions[session_key]
    
    async def cleanup_session(self, user_id: str, language: str = "python"):
        """Clean up sandbox session for user"""
        session_key = f"{user_id}_{language}"
        
        if session_key in self.active_sessions:
            try:
                await self.active_sessions[session_key].close()
                del self.active_sessions[session_key]
                self.logger.info(f"Cleaned up session {session_key}")
            except Exception as e:
                self.logger.error(f"Error cleaning up session {session_key}: {str(e)}")
    
    async def install_packages(self, 
                             user_id: str, 
                             packages: List[str],
                             language: str = "python") -> CodeExecutionResult:
        """Install packages in the sandbox environment"""
        try:
            sandbox = await self._get_or_create_sandbox(user_id, language)
            
            if language == "python":
                install_code = f"import subprocess\nsubprocess.run(['pip', 'install'] + {packages}, check=True)"
            elif language == "node":
                install_code = f"const {{ exec }} = require('child_process'); exec('npm install {' '.join(packages)}')"
            else:
                return CodeExecutionResult(
                    success=False,
                    output="",
                    error=f"Package installation not supported for language: {language}"
                )
            
            return await self.execute_code_safely(install_code, user_id, language, timeout=60)
            
        except Exception as e:
            return CodeExecutionResult(
                success=False,
                output="",
                error=f"Package installation failed: {str(e)}"
            )
    
    async def get_session_info(self, user_id: str, language: str = "python") -> Dict[str, Any]:
        """Get information about active session"""
        session_key = f"{user_id}_{language}"
        
        if session_key not in self.active_sessions:
            return {"active": False, "session_key": session_key}
        
        sandbox = self.active_sessions[session_key]
        
        try:
            # Get basic session info
            return {
                "active": True,
                "session_key": session_key,
                "language": language,
                "sandbox_id": getattr(sandbox, 'id', 'unknown'),
                "created_at": getattr(sandbox, 'created_at', 'unknown')
            }
        except Exception as e:
            self.logger.error(f"Error getting session info: {str(e)}")
            return {"active": False, "error": str(e)}
    
    async def cleanup_all_sessions(self):
        """Clean up all active sessions"""
        for session_key in list(self.active_sessions.keys()):
            try:
                await self.active_sessions[session_key].close()
                del self.active_sessions[session_key]
                self.logger.info(f"Cleaned up session {session_key}")
            except Exception as e:
                self.logger.error(f"Error cleaning up session {session_key}: {str(e)}")

# Global instance for the application
mama_bear_code_executor = EnhancedMamaBearCodeExecution()