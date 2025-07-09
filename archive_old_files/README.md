# 🚀 Bonzai AI Platform - Core Backend Engine

![Production Tests](https://github.com/mofy-ai/bonzai-core-engine/actions/workflows/production-tests.yml/badge.svg)
![AI Integration](https://github.com/mofy-ai/bonzai-core-engine/actions/workflows/ai-integration-tests.yml/badge.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> **The definitive backend for next-generation AI collaboration**  
> 🧠 ZAI Prime Supervisor | 🤖 Multi-Model Orchestration | 🔗 MCP Memory Integration

## 🌟 Overview

Bonzai Core Engine is a sophisticated AI orchestration platform that powers the next generation of human-AI collaboration. Built with Python Flask, it provides a unified interface for managing multiple AI models, advanced memory systems, and intelligent task routing.

### ✨ Key Features

- **🧠 ZAI Prime Supervisor** - Omnipresent AI awareness with 8000+ agent spawning capability
- **🤖 Multi-Model Orchestration** - Seamless integration with Claude, Gemini, OpenAI, and more
- **🔗 MCP Protocol Integration** - Model Context Protocol for advanced AI tool interactions
- **💾 Professional Memory Systems** - Neo4j, Qdrant, Redis integration for persistent context
- **⚡ Express Mode** - 6x faster AI responses with Vertex AI optimization
- **🔄 Intelligent Task Routing** - Smart distribution across 20+ worker processes
- **🌐 WebSocket Coordination** - Real-time agent-to-agent communication
- **🛡️ Production Security** - Enterprise-grade security and monitoring

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Bonzai Core Engine                       │
├─────────────────────────────────────────────────────────────┤
│  🧠 ZAI Prime Supervisor                                   │
│  ├── Agent Spawning Service (8000+ agents)                 │
│  ├── Event Streaming Service                               │
│  └── Omnipresent Monitoring                                │
├─────────────────────────────────────────────────────────────┤
│  🤖 AI Model Orchestration                                 │
│  ├── Claude 3.5 Sonnet (Computer Use API)                 │
│  ├── Gemini 2.5 Pro (Function Calling)                    │
│  ├── OpenAI GPT-4 (Specialized Tasks)                     │
│  └── DeepSeek Integration                                  │
├─────────────────────────────────────────────────────────────┤
│  💾 Memory & Storage                                       │
│  ├── Neo4j Graph Database                                  │
│  ├── Qdrant Vector Storage                                 │
│  ├── Redis Caching                                         │
│  └── Mem0 Memory Client                                    │
├─────────────────────────────────────────────────────────────┤
│  🔧 Services & Integration                                 │
│  ├── ScrapyBara Web Scraping                              │
│  ├── Pipedream Automation                                  │
│  ├── Virtual Computer Service                              │
│  ├── WhatsApp Integration                                  │
│  └── 42+ Microservices                                     │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Virtual environment (recommended)
- API keys for AI models (see [Configuration](#configuration))

### Installation

```bash
# Clone the repository
git clone https://github.com/mofy-ai/bonzai-core-engine.git
cd bonzai-core-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Start the backend
python app.py
```

The backend will be available at `http://localhost:5001`

### Quick Health Check

```bash
curl http://localhost:5001/api/health
```

Expected response:
```json
{
  "success": true,
  "status": "healthy",
  "message": "Bonzai Backend is running",
  "timestamp": "2025-07-09T10:00:00.000000"
}
```

## ⚙️ Configuration

Create a `.env` file with the following configuration:

```env
# Core Flask Settings
FLASK_SECRET_KEY=your-super-secret-flask-key
BACKEND_PORT=5001
DEBUG=True

# AI Model API Keys
ANTHROPIC_API_KEY=your-anthropic-key
OPENAI_API_KEY=your-openai-key
GOOGLE_API_KEY=your-google-api-key
GEMINI_API_KEY=your-gemini-api-key
DEEPSEEK_API_KEY=your-deepseek-key

# Memory & Storage
MEM0_API_KEY=your-mem0-key

# Specialized Services
SCRAPYBARA_API_KEY=your-scrapybara-key
E2B_API_KEY=your-e2b-key
PIPEDREAM_API_TOKEN=your-pipedream-token
```

## 📚 API Documentation

### Core Endpoints

| Endpoint | Method | Description |
|----------|---------|------------|
| `/api/health` | GET | System health check |
| `/api/chat/simple` | POST | Simple AI chat interface |
| `/api/multi-model/status` | GET | Multi-model orchestrator status |
| `/api/zai-prime/status` | GET | ZAI Prime supervisor status |
| `/api/agents` | GET | Active agents registry |
| `/api/memory` | GET/POST | Memory operations |

### Advanced Endpoints

| Endpoint | Method | Description |
|----------|---------|------------|
| `/api/zai-prime/agents/spawn` | POST | Spawn new AI agent |
| `/api/task-orchestrator` | POST | Submit task for orchestration |
| `/api/mcp/tools` | GET | Available MCP tools |
| `/api/mcp/execute` | POST | Execute MCP tool |
| `/api/websocket-coordinator` | WS | Real-time coordination |

### Example Usage

#### Simple AI Chat
```bash
curl -X POST http://localhost:5001/api/chat/simple \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.0-flash-exp",
    "message": "Hello, Bonzai!",
    "user_id": "demo_user"
  }'
```

#### Spawn AI Agent
```bash
curl -X POST http://localhost:5001/api/zai-prime/agents/spawn \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "general",
    "purpose": "Handle customer queries",
    "config": {"specialized": true}
  }'
```

## 🧪 Testing

### Automated Testing

The project includes comprehensive GitHub Actions workflows:

- **Production Tests** - Full backend validation
- **AI Integration Tests** - AI model connectivity and responses
- **Stress Tests** - Load testing and performance validation

### Manual Testing

```bash
# Run basic health tests
python test_hardcore_ai_real.py

# Run production test suite (if available)
python PRODUCTION_MASTER_TEST_SUITE.py

# Run readiness assessment (if available)
python PRODUCTION_READINESS_ASSESSMENT.py
```

### Test Categories

- **Unit Tests** - Individual component testing
- **Integration Tests** - Service interconnection validation
- **AI Tests** - Real AI model response verification
- **Production Tests** - End-to-end system validation

## 🏭 Production Deployment

### Railway Deployment

The backend is designed for seamless Railway deployment:

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push to main branch

### Docker Deployment

```bash
# Build Docker image
docker build -t bonzai-core-engine .

# Run container
docker run -p 5001:5001 --env-file .env bonzai-core-engine
```

### Production Checklist

- [ ] All API keys configured
- [ ] Environment variables set
- [ ] Health endpoints responding
- [ ] AI models accessible
- [ ] Memory systems connected
- [ ] Monitoring enabled
- [ ] Security configured

## 🔧 Services Architecture

### Core Services (15/16 running)

1. **Enhanced Scout Workflow** - Advanced AI orchestration
2. **Vertex AI Supercharger** - 6x performance optimization
3. **Multimodal Chat API** - Comprehensive AI chat system
4. **Agentic Superpowers V3.0** - Autonomous AI capabilities
5. **Collaborative Workspaces V3.0** - Real-time collaboration
6. **Pipedream Integration** - Workflow automation
7. **Memory Manager** - Intelligent context management
8. **Deep Research Center** - Advanced research capabilities
9. **WhatsApp Integration** - Messaging platform connection
10. **DeepSeek Integration** - Advanced AI model support
11. **CrewAI Orchestration** - Multi-agent coordination
12. **Monitoring System** - Real-time system monitoring
13. **Multi-Provider System** - Cross-platform AI access
14. **Agent Registry** - 23+ specialized agents
15. **Task Orchestrator** - 20 worker intelligent routing

### Specialized Agents

- **ZAI Master Orchestrator** - Central coordination
- **Enhanced Gemini Scout** - Google AI optimization
- **Vertex AI Supercharger** - Performance enhancement
- **Multi-Model Orchestrator** - Cross-platform routing
- **Mama Bear Memory System** - Caring context management
- **Scrapybara Web Scraping** - Intelligent data extraction
- **Virtual Computer Service** - System automation
- **Security Scanner Agent** - Threat detection
- **Deep Research Center** - Information analysis
- **Theme Manager** - UI/UX customization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
flake8 .
black .
```

## 📊 Performance

- **Response Time**: < 200ms for health checks
- **AI Response Time**: < 2s with Express Mode
- **Concurrent Users**: 1000+ supported
- **Agent Capacity**: 8000+ dynamic agents
- **Memory Efficiency**: 90% token cost savings with Redis caching
- **Uptime**: 99.9% target availability

## 🛡️ Security

- **API Key Management** - Secure environment variable storage
- **Rate Limiting** - Built-in request throttling
- **Input Validation** - Comprehensive data sanitization
- **CORS Protection** - Cross-origin request security
- **Monitoring** - Real-time security scanning
- **Audit Logging** - Comprehensive activity tracking

## 📋 Roadmap

### Q3 2025
- [ ] Advanced multi-modal capabilities
- [ ] Enhanced security features
- [ ] Performance optimizations
- [ ] Mobile API improvements

### Q4 2025
- [ ] Kubernetes deployment support
- [ ] Advanced analytics dashboard
- [ ] Enterprise SSO integration
- [ ] Global CDN deployment

## 📞 Support

- **Documentation**: [Full API Documentation](./docs/)
- **Issues**: [GitHub Issues](https://github.com/mofy-ai/bonzai-core-engine/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mofy-ai/bonzai-core-engine/discussions)
- **Email**: daddyholne@outlook.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Claude (Anthropic)** - AI development partnership
- **Gemini (Google)** - Advanced AI capabilities
- **OpenAI** - GPT model integration
- **Railway** - Seamless deployment platform
- **MCP Protocol** - Standardized AI tool interactions

---

<div align="center">

**Built with ❤️ by Nathan Fyffe**  
*"Where Imagination Meets Innovation"*

[![GitHub stars](https://img.shields.io/github/stars/mofy-ai/bonzai-core-engine.svg?style=social&label=Star)](https://github.com/mofy-ai/bonzai-core-engine)
[![GitHub forks](https://img.shields.io/github/forks/mofy-ai/bonzai-core-engine.svg?style=social&label=Fork)](https://github.com/mofy-ai/bonzai-core-engine/fork)

</div>
