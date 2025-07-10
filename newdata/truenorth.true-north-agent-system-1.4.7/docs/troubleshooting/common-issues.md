# Common Issues and Troubleshooting

This guide covers the most frequently encountered issues with TrueNorth Agent System and their solutions.

## 🚨 Most Common Issues

### 1. Claude CLI Not Found

**Symptoms**:
- Error: "Claude CLI not found"
- Commands fail to execute
- Status bar shows "Claude CLI not found"

**Solutions**:

#### Check Installation
```bash
# Verify Claude CLI is installed
claude --version

# If not found, install it
curl -sSL https://claude.ai/install | bash
```

#### Check PATH Configuration
```bash
# Check current PATH
echo $PATH

# Find where Claude is installed
which claude

# Add to PATH if needed (macOS/Linux)
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# For Windows, add to System Environment Variables
```

#### Update TrueNorth Configuration
```json
{
  "truenorth.claudeCommand": "/usr/local/bin/claude"
}
```

### 2. Authentication Issues

**Symptoms**:
- "Authentication failed" errors
- API requests rejected
- Commands hang indefinitely

**Solutions**:

#### Re-authenticate Claude CLI
```bash
# Check current auth status
claude auth status

# Re-login if needed
claude auth logout
claude auth login

# Verify authentication
claude auth status
```

#### Check API Quota
```bash
# Check usage and limits
claude usage

# Verify account status
claude account status
```

### 3. Extension Not Loading

**Symptoms**:
- TrueNorth commands not available
- No status bar indicator
- Extension marked as "Not Activated"

**Solutions**:

#### Basic Troubleshooting
1. **Restart VS Code** completely
2. **Check VS Code version**: Must be 1.74.0+
   ```bash
   code --version
   ```
3. **Reload window**: Ctrl+R (Cmd+R on Mac)

#### Check Developer Console
1. Open Developer Tools: `Help > Toggle Developer Tools`
2. Look for TrueNorth-related errors
3. Common errors and solutions:

```javascript
// Error: Module not found
// Solution: Reinstall extension

// Error: Claude CLI spawn error
// Solution: Fix Claude CLI path in settings

// Error: Permission denied
// Solution: Check file permissions
```

#### Reinstall Extension
```bash
# Uninstall
code --uninstall-extension truenorth.true-north-agent-system

# Reinstall
code --install-extension true-north-agent-system-1.0.0.vsix
```

### 4. Dashboard Won't Open

**Symptoms**:
- Browser doesn't open
- "Port in use" error
- Dashboard shows blank page

**Solutions**:

#### Port Conflicts
```json
{
  "truenorth.dashboardPort": 8080
}
```

#### Check Browser Settings
- Disable popup blockers for localhost
- Try different browser
- Check firewall settings

#### Manual Dashboard Access
If auto-open fails, try manually navigating to:
- `http://localhost:7777` (default)
- Check VS Code output panel for actual URL

### 5. Agents Failing to Start

**Symptoms**:
- "Failed to start agent" errors
- Agents stuck in "starting" state
- High failure rate in dashboard

**Solutions**:

#### Reduce Parallel Agents
```json
{
  "truenorth.maxParallelAgents": 4
}
```

#### Check System Resources
```bash
# Check memory usage
htop  # Linux/Mac
taskmgr  # Windows

# Check disk space
df -h  # Linux/Mac
dir C:  # Windows
```

#### Review Agent Logs
1. Open TrueNorth Dashboard
2. Navigate to "Agent Logs" section
3. Look for specific error patterns:
   - Memory errors → Reduce parallel agents
   - Network errors → Check internet connection
   - Permission errors → Check file permissions

### 6. Performance Issues

**Symptoms**:
- VS Code becomes slow/unresponsive
- High CPU/memory usage
- System freezing

**Solutions**:

#### Optimize Settings
```json
{
  "truenorth.maxParallelAgents": 4,
  "truenorth.sessionTimeout": 120000,
  "truenorth.enableDetailedLogging": false
}
```

#### Monitor Resource Usage
- Use TrueNorth Dashboard performance tab
- Check VS Code Task Manager: `Help > Show Running Extensions`
- Monitor system resources

#### Performance Tuning
```json
{
  "truenorth.performanceMode": "optimized",
  "truenorth.backgroundProcessing": true,
  "truenorth.memoryLimit": "2GB"
}
```

## 📋 Frequently Asked Questions

### Q: Can I use TrueNorth without an internet connection?
**A**: No, TrueNorth requires internet access to communicate with Claude's API. However, you can work offline after agents have completed their tasks.

### Q: How much does it cost to run TrueNorth?
**A**: TrueNorth itself is free, but it uses Claude API which has usage-based pricing. Monitor your usage with `claude usage` command.

### Q: Can I run TrueNorth on multiple projects simultaneously?
**A**: Yes, you can open multiple VS Code windows with TrueNorth, but be mindful of resource usage and API rate limits.

### Q: Why are my agents taking so long to complete?
**A**: Agent execution time depends on project complexity and your internet connection. Large projects may take 30+ minutes. Monitor progress in the dashboard.

### Q: Can I cancel running agents?
**A**: Yes, use "TrueNorth: Cancel Execution" command or the stop button in the dashboard.

### Q: What happens if my computer shuts down during agent execution?
**A**: Running agents will be terminated. TrueNorth will detect incomplete tasks on restart and offer to resume or restart them.

## 🔧 Advanced Troubleshooting

### Enable Debug Mode
```json
{
  "truenorth.debugMode": true,
  "truenorth.verboseOutput": true,
  "truenorth.logLevel": "debug"
}
```

### Collect Diagnostic Information
```bash
# Generate system report
code --status

# Check extension logs
# Location varies by OS:
# Windows: %APPDATA%/Code/logs
# macOS: ~/Library/Application Support/Code/logs
# Linux: ~/.config/Code/logs
```

### Reset TrueNorth Configuration
```json
// Remove all TrueNorth settings and restart VS Code
{
  // All truenorth.* settings removed
}
```

### Clean Installation
```bash
# Complete clean reinstall
code --uninstall-extension truenorth.true-north-agent-system
rm -rf ~/.vscode/extensions/truenorth.*
code --install-extension true-north-agent-system-1.0.0.vsix
```

## 🐛 Reporting Bugs

### Before Reporting
1. Check this troubleshooting guide
2. Search existing issues on GitHub
3. Try reproducing with minimal setup
4. Update to latest version

### What to Include
- **System Information**:
  - OS and version
  - VS Code version
  - TrueNorth version
  - Claude CLI version

- **Error Information**:
  - Exact error messages
  - Steps to reproduce
  - Screenshots if relevant
  - Developer Console logs

- **Configuration**:
  - Relevant TrueNorth settings
  - Workspace configuration
  - Extensions that might conflict

### Bug Report Template
```markdown
**Environment**
- OS: [Windows 10 / macOS 12 / Ubuntu 20.04]
- VS Code: [version]
- TrueNorth: [version]
- Claude CLI: [version]

**Description**
[Clear description of the issue]

**Steps to Reproduce**
1. [First step]
2. [Second step]
3. [Third step]

**Expected Behavior**
[What should happen]

**Actual Behavior**
[What actually happens]

**Error Messages**
```
[Any error messages]
```

**Additional Context**
[Screenshots, logs, or other helpful information]
```

## 📊 Performance Optimization

### System Requirements Check
- **Minimum**: 4GB RAM, 2 CPU cores
- **Recommended**: 8GB+ RAM, 4+ CPU cores
- **Optimal**: 16GB+ RAM, 8+ CPU cores

### Optimization Settings
```json
{
  "truenorth.maxParallelAgents": 6,
  "truenorth.agentTimeout": 300000,
  "truenorth.memoryLimit": "4GB",
  "truenorth.enableCaching": true,
  "truenorth.backgroundProcessing": true
}
```

### Monitor Performance
- Use TrueNorth Dashboard performance metrics
- Monitor system resources during execution
- Adjust settings based on performance data

## 🆘 Emergency Procedures

### If TrueNorth Makes VS Code Unresponsive
1. **Force quit VS Code**
2. **Restart VS Code in safe mode**: `code --disable-extensions`
3. **Disable TrueNorth temporarily**
4. **Investigate issue before re-enabling**

### If Agents Are Causing System Issues
1. **Stop all agents**: Use Command Palette → "TrueNorth: Stop All Agents"
2. **Reduce parallel agents** in settings
3. **Check system resources**
4. **Restart with lower limits**

### If Dashboard Won't Stop
1. **Check running processes**: Look for node/http-server processes
2. **Kill processes manually**: 
   ```bash
   # Find TrueNorth processes
   ps aux | grep truenorth
   
   # Kill specific process
   kill -9 [PID]
   ```
3. **Change dashboard port** in settings

---

## 🤝 Getting Additional Help

### Documentation
- [Installation Guide](../guides/installation.md)
- [Configuration Guide](../guides/configuration.md)
- [Quick Start Guide](../guides/quick-start.md)

### Community Support
- **GitHub Issues**: [Report bugs](https://github.com/truenorth/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/truenorth/discussions)
- **Documentation**: [Full documentation](../README.md)

### Professional Support
For enterprise users or complex issues:
- Email: support@truenorth.dev
- Priority support available for enterprise licenses

---

**Remember**: Most issues can be resolved by checking Claude CLI installation, verifying authentication, and adjusting performance settings. When in doubt, try the basic troubleshooting steps first!