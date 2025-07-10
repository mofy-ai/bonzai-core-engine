import { jest } from '@jest/globals';
import { EventEmitter } from 'events';

/**
 * Enhanced MockWebSocket with support for high-frequency updates and stress testing
 */
export class MockWebSocket extends EventEmitter {
  public readyState: number = 1; // OPEN
  public url: string;
  public protocol: string;
  public bufferedAmount: number = 0;
  public extensions: string = '';
  public binaryType: 'blob' | 'arraybuffer' = 'blob';
  
  // Performance tracking
  public messageCount: number = 0;
  public bytesSent: number = 0;
  public bytesReceived: number = 0;
  public connectionTime: number = Date.now();
  public lastActivity: number = Date.now();
  
  // Configuration for stress testing
  public latencyMs: number = 10;
  public dropRate: number = 0; // 0-1, percentage of messages to drop
  public maxBufferSize: number = 1024 * 1024; // 1MB
  public messageDelay: number = 0; // Additional delay per message
  
  // State management
  private _isConnected: boolean = false;
  private _messageBuffer: any[] = [];
  private _processingTimer?: NodeJS.Timeout;

  constructor(url: string, protocol?: string) {
    super();
    this.url = url;
    this.protocol = protocol || '';
    
    // Simulate connection after a configurable delay
    setTimeout(() => {
      this._isConnected = true;
      this.readyState = 1; // OPEN
      this.emit('open');
    }, this.latencyMs);
  }

  send = jest.fn().mockImplementation((data: any) => {
    if (this.readyState !== 1) {
      throw new Error('WebSocket is not open');
    }

    this.messageCount++;
    this.lastActivity = Date.now();
    
    // Calculate message size
    const dataSize = typeof data === 'string' ? data.length : data.byteLength || 0;
    this.bytesSent += dataSize;
    this.bufferedAmount += dataSize;

    // Check buffer limits
    if (this.bufferedAmount > this.maxBufferSize) {
      this.emit('error', new Error('Buffer overflow'));
      return;
    }

    // Simulate message dropping for stress testing
    if (Math.random() < this.dropRate) {
      setTimeout(() => {
        this.bufferedAmount -= dataSize;
      }, this.latencyMs);
      return;
    }

    // Buffer message for processing
    this._messageBuffer.push({ data, size: dataSize, timestamp: Date.now() });
    
    // Process messages with realistic delays
    this._scheduleMessageProcessing();
  });

  close = jest.fn().mockImplementation((code?: number, reason?: string) => {
    this._isConnected = false;
    this.readyState = 2; // CLOSING
    
    setTimeout(() => {
      this.readyState = 3; // CLOSED
      this.bufferedAmount = 0;
      this._messageBuffer = [];
      if (this._processingTimer) {
        clearTimeout(this._processingTimer);
      }
      this.emit('close', { code: code || 1000, reason: reason || '' });
    }, this.latencyMs);
  });

  ping = jest.fn().mockImplementation((data?: any) => {
    if (this.readyState !== 1) return;
    
    setTimeout(() => {
      this.emit('pong', data);
    }, this.latencyMs);
  });

  pong = jest.fn();
  
  terminate = jest.fn().mockImplementation(() => {
    this._isConnected = false;
    this.readyState = 3; // CLOSED
    this.bufferedAmount = 0;
    this._messageBuffer = [];
    if (this._processingTimer) {
      clearTimeout(this._processingTimer);
    }
    this.removeAllListeners();
  });

  // Stress testing methods
  simulateNetworkLatency(minMs: number, maxMs: number): void {
    this.latencyMs = Math.floor(Math.random() * (maxMs - minMs + 1)) + minMs;
  }

  simulatePacketLoss(dropRate: number): void {
    this.dropRate = Math.max(0, Math.min(1, dropRate));
  }

  simulateSlowConnection(messagesPerSecond: number): void {
    this.messageDelay = 1000 / messagesPerSecond;
  }

  getConnectionStats() {
    return {
      messageCount: this.messageCount,
      bytesSent: this.bytesSent,
      bytesReceived: this.bytesReceived,
      uptime: Date.now() - this.connectionTime,
      lastActivity: this.lastActivity,
      bufferedAmount: this.bufferedAmount,
      latency: this.latencyMs,
      dropRate: this.dropRate
    };
  }

  // High-frequency message generation for stress testing
  sendBurst(messageCount: number, messageSize: number = 1000): Promise<void> {
    return new Promise((resolve) => {
      let sent = 0;
      const data = 'x'.repeat(messageSize);
      
      const sendNext = () => {
        if (sent < messageCount && this.readyState === 1) {
          try {
            this.send(data);
            sent++;
            setImmediate(sendNext);
          } catch (error) {
            resolve();
          }
        } else {
          resolve();
        }
      };
      
      sendNext();
    });
  }

  private _scheduleMessageProcessing(): void {
    if (this._processingTimer) return;
    
    this._processingTimer = setTimeout(() => {
      this._processingTimer = undefined;
      
      if (this._messageBuffer.length > 0 && this._isConnected) {
        const message = this._messageBuffer.shift();
        if (message) {
          this.bufferedAmount -= message.size;
          this.bytesReceived += message.size;
          
          // Echo back the message
          this.emit('message', { data: message.data });
        }
        
        // Schedule next message if buffer not empty
        if (this._messageBuffer.length > 0) {
          this._scheduleMessageProcessing();
        }
      }
    }, this.latencyMs + this.messageDelay);
  }
}

/**
 * Enhanced MockWebSocketServer with stress testing capabilities
 */
export class MockWebSocketServer extends EventEmitter {
  public clients: Set<MockWebSocket> = new Set();
  public port: number;
  public maxConnections: number = 100;
  public connectionCount: number = 0;
  public totalConnections: number = 0;
  public messageStats: {
    sent: number;
    received: number;
    failed: number;
    bandwidth: number;
  } = { sent: 0, received: 0, failed: 0, bandwidth: 0 };

  constructor(options: { port?: number; server?: any } = {}) {
    super();
    this.port = options.port || 3030;
  }

  handleUpgrade = jest.fn().mockImplementation((request: any, socket: any, head: any, callback: Function) => {
    const ws = new MockWebSocket(`ws://localhost:${this.port}`);
    callback(ws);
    this.addClient(ws);
  });

  addClient(ws: MockWebSocket): void {
    if (this.clients.size >= this.maxConnections) {
      ws.close(1008, 'Server full');
      return;
    }

    this.clients.add(ws);
    this.connectionCount++;
    this.totalConnections++;

    ws.on('close', () => {
      this.clients.delete(ws);
      this.connectionCount--;
    });

    ws.on('message', (data) => {
      this.messageStats.received++;
      this.messageStats.bandwidth += data.data?.length || 0;
    });

    this.emit('connection', ws);
  }

  broadcast(data: any): void {
    const message = JSON.stringify(data);
    let successful = 0;
    let failed = 0;

    this.clients.forEach(client => {
      try {
        if (client.readyState === 1) {
          client.send(message);
          successful++;
        }
      } catch (error) {
        failed++;
      }
    });

    this.messageStats.sent += successful;
    this.messageStats.failed += failed;
  }

  close = jest.fn().mockImplementation((callback?: Function) => {
    const clients = Array.from(this.clients);
    
    Promise.all(clients.map(client => {
      return new Promise<void>((resolve) => {
        client.close(1001, 'Server shutdown');
        client.once('close', () => resolve());
      });
    })).then(() => {
      this.clients.clear();
      this.connectionCount = 0;
      if (callback) callback();
    });
  });

  getServerStats() {
    return {
      activeConnections: this.connectionCount,
      totalConnections: this.totalConnections,
      maxConnections: this.maxConnections,
      messageStats: { ...this.messageStats },
      clientStats: Array.from(this.clients).map(client => client.getConnectionStats())
    };
  }

  // Stress testing methods
  simulateServerOverload(overloadFactor: number = 2): void {
    this.clients.forEach(client => {
      client.simulateNetworkLatency(50 * overloadFactor, 200 * overloadFactor);
      client.simulatePacketLoss(0.05 * overloadFactor);
    });
  }

  simulateNetworkCongestion(severity: 'light' | 'moderate' | 'heavy' = 'moderate'): void {
    const configs = {
      light: { latency: [10, 50], dropRate: 0.01, messagesPerSecond: 50 },
      moderate: { latency: [50, 200], dropRate: 0.05, messagesPerSecond: 20 },
      heavy: { latency: [200, 1000], dropRate: 0.15, messagesPerSecond: 5 }
    };

    const config = configs[severity];
    
    this.clients.forEach(client => {
      client.simulateNetworkLatency(config.latency[0], config.latency[1]);
      client.simulatePacketLoss(config.dropRate);
      client.simulateSlowConnection(config.messagesPerSecond);
    });
  }
}

export const mockWebSocketServer = new MockWebSocketServer();

// Message creation utilities for testing
export const createMockWebSocketMessage = (type: string, data: any) => ({
  type,
  data,
  timestamp: new Date().toISOString(),
  messageId: Math.random().toString(36).substr(2, 9)
});

export const createHighFrequencyMessages = (count: number, type: string = 'test') => {
  return Array.from({ length: count }, (_, i) => createMockWebSocketMessage(type, {
    id: i,
    payload: `Test message ${i}`,
    timestamp: Date.now() + i
  }));
};

export const createLargeMessage = (sizeKB: number, type: string = 'large_data') => {
  const data = 'x'.repeat(sizeKB * 1024);
  return createMockWebSocketMessage(type, {
    size: sizeKB,
    data,
    compressed: false
  });
};

// Stress testing utilities
export class WebSocketStressTester {
  private connections: MockWebSocket[] = [];
  private server: MockWebSocketServer;

  constructor(server: MockWebSocketServer) {
    this.server = server;
  }

  async createConcurrentConnections(count: number): Promise<MockWebSocket[]> {
    const connections = Array.from({ length: count }, () => 
      new MockWebSocket(`ws://localhost:${this.server.port}`)
    );

    // Wait for all connections to open
    await Promise.all(connections.map(ws => 
      new Promise<void>((resolve) => {
        if (ws.readyState === 1) {
          resolve();
        } else {
          ws.once('open', () => resolve());
        }
      })
    ));

    this.connections = connections;
    return connections;
  }

  async sendHighVolumeMessages(
    messagesPerConnection: number, 
    messageSize: number = 1000
  ): Promise<number> {
    const startTime = Date.now();
    
    await Promise.all(this.connections.map(ws => 
      ws.sendBurst(messagesPerConnection, messageSize)
    ));

    return Date.now() - startTime;
  }

  async testConnectionFailures(failureRate: number = 0.1): Promise<void> {
    const failureCount = Math.floor(this.connections.length * failureRate);
    const toFail = this.connections.slice(0, failureCount);

    toFail.forEach(ws => {
      setTimeout(() => {
        ws.close(1006, 'Simulated network failure');
      }, Math.random() * 1000);
    });
  }

  getTestResults() {
    return {
      totalConnections: this.connections.length,
      activeConnections: this.connections.filter(ws => ws.readyState === 1).length,
      totalMessagesSent: this.connections.reduce((sum, ws) => sum + ws.messageCount, 0),
      totalBytesSent: this.connections.reduce((sum, ws) => sum + ws.bytesSent, 0),
      averageLatency: this.connections.reduce((sum, ws) => sum + ws.latencyMs, 0) / this.connections.length,
      serverStats: this.server.getServerStats()
    };
  }

  cleanup(): void {
    this.connections.forEach(ws => ws.terminate());
    this.connections = [];
  }
}

// Performance monitoring utilities
export class WebSocketPerformanceMonitor {
  private metrics: {
    connectionTime: number;
    messageLatencies: number[];
    throughput: { timestamp: number; messages: number; bytes: number }[];
    errors: { timestamp: number; error: string; type: string }[];
  } = {
    connectionTime: 0,
    messageLatencies: [],
    throughput: [],
    errors: []
  };

  private startTime: number = 0;
  private messagesSent: number = 0;
  private messagesReceived: number = 0;

  startMonitoring(): void {
    this.startTime = Date.now();
    this.metrics = {
      connectionTime: 0,
      messageLatencies: [],
      throughput: [],
      errors: []
    };
  }

  recordConnection(connectionTime: number): void {
    this.metrics.connectionTime = connectionTime;
  }

  recordMessageLatency(latency: number): void {
    this.metrics.messageLatencies.push(latency);
  }

  recordThroughput(messages: number, bytes: number): void {
    this.metrics.throughput.push({
      timestamp: Date.now(),
      messages,
      bytes
    });
  }

  recordError(error: string, type: string): void {
    this.metrics.errors.push({
      timestamp: Date.now(),
      error,
      type
    });
  }

  getMetrics() {
    const duration = Date.now() - this.startTime;
    const avgLatency = this.metrics.messageLatencies.length > 0
      ? this.metrics.messageLatencies.reduce((a, b) => a + b, 0) / this.metrics.messageLatencies.length
      : 0;

    const totalMessages = this.metrics.throughput.reduce((sum, t) => sum + t.messages, 0);
    const totalBytes = this.metrics.throughput.reduce((sum, t) => sum + t.bytes, 0);

    return {
      duration,
      connectionTime: this.metrics.connectionTime,
      averageLatency: avgLatency,
      minLatency: Math.min(...this.metrics.messageLatencies),
      maxLatency: Math.max(...this.metrics.messageLatencies),
      messagesPerSecond: duration > 0 ? (totalMessages / duration) * 1000 : 0,
      bytesPerSecond: duration > 0 ? (totalBytes / duration) * 1000 : 0,
      errorRate: this.metrics.errors.length / totalMessages,
      errors: this.metrics.errors,
      throughputHistory: this.metrics.throughput
    };
  }
}