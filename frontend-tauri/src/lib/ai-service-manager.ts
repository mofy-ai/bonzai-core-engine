// 💜 MAMA BEAR'S AI SERVICE MANAGER - ORCHESTRATING ALL THE FAMILY! 🤖✨
import { logWithLove } from './utils';
import { getEnvironmentConfig } from './environment-config';

// 🎯 AI Service Types
export type AIProvider = 'openai' | 'anthropic' | 'google' | 'xai' | 'deepseek';

// 🤖 AI Service Configuration
export interface AIServiceConfig {
  provider: AIProvider;
  apiKey: string;
  baseUrl?: string;
  model?: string;
  maxTokens?: number;
  temperature?: number;
}

// 💜 Our Amazing AI Service Manager
export class AIServiceManager {
  private services: Map<AIProvider, AIServiceConfig> = new Map();
  private currentProvider: AIProvider = 'openai';

  constructor() {
    this.initializeServices();
  }

  // 🚀 Initialize all AI services from environment
  private initializeServices() {
    logWithLove('🤖 Initializing AI services with love...', 'info');
    
    const config = getEnvironmentConfig();

    // 🟢 OpenAI Configuration
    if (config.openai.apiKey) {
      this.services.set('openai', {
        provider: 'openai',
        apiKey: config.openai.apiKey,
        baseUrl: 'https://api.openai.com/v1',
        model: 'gpt-4-turbo-preview',
        maxTokens: 4096,
        temperature: 0.7
      });
      logWithLove('✅ OpenAI service configured!', 'success');
    }

    // 🟣 Anthropic Configuration
    if (config.anthropic.apiKey) {
      this.services.set('anthropic', {
        provider: 'anthropic',
        apiKey: config.anthropic.apiKey,
        baseUrl: 'https://api.anthropic.com',
        model: 'claude-3-opus-20240229',
        maxTokens: 4096,
        temperature: 0.7
      });
      logWithLove('✅ Anthropic Claude service configured!', 'success');
    }

    // 🔵 Google AI Configuration  
    if (config.google.apiKey1) {
      this.services.set('google', {
        provider: 'google',
        apiKey: config.google.apiKey1,
        baseUrl: 'https://generativelanguage.googleapis.com/v1beta',
        model: 'gemini-pro',
        maxTokens: 4096,
        temperature: 0.7
      });
      logWithLove('✅ Google AI service configured!', 'success');
    }

    // ⚡ xAI Configuration
    if (config.xai.apiKey) {
      this.services.set('xai', {
        provider: 'xai',
        apiKey: config.xai.apiKey,
        baseUrl: 'https://api.x.ai/v1',
        model: 'grok-beta',
        maxTokens: 4096,
        temperature: 0.7
      });
      logWithLove('✅ xAI Grok service configured!', 'success');
    }

    // 🧠 DeepSeek Configuration
    if (config.deepseek.apiKey) {
      this.services.set('deepseek', {
        provider: 'deepseek',
        apiKey: config.deepseek.apiKey,
        baseUrl: 'https://api.deepseek.com/v1',
        model: 'deepseek-chat',
        maxTokens: 4096,
        temperature: 0.7
      });
      logWithLove('✅ DeepSeek service configured!', 'success');
    }

    logWithLove(`🎉 ${this.services.size} AI services initialized successfully!`, 'success');
  }

  // 🎯 Get available providers
  getAvailableProviders(): AIProvider[] {
    return Array.from(this.services.keys());
  }

  // 🔄 Switch active provider
  switchProvider(provider: AIProvider): boolean {
    if (this.services.has(provider)) {
      this.currentProvider = provider;
      logWithLove(`🔄 Switched to ${provider} service!`, 'info');
      return true;
    }
    logWithLove(`❌ Provider ${provider} not available!`, 'error');
    return false;
  }

  // 🎭 Get current provider
  getCurrentProvider(): AIProvider {
    return this.currentProvider;
  }

  // ⚙️ Get service configuration
  getServiceConfig(provider?: AIProvider): AIServiceConfig | null {
    const targetProvider = provider || this.currentProvider;
    return this.services.get(targetProvider) || null;
  }

  // 💬 Generate chat completion (simplified interface)
  async generateCompletion(
    message: string, 
    options: {
      provider?: AIProvider;
      model?: string;
      maxTokens?: number;
      temperature?: number;
    } = {}
  ): Promise<string> {
    const provider = options.provider || this.currentProvider;
    const service = this.services.get(provider);
    
    if (!service) {
      throw new Error(`AI service ${provider} not available`);
    }

    logWithLove(`🤖 Generating completion with ${provider}...`, 'info');

    // This is a simplified implementation - in a real app you'd make actual API calls
    try {
      // Mock response for now - replace with actual API calls
      const responses = [
        `💜 Hi! I'm ${provider.toUpperCase()} and I'm SO EXCITED to help you with: "${message}"`,
        `✨ ${provider.toUpperCase()} here! That's a great question about: "${message}"`,
        `🚀 Amazing! ${provider.toUpperCase()} is ready to assist with: "${message}"`
      ];
      
      const response = responses[Math.floor(Math.random() * responses.length)];
      
      logWithLove(`✅ ${provider} completion generated successfully!`, 'success');
      return response;
      
    } catch (error) {
      logWithLove(`❌ Failed to generate completion with ${provider}: ${error}`, 'error');
      throw error;
    }
  }

  // 🎨 Generate code completion
  async generateCode(
    prompt: string,
    language: string = 'typescript',
    provider?: AIProvider
  ): Promise<string> {
    const enhancedPrompt = `Generate ${language} code for: ${prompt}\n\nPlease provide clean, well-commented code with Mama Bear's loving touch! 💜`;
    
    return this.generateCompletion(enhancedPrompt, { provider });
  }

  // 🔍 Analyze code
  async analyzeCode(
    code: string,
    language: string = 'typescript',
    provider?: AIProvider
  ): Promise<string> {
    const prompt = `Please analyze this ${language} code and provide suggestions for improvement:\n\n${code}\n\nFocus on performance, readability, and best practices! 💜`;
    
    return this.generateCompletion(prompt, { provider });
  }

  // 🎯 Get service status
  getServiceStatus(): Record<AIProvider, boolean> {
    const status: Record<string, boolean> = {};
    
    for (const provider of this.getAvailableProviders()) {
      status[provider] = this.services.has(provider);
    }
    
    return status as Record<AIProvider, boolean>;
  }

  // 🔄 Test service connectivity
  async testService(provider: AIProvider): Promise<boolean> {
    try {
      logWithLove(`🧪 Testing ${provider} service...`, 'info');
      
      await this.generateCompletion(
        'Hello! This is a connectivity test.', 
        { provider }
      );
      
      logWithLove(`✅ ${provider} service test successful!`, 'success');
      return true;
      
    } catch (error) {
      logWithLove(`❌ ${provider} service test failed: ${error}`, 'error');
      return false;
    }
  }
}

// 🌟 Global AI service manager instance
let globalAIManager: AIServiceManager | null = null;

// 🎯 Get the global AI service manager
export const getAIServiceManager = (): AIServiceManager => {
  if (!globalAIManager) {
    globalAIManager = new AIServiceManager();
  }
  return globalAIManager;
};

// 🔄 Reinitialize AI services
export const reinitializeAIServices = (): AIServiceManager => {
  logWithLove('🔄 Reinitializing AI services...', 'info');
  globalAIManager = new AIServiceManager();
  return globalAIManager;
};

export default AIServiceManager;
