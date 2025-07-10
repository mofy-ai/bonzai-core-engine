# TrueNorth Configuration Guide

This guide covers all configuration options available in TrueNorth Agent System, from basic settings to advanced customizations.

## Configuration Locations

TrueNorth uses VS Code's configuration system with multiple levels of settings:

### User Settings (Global)
- **Location**: VS Code User Settings
- **Scope**: Applies to all workspaces
- **Access**: File > Preferences > Settings > Extensions > TrueNorth

### Workspace Settings (Local)
- **Location**: `.vscode/settings.json` in your workspace
- **Scope**: Applies only to current workspace
- **Access**: Workspace Settings tab in VS Code Settings

### Example Workspace Configuration
```json
{
  \"truenorth.claudeCommand\": \"/usr/local/bin/claude\",
  \"truenorth.maxParallelAgents\": 12,
  \"truenorth.audioNotifications\": false,
  \"truenorth.dashboardPort\": 8080,
  \"truenorth.autoAnalyzeOnOpen\": true
}
```

## Core Configuration Options

### Claude CLI Settings

#### `truenorth.claudeCommand`
- **Type**: `string`
- **Default**: `\"claude\"`
- **Description**: Path to Claude CLI executable
- **Examples**:
  ```json
  \"truenorth.claudeCommand\": \"claude\"          // Global PATH
  \"truenorth.claudeCommand\": \"/usr/local/bin/claude\"  // Absolute path
  \"truenorth.claudeCommand\": \"./bin/claude\"   // Relative path
  ```

### Agent Management

#### `truenorth.maxParallelAgents`
- **Type**: `number`
- **Default**: `8`
- **Range**: `1-25`
- **Description**: Maximum number of agents running simultaneously
- **Impact**: Higher values = faster completion but more resource usage
- **Recommendations**:
  - **Small projects**: 4-6 agents
  - **Medium projects**: 8-12 agents
  - **Large projects**: 12-20 agents
  - **Enterprise**: 20-25 agents

### User Experience

#### `truenorth.audioNotifications`
- **Type**: `boolean`
- **Default**: `true`
- **Description**: Enable audio notifications for agent status changes
- **When disabled**: Only visual notifications in VS Code

#### `truenorth.autoAnalyzeOnOpen`
- **Type**: `boolean`
- **Default**: `false`
- **Description**: Automatically analyze project when opening workspace
- **Warning**: May slow down VS Code startup for large projects

### Dashboard Settings

#### `truenorth.dashboardPort`
- **Type**: `number`
- **Default**: `7777`
- **Range**: `1024-65535`
- **Description**: Port for TrueNorth dashboard server
- **Note**: Change if port is already in use

## Advanced Configuration

### Performance Tuning

#### Memory Management
```json
{
  \"truenorth.maxParallelAgents\": 6,
  \"truenorth.agentMemoryLimit\": \"512MB\",
  \"truenorth.sessionTimeout\": 300000,
  \"truenorth.cleanupInterval\": 60000
}
```

#### CPU Optimization
```json
{
  \"truenorth.cpuPriority\": \"normal\",
  \"truenorth.maxCpuUsage\": 80,
  \"truenorth.adaptiveThrottling\": true
}
```

### Security Configuration

#### Execution Security
```json
{
  \"truenorth.dangerouslySkipPermissions\": false,
  \"truenorth.allowFileModification\": true,
  \"truenorth.restrictedPaths\": [
    \"/etc\",
    \"/usr/bin\",
    \"~/.ssh\"
  ]
}
```

#### Network Security
```json
{
  \"truenorth.enableNetworkAccess\": true,
  \"truenorth.allowedDomains\": [
    \"api.anthropic.com\",
    \"claude.ai\"
  ],
  \"truenorth.proxySettings\": {
    \"enabled\": false,
    \"host\": \"\",
    \"port\": 0
  }
}
```

### Logging and Debugging

#### Log Configuration
```json
{
  \"truenorth.logLevel\": \"info\",
  \"truenorth.logToFile\": true,
  \"truenorth.logFilePath\": \"./logs/truenorth.log\",
  \"truenorth.maxLogSize\": \"10MB\",
  \"truenorth.enableDetailedLogging\": false
}
```

#### Debug Settings
```json
{
  \"truenorth.debugMode\": false,
  \"truenorth.verboseOutput\": false,
  \"truenorth.traceExecution\": false,
  \"truenorth.enableTelemetry\": true
}
```

## Project-Specific Configuration

### File Type Handling
```json
{
  \"truenorth.fileTypes\": {
    \"include\": [\"*.ts\", \"*.js\", \"*.py\", \"*.java\"],
    \"exclude\": [\"*.min.js\", \"*.d.ts\", \"node_modules/**\"],
    \"maxFileSize\": \"1MB\"
  }
}
```

### Task Customization
```json
{
  \"truenorth.customTasks\": {
    \"codeReview\": {
      \"enabled\": true,
      \"priority\": \"high\",
      \"timeout\": 600000
    },
    \"documentation\": {
      \"enabled\": true,
      \"format\": \"markdown\",
      \"includeExamples\": true
    }
  }
}
```

### Language-Specific Settings
```json
{
  \"truenorth.languageSettings\": {
    \"typescript\": {
      \"strictMode\": true,
      \"includeTypes\": true,
      \"lintOnAnalysis\": true
    },
    \"python\": {
      \"pythonPath\": \"/usr/bin/python3\",
      \"includeDocstrings\": true,
      \"formatStyle\": \"black\"
    }
  }
}
```

## Environment-Specific Configurations

### Development Environment
```json
{
  \"truenorth.environment\": \"development\",
  \"truenorth.maxParallelAgents\": 4,
  \"truenorth.debugMode\": true,
  \"truenorth.verboseOutput\": true,
  \"truenorth.autoAnalyzeOnOpen\": false
}
```

### CI/CD Environment
```json
{
  \"truenorth.environment\": \"ci\",
  \"truenorth.maxParallelAgents\": 2,
  \"truenorth.audioNotifications\": false,
  \"truenorth.headlessMode\": true,
  \"truenorth.exitOnCompletion\": true
}
```

### Production Environment
```json
{
  \"truenorth.environment\": \"production\",
  \"truenorth.maxParallelAgents\": 16,
  \"truenorth.enableTelemetry\": true,
  \"truenorth.performanceMonitoring\": true,
  \"truenorth.errorReporting\": true
}
```

## Configuration Validation

TrueNorth automatically validates your configuration on startup. Common validation errors:

### Invalid Claude CLI Path
```
Error: Claude CLI not found at path '/invalid/path/claude'
Solution: Update truenorth.claudeCommand to valid path
```

### Port Conflicts
```
Error: Dashboard port 7777 is already in use
Solution: Change truenorth.dashboardPort to available port
```

### Resource Limits
```
Warning: maxParallelAgents (50) exceeds recommended limit (25)
Solution: Reduce truenorth.maxParallelAgents for better performance
```

## Configuration Best Practices

### 1. Start Conservative
Begin with default settings and gradually increase:
```json
{
  \"truenorth.maxParallelAgents\": 4,  // Start low
  \"truenorth.sessionTimeout\": 120000  // 2 minutes
}
```

### 2. Monitor Resource Usage
Use dashboard to monitor system performance:
- CPU usage
- Memory consumption
- Network activity
- Disk I/O

### 3. Environment-Specific Configs
Create different configurations for different environments:
- `.vscode/settings.dev.json`
- `.vscode/settings.prod.json`
- `.vscode/settings.ci.json`

### 4. Version Control
**Include in Git**:
- `.vscode/settings.json` (workspace settings)
- `.vscode/truenorth.json` (TrueNorth-specific config)

**Exclude from Git**:
- User-specific paths
- API keys or secrets
- Local debugging settings

## Troubleshooting Configuration

### Check Current Configuration
```typescript
// Open VS Code Developer Console
// Run this command to see current config
vscode.workspace.getConfiguration('truenorth')
```

### Reset to Defaults
1. Open VS Code Settings
2. Search for \"TrueNorth\"
3. Click gear icon next to each setting
4. Select \"Reset Setting\"

### Configuration Conflicts
If settings don't take effect:
1. Check workspace vs user settings precedence
2. Reload VS Code window (`Ctrl+R`)
3. Verify JSON syntax in settings files
4. Check VS Code Developer Console for errors

## Configuration Templates

### Minimal Configuration
```json
{
  \"truenorth.claudeCommand\": \"claude\",
  \"truenorth.maxParallelAgents\": 4
}
```

### Power User Configuration
```json
{
  \"truenorth.claudeCommand\": \"/usr/local/bin/claude\",
  \"truenorth.maxParallelAgents\": 16,
  \"truenorth.audioNotifications\": true,
  \"truenorth.autoAnalyzeOnOpen\": true,
  \"truenorth.dashboardPort\": 8080,
  \"truenorth.logLevel\": \"debug\",
  \"truenorth.enableDetailedLogging\": true,
  \"truenorth.performanceMonitoring\": true
}
```

### Team Configuration
```json
{
  \"truenorth.claudeCommand\": \"claude\",
  \"truenorth.maxParallelAgents\": 8,
  \"truenorth.audioNotifications\": false,
  \"truenorth.enableTelemetry\": true,
  \"truenorth.logLevel\": \"info\",
  \"truenorth.restrictedPaths\": [\"/etc\", \"/usr\"],
  \"truenorth.allowFileModification\": true
}
```

---

**Next Steps**: 
- [Dashboard Guide](./dashboard.md) - Master the monitoring interface
- [Performance Optimization](../tutorials/performance-optimization.md) - Optimize for your setup
- [Troubleshooting](../troubleshooting/configuration.md) - Solve configuration issues