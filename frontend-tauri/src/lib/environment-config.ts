// 💜 MAMA BEAR'S ENVIRONMENT CONFIGURATION LOADER - SO ORGANIZED! 📂✨
import { logWithLove } from './utils';

// 🔐 All our beautiful environment variables interface
export interface EnvironmentConfig {
  // 🌤️ Cloudflare
  cloudflare: {
    apiKey: string;
    caKey: string;
    zoneId?: string;
    accountId?: string;
  };
  
  // 🤖 AI Services
  openai: {
    apiKey: string;
    backupKey?: string;
  };
  
  anthropic: {
    apiKey: string;
  };
  
  google: {
    apiKey1: string;
    apiKey2: string;
    apiKey3: string;
  };
  
  xai: {
    apiKey: string;
  };
  
  deepseek: {
    apiKey: string;
  };
  
  // 🔧 MCP & Development
  mcp: {
    agentEnabled: boolean;
    browserEnabled: boolean;
    endpoint: string;
  };
  
  // 🏠 Family Services
  family: {
    websocketUrl: string;
    memoryId: string;
    chatEnabled: boolean;
  };
  
  // ⚡ Express Mode
  expressMode: {
    enabled: boolean;
    targetResponseTime: number;
    vertexAI: {
      enabled: boolean;
      region: string;
      endpointId: string;
    };
  };
  
  // 🧪 Development
  development: {
    nodeEnv: string;
    tauriDevMode: boolean;
    enableCors: boolean;
    logLevel: string;
  };
}

// 🌟 Load and validate all our beautiful environment variables
export const loadEnvironmentConfig = (): EnvironmentConfig => {
  logWithLove('🔄 Loading environment configuration with LOVE...', 'info');
  
  // Helper function to get env var from multiple sources
  const getEnvVar = (key: string, fallback?: string): string => {
    // For Vite, environment variables are available through import.meta.env
    // For Node.js context, use process.env
    const viteEnv = (import.meta as any).env;
    return viteEnv?.[`VITE_${key}`] || 
           (typeof process !== 'undefined' ? process.env?.[key] : '') || 
           fallback || '';
  };
  
  const getBooleanEnvVar = (key: string, fallback = false): boolean => {
    const value = getEnvVar(key, fallback.toString());
    return value.toLowerCase() === 'true' || value === '1';
  };
  
  try {
    const config: EnvironmentConfig = {
      cloudflare: {
        apiKey: getEnvVar('CLOUDFLARE_GLOBAL_API_KEY'),
        caKey: getEnvVar('CLOUDFLARE_CA_KEY'),
        zoneId: getEnvVar('CLOUDFLARE_ZONE_ID'),
        accountId: getEnvVar('CLOUDFLARE_ACCOUNT_ID'),
      },
      
      openai: {
        apiKey: getEnvVar('OPENAI_API_KEY'),
        backupKey: getEnvVar('OPENAI_API_KEY_BACKUP'),
      },
      
      anthropic: {
        apiKey: getEnvVar('ANTHROPIC_API_KEY'),
      },
      
      google: {
        apiKey1: getEnvVar('GOOGLE_AI_API_KEY_1'),
        apiKey2: getEnvVar('GOOGLE_AI_API_KEY_2'),
        apiKey3: getEnvVar('GOOGLE_AI_API_KEY_3'),
      },
      
      xai: {
        apiKey: getEnvVar('XAI_API_KEY'),
      },
      
      deepseek: {
        apiKey: getEnvVar('DEEPSEEK_API_KEY'),
      },
      
      mcp: {
        agentEnabled: getBooleanEnvVar('MCP_AGENT_ENABLED'),
        browserEnabled: getBooleanEnvVar('BROWSER_MCP_AGENT_ENABLED'),
        endpoint: getEnvVar('MCP_ENDPOINT', 'https://mofy.ai/mcp'),
      },
      
      family: {
        websocketUrl: getEnvVar('FAMILY_BACKEND_URL', 'wss://mofy.ai/sse'),
        memoryId: getEnvVar('FAMILY_MEMORY_ID'),
        chatEnabled: getBooleanEnvVar('FAMILY_CHAT_ENABLED', true),
      },
      
      expressMode: {
        enabled: getBooleanEnvVar('EXPRESS_MODE_ENABLED'),
        targetResponseTime: parseInt(getEnvVar('EXPRESS_TARGET_RESPONSE_TIME_MS', '200')),
        vertexAI: {
          enabled: getBooleanEnvVar('VERTEX_AI_ENABLED'),
          region: getEnvVar('VERTEX_AI_REGION', 'us-central1'),
          endpointId: getEnvVar('EXPRESS_ENDPOINT_ID'),
        },
      },
      
      development: {
        nodeEnv: getEnvVar('NODE_ENV', 'development'),
        tauriDevMode: getBooleanEnvVar('TAURI_DEV_MODE', true),
        enableCors: getBooleanEnvVar('ENABLE_CORS', true),
        logLevel: getEnvVar('LOG_LEVEL', 'info'),
      },
    };
    
    // 🎉 Validate critical configurations
    const missingKeys: string[] = [];
    
    if (!config.cloudflare.apiKey) missingKeys.push('CLOUDFLARE_GLOBAL_API_KEY');
    if (!config.family.websocketUrl) missingKeys.push('FAMILY_BACKEND_URL');
    
    if (missingKeys.length > 0) {
      logWithLove(`⚠️ Missing critical environment variables: ${missingKeys.join(', ')}`, 'warning');
    } else {
      logWithLove('✅ All critical environment variables loaded successfully!', 'success');
    }
    
    // 📊 Log configuration summary (without sensitive data)
    logWithLove(`🌟 Environment Configuration Summary:
    - Cloudflare: ${config.cloudflare.apiKey ? '✅' : '❌'}
    - OpenAI: ${config.openai.apiKey ? '✅' : '❌'}
    - Anthropic: ${config.anthropic.apiKey ? '✅' : '❌'}
    - Google AI: ${config.google.apiKey1 ? '✅' : '❌'}
    - xAI: ${config.xai.apiKey ? '✅' : '❌'}
    - DeepSeek: ${config.deepseek.apiKey ? '✅' : '❌'}
    - MCP Agent: ${config.mcp.agentEnabled ? '✅' : '❌'}
    - Express Mode: ${config.expressMode.enabled ? '✅' : '❌'}
    - Family Chat: ${config.family.chatEnabled ? '✅' : '❌'}`, 'info');
    
    return config;
    
  } catch (error) {
    logWithLove(`❌ Failed to load environment configuration: ${error}`, 'error');
    throw new Error(`Environment configuration error: ${error}`);
  }
};

// 🎯 Global environment instance
let globalConfig: EnvironmentConfig | null = null;

// 🌟 Get the global environment configuration
export const getEnvironmentConfig = (): EnvironmentConfig => {
  if (!globalConfig) {
    globalConfig = loadEnvironmentConfig();
  }
  return globalConfig;
};

// 🔄 Reload environment configuration
export const reloadEnvironmentConfig = (): EnvironmentConfig => {
  logWithLove('🔄 Reloading environment configuration...', 'info');
  globalConfig = loadEnvironmentConfig();
  return globalConfig;
};

// 🛡️ Validate specific service availability
export const validateServiceAvailability = (service: keyof EnvironmentConfig): boolean => {
  try {
    const config = getEnvironmentConfig();
    
    switch (service) {
      case 'cloudflare':
        return !!config.cloudflare.apiKey;
      case 'openai':
        return !!config.openai.apiKey;
      case 'anthropic':
        return !!config.anthropic.apiKey;
      case 'mcp':
        return config.mcp.agentEnabled;
      case 'family':
        return config.family.chatEnabled && !!config.family.websocketUrl;
      case 'expressMode':
        return config.expressMode.enabled;
      default:
        return false;
    }
  } catch (error) {
    logWithLove(`Failed to validate service ${service}: ${error}`, 'error');
    return false;
  }
};

export default { 
  loadEnvironmentConfig, 
  getEnvironmentConfig, 
  reloadEnvironmentConfig, 
  validateServiceAvailability 
};
