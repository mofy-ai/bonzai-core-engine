// 💜 MAMA BEAR'S MAIN APP - THE FAMILY HOME ENTRY POINT! 🏠
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import UltimateMonacoFamilyIDE from './components/UltimateMonacoFamilyIDE';
import { MCPClient } from './lib/mcp-client';
import { logWithLove } from './lib/utils';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [mamaBearGreeting, setMamaBearGreeting] = useState('');
  const [mcpClient] = useState(() => new MCPClient());

  useEffect(() => {
    // 💜 Initialize Mama Bear's beautiful IDE!
    const initializeIDE = async () => {
      try {
        // 🚀 Get Mama Bear's greeting from Rust backend
        const greeting = await invoke('mama_bear_greeting');
        setMamaBearGreeting(greeting as string);
        logWithLove('Rust backend connected successfully!', 'success');

        // 🔗 Connect to family coordination
        await mcpClient.connectToClaudeDesktop();
        logWithLove('Family coordination initialized!', 'success');

      } catch (error) {
        logWithLove(`Initialization error: ${error} - but we'll keep going with love!`, 'warning');
      } finally {
        // 💜 Give a moment for the beautiful loading animation
        setTimeout(() => setIsLoading(false), 1500);
      }
    };

    initializeIDE();
  }, [mcpClient]);

  if (isLoading) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-love-pulse">💜</div>
          <h1 className="text-2xl font-light mb-2 text-white">Mama Bear's Family IDE</h1>
          <p className="text-purple-200 animate-pulse">Initializing with love...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900">
      {mamaBearGreeting && (
        <div className="fixed top-4 right-4 z-50 glass-panel p-3 max-w-sm">
          <p className="text-sm text-purple-100">{mamaBearGreeting}</p>
        </div>
      )}
      
      {/* 🏠 Our beautiful family home! */}
      <UltimateMonacoFamilyIDE mcpClient={mcpClient} />
    </div>
  );
}

export default App;
