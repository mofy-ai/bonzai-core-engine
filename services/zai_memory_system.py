import json
import os
import logging
from datetime import datetime
from mem0 import Memory

logger = logging.getLogger(__name__)

class EnhancedMemoryManager:
    def __init__(self):
        """Initialize Enhanced Memory Manager with optional Mem0 integration"""
        self.memory_client = self._setup_mem0_client()
        self.conversation_memory = {}
        self.project_memory = {}
        self.task_memory = {}
        self.context_cache = {}
        self.learning_data = {}

    def _setup_mem0_client(self):
        """Initialize Mem0 client with graceful fallback"""
        try:
            import os

            # Check if we should skip Mem0 initialization
            skip_init = os.getenv('MEM0_SKIP_INITIALIZATION', 'False').lower() == 'true'
            if skip_init:
                logger.info("[LIGHTNING] Skipping Mem0 client initialization (MEM0_SKIP_INITIALIZATION=true)")
                return None

            from mem0 import MemoryClient

            # Check if API key exists in environment
            api_key = os.getenv('MEM0_API_KEY')
            if not api_key:
                logger.warning("[EMOJI] MEM0_API_KEY not found, using local memory only")
                return None

            # Set environment variable explicitly (Mem0 reads from env)
            os.environ['MEM0_API_KEY'] = api_key

            # Initialize client (no api_key parameter - reads from env)
            client = MemoryClient()

            # Test the connection with a simple request
            try:
                # Try to get users to test if API key works
                client.users()
                logger.info("[OK] Mem0 client initialized and authenticated successfully")
                return client
            except Exception as auth_error:
                logger.warning(f"[WARNING] Mem0 API authentication failed: {auth_error}")
                logger.info("[INFO] Falling back to local memory system")
                return None

        except ImportError:
            logger.warning("[EMOJI] mem0 library not available, using local memory only")
            return None
        except Exception as e:
            logger.warning(f"[EMOJI] Failed to initialize Mem0 client: {e}")
            logger.info("[INFO] Falling back to local memory system")
            return None

class EnhancedMemoryManagerDocs:
    """Documentation manager for Zai"""

    def __init__(self, mem0_client, local_storage_path):
        self.mem0_client = mem0_client
        self.local_storage_path = local_storage_path
        self.knowledge_base = {}

        # Check if we should skip initialization (for fast development)
        skip_init = os.getenv('MEM0_SKIP_INITIALIZATION', 'False').lower() == 'true'
        if skip_init:
            print("[SKIP] Skipping Mem0 documentation loading for fast development startup")
        else:
            self.load_scraped_docs()

    def load_scraped_docs(self):
        """Load scraped documentation into memory."""
        docs_file = "docs/scraped_docs.jsonl"
        if not os.path.exists(docs_file):
            print(f"Warning: {docs_file} not found. Skipping documentation loading.")
            return

        try:
            docs_loaded = 0
            with open(docs_file, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue

                    doc = json.loads(line.strip())

                    # Handle different document formats
                    if 'content' in doc:
                        if isinstance(doc['content'], str):
                            content = doc['content']
                        else:
                            content = json.dumps(doc['content'])
                    else:
                        # For local docs that have content directly
                        content = doc.get('description', '') + '\n\n' + str(doc)

                    doc_title = doc.get('title', doc.get('url', 'Unknown'))
                    doc_source = doc.get('url', 'unknown')

                    if self.mem0_client:
                        # Add to Mem0 with comprehensive metadata - fix format to use list
                        self.mem0_client.add(
                            [{"role": "system", "content": f"Scrapybara Documentation - {doc_title}: {content}"}],
                            user_id="zai_system",
                            metadata={
                                "type": "scrapybara_documentation",
                                "source": doc_source,
                                "title": doc_title,
                                "doc_type": doc.get('type', 'web_scraped'),
                                "timestamp": datetime.now().isoformat()
                            }
                        )

                    # Store in local memory as well
                    self.knowledge_base[doc_source] = {
                        'title': doc_title,
                        'content': content,
                        'type': doc.get('type', 'documentation'),
                        'metadata': doc
                    }
                    docs_loaded += 1

            print(f"Successfully loaded {docs_loaded} documentation entries from {docs_file}")
        except Exception as e:
            print(f"Error loading scraped docs: {e}")

    def get_conversation_history(self, user_id, limit=50):
        """Get conversation history for a user"""
        try:
            if self.mem0_client:
                memories = self.mem0_client.search(
                    query=f"conversation history for {user_id}",
                    user_id=user_id,
                    limit=limit
                )
                return [memory.get('memory', '') for memory in memories]
            return []
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []

    def update_user_preferences(self, user_id, preferences):
        """Update user preferences in memory"""
        try:
            if self.mem0_client:
                self.mem0_client.add(
                    [{"role": "system", "content": f"User preferences: {json.dumps(preferences)}"}],
                    user_id=user_id,
                    metadata={
                        "type": "user_preferences",
                        "timestamp": datetime.now().isoformat()
                    }
                )
        except Exception as e:
            print(f"Error updating user preferences: {e}")

    def get_user_preferences(self, user_id):
        """Get user preferences from memory"""
        try:
            if self.mem0_client:
                memories = self.mem0_client.search(
                    query="user preferences",
                    user_id=user_id,
                    limit=1
                )
                if memories:
                    return json.loads(memories[0].get('memory', '{}'))
            return {}
        except Exception as e:
            print(f"Error getting user preferences: {e}")
            return {}

class MemoryManager:
    """Real MemoryManager implementation with Mem0 integration"""

    def __init__(self, mem0_client=None):
        self.mem0_client = mem0_client or self._initialize_mem0()
        self.enhanced_manager = EnhancedMemoryManager()

    def _initialize_mem0(self):
        """Initialize Mem0 client with API key"""
        try:
            from mem0 import MemoryClient
            import os
            api_key = os.getenv('MEM0_API_KEY')
            if api_key:
                return MemoryClient(api_key=api_key)
            else:
                print("Warning: MEM0_API_KEY not found, using local memory only")
                return None
        except ImportError:
            print("Warning: mem0 library not available, using local memory only")
            return None
        except Exception as e:
            print(f"Error initializing Mem0: {e}")
            return None

    def save_conversation(self, user_id: str, conversation: dict) -> str:
        """Save conversation with persistent memory"""
        try:
            conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"

            if self.mem0_client:
                # Save to Mem0 - fix format to use list
                self.mem0_client.add(
                    [{"role": "system", "content": f"Conversation: {json.dumps(conversation)}"}],
                    user_id=user_id,
                    metadata={
                        "type": "conversation",
                        "conversation_id": conversation_id,
                        "timestamp": datetime.now().isoformat(),
                        "model": conversation.get('model'),
                        "zai_variant": conversation.get('zai_variant')
                    }
                )

            return conversation_id
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def get_conversation_history(self, user_id: str, limit: int = 50) -> list:
        """Retrieve conversation history"""
        return self.enhanced_manager.get_conversation_history(user_id, limit)

    def update_user_preferences(self, user_id: str, preferences: dict):
        """Update user preferences with Mem0"""
        self.enhanced_manager.update_user_preferences(user_id, preferences)

    def get_user_preferences(self, user_id: str) -> dict:
        """Get user preferences"""
        return self.enhanced_manager.get_user_preferences(user_id)

    def search_memories(self, user_id: str, query: str) -> list:
        """Semantic search through memories"""
        try:
            if self.mem0_client:
                memories = self.mem0_client.search(
                    query=query,
                    user_id=user_id,
                    limit=10
                )
                return memories
            return []
        except Exception as e:
            print(f"Error searching memories: {e}")
            return []

    def update_relationship(self, user_id: str, variant: str, interaction_data: dict):
        """Update Zai relationship data"""
        try:
            if self.mem0_client:
                self.mem0_client.add(
                    [{"role": "system", "content": f"Zai {variant} interaction: {json.dumps(interaction_data)}"}],
                    user_id=user_id,
                    metadata={
                        "type": "zai_relationship",
                        "variant": variant,
                        "timestamp": datetime.now().isoformat(),
                        "helpful": interaction_data.get('helpful', True)
                    }
                )
        except Exception as e:
            print(f"Error updating relationship: {e}")

def initialize_enhanced_memory(mem0_client=None):
    return EnhancedMemoryManager(mem0_client, './zai_memory')

def initialize_memory_manager():
    """Initialize the main MemoryManager"""
    return MemoryManager()
