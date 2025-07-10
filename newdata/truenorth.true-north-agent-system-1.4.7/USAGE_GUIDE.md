# TrueNorth Extension - Complete Usage Guide

## 🚀 Quick Start

### Installation

1. **Install from VSIX file**: Open VSCode → Extensions → Install from VSIX → Select `true-north-agent-system-1.0.0.vsix`
2. **Restart VSCode** to activate the extension
3. **Verify installation**: Look for the 🧭 TrueNorth icon in the Activity Bar

### Prerequisites

- **Claude CLI must be installed and configured**
- Test required command: `claude --dangerously-skip-permissions --model sonnet -p "test"`
- If this fails, TrueNorth will not work

## 📋 Core Features

### 1. TrueNorth Sidebar

- **Location**: Activity Bar (🧭 compass icon)
- **Sections**:
  - Project Status (shows running/completed/failed agents)
  - Quick Actions (most common operations)
  - Agent Categories (Analysis, Improvement, Deployment)

### 2. Four MVP Commands

#### 🚀 Launch Agents (`truenorth.launchAgents`)

- **Purpose**: Start the agent orchestration system
- **Usage**: Command Palette → "True North: 🚀 Launch Agents"
- **Keyboard**: `Ctrl+Alt+L` (Mac: `Cmd+Alt+L`)
- **What it does**: Initializes and runs intelligent code analysis agents

#### 🔍 Analyze Project (`truenorth.analyzeProject`)

- **Purpose**: Comprehensive project analysis using Claude CLI
- **Usage**: Command Palette → "True North: 🔍 Analyze Project"
- **Keyboard**: `Ctrl+Alt+A` (Mac: `Cmd+Alt+A`)
- **What it does**: Analyzes code architecture, quality, and suggests improvements

#### 🎛️ Open Dashboard (`truenorth.openDashboard`)

- **Purpose**: Launch real-time monitoring dashboard
- **Usage**: Command Palette → "True North: 🎛️ Open Dashboard"
- **Keyboard**: `Ctrl+Alt+D` (Mac: `Cmd+Alt+D`)
- **What it does**: Opens WebSocket dashboard at http://localhost:8080 (or next available port)

#### 🛑 Stop All Agents (`truenorth.stopAllAgents`)

- **Purpose**: Emergency stop for all running operations
- **Usage**: Command Palette → "True North: 🛑 Stop All Agents"
- **What it does**: Cleanly stops all running Claude CLI sessions and agents

## 🎯 Common Workflows

### Workflow 1: Project Analysis

1. Open your project in VSCode
2. Click TrueNorth sidebar (🧭)
3. Click "Quick Analysis" or use `Ctrl+Alt+A`
4. View results in the output panel
5. Open dashboard for real-time monitoring: `Ctrl+Alt+D`

### Workflow 2: Code Cleanup

1. Run "🚀 Launch Agents" to start the orchestration system
2. Use sidebar to select specific improvement agents
3. Monitor progress in the dashboard
4. Stop when complete with "🛑 Stop All Agents"

### Workflow 3: Dashboard Monitoring

1. Open dashboard: `Ctrl+Alt+D`
2. Dashboard shows:
   - System status (Connected/Disconnected)
   - Active tasks and progress
   - Real-time activity logs
3. WebSocket connection provides live updates

## ⚙️ Configuration

### Extension Settings

Access via: Settings → Extensions → True North Agent System

- **truenorth.claudeCommand**: Path to Claude CLI (default: "claude")
- **truenorth.maxAgents**: Max simultaneous agents (default: 5)
- **truenorth.dashboardPort**: Dashboard port (default: 8080)
- **truenorth.timeout**: Claude CLI timeout in ms (default: 120000)

### VSCode Settings Example

```json
{
  "truenorth.claudeCommand": "claude",
  "truenorth.maxAgents": 5,
  "truenorth.dashboardPort": 8080,
  "truenorth.timeout": 120000
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "Claude CLI not found"

**Problem**: Extension can't find Claude CLI
**Solution**:

```bash
# Verify Claude CLI is installed
claude --version

# If not installed:
curl -sSL https://claude.ai/install | bash

# Test required command:
claude --dangerously-skip-permissions --model sonnet -p "test"
```

#### 2. "Failed to start dashboard"

**Problem**: Dashboard won't start (port conflict)
**Solution**:

- Check if port 8080 is in use: `lsof -i :8080`
- Change port in settings: `truenorth.dashboardPort`
- Or let TrueNorth auto-find available port

#### 3. "No workspace folder found"

**Problem**: Commands disabled
**Solution**: Open a folder/project in VSCode (File → Open Folder)

#### 4. Extension not activating

**Problem**: TrueNorth sidebar missing
**Solution**:

1. Check Extensions view - ensure TrueNorth is enabled
2. Reload window: `Ctrl+Shift+P` → "Developer: Reload Window"
3. Check output panel for error messages

### Debug Information

- **Output Panel**: View → Output → Select "True North"
- **Developer Tools**: Help → Toggle Developer Tools
- **Extension Host**: Check for errors in Console tab

## 📖 Command Reference

### Command Palette Commands

- `True North: 🚀 Launch Agents` - Start agent orchestration
- `True North: 🔍 Analyze Project` - Run project analysis
- `True North: 🎛️ Open Dashboard` - Open monitoring dashboard
- `True North: 🛑 Stop All Agents` - Stop all operations

### Keyboard Shortcuts

- `Ctrl+Alt+L` (Mac: `Cmd+Alt+L`) - Launch Agents
- `Ctrl+Alt+A` (Mac: `Cmd+Alt+A`) - Analyze Project
- `Ctrl+Alt+D` (Mac: `Cmd+Alt+D`) - Open Dashboard

### Context Menu

Right-click on folders in Explorer:

- "True North: Analyze Project"
- "True North: Launch Agents"
- "True North: Open Dashboard"

## 🚀 Advanced Usage

### Custom Claude CLI Path

If Claude CLI is installed in a custom location:

```json
{
  "truenorth.claudeCommand": "/custom/path/to/claude"
}
```

### Multiple Projects

- TrueNorth works per-workspace
- Each workspace has independent agent sessions
- Dashboard shows current workspace status

### Performance Tuning

- Reduce `truenorth.maxAgents` for slower systems
- Increase `truenorth.timeout` for complex projects
- Use `truenorth.dashboardPort` to avoid conflicts

## 📊 Dashboard Features

### Real-time Monitoring

- **System Status**: Connection health indicator
- **Agent Counts**: Running/Completed/Failed statistics
- **Activity Log**: Timestamped events and updates
- **Task Progress**: Live progress bars for active operations

### WebSocket Connection

- Automatic reconnection on disconnect
- Real-time updates without page refresh
- Responsive design works on any screen size

## 🔐 Security Notes

- TrueNorth uses `--dangerously-skip-permissions` for automation
- Only operates on local workspace files
- No external network requests beyond Claude API
- All operations are logged and transparent

## 💡 Tips & Best Practices

1. **Start with Analysis**: Always run "Analyze Project" first
2. **Monitor Dashboard**: Keep dashboard open for real-time feedback
3. **Use Keyboard Shortcuts**: Faster than Command Palette
4. **Check Output**: View detailed logs in Output panel
5. **Stop When Done**: Use "Stop All Agents" to clean up resources

## 🆘 Getting Help

- **Issue Tracking**: Check VSCode Developer Console for errors
- **Extension Logs**: View → Output → True North
- **Claude CLI Issues**: Test `claude --dangerously-skip-permissions --model sonnet -p "test"`
- **Reset Extension**: Disable/Enable in Extensions view

---

**Ready to go!** Your TrueNorth extension is now installed and ready for intelligent code analysis with Claude CLI integration.
