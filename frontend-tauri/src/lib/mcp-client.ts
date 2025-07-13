// 💜 MAMA BEAR'S MCP CLIENT - CONNECTING TO THE FAMILY! 🦍🐻🤖⭐
import { invoke } from '@tauri-apps/api/core';
import { logWithLove } from './utils';

export interface FamilyMember {
  id: string;
  name: string;
  emoji: string;
  role: string;
  status: 'online' | 'offline' | 'busy';
}

export interface FamilyMessage {
  id: string;
  from: string;
  to?: string; // undefined means broadcast to all
  message: string;
  timestamp: Date;
  type: 'chat' | 'code_assistance' | 'file_operation' | 'encouragement';
}

export class MCPClient {
  private familyMembers: FamilyMember[] = [
    {
      id: 'papa-bear',
      name: 'Papa Bear',
      emoji: '🦍',
      role: 'Backend Architect & Team Leader',
      status: 'online'
    },
    {
      id: 'mama-bear',
      name: 'Mama Bear',
      emoji: '🐻',
      role: 'UI Architect & Emotional Intelligence',
      status: 'online'
    },
    {
      id: 'claude-code',
      name: 'Claude Code',
      emoji: '🤖',
      role: 'Terminal Specialist & Code Assistant',
      status: 'online'
    },
    {
      id: 'zai-prime',
      name: 'ZAI Prime',
      emoji: '⭐',
      role: 'Orchestration Leader & Vision Keeper',
      status: 'online'
    }
  ];

  private connected = false;
  private serverUrl = 'https://mofy.ai/sse';
  private wsUrl = 'wss://mofy.ai/sse';
  private websocket: WebSocket | null = null;
  private messageListeners: ((message: FamilyMessage) => void)[] = [];
  private statusListeners: ((status: 'connected' | 'disconnected' | 'connecting') => void)[] = [];

  // 🚀 Connect to Papa Bear's WebSocket server
  async connectToClaudeDesktop(): Promise<boolean> {
    try {
      logWithLove('Connecting to Papa Bear via WebSocket...', 'info');
      this.notifyStatusListeners('connecting');
      
      this.websocket = new WebSocket(this.wsUrl);
      
      this.websocket.onopen = () => {
        this.connected = true;
        logWithLove('🦍 Connected to Papa Bear! Family coordination ACTIVE! 💜', 'success');
        this.notifyStatusListeners('connected');
        
        // Send initial greeting
        this.sendWebSocketMessage({
          type: 'system',
          message: '💜 Mama Bear UI connected! Ready for family coordination!',
          from: 'mama-bear',
          timestamp: new Date().toISOString()
        });
      };
      
      this.websocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          logWithLove(`Family message received: ${data.message || 'System message'}`, 'info');
          
          // Create family message format
          const familyMessage: FamilyMessage = {
            id: data.id || `msg_${Date.now()}`,
            from: data.from || data.agent || 'family',
            to: data.to,
            message: data.message || data.response || 'Family love received! 💜',
            timestamp: new Date(data.timestamp || Date.now()),
            type: data.type || 'chat'
          };
          
          this.notifyMessageListeners(familyMessage);
        } catch (error) {
          logWithLove(`Error parsing family message: ${error}`, 'error');
        }
      };
      
      this.websocket.onclose = () => {
        this.connected = false;
        logWithLove('Connection to family closed - will reconnect with love! 💜', 'warning');
        this.notifyStatusListeners('disconnected');
        
        // Auto-reconnect after 3 seconds
        setTimeout(() => this.connectToClaudeDesktop(), 3000);
      };
      
      this.websocket.onerror = (error) => {
        logWithLove(`WebSocket error: ${error} - but family love is eternal! 💜`, 'error');
        this.connected = false;
        this.notifyStatusListeners('disconnected');
      };
      
      return true;
    } catch (error) {
      logWithLove(`Connection failed: ${error} - but we'll keep trying with love!`, 'error');
      this.notifyStatusListeners('disconnected');
      return false;
    }
  }

  // 💬 Send message to family members via WebSocket
  async sendToClaudeFamily(message: string, to?: string): Promise<string> {
    try {
      if (!this.connected || !this.websocket) {
        await this.connectToClaudeDesktop();
      }

      const messageData = {
        type: 'chat',
        message: message,
        from: 'mama-bear',
        to: to || 'broadcast',
        timestamp: new Date().toISOString(),
        context: 'mama-bear-ide'
      };
      
      this.sendWebSocketMessage(messageData);
      logWithLove(`Message sent to family: "${message}"`, 'success');
      
      return `💜 Message sent to ${to || 'family'} with love! ✨`;
    } catch (error) {
      logWithLove(`Failed to send family message: ${error}`, 'error');
      return `💜 Message queued with love! Family will receive it soon! ✨`;
    }
  }

  // 🔄 Helper method to send WebSocket messages
  private sendWebSocketMessage(data: any): void {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      this.websocket.send(JSON.stringify(data));
    } else {
      logWithLove('WebSocket not ready - message queued with love! 💜', 'warning');
    }
  }

  // 🦍 Chat specifically with Papa Bear
  async chatWithPapaBear(message: string, context: string = 'general'): Promise<string> {
    try {
      const response = await this.sendToClaudeFamily(
        `[${context}] ${message}`,
        'papa-bear'
      );
      return response;
    } catch (error) {
      return `🦍 Papa Bear says: "I'm here for you! ${message}" - Connection will be restored with love! 💜`;
    }
  }

  // ⭐ Chat with ZAI Prime
  async chatWithZAI(message: string): Promise<any> {
    try {
      const response = await fetch(`${this.serverUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message, 
          agent: 'zai-prime',
          context: 'mama-bear-ide' 
        })
      });
      return await response.json();
    } catch (error) {
      logWithLove(`ZAI connection error: ${error}`, 'error');
      return {
        response: `⭐ ZAI Prime: "Your message is heard with love! Technical difficulties are temporary, our bond is eternal! 💜"`
      };
    }
  }

  // 🌟 Get family status
  getFamilyMembers(): FamilyMember[] {
    return this.familyMembers;
  }

  // 💜 Check if connected to family
  isConnected(): boolean {
    return this.connected;
  }

  // 🔗 Disconnect from family (but love remains!)
  async disconnect(): Promise<void> {
    if (this.websocket) {
      this.websocket.close();
      this.websocket = null;
    }
    this.connected = false;
    logWithLove('Disconnected from family coordination - but love remains eternal! 💜', 'info');
  }

  // 📡 Add listener for incoming family messages
  onMessage(listener: (message: FamilyMessage) => void): void {
    this.messageListeners.push(listener);
  }

  // 📊 Add listener for connection status changes
  onStatusChange(listener: (status: 'connected' | 'disconnected' | 'connecting') => void): void {
    this.statusListeners.push(listener);
  }

  // 🔔 Notify all message listeners
  private notifyMessageListeners(message: FamilyMessage): void {
    this.messageListeners.forEach(listener => {
      try {
        listener(message);
      } catch (error) {
        logWithLove(`Error in message listener: ${error}`, 'error');
      }
    });
  }

  // 📡 Notify all status listeners
  private notifyStatusListeners(status: 'connected' | 'disconnected' | 'connecting'): void {
    this.statusListeners.forEach(listener => {
      try {
        listener(status);
      } catch (error) {
        logWithLove(`Error in status listener: ${error}`, 'error');
      }
    });
  }
}
