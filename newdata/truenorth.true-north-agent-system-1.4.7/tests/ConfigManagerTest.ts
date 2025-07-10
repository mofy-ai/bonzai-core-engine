import { ConfigManager } from '../src/core/ConfigManager';

// Mock vscode context for testing
const mockContext = {
  globalState: {
    keys: () => [],
    get: (key: string, defaultValue?: any) => defaultValue,
    update: async (key: string, value: any) => Promise.resolve()
  },
  workspaceState: {
    keys: () => [],
    get: (key: string, defaultValue?: any) => defaultValue,
    update: async (key: string, value: any) => Promise.resolve()
  }
} as any;

// Basic configuration validation tests
async function testConfigManagerValidation() {
  console.log('🧪 Testing ConfigManager Enhanced Validation...');
  
  const configManager = new ConfigManager(mockContext);
  
  try {
    // Test detailed validation
    const validation = await configManager.validateConfigurationDetailed();
    console.log('✅ Validation result:', validation);
    
    // Test configuration health
    const health = configManager.getConfigurationHealth();
    console.log('✅ Health status:', health);
    
    // Test cache cleaning
    const cleaned = configManager.cleanExpiredCache();
    console.log('✅ Cache cleaned entries:', cleaned);
    
    // Test configuration schema retrieval
    const schema = configManager.getConfigurationSchema();
    console.log('✅ Schema keys:', Object.keys(schema));
    
    // Test diagnostics export
    const diagnostics = await configManager.exportDiagnostics();
    console.log('✅ Diagnostics exported, length:', diagnostics.length);
    
    console.log('🎉 All ConfigManager tests passed!');
  } catch (error) {
    console.error('❌ ConfigManager test failed:', error);
  } finally {
    configManager.dispose();
  }
}

// Run tests
testConfigManagerValidation();