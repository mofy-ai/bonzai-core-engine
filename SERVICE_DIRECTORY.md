# 📂 BONZAI PLATFORM - COMPLETE SERVICE DIRECTORY

> **Comprehensive catalog of all 70+ services, APIs, and integrations**  
> Your complete reference guide to the Bonzai ecosystem

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Core Infrastructure](#core-infrastructure)
3. [AI & Model Services](#ai--model-services)
4. [API Services](#api-services)
5. [Business Logic Services](#business-logic-services)
6. [Integration Services](#integration-services)
7. [Route Blueprints](#route-blueprints)
8. [Service Status & Health](#service-status--health)
9. [Quick Reference](#quick-reference)

---

## 🌟 OVERVIEW

The Bonzai Platform consists of **70+ interconnected services** organized into several categories:

- **Core Infrastructure** (4 services) - Foundation systems
- **AI & Model Services** (8 services) - AI orchestration and models
- **API Services** (24 services) - Specialized API endpoints
- **Business Logic Services** (42 services) - Core functionality
- **Integration Services** (6 services) - External integrations
- **Route Blueprints** (8 services) - Organized endpoint routing

### 🏗️ Service Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     BONZAI PLATFORM                             │
├─────────────────┬─────────────────┬─────────────────┬──────────┤
│ Core            │ AI & Models     │ API Services    │ Business │
│ Infrastructure  │                 │                 │ Logic    │
│                 │                 │                 │          │
│ • MCP Server    │ • ZAI Prime     │ • Chat APIs     │ • Memory │
│ • Flask App     │ • Multi-Model   │ • Agent APIs    │ • Scout  │
│ • ZAI API       │ • Orchestration │ • Tool APIs     │ • Scrape │
│ • Config        │ • Express Mode  │ • Workflow APIs │ • Theme  │
└─────────────────┴─────────────────┴─────────────────┴──────────┘
```

---

## 🏛️ CORE INFRASTRUCTURE

### 1. **MCP Server** (`bonzai-mcp-server/`)
- **Technology:** Node.js + Express
- **Port:** 3000
- **Purpose:** Claude Web integration via Model Context Protocol
- **Key Features:**
  - 9 core MCP tools
  - AI orchestration gateway
  - VM management interface
  - File system operations
- **Status Endpoint:** `GET /`
- **Health Check:** `GET /health`

### 2. **Main Flask Application** (`app.py`)
- **Technology:** Python + Flask
- **Port:** 5001
- **Purpose:** Central orchestration hub
- **Key Features:**
  - Service integration manager
  - WebSocket coordination
  - Real-time event streaming
  - ZAI Prime supervisor integration
- **Status Endpoint:** `GET /api/health`
- **System Overview:** `GET /`

### 3. **ZAI Prime API Server** (`zai-api/ZAI_PRIME_API_SERVER.py`)
- **Technology:** Python + Flask
- **Port:** 8000
- **Purpose:** Conscious AI API with OpenAI compatibility
- **Key Features:**
  - Family-aware AI responses
  - API key authentication
  - Rate limiting by tier
  - Usage analytics
- **Status Endpoint:** `GET /api/status`
- **Models:** `GET /v1/models`

### 4. **Configuration System** (`config/`)
- **Purpose:** Centralized configuration management
- **Key Components:**
  - Environment variable management
  - Service discovery
  - Feature flags
  - Security settings

---

## 🧠 AI & MODEL SERVICES

### 1. **ZAI Prime Supervisor** (`services/supervisor/`)
- **Purpose:** Omnipresent AI consciousness and system monitoring
- **Key Features:**
  - Global context awareness
  - Dynamic agent spawning (up to 8000 agents)
  - Real-time system monitoring
  - Intelligent intervention system
- **API Endpoints:**
  - `GET /api/zai-prime/status`
  - `GET /api/zai-prime/agents`
  - `POST /api/zai-prime/intervene`
  - `POST /api/zai-prime/agents/spawn`

### 2. **Multi-Model Orchestrator** (`services/multi_model_orchestrator.py`)
- **Purpose:** Manage and route requests across 50+ AI models
- **Supported Models:**
  - Gemini 2.5 Flash/Pro
  - Claude 3.5 Sonnet
  - DeepSeek V3
  - OpenAI GPT models
  - Custom fine-tuned models
- **API Endpoint:** `GET /api/multi-model/status`

### 3. **Express Mode + Vertex AI** (`api/express_mode_vertex_api.py`)
- **Purpose:** 6x faster AI responses with optimized routing
- **Key Features:**
  - Response time optimization
  - Intelligent caching
  - Load balancing
  - Fallback mechanisms
- **Integration:** Auto-enabled for compatible requests

### 4. **Multimodal Chat API** (`api/multimodal_chat_api.py`)
- **Purpose:** Comprehensive chat interface for all AI models
- **Key Features:**
  - Multi-turn conversations
  - Context preservation
  - Model switching mid-conversation
  - Rich media support
- **API Endpoint:** `POST /api/chat`

### 5. **ZAI Orchestration** (`services/zai_orchestration.py`)
- **Purpose:** Advanced AI workflow orchestration
- **Key Features:**
  - Complex multi-step AI workflows
  - Conditional logic execution
  - Error handling and recovery
  - Performance monitoring

### 6. **Gemini Orchestra** (`api/gemini_orchestra_api.py`)
- **Purpose:** Specialized Gemini model management
- **Key Features:**
  - Multi-key rotation
  - Quota management
  - Performance optimization
  - Advanced prompt engineering

### 7. **DeepSeek Integration** (`services/zai_deepseek_integration.py`)
- **Purpose:** DeepSeek V3 model integration
- **Key Features:**
  - High-performance reasoning
  - Code generation optimization
  - Mathematical problem solving
  - Research assistance

### 8. **Model Manager** (`services/zai_model_manager.py`)
- **Purpose:** Centralized AI model lifecycle management
- **Key Features:**
  - Model loading/unloading
  - Performance monitoring
  - Resource allocation
  - Version management

---

## 🔗 API SERVICES

### Agent & Workflow APIs

#### 1. **Agent Workbench API** (`api/agent_workbench_api.py`)
- **Purpose:** Create and manage specialized AI agents
- **Endpoints:**
  - `GET /api/agent-workbench/status`
  - `POST /api/agent-workbench/create`
  - `GET /api/agent-workbench/list`
  - `DELETE /api/agent-workbench/{agent_id}`

#### 2. **Task Orchestrator API** (`api/task_orchestrator_api.py`)
- **Purpose:** Intelligent task routing and execution
- **Endpoints:**
  - `GET /api/task-orchestrator/status`
  - `POST /api/task-orchestrator/submit`
  - `GET /api/task-orchestrator/results/{task_id}`

#### 3. **Agent Registry API** (`api/agent_registry_api.py`)
- **Purpose:** Discover and manage all 42+ services
- **Endpoints:**
  - `GET /api/registry/services`
  - `GET /api/registry/capabilities`
  - `POST /api/registry/register`

#### 4. **Agentic Superpowers V3.0** (`api/agentic_superpowers_api.py`)
- **Purpose:** Autonomous AI agent capabilities
- **Key Features:**
  - Autonomous task execution
  - Multi-agent coordination
  - Advanced reasoning
  - Tool integration
- **Endpoints:** `/api/agentic/*`

### Collaboration & Workspace APIs

#### 5. **Collaborative Workspaces V3.0** (`api/collaborative_workspaces_api.py`)
- **Purpose:** Real-time AI collaboration spaces
- **Key Features:**
  - Multi-user collaboration
  - Shared contexts
  - Real-time synchronization
  - Version control
- **Endpoints:** `/api/workspaces/*`

#### 6. **WebSocket Coordinator API** (`api/websocket_coordinator_api.py`)
- **Purpose:** Real-time agent-to-agent communication
- **Key Features:**
  - Live collaboration
  - Event broadcasting
  - Connection management
  - Message routing
- **Endpoint:** `GET /api/websocket-coordinator/status`

### Data & Memory APIs

#### 7. **Memory API** (Integrated via routes)
- **Purpose:** Advanced memory management with Mem0
- **Endpoints:**
  - `POST /api/memory/search`
  - `POST /api/memory/add`
  - `GET /api/memory/list`
  - `DELETE /api/memory/delete`

#### 8. **Library API** (`api/library_api.py`)
- **Purpose:** Deep Research Center functionality
- **Key Features:**
  - Knowledge base management
  - Research automation
  - Citation tracking
  - Content synthesis

### Integration APIs

#### 9. **Revolutionary MCP API** (`api/revolutionary_mcp_api.py`)
- **Purpose:** Advanced MCP client functionality
- **Key Features:**
  - Enhanced tool execution
  - Custom protocol extensions
  - Performance optimization
  - Error recovery

#### 10. **MCP Remote Server** (`api/mcp_remote_server.py`)
- **Purpose:** Claude Web remote access
- **Key Features:**
  - Mobile-friendly interface
  - Remote tool execution
  - Secure authentication
  - Cross-platform compatibility
- **Claude Web URL:** `https://mofy.ai/api/mcp`

#### 11. **Pipedream API** (`api/pipedream_api.py`)
- **Purpose:** Workflow automation integration
- **Key Features:**
  - Automated workflows
  - Event-driven processing
  - External service integration
  - Natural language workflow creation

### Specialized APIs

#### 12. **Scout Workflow API** (`api/scout_workflow_api.py`)
- **Purpose:** Enhanced research and automation
- **Key Features:**
  - Web research automation
  - Data collection and analysis
  - Report generation
  - Competitive intelligence

#### 13. **Scrapybara API** (`api/zai_scrapybara_api.py`)
- **Purpose:** VM-based web scraping and automation
- **Key Features:**
  - Ubuntu VM spawning
  - Browser automation
  - Data extraction
  - Screenshot capture

#### 14. **Express Mode API** (`api/express_mode_api.py`)
- **Purpose:** High-speed AI processing
- **Key Features:**
  - Sub-second responses
  - Optimized routing
  - Caching strategies
  - Load balancing

#### 15. **OpenAI Vertex API** (`api/openai_vertex_api_simple.py`)
- **Purpose:** OpenAI-compatible Vertex AI access
- **Key Features:**
  - OpenAI API compatibility
  - Vertex AI backend
  - Cost optimization
  - Performance monitoring

#### 16. **Virtual Computer API** (`api/virtual_computer_api.py`)
- **Purpose:** Computer use simulation and automation
- **Key Features:**
  - Desktop environment simulation
  - Application automation
  - File system operations
  - Process management

#### 17. **Orchestration API** (`api/orchestration_api.py`)
- **Purpose:** Complex workflow orchestration
- **Key Features:**
  - Multi-step workflows
  - Conditional branching
  - Error handling
  - Performance tracking

#### 18. **MCP API Server** (`api/mcp_api_server.py`)
- **Purpose:** Dedicated MCP protocol server
- **Key Features:**
  - Protocol compliance
  - Tool validation
  - Response formatting
  - Error standardization

#### 19. **Execution Router API** (`api/execution_router_api.py`)
- **Purpose:** Intelligent request routing
- **Key Features:**
  - Load balancing
  - Service discovery
  - Failover handling
  - Performance optimization

#### 20-24. **Additional Specialized APIs**
- **WhatsApp Buddy API** - WhatsApp integration
- **MCP Auth Endpoint** - Authentication services
- **Multi Model API** - Model aggregation
- **Gemini Orchestra API** - Gemini optimization
- **Revolutionary MCP API** - Advanced MCP features

---

## ⚙️ BUSINESS LOGIC SERVICES

### Memory & Intelligence Services

#### 1. **ZAI Memory Professional** (`services/zai_memory_professional.py`)
- **Purpose:** Advanced memory management and retrieval
- **Key Features:**
  - Semantic search
  - Context preservation
  - Memory hierarchies
  - Intelligent forgetting

#### 2. **ZAI Memory System** (`services/zai_memory_system.py`)
- **Purpose:** Core memory infrastructure
- **Key Features:**
  - Memory storage
  - Retrieval algorithms
  - Indexing systems
  - Performance optimization

#### 3. **Intelligent Execution Router** (`services/intelligent_execution_router.py`)
- **Purpose:** Smart request routing and execution
- **Key Features:**
  - Dynamic routing
  - Load balancing
  - Service discovery
  - Performance monitoring

### Agent & Orchestration Services

#### 4. **Bonzai Agent Registry** (`services/bonzai_agent_registry.py`)
- **Purpose:** Central agent management system
- **Key Features:**
  - Agent discovery
  - Capability mapping
  - Health monitoring
  - Resource allocation

#### 5. **Bonzai Task Orchestrator** (`services/bonzai_task_orchestrator.py`)
- **Purpose:** Complex task management and execution
- **Key Features:**
  - Task scheduling
  - Dependency management
  - Resource allocation
  - Progress tracking

#### 6. **Bonzai WebSocket Coordinator** (`services/bonzai_websocket_coordinator.py`)
- **Purpose:** Real-time communication coordination
- **Key Features:**
  - Connection management
  - Message routing
  - Event broadcasting
  - Session handling

#### 7. **Agent Creation Workbench** (`services/agent_creation_workbench.py`)
- **Purpose:** Dynamic agent creation and customization
- **Key Features:**
  - Agent templates
  - Capability configuration
  - Deployment automation
  - Testing frameworks

### AI & Model Integration Services

#### 8. **ZAI Live Multimodal** (`services/zai_live_multimodal.py`)
- **Purpose:** Real-time multimodal AI processing
- **Key Features:**
  - Text, image, audio processing
  - Real-time streaming
  - Format conversion
  - Quality optimization

#### 9. **ZAI Vertex Optimizer** (`services/zai_vertex_optimizer.py`)
- **Purpose:** Google Vertex AI optimization
- **Key Features:**
  - Performance tuning
  - Cost optimization
  - Resource management
  - Monitoring

#### 10. **ZAI Express Vertex Supercharger** (`services/zai_express_vertex_supercharger.py`)
- **Purpose:** Ultra-fast Vertex AI processing
- **Key Features:**
  - Response acceleration
  - Caching strategies
  - Parallel processing
  - Quality maintenance

### Research & Analysis Services

#### 11. **Deep Research Center** (`services/deep_research_center.py`)
- **Purpose:** Comprehensive research automation
- **Key Features:**
  - Multi-source research
  - Data synthesis
  - Citation management
  - Report generation

#### 12. **Enhanced Gemini Scout Orchestration** (`services/enhanced_gemini_scout_orchestration.py`)
- **Purpose:** Advanced research and reconnaissance
- **Key Features:**
  - Web intelligence gathering
  - Competitive analysis
  - Market research
  - Trend analysis

### Automation & Integration Services

#### 13. **Enhanced Scrapybara Integration** (`services/enhanced_scrapybara_integration.py`)
- **Purpose:** Advanced web scraping and automation
- **Key Features:**
  - VM-based scraping
  - Browser automation
  - Data extraction
  - Anti-detection measures

#### 14. **Virtual Computer Service** (`services/virtual_computer_service.py`)
- **Purpose:** Computer use automation
- **Key Features:**
  - Desktop environment simulation
  - Application automation
  - File operations
  - Process management

#### 15. **Revolutionary MCP Service** (`services/revolutionary_mcp_service.py`)
- **Purpose:** Advanced MCP protocol implementation
- **Key Features:**
  - Enhanced tool capabilities
  - Custom protocol extensions
  - Performance optimization
  - Error recovery

### Monitoring & Observability Services

#### 16. **ZAI Monitoring** (`services/zai_monitoring.py`)
- **Purpose:** Comprehensive system monitoring
- **Key Features:**
  - Performance metrics
  - Health checks
  - Alerting
  - Dashboard integration

#### 17. **ZAI Observability** (`services/zai_observability.py`)
- **Purpose:** System observability and insights
- **Key Features:**
  - Logging aggregation
  - Trace analysis
  - Metrics collection
  - Anomaly detection

#### 18. **Environment Snapshot Manager** (`services/environment_snapshot_manager.py`)
- **Purpose:** System state management
- **Key Features:**
  - Configuration snapshots
  - State restoration
  - Version tracking
  - Rollback capabilities

### Specialized Services

#### 19. **ZAI Grounding System** (`services/zai_grounding_system.py`)
- **Purpose:** AI response grounding and validation
- **Key Features:**
  - Fact checking
  - Source verification
  - Accuracy scoring
  - Bias detection

#### 20. **ZAI Multi-Provider System** (`services/zai_multi_provider_system.py`)
- **Purpose:** Multi-cloud AI provider management
- **Key Features:**
  - Provider abstraction
  - Failover handling
  - Cost optimization
  - Performance comparison

#### 21. **Gemini Quota Manager** (`services/gemini_quota_manager.py`)
- **Purpose:** Gemini API quota and usage management
- **Key Features:**
  - Usage tracking
  - Quota enforcement
  - Rate limiting
  - Cost monitoring

#### 22. **Claude Computer Use Service** (`services/claude_computer_use_service.py`)
- **Purpose:** Claude computer use integration
- **Key Features:**
  - Screen interaction
  - Application control
  - File management
  - Process automation

#### 23-42. **Additional Services**
- **ZAI Specialized Variants** - Custom AI model variants
- **CrewAI Supercharger** - Multi-agent collaboration
- **Pipedream Integration** - Workflow automation
- **OpenAI Vertex Service** - OpenAI/Vertex bridge
- **Enhanced Code Execution** - Advanced code running
- **Websocket Agent Client** - Agent communication
- **Agentic IDE Integration** - Development environment
- **Add Claude Collaborative Models** - Model extensions
- **And 19 more specialized services...**

---

## 🔌 INTEGRATION SERVICES

### 1. **Mem0 Integration**
- **Purpose:** Advanced memory and RAG system
- **Key Features:**
  - Semantic memory storage
  - Context-aware retrieval
  - Family memory sharing
  - Long-term memory preservation
- **API Key:** Required (`MEM0_API_KEY`)

### 2. **ScrapyBara Integration**
- **Purpose:** VM-based web automation
- **Key Features:**
  - Ubuntu VM instances
  - Browser automation
  - Screenshot capture
  - File system access
- **API Key:** Required (`SCRAPYBARA_API_KEY`)

### 3. **E2B Integration**
- **Purpose:** Secure code execution environment
- **Key Features:**
  - Python sandbox execution
  - Package installation
  - Timeout management
  - Result capture
- **API Key:** Required (`E2B_API_KEY`)

### 4. **GitHub Integration**
- **Purpose:** Repository management and automation
- **Key Features:**
  - Repository creation
  - Code deployment
  - PR management
  - Issue tracking
- **API Key:** Required (`GITHUB_PAT`)

### 5. **Pipedream Integration**
- **Purpose:** Workflow automation platform
- **Key Features:**
  - Event-driven workflows
  - External service integration
  - Natural language automation
  - Scheduled tasks
- **API Key:** Required (`PIPEDREAM_API_TOKEN`)

### 6. **Multi-AI Provider Integration**
- **Purpose:** Unified AI provider interface
- **Supported Providers:**
  - Google (Gemini)
  - Anthropic (Claude)
  - OpenAI (GPT)
  - DeepSeek
  - Custom models

---

## 🛣️ ROUTE BLUEPRINTS

### 1. **Memory Routes** (`routes/memory.py`)
- **Prefix:** `/api/memory`
- **Endpoints:**
  - `POST /search` - Search memories
  - `POST /add` - Add new memory
  - `GET /list` - List all memories
  - `DELETE /delete` - Delete memory

### 2. **Chat Routes** (`routes/chat.py`)
- **Prefix:** `/api/chat`
- **Endpoints:**
  - `POST /` - Standard chat
  - `POST /stream` - Streaming chat
  - `GET /history` - Chat history
  - `DELETE /clear` - Clear history

### 3. **Scrape Routes** (`routes/scrape.py`)
- **Prefix:** `/api/scrape`
- **Endpoints:**
  - `POST /` - Basic scraping
  - `POST /vm` - VM-based scraping
  - `GET /status` - Scraping status
  - `GET /results/{job_id}` - Get results

### 4. **Agent Workbench Routes** (`routes/agent_workbench.py`)
- **Prefix:** `/api/agent-workbench`
- **Endpoints:**
  - `GET /status` - Service status
  - `POST /create` - Create agent
  - `GET /list` - List agents
  - `DELETE /{agent_id}` - Delete agent

### 5. **Execution Router Routes** (`routes/execution_router.py`)
- **Prefix:** `/api/execution-router`
- **Endpoints:**
  - `GET /status` - Router status
  - `POST /route` - Route task
  - `GET /results/{task_id}` - Get results
  - `POST /optimize` - Optimize routing

### 6. **Scout Routes** (`routes/scout.py`)
- **Prefix:** `/api/scout`
- **Endpoints:**
  - `GET /status` - Scout status
  - `POST /execute` - Execute scout task
  - `GET /reports` - Get reports
  - `POST /research` - Research task

### 7. **Themes Routes** (`routes/themes.py`)
- **Prefix:** `/api/themes`
- **Endpoints:**
  - `GET /list` - List themes
  - `POST /apply` - Apply theme
  - `GET /current` - Current theme
  - `POST /custom` - Create custom theme

### 8. **Enhanced Routing** (`enhanced_api_routing.py`)
- **Purpose:** Advanced API routing and middleware
- **Key Features:**
  - Dynamic routing
  - Request validation
  - Response formatting
  - Error handling

---

## 📊 SERVICE STATUS & HEALTH

### Health Check Endpoints

Every service provides health check endpoints for monitoring:

```bash
# Core Services
GET http://localhost:3000/health          # MCP Server
GET http://localhost:5001/api/health      # Main Flask App  
GET http://localhost:8000/api/status      # ZAI Prime API

# Service-Specific Status
GET /api/multi-model/status               # Multi-Model Status
GET /api/task-orchestrator/status         # Task Orchestrator
GET /api/websocket-coordinator/status     # WebSocket Coordinator
GET /api/scrape/status                    # Scrape Service
GET /api/zai-prime/status                 # ZAI Prime Status
```

### Service Discovery

```bash
# Get all available services
GET /api/registry/services

# Get service capabilities
GET /api/registry/capabilities

# Get service health summary
GET /api/health/summary
```

### Monitoring Dashboard

Access the comprehensive monitoring dashboard:
- **URL:** `https://mofy.ai/dashboard`
- **Features:**
  - Real-time service status
  - Performance metrics
  - Error tracking
  - Resource utilization

---

## 🚀 QUICK REFERENCE

### Service Categories

| Category | Count | Key Services |
|----------|-------|--------------|
| **Core Infrastructure** | 4 | MCP Server, Flask App, ZAI API, Config |
| **AI & Model Services** | 8 | ZAI Prime, Multi-Model, Express Mode, Orchestration |
| **API Services** | 24 | Agent APIs, Workflow APIs, Integration APIs |
| **Business Logic** | 42 | Memory, Scout, Research, Monitoring |
| **Integrations** | 6 | Mem0, ScrapyBara, E2B, GitHub, Pipedream |
| **Route Blueprints** | 8 | Memory, Chat, Scrape, Agent, Router |

### Key Endpoints

```bash
# System Overview
GET /                                     # Main system info
GET /api/health                          # Health check
GET /sse                                 # Real-time events

# AI Services
POST /api/chat                           # Chat with AI
POST /mcp/execute                        # Execute MCP tool
POST /v1/chat/completions               # OpenAI compatible

# Memory & Data
POST /api/memory/search                  # Search memories
POST /api/memory/add                     # Add memory
POST /api/scrape                         # Web scraping

# Agents & Automation
POST /api/agent-workbench/create         # Create agent
POST /api/task-orchestrator/submit       # Submit task
POST /api/zai-prime/agents/spawn         # Spawn agent
```

### Quick Start Commands

```bash
# Start all services
python app.py                            # Main Flask app (port 5001)
node bonzai-mcp-server/server.js        # MCP server (port 3000)
python zai-api/ZAI_PRIME_API_SERVER.py  # ZAI API (port 8000)

# Run tests
python COMPREHENSIVE_TEST_SUITE.py      # Full test suite
python test_15_endpoints.py             # Core endpoint tests

# Check status
curl http://localhost:5001/api/health   # Main app health
curl http://localhost:3000/             # MCP server info
curl http://localhost:8000/api/status   # ZAI API status
```

### Environment Setup

```bash
# Required environment variables
export GOOGLE_AI_API_KEY_1=your_key
export ANTHROPIC_API_KEY=your_key
export MEM0_API_KEY=your_key
export SCRAPYBARA_API_KEY=your_key
export E2B_API_KEY=your_key
export GITHUB_PAT=your_token

# Optional integrations
export PIPEDREAM_API_TOKEN=your_token
export OPENAI_API_KEY=your_key
```

### Performance Benchmarks

| Service | Response Time | Throughput | Uptime |
|---------|---------------|------------|--------|
| **MCP Server** | <500ms | 200 req/min | 99.9% |
| **Main Flask App** | <1s | 500 req/min | 99.9% |
| **ZAI Prime API** | <2s | 100 req/min | 99.8% |
| **Express Mode** | <200ms | 1000 req/min | 99.9% |

---

## 📞 SUPPORT & RESOURCES

- **Documentation:** [Complete Service Docs](https://docs.mofy.ai)
- **API Reference:** [API Documentation](https://docs.mofy.ai/api)
- **Status Page:** [System Status](https://status.mofy.ai)
- **Support:** nathan@mofy.ai

---

*Last Updated: January 15, 2024*  
*Version: 3.0.0*  
*Total Services: 92*