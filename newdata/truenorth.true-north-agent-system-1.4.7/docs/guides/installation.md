# TrueNorth Installation Guide

Complete installation instructions for the TrueNorth Agent System VSCode extension.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux Ubuntu 18.04+
- **VS Code**: Version 1.74.0 or higher
- **Node.js**: Version 16.0+ (for development)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB free space

### Recommended Requirements
- **Memory**: 16GB RAM for optimal performance
- **CPU**: Multi-core processor (4+ cores)
- **Storage**: 2GB free space for agent outputs
- **Network**: Stable internet connection for Claude API

## Installing Claude CLI

TrueNorth requires Claude CLI to function. Install it first:

### Automatic Installation (Recommended)
```bash
curl -sSL https://claude.ai/install | bash
```

### Manual Installation

#### macOS
```bash
# Using Homebrew
brew install claude-cli

# Or download directly
curl -L https://github.com/anthropic/claude-cli/releases/latest/download/claude-macos.tar.gz | tar xz
sudo mv claude /usr/local/bin/
```

#### Windows
```powershell
# Using Chocolatey
choco install claude-cli

# Or using Scoop
scoop install claude-cli

# Or download from releases
# Visit: https://github.com/anthropic/claude-cli/releases
```

#### Linux
```bash
# Ubuntu/Debian
wget https://github.com/anthropic/claude-cli/releases/latest/download/claude-linux.tar.gz
tar xzf claude-linux.tar.gz
sudo mv claude /usr/local/bin/

# Arch Linux
yay -S claude-cli
```

### Verify Claude CLI Installation
```bash
claude --version
```

### Configure Claude CLI
```bash
# Login to Claude
claude auth login

# Verify authentication
claude auth status
```

## Installing TrueNorth Extension

### Method 1: VS Code Marketplace (Coming Soon)
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "TrueNorth Agent System"
4. Click "Install"

### Method 2: From VSIX File
```bash
# Download the latest release
wget https://github.com/truenorth/releases/latest/download/true-north-agent-system-1.0.0.vsix

# Install via command line
code --install-extension true-north-agent-system-1.0.0.vsix
```

### Method 3: From VS Code UI
1. Download the `.vsix` file from releases
2. Open VS Code
3. Go to Extensions (Ctrl+Shift+X)
4. Click the "..." menu
5. Select "Install from VSIX..."
6. Choose the downloaded file

### Method 4: Development Installation
```bash
# Clone repository
git clone https://github.com/truenorth/true-north-ai-assistant.git
cd true-north-ai-assistant

# Install dependencies
npm install

# Build extension
npm run compile

# Package extension
npm run package

# Install packaged extension
code --install-extension true-north-agent-system-1.0.0.vsix
```

## Post-Installation Setup

### 1. Verify Installation
1. Restart VS Code
2. Open Command Palette (Ctrl+Shift+P)
3. Look for "TrueNorth" commands
4. Check status bar for TrueNorth indicator

### 2. Initial Configuration
Open VS Code Settings and configure:

```json
{
  "truenorth.claudeCommand": "claude",
  "truenorth.maxParallelAgents": 8,
  "truenorth.audioNotifications": true
}
```

### 3. Test Installation
1. Open a project folder in VS Code
2. Run "TrueNorth: Test Claude CLI" from Command Palette
3. You should see: "✅ Claude CLI is available and ready"

## Troubleshooting Installation

### Claude CLI Not Found
**Error**: `Claude CLI not found`

**Solutions**:
```bash
# Check if Claude is in PATH
which claude

# Add to PATH if needed (macOS/Linux)
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# For Windows, add to System PATH
```

### Permission Denied
**Error**: `Permission denied`

**Solutions**:
```bash
# Make Claude executable
chmod +x /usr/local/bin/claude

# Or run with sudo
sudo claude --version
```

### Extension Not Loading
**Error**: Extension fails to activate

**Solutions**:
1. Check VS Code version: `code --version`
2. Restart VS Code completely
3. Check Developer Console: Help > Toggle Developer Tools
4. Reinstall extension

### Network Issues
**Error**: Claude API connection fails

**Solutions**:
1. Check internet connection
2. Verify Claude API credentials: `claude auth status`
3. Check firewall settings
4. Try: `claude auth login` to re-authenticate

### Memory Issues
**Error**: High memory usage or crashes

**Solutions**:
1. Reduce `maxParallelAgents` in settings
2. Close other VS Code windows
3. Increase system memory
4. Monitor usage in Activity Monitor/Task Manager

## Platform-Specific Instructions

### Windows Subsystem for Linux (WSL)
```bash
# Install Claude CLI in WSL
curl -sSL https://claude.ai/install | bash

# Configure VS Code to use WSL Claude
# In VS Code settings:
"truenorth.claudeCommand": "/usr/local/bin/claude"
```

### Docker Environment
```dockerfile
# Add to Dockerfile
RUN curl -sSL https://claude.ai/install | bash
RUN npm install -g @vscode/vsce

# Install extension in container
COPY true-north-agent-system-1.0.0.vsix /tmp/
RUN code --install-extension /tmp/true-north-agent-system-1.0.0.vsix
```

### Remote Development
For VS Code Remote Development:

1. Install TrueNorth on remote machine
2. Install Claude CLI on remote machine
3. Configure remote settings
4. Test connection: `claude --version`

## Updating TrueNorth

### Automatic Updates
VS Code will automatically update TrueNorth when new versions are available.

### Manual Updates
```bash
# Download latest version
wget https://github.com/truenorth/releases/latest/download/true-north-agent-system-latest.vsix

# Uninstall current version
code --uninstall-extension truenorth.true-north-agent-system

# Install new version
code --install-extension true-north-agent-system-latest.vsix
```

## Uninstalling TrueNorth

### Via VS Code
1. Go to Extensions (Ctrl+Shift+X)
2. Find "TrueNorth Agent System"
3. Click "Uninstall"

### Via Command Line
```bash
code --uninstall-extension truenorth.true-north-agent-system
```

### Clean Uninstall
Remove all configuration and data:
```bash
# Remove extension
code --uninstall-extension truenorth.true-north-agent-system

# Remove configuration (optional)
# Location varies by OS:
# Windows: %APPDATA%/Code/User/settings.json
# macOS: ~/Library/Application Support/Code/User/settings.json
# Linux: ~/.config/Code/User/settings.json

# Remove workspace settings
rm .vscode/settings.json  # If TrueNorth-specific
```

## Verification Checklist

After installation, verify these items:

- [ ] Claude CLI installed and accessible (`claude --version`)
- [ ] Claude CLI authenticated (`claude auth status`)
- [ ] TrueNorth extension visible in VS Code Extensions
- [ ] TrueNorth commands available in Command Palette
- [ ] Status bar shows TrueNorth indicator
- [ ] Test command works: "TrueNorth: Test Claude CLI"
- [ ] Can open dashboard: "TrueNorth: Open Dashboard"

## Getting Help

### Documentation
- [Quick Start Guide](./quick-start.md) - Get started quickly
- [Configuration Guide](./configuration.md) - Detailed configuration
- [Troubleshooting](../troubleshooting/common-issues.md) - Common problems

### Support Channels
- **GitHub Issues**: [Report problems](https://github.com/truenorth/issues)
- **Discussions**: [Ask questions](https://github.com/truenorth/discussions)
- **Claude CLI Support**: [Claude.ai documentation](https://claude.ai/code)

### Common Support Information
When requesting help, please provide:
- Operating system and version
- VS Code version (`code --version`)
- TrueNorth extension version
- Claude CLI version (`claude --version`)
- Error messages from Developer Console
- Steps to reproduce the issue

---

**Next Steps**: Once installed, check out the [Quick Start Guide](./quick-start.md) to deploy your first AI agents!