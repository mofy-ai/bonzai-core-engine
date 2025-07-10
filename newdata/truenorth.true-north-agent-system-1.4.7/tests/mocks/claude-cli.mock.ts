import { jest } from '@jest/globals';
import { ChildProcess } from 'child_process';

export const mockClaudeProcess = {
  stdout: {
    on: jest.fn(),
    pipe: jest.fn()
  },
  stderr: {
    on: jest.fn(),
    pipe: jest.fn()
  },
  stdin: {
    write: jest.fn(),
    end: jest.fn()
  },
  on: jest.fn(),
  kill: jest.fn(),
  pid: 12345,
  killed: false,
  exitCode: null,
  signalCode: null
} as unknown as ChildProcess;

export const createMockClaudeResponse = (content: string, success: boolean = true) => ({
  success,
  content,
  metadata: {
    timestamp: new Date().toISOString(),
    executionTime: Math.floor(Math.random() * 1000),
    tokenCount: content.length / 4
  }
});

export const mockClaudeCliManager = {
  executeClaudeCommand: jest.fn().mockResolvedValue(
    createMockClaudeResponse('Mock Claude response')
  ),
  isClaudeAvailable: jest.fn().mockResolvedValue(true),
  validateClaudeInstallation: jest.fn().mockResolvedValue({
    isValid: true,
    version: '1.0.0',
    path: '/usr/local/bin/claude'
  }),
  createSession: jest.fn().mockResolvedValue('session-id-123'),
  endSession: jest.fn().mockResolvedValue(true),
  getActiveSessions: jest.fn().mockReturnValue(['session-id-123']),
  dispose: jest.fn()
};

export const mockSpawn = jest.fn().mockReturnValue(mockClaudeProcess);