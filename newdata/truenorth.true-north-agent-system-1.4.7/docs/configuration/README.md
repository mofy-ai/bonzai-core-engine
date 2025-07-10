# TrueNorth Configuration Management

This document provides comprehensive documentation for the TrueNorth Agent System configuration management features.

## Table of Contents

1. [Overview](#overview)
2. [Configuration Structure](#configuration-structure)
3. [Environment-Specific Configurations](#environment-specific-configurations)
4. [Configuration Schema](#configuration-schema)
5. [Validation](#validation)
6. [Hot Reloading](#hot-reloading)
7. [Backup and Restore](#backup-and-restore)
8. [Migration](#migration)
9. [CLI Commands](#cli-commands)
10. [Best Practices](#best-practices)

## Overview

The TrueNorth configuration system provides:

- **Environment-specific configurations** (development, staging, production, test)
- **JSON Schema validation** with custom business rules
- **Hot reloading** with file watching
- **Backup and restore** capabilities
- **Configuration migration** with version control
- **CLI interface** for configuration management
- **Encryption** for sensitive values
- **Audit logging** for compliance

## Configuration Structure

Configuration files are organized in the following structure:

```
config/
├── environments/
│   ├── development.json
│   ├── staging.json
│   ├── production.json
│   └── test.json
├── schemas/
│   └── config.schema.json
├── backups/
│   └── *.json
└── migrations/
    └── *.js
```

### Base Configuration

All configuration files follow this basic structure:

```json
{
  "$schema": "../schemas/config.schema.json",
  "environment": "development",
  "claudeCommand": "claude",
  "maxParallelAgents": 4,
  "audioNotifications": true,
  "dashboardPort": 3891,
  "autoAnalyzeOnOpen": true,
  "sessionTimeout": 300000,
  "maxRetries": 3,
  "logLevel": "debug",
  "hotReload": true
}
```

## Environment-Specific Configurations

### Development Environment

```json
{
  "environment": "development",
  "logLevel": "debug",
  "maxParallelAgents": 4,
  "hotReload": true,
  "autoAnalyzeOnOpen": true,
  "performance": {
    "cacheEnabled": true,
    "cacheTtl": 30000,
    "compressionEnabled": false
  }
}
```

### Staging Environment

```json
{
  "environment": "staging",
  "logLevel": "info",
  "maxParallelAgents": 6,
  "hotReload": true,
  "autoAnalyzeOnOpen": false,
  "performance": {
    "cacheEnabled": true,
    "cacheTtl": 60000,
    "compressionEnabled": true
  }
}
```

### Production Environment

```json
{
  "environment": "production",
  "logLevel": "warn",
  "maxParallelAgents": 12,
  "hotReload": false,
  "autoAnalyzeOnOpen": false,
  "performance": {
    "cacheEnabled": true,
    "cacheTtl": 300000,
    "compressionEnabled": true
  },
  "security": {
    "encryptionEnabled": true,
    "auditLogging": true,
    "sensitiveDataMasking": true
  }
}
```

### Test Environment

```json
{
  "environment": "test",
  "logLevel": "error",
  "maxParallelAgents": 2,
  "hotReload": false,
  "sessionTimeout": 30000,
  "maxRetries": 1,
  "monitoring": {
    "enabled": false,
    "metricsCollection": false
  }
}
```

## Configuration Schema

The configuration schema defines the structure and validation rules for all configuration options.

### Core Settings

| Setting | Type | Required | Description |
|---------|------|----------|-------------|
| `environment` | string | Yes | Current environment (development, staging, production, test) |
| `claudeCommand` | string | Yes | Path to Claude CLI command |
| `maxParallelAgents` | integer | Yes | Maximum number of agents running simultaneously (1-50) |
| `audioNotifications` | boolean | No | Enable audio notifications for agent status |
| `dashboardPort` | integer | No | Port for the dashboard web interface (1024-65535) |
| `autoAnalyzeOnOpen` | boolean | No | Automatically analyze project when workspace opens |
| `sessionTimeout` | integer | No | Session timeout in milliseconds (1000-3600000) |
| `maxRetries` | integer | No | Maximum retry attempts (0-10) |
| `logLevel` | string | Yes | Logging level (debug, info, warn, error) |
| `hotReload` | boolean | No | Enable hot reload for configuration changes |

### Accessibility Settings

```json
{
  "accessibility": {
    "screenReader": true,
    "highContrast": false,
    "largeText": false,
    "reducedMotion": false,
    "voiceControl": false,
    "keyboardNavigation": true,
    "colorBlindnessFilter": "none",
    "theme": "default",
    "focusIndicatorStyle": "default",
    "notifications": {
      "screenReader": true,
      "soundAlerts": true,
      "visualAlerts": true,
      "soundVolume": 0.7,
      "duration": 5000,
      "maxSimultaneous": 3,
      "priorityFiltering": true
    }
  }
}
```

### Enterprise Settings

```json
{
  "enterprise": {
    "sso": {
      "enabled": false,
      "provider": "azure",
      "config": {}
    },
    "multiTenant": {
      "enabled": false,
      "isolationLevel": "strict"
    },
    "compliance": {
      "framework": "soc2",
      "auditLogging": true,
      "dataRetentionDays": 365
    }
  }
}
```

### Monitoring Settings

```json
{
  "monitoring": {
    "enabled": true,
    "metricsCollection": true,
    "performanceTracking": true,
    "errorReporting": true,
    "healthChecks": {
      "enabled": true,
      "interval": 30000,
      "timeout": 5000
    }
  }
}
```

### Security Settings

```json
{
  "security": {
    "encryptionEnabled": true,
    "auditLogging": true,
    "sensitiveDataMasking": true,
    "rateLimiting": {
      "enabled": true,
      "windowMs": 900000,
      "maxRequests": 100
    }
  }
}
```

### Performance Settings

```json
{
  "performance": {
    "cacheEnabled": true,
    "cacheTtl": 30000,
    "maxCacheSize": 100,
    "compressionEnabled": false,
    "concurrency": {
      "maxConcurrentOperations": 10,
      "queueSize": 100
    }
  }
}
```

### Integration Settings

```json
{
  "integrations": {
    "github": {
      "enabled": false,
      "token": "ghp_...",
      "webhookSecret": "..."
    },
    "slack": {
      "enabled": false,
      "webhookUrl": "https://hooks.slack.com/services/...",
      "channel": "#truenorth"
    }
  }
}
```

### Feature Flags

```json
{
  "features": {
    "advancedAnalytics": false,
    "quantumComputing": false,
    "aiModels": true,
    "iotIntegration": false,
    "mobileSupport": false,
    "enterpriseMode": false
  }
}
```

## Validation

The configuration system includes comprehensive validation:

### JSON Schema Validation

- **Structure validation**: Ensures required fields are present
- **Type validation**: Verifies data types (string, number, boolean, etc.)
- **Range validation**: Checks numeric ranges and string patterns
- **Enum validation**: Validates allowed values for specific fields

### Custom Business Rules

- **Environment consistency**: Validates environment-specific settings
- **Security requirements**: Ensures security settings are appropriate
- **Performance optimization**: Checks performance configuration
- **Resource limits**: Validates resource allocation
- **Accessibility compliance**: Ensures accessibility standards
- **Integration compatibility**: Validates external integrations

### Validation Examples

```typescript
// Validate configuration programmatically
const validator = new ConfigurationValidator(schemaPath);
const result = await validator.validateConfiguration(config, 'production');

if (!result.isValid) {
  console.error('Validation errors:', result.errors);
  console.warn('Validation warnings:', result.warnings);
}
```

## Hot Reloading

Configuration hot reloading automatically detects and applies configuration changes without restarting the application.

### Features

- **File watching**: Monitors configuration files for changes
- **Debounced reloading**: Prevents excessive reloads during rapid changes
- **Change notifications**: Notifies components of configuration updates
- **Error handling**: Gracefully handles invalid configurations

### Configuration

```json
{
  "hotReload": true,
  "hotReloadConfig": {
    "enabled": true,
    "debounceMs": 500,
    "watchPaths": ["./config"],
    "excludePaths": ["*.tmp", "*.bak"]
  }
}
```

## Backup and Restore

### Creating Backups

```typescript
// Create manual backup
const backupId = await configManager.createBackup('Manual backup before changes');

// Automatic backups are created before:
// - Configuration imports
// - Migrations
// - Bulk updates
```

### Restoring Backups

```typescript
// List available backups
const backups = await configManager.listBackups();

// Restore from backup
await configManager.restoreBackup(backupId);
```

### Backup Structure

```json
{
  "version": "2.0.0",
  "timestamp": "2023-12-07T10:30:00.000Z",
  "environment": "production",
  "hash": "sha256-hash-of-config",
  "configuration": { /* configuration object */ },
  "metadata": {
    "creator": "system",
    "description": "Pre-migration backup",
    "automated": true
  }
}
```

## Migration

Configuration migrations handle version upgrades and schema changes.

### Migration Process

1. **Check current version**: Determine configuration version
2. **Identify migrations**: Find applicable migrations
3. **Create backup**: Automatic backup before migration
4. **Apply migrations**: Sequential application of changes
5. **Validate results**: Ensure migration success
6. **Update version**: Set new configuration version

### Migration Example

```typescript
// Check if migration is needed
const migrationNeeded = await migration.isMigrationNeeded();

// Perform migration
const result = await migration.migrate();

if (result.success) {
  console.log('Migration completed successfully');
} else {
  console.error('Migration failed:', result.errors);
}
```

### Custom Migrations

```typescript
// Add custom migration
migration.addMigration({
  version: '2.1.0',
  description: 'Add new feature configuration',
  up: (config) => {
    config.newFeature = { enabled: false };
    return config;
  },
  down: (config) => {
    delete config.newFeature;
    return config;
  },
  validate: (config) => config.newFeature !== undefined
});
```

## CLI Commands

The configuration CLI provides command-line access to configuration operations.

### Basic Commands

```bash
# Get configuration value
config get --key claudeCommand --environment production

# Set configuration value
config set --key maxParallelAgents --value 8 --environment staging

# Validate configuration
config validate --environment production --format markdown

# Show configuration health
config health
```

### Backup Commands

```bash
# Create backup
config backup --description "Manual backup"

# List backups
config list-backups

# Restore backup
config restore --backupId backup-id-here
```

### Migration Commands

```bash
# Check migration status
config migration-status

# Perform migration
config migrate --version 2.0.0

# Rollback to previous version
config rollback --version 1.9.0
```

### Export/Import Commands

```bash
# Export configuration
config export --environment production --format json

# Import configuration
config import --data '{"key": "value"}' --environment development

# Reset to defaults
config reset --confirm
```

### Help Command

```bash
# Show all commands
config help

# Show command-specific help
config help validate
```

## Best Practices

### Environment Configuration

1. **Use environment-specific settings**: Configure different values for each environment
2. **Minimize production changes**: Keep production configurations stable
3. **Test configuration changes**: Validate in development/staging before production
4. **Document configuration**: Add descriptions for custom settings

### Security

1. **Encrypt sensitive values**: Use encryption for API keys and secrets
2. **Enable audit logging**: Track configuration changes
3. **Validate inputs**: Use schema validation for all configuration changes
4. **Backup before changes**: Always create backups before major changes

### Performance

1. **Use caching**: Enable caching for frequently accessed values
2. **Optimize cache TTL**: Balance freshness vs performance
3. **Monitor resource usage**: Track configuration impact on performance
4. **Enable compression**: Use compression in production environments

### Maintenance

1. **Regular backups**: Create periodic configuration backups
2. **Monitor health**: Check configuration health regularly
3. **Update schemas**: Keep validation schemas current
4. **Review migrations**: Test migrations thoroughly before deployment

### Development Workflow

1. **Version control**: Store configuration templates in version control
2. **Environment parity**: Keep environments as similar as possible
3. **Automated validation**: Include validation in CI/CD pipelines
4. **Documentation**: Maintain up-to-date configuration documentation

## Troubleshooting

### Common Issues

1. **Validation failures**: Check schema compliance and required fields
2. **Migration errors**: Verify configuration format and dependencies
3. **Hot reload not working**: Check file permissions and watch paths
4. **Backup corruption**: Verify backup integrity using hash validation

### Debugging

1. **Enable debug logging**: Set `logLevel` to `debug` for detailed logs
2. **Check health status**: Use `config health` command to identify issues
3. **Validate configuration**: Run validation to find specific problems
4. **Review audit logs**: Check configuration change history

### Performance Issues

1. **Disable unnecessary features**: Turn off unused monitoring/tracking
2. **Optimize cache settings**: Adjust cache size and TTL values
3. **Reduce hot reload sensitivity**: Increase debounce time
4. **Limit concurrent operations**: Adjust concurrency limits

For additional support, please refer to the [troubleshooting guide](../troubleshooting/configuration.md) or contact the development team.