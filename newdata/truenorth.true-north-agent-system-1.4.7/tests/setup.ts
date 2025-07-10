// Mock console to prevent test noise
const mockConsole = {
  log: jest.fn(),
  warn: jest.fn(),
  error: jest.fn(),
  info: jest.fn(),
  debug: jest.fn(),
};

global.console = {
  ...console,
  ...mockConsole,
};

// Mock VSCode extension context
const mockExtensionContext = {
  subscriptions: [] as any[],
  workspaceState: {
    get: jest.fn(),
    update: jest.fn(),
  },
  globalState: {
    get: jest.fn(),
    update: jest.fn(),
  },
  extensionPath: '/mock/extension/path',
  storagePath: '/mock/storage/path',
  globalStoragePath: '/mock/global/storage/path',
  logPath: '/mock/log/path',
  extensionUri: { fsPath: '/mock/extension/path' },
  environmentVariableCollection: {
    persistent: true,
    replace: jest.fn(),
    append: jest.fn(),
    prepend: jest.fn(),
    get: jest.fn(),
    forEach: jest.fn(),
    delete: jest.fn(),
    clear: jest.fn(),
  },
  secrets: {
    get: jest.fn(),
    store: jest.fn(),
    delete: jest.fn(),
    onDidChange: jest.fn(),
  },
};

// Make mock context globally available
(global as any).mockExtensionContext = mockExtensionContext;

// Mock workspace
const mockWorkspace = {
  workspaceFolders: [
    {
      uri: { fsPath: '/mock/workspace' },
      name: 'mock-workspace',
      index: 0,
    },
  ],
  getConfiguration: jest.fn(() => ({
    get: jest.fn(),
    update: jest.fn(),
    has: jest.fn(),
    inspect: jest.fn(),
  })),
};

(global as any).mockWorkspace = mockWorkspace;

// Global test setup
beforeEach(() => {
  jest.clearAllMocks();
  // Reset timers for each test
  jest.clearAllTimers();
});

afterEach(() => {
  jest.restoreAllMocks();
  // Clean up any pending timers
  jest.runOnlyPendingTimers();
  jest.useRealTimers();
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.warn('Unhandled Promise Rejection:', reason);
});

// Mock Node.js modules that cause issues in tests
jest.mock('fs', () => ({
  promises: {
    readFile: jest.fn(),
    writeFile: jest.fn(),
    mkdir: jest.fn(),
    stat: jest.fn(),
    access: jest.fn(),
  },
  readFileSync: jest.fn(),
  writeFileSync: jest.fn(),
  existsSync: jest.fn(),
  mkdirSync: jest.fn(),
}));

jest.mock('path', () => ({
  join: jest.fn((...args) => args.join('/')),
  resolve: jest.fn((...args) => '/' + args.join('/')),
  dirname: jest.fn(),
  basename: jest.fn(),
  extname: jest.fn(),
}));

// Mock child_process to prevent actual process spawning
jest.mock('child_process', () => ({
  spawn: jest.fn(),
  exec: jest.fn(),
  execSync: jest.fn(),
}));