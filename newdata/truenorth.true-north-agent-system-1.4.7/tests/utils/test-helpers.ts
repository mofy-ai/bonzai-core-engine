import { jest } from '@jest/globals';

export const waitFor = (ms: number): Promise<void> => 
  new Promise(resolve => setTimeout(resolve, ms));

export const waitForCondition = (
  condition: () => boolean,
  timeout: number = 5000,
  interval: number = 100
): Promise<void> => {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();
    const check = () => {
      if (condition()) {
        resolve();
      } else if (Date.now() - startTime > timeout) {
        reject(new Error(`Condition not met within ${timeout}ms`));
      } else {
        setTimeout(check, interval);
      }
    };
    check();
  });
};

export const createMockLogger = () => ({
  info: jest.fn(),
  warn: jest.fn(),
  error: jest.fn(),
  debug: jest.fn(),
  trace: jest.fn()
});

export const createMockFileSystem = () => ({
  readFile: jest.fn(),
  writeFile: jest.fn(),
  exists: jest.fn(),
  mkdir: jest.fn(),
  readdir: jest.fn(),
  stat: jest.fn()
});

export const generateTestData = {
  agentConfig: () => ({
    id: `agent-${Math.random().toString(36).substr(2, 9)}`,
    name: 'Test Agent',
    description: 'A test agent for unit testing',
    type: 'test',
    priority: 1,
    maxRetries: 3,
    timeout: 30000,
    enabled: true
  }),
  
  projectMetadata: () => ({
    name: 'test-project',
    path: '/test/project',
    type: 'typescript',
    dependencies: ['jest', 'typescript'],
    files: ['package.json', 'tsconfig.json'],
    size: 1024 * 1024
  }),
  
  executionResult: (success: boolean = true) => ({
    success,
    output: success ? 'Test completed successfully' : 'Test failed',
    error: success ? null : new Error('Test error'),
    duration: Math.floor(Math.random() * 1000),
    timestamp: new Date().toISOString()
  })
};

export const assertEventuallyEquals = async <T>(
  getValue: () => T,
  expected: T,
  timeout: number = 5000
): Promise<void> => {
  await waitForCondition(() => getValue() === expected, timeout);
};

export const assertEventuallyThrows = async (
  fn: () => Promise<any>,
  errorMatcher?: RegExp | string,
  timeout: number = 5000
): Promise<void> => {
  const startTime = Date.now();
  
  while (Date.now() - startTime < timeout) {
    try {
      await fn();
      await waitFor(100);
      continue;
    } catch (error) {
      if (errorMatcher) {
        const message = error instanceof Error ? error.message : String(error);
        if (typeof errorMatcher === 'string') {
          if (message.includes(errorMatcher)) {
            return;
          }
        } else if (errorMatcher.test(message)) {
          return;
        }
      } else {
        return; // Any error is acceptable
      }
    }
  }
  
  throw new Error(`Function did not throw expected error within ${timeout}ms`);
};

export const createPerformanceBenchmark = () => {
  const measurements: number[] = [];
  
  return {
    start: (): number => performance.now(),
    
    end: (startTime: number): number => {
      const duration = performance.now() - startTime;
      measurements.push(duration);
      return duration;
    },
    
    getStats: () => {
      if (measurements.length === 0) {
        return { avg: 0, min: 0, max: 0, count: 0 };
      }
      
      const avg = measurements.reduce((a, b) => a + b, 0) / measurements.length;
      const min = Math.min(...measurements);
      const max = Math.max(...measurements);
      
      return { avg, min, max, count: measurements.length };
    },
    
    reset: () => {
      measurements.length = 0;
    }
  };
};