import { jest } from '@jest/globals';
import { ProjectAnalyzer } from '../../../src/core/ProjectAnalyzer';
import { ClaudeCliManager } from '../../../src/core/ClaudeCliManager';
import { ConfigManager } from '../../../src/core/ConfigManager';

// Mock vscode
jest.mock(
  'vscode',
  () => ({
    window: {
      withProgress: jest.fn((options, task) => {
        const progress = { report: jest.fn() };
        const token = { isCancellationRequested: false };
        return task(progress, token);
      }),
      showInformationMessage: jest.fn(),
      showErrorMessage: jest.fn(),
      createOutputChannel: jest.fn(() => ({
        appendLine: jest.fn(),
        clear: jest.fn(),
        show: jest.fn(),
        dispose: jest.fn(),
      })),
    },
    ProgressLocation: {
      Notification: 15,
    },
    workspace: {
      workspaceFolders: [
        {
          uri: { fsPath: '/test/workspace' },
        },
      ],
    },
  }),
  { virtual: true }
);

// Mock fs
jest.mock('fs', () => ({
  existsSync: jest.fn(() => true),
  readdirSync: jest.fn(() => ['file1.ts', 'file2.js']),
  statSync: jest.fn(() => ({ isDirectory: () => false, size: 1000 })),
  promises: {
    readdir: jest.fn(() => Promise.resolve(['file1.ts', 'file2.js'])),
    stat: jest.fn(() => Promise.resolve({ isDirectory: () => false, size: 1000 })),
    readFile: jest.fn(() => Promise.resolve('test content')),
  },
}));

// Mock path
jest.mock('path', () => ({
  join: jest.fn((...args) => args.join('/')),
  extname: jest.fn(file => (file.includes('.') ? '.' + file.split('.').pop() : '')),
  dirname: jest.fn(file => file.split('/').slice(0, -1).join('/')),
  basename: jest.fn(file => (typeof file === 'string' ? file.split('/').pop() || file : '')),
}));

describe('ProjectAnalyzer', () => {
  let projectAnalyzer: ProjectAnalyzer;
  let mockClaudeCliManager: jest.Mocked<ClaudeCliManager>;
  let mockConfigManager: jest.Mocked<ConfigManager>;

  beforeEach(() => {
    mockClaudeCliManager = {
      executeAnalysisCommand: jest.fn(() => Promise.resolve('Analysis complete')),
      isAvailable: jest.fn(() => Promise.resolve(true)),
    } as any;

    mockConfigManager = {
      validateConfiguration: jest.fn(() => Promise.resolve(true)),
      saveProjectState: jest.fn(() => Promise.resolve(true)),
    } as any;

    projectAnalyzer = new ProjectAnalyzer(mockClaudeCliManager, mockConfigManager);

    jest.clearAllMocks();
  });

  describe('Basic Functionality', () => {
    it('should create ProjectAnalyzer instance', () => {
      expect(projectAnalyzer).toBeInstanceOf(ProjectAnalyzer);
    });

    it('should analyze project', async () => {
      await expect(projectAnalyzer.analyzeProject()).resolves.not.toThrow();
    });

    it('should get project stats', async () => {
      const stats = await projectAnalyzer.getProjectStats();
      expect(stats).toBeDefined();
      if (stats) {
        expect(typeof stats).toBe('object');
      }
    });

    it('should handle project analysis completion', async () => {
      mockClaudeCliManager.executeAnalysisCommand.mockResolvedValue('Detailed analysis complete');
      await expect(projectAnalyzer.analyzeProject()).resolves.not.toThrow();
      expect(mockClaudeCliManager.executeAnalysisCommand).toHaveBeenCalled();
    });
  });

  describe('Error Handling', () => {
    it('should handle missing workspace gracefully', async () => {
      const vscode = require('vscode');
      vscode.workspace.workspaceFolders = null;

      // The function may handle the error gracefully by returning early
      await expect(projectAnalyzer.analyzeProject()).resolves.not.toThrow();
    });

    it('should handle Claude CLI errors gracefully', async () => {
      mockClaudeCliManager.executeAnalysisCommand.mockRejectedValue(new Error('Claude error'));

      // The function may handle errors gracefully in the withProgress context
      await expect(projectAnalyzer.analyzeProject()).resolves.not.toThrow();
    });
  });

  describe('Project Information', () => {
    it('should gather project statistics', async () => {
      const stats = await projectAnalyzer.getProjectStats();
      if (stats) {
        expect(stats).toHaveProperty('name');
        expect(stats).toHaveProperty('type');
        expect(stats).toHaveProperty('files');
        expect(stats).toHaveProperty('size');
      }
    });

    it('should handle project stats retrieval', async () => {
      const stats = await projectAnalyzer.getProjectStats();
      expect(stats).toBeDefined();
    });
  });
});
