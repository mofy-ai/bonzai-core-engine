# TrueNorth Testing Framework

## Overview

This comprehensive testing framework provides 90%+ code coverage and automated test execution for the TrueNorth extension. The framework includes unit tests, integration tests, end-to-end tests, performance benchmarks, security validation, and CI/CD integration.

## Test Structure

```
tests/
├── e2e/                     # End-to-end tests
│   └── agent-orchestration.test.ts
├── integration/             # Integration tests
│   └── claude-cli.integration.test.ts
├── mocks/                   # Mock implementations
│   ├── claude-cli.mock.ts
│   ├── vscode.mock.ts
│   └── websocket.mock.ts
├── performance/             # Performance benchmarks
│   └── agent-performance.test.ts
├── security/                # Security validation
│   └── security-validation.test.ts
├── unit/                    # Unit tests
│   ├── core/
│   │   ├── ConfigManager.test.ts
│   │   └── ClaudeCliManager.test.ts
│   └── websocket/
│       └── websocket-communication.test.ts
├── utils/                   # Testing utilities
│   └── test-helpers.ts
├── setup.ts                 # Global test setup
├── test-runner.ts           # Custom test runner
└── README.md               # This file
```

## Running Tests

### Quick Start

```bash
# Run all tests
npm test

# Run specific test suites
npm run test:unit
npm run test:integration
npm run test:e2e
npm run test:performance
npm run test:security

# Run with coverage
npm run test:coverage

# Watch mode for development
npm run test:watch
```

### Advanced Usage

```bash
# Run specific test suite
npm run test:suite unit
npm run test:suite performance

# Run tests for CI/CD
npm run test:ci

# Run all Jest tests directly
npm run test:all
```

## Test Categories

### 1. Unit Tests (`tests/unit/`)

Tests individual components in isolation with comprehensive mocking.

**Coverage Areas:**
- ConfigManager: Configuration validation, caching, encryption
- ClaudeCliManager: Command execution, session management, error handling
- WebSocket Communication: Message handling, connection lifecycle

**Key Features:**
- 95%+ code coverage for core modules
- Comprehensive error scenario testing
- Performance validation
- Memory leak detection

### 2. Integration Tests (`tests/integration/`)

Tests component interactions and external dependencies.

**Coverage Areas:**
- Claude CLI integration workflows
- Configuration system integration
- Real-world command execution scenarios
- Error recovery mechanisms

**Key Features:**
- End-to-end command execution
- Session state management
- Concurrent operation handling
- Network failure simulation

### 3. End-to-End Tests (`tests/e2e/`)

Tests complete workflows from user action to final result.

**Coverage Areas:**
- Full project analysis workflows
- Agent orchestration scenarios
- Dashboard real-time monitoring
- Multi-agent coordination

**Key Features:**
- Complete workflow validation
- Real-time monitoring verification
- Failure recovery testing
- Resource optimization validation

### 4. Performance Tests (`tests/performance/`)

Benchmarks system performance and identifies bottlenecks.

**Coverage Areas:**
- Command execution performance
- Memory usage optimization
- Concurrent operation scaling
- Cache performance

**Key Metrics:**
- Average execution time < 3 seconds
- Memory increase < 100MB during extended operation
- 80%+ success rate under load
- Throughput scaling with concurrency

### 5. Security Tests (`tests/security/`)

Validates security measures and prevents vulnerabilities.

**Coverage Areas:**
- Input validation and sanitization
- Command injection prevention
- Path traversal protection
- Sensitive data encryption

**Security Validations:**
- XSS prevention
- SQL injection protection
- File system access restrictions
- Network security validations

### 6. WebSocket Tests (`tests/unit/websocket/`)

Tests real-time communication infrastructure.

**Coverage Areas:**
- Connection establishment and lifecycle
- Message transmission and formatting
- Dashboard communication protocol
- Error handling and recovery

## Mocking System

### VSCode API (`tests/mocks/vscode.mock.ts`)

Comprehensive mock of VSCode extension API:
- Workspace management
- Configuration access
- UI components (status bar, webview panels)
- Command registration and execution

### Claude CLI (`tests/mocks/claude-cli.mock.ts`)

Mock implementation of Claude CLI interactions:
- Command execution simulation
- Process management
- Response generation
- Error scenario simulation

### WebSocket (`tests/mocks/websocket.mock.ts`)

Mock WebSocket implementation:
- Connection simulation
- Message handling
- Event emission
- Error simulation

## Testing Utilities

### Test Helpers (`tests/utils/test-helpers.ts`)

Common utilities for test implementation:
- `waitFor(ms)`: Async delay utility
- `waitForCondition()`: Condition polling
- `createPerformanceBenchmark()`: Performance measurement
- `generateTestData`: Test data generation
- `assertEventuallyEquals()`: Eventual consistency testing

## Configuration

### Jest Configuration (`jest.config.js`)

- TypeScript support with ts-jest
- Multi-project setup for different test types
- Coverage thresholds (80% minimum)
- Custom test environment setup
- Parallel test execution

### Coverage Requirements

- **Lines**: 80% minimum
- **Functions**: 80% minimum  
- **Branches**: 80% minimum
- **Statements**: 80% minimum

Current coverage targets 90%+ for critical modules.

## CI/CD Integration

### GitHub Actions (`.github/workflows/test.yml`)

Automated testing pipeline:
- Lint and static analysis
- Unit test execution
- Integration test validation
- Performance benchmarking
- Security scanning
- E2E test verification
- Coverage reporting

### Test Runner (`tests/test-runner.ts`)

Custom test orchestration:
- Parallel and sequential execution
- Timeout management
- Result aggregation
- Coverage reporting
- CI/CD integration

## Performance Benchmarks

### Target Metrics

- **Single Command**: < 3 seconds average
- **Concurrent Commands**: > 0.5 ops/second
- **Memory Usage**: < 100MB increase over 200 operations
- **Startup Time**: < 2 seconds for core systems
- **Cache Performance**: > 90% hit rate for configurations

### Monitoring

Performance tests continuously monitor:
- Execution time distribution
- Memory usage patterns
- Resource utilization
- Throughput scaling
- Error rates under load

## Security Validation

### Input Validation

- Path traversal prevention
- Command injection protection
- XSS sanitization
- Template injection blocking

### Data Protection

- Sensitive data encryption
- Secure storage practices
- Export data redaction
- Access control validation

### Network Security

- URL validation
- DNS rebinding protection
- Connection restriction
- Protocol validation

## Development Guidelines

### Writing Tests

1. **Follow the AAA Pattern**: Arrange, Act, Assert
2. **Use Descriptive Names**: Test names should explain what is being tested
3. **Mock External Dependencies**: Use provided mocks for consistent testing
4. **Test Error Scenarios**: Include failure cases and edge conditions
5. **Validate Performance**: Include timing assertions for critical paths

### Best Practices

```typescript
describe('Component Name', () => {
  let component: ComponentType;
  
  beforeEach(() => {
    // Setup test environment
    component = new ComponentType(mockDependencies);
  });
  
  afterEach(() => {
    // Cleanup resources
    component.dispose();
  });
  
  describe('method name', () => {
    it('should handle normal operation successfully', async () => {
      // Arrange
      const input = generateTestData.validInput();
      
      // Act
      const result = await component.method(input);
      
      // Assert
      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
    });
    
    it('should handle error conditions gracefully', async () => {
      // Test error scenarios
    });
    
    it('should meet performance requirements', async () => {
      // Performance validation
    });
  });
});
```

### Mock Usage

```typescript
import { mockVSCode, createMockContext } from '../mocks/vscode.mock';
import { mockClaudeCliManager } from '../mocks/claude-cli.mock';

// Setup mocks
const mockContext = createMockContext();
mockClaudeCliManager.executeClaudeCommand.mockResolvedValue(
  createMockClaudeResponse('Success')
);
```

## Troubleshooting

### Common Issues

1. **Test Timeouts**: Increase timeout for slow operations
2. **Mock Conflicts**: Ensure proper mock cleanup between tests
3. **Memory Issues**: Use `beforeEach`/`afterEach` for proper cleanup
4. **Async Issues**: Use proper `await` and `waitForCondition`

### Debugging

```bash
# Run tests with verbose output
npm run test:all -- --verbose

# Debug specific test file
npm run test:all -- --testNamePattern="specific test name"

# Run with coverage details
npm run test:coverage -- --verbose
```

### Performance Issues

```bash
# Run performance tests only
npm run test:performance

# Monitor memory usage
node --expose-gc npm run test:all
```

## Contributing

1. **Add tests for new features**: All new code must include comprehensive tests
2. **Maintain coverage**: Ensure coverage thresholds are met
3. **Update documentation**: Keep test documentation current
4. **Run full suite**: Execute all tests before submitting changes

## Support

For testing framework issues or questions:
1. Check existing test examples
2. Review mock implementations
3. Consult test utilities documentation
4. Create detailed issue reports with test reproduction steps