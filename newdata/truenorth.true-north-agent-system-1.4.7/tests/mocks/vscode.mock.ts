import { jest } from '@jest/globals';

export const mockVSCode = {
  workspace: {
    getConfiguration: jest.fn().mockReturnValue({
      get: jest.fn(),
      update: jest.fn(),
      has: jest.fn(),
      inspect: jest.fn()
    }),
    workspaceFolders: [
      {
        uri: { fsPath: '/test/workspace' },
        name: 'test-workspace',
        index: 0
      }
    ],
    onDidChangeConfiguration: jest.fn(),
    openTextDocument: jest.fn(),
    saveAll: jest.fn()
  },
  window: {
    showInformationMessage: jest.fn(),
    showWarningMessage: jest.fn(),
    showErrorMessage: jest.fn(),
    showQuickPick: jest.fn(),
    showInputBox: jest.fn(),
    createStatusBarItem: jest.fn().mockReturnValue({
      text: '',
      tooltip: '',
      command: '',
      show: jest.fn(),
      hide: jest.fn(),
      dispose: jest.fn()
    }),
    createWebviewPanel: jest.fn().mockReturnValue({
      webview: {
        html: '',
        postMessage: jest.fn(),
        onDidReceiveMessage: jest.fn()
      },
      onDidDispose: jest.fn(),
      dispose: jest.fn()
    }),
    createOutputChannel: jest.fn().mockReturnValue({
      append: jest.fn(),
      appendLine: jest.fn(),
      clear: jest.fn(),
      show: jest.fn(),
      hide: jest.fn(),
      dispose: jest.fn()
    })
  },
  commands: {
    registerCommand: jest.fn(),
    executeCommand: jest.fn()
  },
  Uri: {
    file: jest.fn().mockImplementation((path: any) => ({ fsPath: path })),
    parse: jest.fn()
  },
  ViewColumn: {
    One: 1,
    Two: 2,
    Three: 3
  },
  StatusBarAlignment: {
    Left: 1,
    Right: 2
  },
  ThemeColor: jest.fn().mockImplementation((id: string) => ({ id })),
  Disposable: jest.fn().mockImplementation(() => ({
    dispose: jest.fn()
  })),
  EventEmitter: jest.fn().mockImplementation(() => ({
    event: jest.fn(),
    fire: jest.fn(),
    dispose: jest.fn()
  }))
};

export const createMockContext = () => ({
  subscriptions: [] as any[],
  workspaceState: {
    keys: jest.fn().mockReturnValue([]),
    get: jest.fn(),
    update: jest.fn()
  },
  globalState: {
    keys: jest.fn().mockReturnValue([]),
    get: jest.fn(),
    update: jest.fn(),
    setKeysForSync: jest.fn()
  },
  extensionUri: { fsPath: '/test/extension' },
  extensionPath: '/test/extension',
  storagePath: '/test/storage',
  globalStoragePath: '/test/global-storage',
  logPath: '/test/logs',
  environmentVariableCollection: {
    persistent: true,
    replace: jest.fn(),
    append: jest.fn(),
    prepend: jest.fn(),
    get: jest.fn(),
    forEach: jest.fn(),
    delete: jest.fn(),
    clear: jest.fn()
  },
  secrets: {
    get: jest.fn(),
    store: jest.fn(),
    delete: jest.fn(),
    onDidChange: jest.fn()
  },
  extension: {
    id: 'test.extension',
    extensionUri: { fsPath: '/test/extension' },
    extensionPath: '/test/extension',
    isActive: true,
    packageJSON: {},
    exports: undefined as any
  }
});

// Global mock context for easy access
export const mockContext = createMockContext();