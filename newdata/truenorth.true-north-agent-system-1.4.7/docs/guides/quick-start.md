# TrueNorth Quick Start Guide

Get up and running with TrueNorth in just 5 minutes! This guide will walk you through installing, configuring, and deploying your first AI agents.

## Prerequisites

Before you begin, ensure you have:

- **VS Code** version 1.74.0 or higher
- **Claude CLI** installed and configured
- An active **Claude API subscription**
- A **workspace folder** open in VS Code

## Step 1: Install Claude CLI

If you haven't already installed Claude CLI, run:

```bash
# Install Claude CLI
curl -sSL https://claude.ai/install | bash

# Verify installation
claude --version
```

For alternative installation methods, visit [claude.ai/code](https://claude.ai/code).

## Step 2: Install TrueNorth Extension

### Option A: From VSIX File
```bash
code --install-extension true-north-agent-system-1.0.0.vsix
```

### Option B: From VS Code Marketplace
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "TrueNorth Agent System"
4. Click "Install"

## Step 3: Configure TrueNorth

1. **Open VS Code Settings**
   - Press `Ctrl+,` (Windows/Linux) or `Cmd+,` (Mac)
   - Or go to File > Preferences > Settings

2. **Configure TrueNorth Settings**
   ```json
   {
     "truenorth.claudeCommand": "claude",
     "truenorth.maxParallelAgents": 8,
     "truenorth.audioNotifications": true
   }
   ```

3. **Verify Configuration**
   - Open Command Palette (`Ctrl+Shift+P`)
   - Run "TrueNorth: Test Claude CLI"
   - You should see a success message

## Step 4: Your First Agent Deployment

### Open a Project
1. Open a folder/workspace in VS Code (`File > Open Folder`)
2. TrueNorth works best with projects containing:
   - Code files (JavaScript, TypeScript, Python, etc.)
   - Configuration files (package.json, requirements.txt, etc.)
   - Documentation files

### Launch the Dashboard
1. Press `Ctrl+Shift+M` (or `Cmd+Shift+M` on Mac)
2. Or use Command Palette: "TrueNorth: Open Dashboard"
3. Your browser will open to the monitoring dashboard

### Deploy Your First Agents
1. **Clean Your Codebase** (Recommended first step)
   - Press `Ctrl+Shift+C` or use Command Palette
   - Run "TrueNorth: Clean Codebase"
   - This optimizes your project structure

2. **Analyze Your Project**
   - Press `Ctrl+Shift+A` or use Command Palette
   - Run "TrueNorth: Analyze Project & Generate Agents"
   - Wait for analysis to complete (1-3 minutes)

3. **Deploy AI Agents**
   - Press `Ctrl+Shift+D` or use Command Palette
   - Run "TrueNorth: Deploy AI Agents"
   - Monitor progress in the dashboard

## Step 5: Monitor Progress

### Dashboard Features
- **Real-time Agent Status** - See which agents are running
- **Phase Progress** - Track completion across phases
- **Performance Metrics** - Monitor system resource usage
- **Agent Logs** - View detailed execution logs

### Status Bar Integration
The TrueNorth status bar shows:
- Current operation status
- Number of active agents
- Quick access to commands

## What Happens Next?

Once agents are deployed, they will:

1. **Phase 1: Foundation** - Core optimizations and fixes
2. **Phase 2: Enhancement** - Advanced features and improvements
3. **Phase 3: Optimization** - Performance and efficiency gains
4. **Phase 4: Security & Testing** - Security hardening and test coverage
5. **Phase 5: Finalization** - Final polish and documentation

## Common First-Time Tasks

### Task Selection
Use `Ctrl+Shift+T` to access the task menu:
- 🧹 **Clean Codebase** - Optimize project structure
- 🔐 **Add Authentication** - Implement auth systems
- ⚡ **Optimize Performance** - Improve speed and efficiency
- 🛡️ **Enhance Security** - Security audit and hardening
- 🧪 **Add Testing** - Comprehensive testing strategy
- 📚 **Improve Documentation** - Create and enhance docs

### Monitor Agent Health
- Check dashboard for agent status
- Review logs for any errors
- Use "Retry Failed Agents" if needed

## Troubleshooting

### Claude CLI Issues
```bash
# Check Claude CLI status
claude --version

# Update Claude CLI
curl -sSL https://claude.ai/install | bash
```

### Extension Issues
1. Reload VS Code window (`Ctrl+R`)
2. Check VS Code Developer Console (`Help > Toggle Developer Tools`)
3. Verify workspace permissions

### Agent Failures
1. Check the dashboard for error details
2. Use "TrueNorth: Retry Failed Agents"
3. Review agent logs in the dashboard

## Next Steps

### Explore Advanced Features
- [Configuration Guide](./configuration.md) - Customize TrueNorth settings
- [Dashboard Guide](./dashboard.md) - Master the monitoring interface
- [Advanced Tasks](../tutorials/advanced-configuration.md) - Complex configurations

### Get Help
- [Troubleshooting Guide](../troubleshooting/common-issues.md)
- [Community Support](https://github.com/truenorth/issues)
- [Documentation](../README.md)

## Success! 🎉

You've successfully:
- ✅ Installed and configured TrueNorth
- ✅ Deployed your first AI agents
- ✅ Monitored progress through the dashboard
- ✅ Optimized your project with intelligent automation

Your codebase is now being systematically enhanced by specialized AI agents. Welcome to the future of development! 🚀

---

**Need help?** Check our [FAQ](../troubleshooting/common-issues.md#frequently-asked-questions) or [create an issue](https://github.com/truenorth/issues/new).