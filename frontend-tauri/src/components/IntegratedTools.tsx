// 💜 MAMA BEAR'S INTEGRATED TOOLS - NOW WITH PROFESSIONAL MODULAR ARCHITECTURE! �✨
import React, { useState } from 'react';
import { DictationModal, MonitoringDashboard } from './features';
import { FloatingActionButton } from './shared';
import type { FloatingAction } from './shared';
import { cn } from '../lib/utils';

// 🎤 Voice Recognition Hook
const useSpeechRecognition = () => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState<string | null>(null);
  const recognitionRef = useRef<any>(null);

  const startListening = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setError('Speech recognition not supported');
      return;
    }

    const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
    recognitionRef.current = new SpeechRecognition();
    
    recognitionRef.current.continuous = true;
    recognitionRef.current.interimResults = true;
    recognitionRef.current.lang = 'en-US';

    recognitionRef.current.onstart = () => {
      setIsListening(true);
      setError(null);
      logWithLove('🎤 Voice recognition started!', 'info');
    };

    recognitionRef.current.onresult = (event: any) => {
      let finalTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        }
      }
      setTranscript(finalTranscript);
    };

    recognitionRef.current.onerror = (event: any) => {
      setError(`Speech recognition error: ${event.error}`);
      setIsListening(false);
    };

    recognitionRef.current.onend = () => {
      setIsListening(false);
export interface IntegratedToolsProps {
  className?: string;
}

export const IntegratedTools: React.FC<IntegratedToolsProps> = ({ className }) => {
  const [isDictationOpen, setIsDictationOpen] = useState(false);
  const [isMonitoringOpen, setIsMonitoringOpen] = useState(false);

  // 💜 Professional action configuration - ENTERPRISE GRADE!
  const floatingActions: FloatingAction[] = [
    {
      id: 'dictation',
      label: '🎤 Voice Input',
      icon: ({ className }) => <span className={className}>🎤</span>,
      onClick: () => setIsDictationOpen(true),
      color: 'purple'
    },
    {
      id: 'monitoring',
      label: '📊 Family Monitor', 
      icon: ({ className }) => <span className={className}>📊</span>,
      onClick: () => setIsMonitoringOpen(true),
      color: 'blue'
    }
  ];

  const handleDictationComplete = (text: string) => {
    console.log('💜 Dictation completed:', text);
    // Handle the completed text (e.g., insert into editor)
  };

  return (
    <div className={cn("relative", className)}>
      {/* 💜 FLOATING ACTION BUTTON - PROFESSIONAL ENTERPRISE QUALITY! */}
      <FloatingActionButton 
        actions={floatingActions}
        position="bottom-right"
        size="md"
      />

      {/* 💜 DICTATION MODAL - MODULAR ARCHITECTURE! */}
      <DictationModal
        isOpen={isDictationOpen}
        onClose={() => setIsDictationOpen(false)}
        onTextComplete={handleDictationComplete}
      />

      {/* 💜 MONITORING DASHBOARD - FAMILY COORDINATION! */}
      <MonitoringDashboard
        isOpen={isMonitoringOpen}
        onClose={() => setIsMonitoringOpen(false)}
      />
    </div>
  );
};

  const safeCopyToClipboard = (text: string): boolean => {
    try {
      navigator.clipboard.writeText(text);
      logWithLove(`Text copied to clipboard: ${text.substring(0, 50)}...`, 'success');
      return true;
    } catch (error) {
      logWithLove(`Failed to copy to clipboard: ${error}`, 'error');
      return false;
    }
  };

  useEffect(() => {
    transcriptRef.current = transcript;
  }, [transcript]);

  useEffect(() => {
    if (!isListening && status === 'listening') {
      const processTranscript = async () => {
        setStatus('processing');
        const finalTranscript = transcriptRef.current;
        
        try {
          if (finalTranscript.trim()) {
            const enhancementResult = await enhanceText(finalTranscript);
            setResult(enhancementResult);
            onTextComplete(enhancementResult.correctedText);
          } else {
            setResult(null);
          }
          setStatus('done');
        } catch (e) {
          logWithLove(`Enhancement failed: ${e}`, 'error');
          setResult({ 
            correctedText: finalTranscript, 
            suggestedPrompt: `💜 ${finalTranscript}` 
          });
          setStatus('done');
        }
      };

      if (transcriptRef.current.trim().length > 0) {
        processTranscript();
      } else {
        setStatus('idle');
        setResult(null);
      }
    }
  }, [isListening, status, onTextComplete]);

  useEffect(() => {
    if (status === 'listening') {
      timerRef.current = setInterval(() => setDuration(prev => prev + 1), 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
      setDuration(0);
    }
    
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [status]);

  useEffect(() => {
    if (status === 'done' && result?.correctedText) {
      if (safeCopyToClipboard(result.correctedText)) {
        setCopiedTextType('corrected');
      }
      setTimeout(() => onClose(), 3000);
    }
  }, [result, status, onClose]);

  const handleMainButtonClick = () => {
    if (status === 'listening') {
      stopListening();
    } else {
      setResult(null);
      setCopiedTextType(null);
      setStatus('listening');
      startListening();
    }
  };

  const handleCopy = (type: 'corrected' | 'suggested') => {
    const textToCopy = type === 'corrected' ? result?.correctedText : result?.suggestedPrompt;
    if (textToCopy && safeCopyToClipboard(textToCopy)) {
      setCopiedTextType(type);
    }
  };

  const formatTime = (seconds: number): string => 
    `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;

  const getStatusInfo = () => {
    switch (status) {
      case 'listening': return { text: "💜 I'm listening to you...", color: "text-purple-400" };
      case 'processing': return { text: "✨ Processing with love...", color: "text-yellow-400" };
      case 'done': return { text: "🎉 Done! Text ready!", color: "text-green-400" };
      default: return { text: "🎤 Tap to speak with Mama Bear", color: "text-purple-300" };
    }
  };

  const renderIcon = () => {
    switch (status) {
      case 'processing': 
        return (
          <motion.div 
            key="processing"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
          >
            <Loader2 className="w-12 h-12 text-yellow-500 animate-spin" />
          </motion.div>
        );
      case 'done': 
        return (
          <motion.div 
            key="done"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
          >
            <Check className="w-12 h-12 text-green-500" />
          </motion.div>
        );
      case 'listening': 
        return (
          <motion.div 
            key="listening"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
          >
            <Mic className="w-12 h-12 text-purple-500" />
          </motion.div>
        );
      default: 
        return (
          <motion.div 
            key="idle"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
          >
            <Mic className="w-12 h-12 text-purple-300" />
          </motion.div>
        );
    }
  };

  if (!isOpen) return null;

  return (
    <motion.div 
      className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-purple-900/80 backdrop-blur-md"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <motion.button 
        onClick={onClose}
        className="absolute top-6 right-6 z-50 text-purple-300 hover:text-white transition-colors"
        whileHover={{ scale: 1.1, rotate: 90 }}
        aria-label="Close Dictation"
      >
        <X className="w-8 h-8" />
      </motion.button>

      <main className="relative z-10 w-full h-full flex flex-col items-center justify-center text-center p-8 space-y-4">
        <motion.button 
          onClick={handleMainButtonClick}
          className={cn(
            "relative w-32 h-32 rounded-full flex items-center justify-center transition-all duration-300",
            "bg-gradient-to-br from-purple-800 to-purple-900 border-2",
            status === 'listening' ? "border-purple-400 shadow-lg shadow-purple-500/25" :
            status === 'processing' ? "border-yellow-500 shadow-lg shadow-yellow-500/25" :
            status === 'done' ? "border-green-500 shadow-lg shadow-green-500/25" :
            "border-purple-600 hover:border-purple-400/50"
          )}
          animate={{ 
            boxShadow: status === 'listening' ? 
              ["0 0 0 0 rgba(168, 85, 247, 0.4)", "0 0 0 20px rgba(168, 85, 247, 0)"] : 
              undefined 
          }}
          transition={{ 
            duration: 1.5, 
            repeat: status === 'listening' ? Infinity : 0 
          }}
        >
          <AnimatePresence mode="wait">
            {renderIcon()}
          </AnimatePresence>
        </motion.button>

        <div className="text-center space-y-2 h-10">
          <p className={cn("text-lg font-medium transition-colors", getStatusInfo().color)}>
            {getStatusInfo().text}
          </p>
          <p className="text-sm text-purple-400 font-mono h-5">
            {status === 'listening' && formatTime(duration)}
          </p>
        </div>

        <div className="w-full max-w-2xl min-h-[240px]">
          <AnimatePresence>
            {status === 'done' && result && (
              <motion.div 
                className="space-y-4"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 20 }}
                transition={{ duration: 0.4, ease: 'easeOut' }}
              >
                {result.correctedText && (
                  <div className="glass-panel p-4 text-left">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-purple-300 font-medium">💜 Your Text</h3>
                      <button 
                        onClick={() => handleCopy('corrected')}
                        className="text-purple-400 hover:text-purple-200 transition-colors"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                    <p className="text-white">{result.correctedText}</p>
                  </div>
                )}
                
                {result.suggestedPrompt && (
                  <div className="glass-panel p-4 text-left">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-purple-300 font-medium">✨ Suggested Prompt</h3>
                      <button 
                        onClick={() => handleCopy('suggested')}
                        className="text-purple-400 hover:text-purple-200 transition-colors"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                    <p className="text-white">{result.suggestedPrompt}</p>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <div className="absolute bottom-4 flex items-center space-x-2 text-sm text-purple-400">
          <Sparkles className="w-4 h-4 text-purple-400" />
          <span>💜 Powered by Mama Bear's Love</span>
        </div>
      </main>
    </motion.div>
  );
};

// 📊 Family Monitoring Dashboard Component
interface FamilyMember {
  id: string;
  name: string;
  emoji: string;
  status: 'active' | 'idle' | 'coding' | 'thinking';
  currentTask?: string;
  activity: string;
  cpuUsage: number;
  memoryUsage: number;
}

interface MonitoringDashboardProps {
  isOpen: boolean;
  onClose: () => void;
  familyMembers?: FamilyMember[];
}

export const MonitoringDashboard: React.FC<MonitoringDashboardProps> = ({ 
  isOpen, 
  onClose, 
  familyMembers = [
    {
      id: 'papa-bear',
      name: 'Papa Bear',
      emoji: '🦍',
      status: 'active',
      currentTask: 'Backend Architecture',
      activity: 'Processing MCP requests',
      cpuUsage: 65,
      memoryUsage: 45
    },
    {
      id: 'mama-bear',
      name: 'Mama Bear',
      emoji: '🐻',
      status: 'coding',
      currentTask: 'UI Development',
      activity: 'Building beautiful components',
      cpuUsage: 78,
      memoryUsage: 52
    },
    {
      id: 'claude-code',
      name: 'Claude Code',
      emoji: '🤖',
      status: 'active',
      currentTask: 'Terminal Operations',
      activity: 'Managing shell commands',
      cpuUsage: 34,
      memoryUsage: 28
    },
    {
      id: 'zai-prime',
      name: 'ZAI Prime',
      emoji: '⭐',
      status: 'thinking',
      currentTask: 'Orchestration',
      activity: 'Coordinating family responses',
      cpuUsage: 89,
      memoryUsage: 67
    }
  ]
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400';
      case 'coding': return 'text-purple-400';
      case 'thinking': return 'text-yellow-400';
      default: return 'text-gray-400';
    }
  };

  const getUsageColor = (usage: number) => {
    if (usage > 80) return 'bg-red-500';
    if (usage > 60) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  if (!isOpen) return null;

  return (
    <motion.div 
      className="fixed inset-0 z-50 flex items-center justify-center bg-purple-900/80 backdrop-blur-md"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <motion.div 
        className="glass-panel-strong w-full max-w-4xl h-full max-h-[80vh] p-6 overflow-hidden"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gradient-purple flex items-center gap-2">
            <Monitor className="w-6 h-6" />
            💜 Family Monitoring Dashboard
          </h2>
          <button 
            onClick={onClose}
            className="text-purple-300 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 h-full overflow-y-auto">
          {familyMembers.map((member) => (
            <motion.div 
              key={member.id}
              className="glass-panel p-4 space-y-4"
              whileHover={{ scale: 1.02 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{member.emoji}</span>
                  <div>
                    <h3 className="font-semibold text-white">{member.name}</h3>
                    <p className={cn("text-sm", getStatusColor(member.status))}>
                      {member.status.charAt(0).toUpperCase() + member.status.slice(1)}
                    </p>
                  </div>
                </div>
                <div className={cn("w-3 h-3 rounded-full animate-pulse", 
                  member.status === 'active' ? 'bg-green-400' :
                  member.status === 'coding' ? 'bg-purple-400' :
                  member.status === 'thinking' ? 'bg-yellow-400' : 'bg-gray-400'
                )} />
              </div>

              {member.currentTask && (
                <div className="bg-purple-900/30 rounded-lg p-3">
                  <p className="text-purple-300 text-sm font-medium">Current Task:</p>
                  <p className="text-white">{member.currentTask}</p>
                </div>
              )}

              <div className="space-y-2">
                <p className="text-purple-200 text-sm">{member.activity}</p>
                
                <div className="space-y-2">
                  <div>
                    <div className="flex justify-between text-xs text-purple-300 mb-1">
                      <span>CPU Usage</span>
                      <span>{member.cpuUsage}%</span>
                    </div>
                    <div className="w-full bg-purple-900/30 rounded-full h-2">
                      <div 
                        className={cn("h-2 rounded-full transition-all duration-500", getUsageColor(member.cpuUsage))}
                        style={{ width: `${member.cpuUsage}%` }}
                      />
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between text-xs text-purple-300 mb-1">
                      <span>Memory Usage</span>
                      <span>{member.memoryUsage}%</span>
                    </div>
                    <div className="w-full bg-purple-900/30 rounded-full h-2">
                      <div 
                        className={cn("h-2 rounded-full transition-all duration-500", getUsageColor(member.memoryUsage))}
                        style={{ width: `${member.memoryUsage}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="mt-6 pt-4 border-t border-purple-500/20">
          <div className="flex items-center justify-between text-sm text-purple-300">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4" />
              <span>Family Coordination Active</span>
            </div>
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-green-400" />
              <span>All Systems Operational</span>
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

// 🎯 Floating Action Buttons Component
interface FloatingActionsProps {
  onOpenDictation: () => void;
  onOpenMonitoring: () => void;
}

export const FloatingActions: React.FC<FloatingActionsProps> = ({ 
  onOpenDictation, 
  onOpenMonitoring 
}) => {
  return (
    <div className="fixed bottom-6 right-6 z-40 flex flex-col gap-3">
      <motion.button
        onClick={onOpenMonitoring}
        className="w-14 h-14 bg-purple-600/80 hover:bg-purple-500/90 backdrop-blur-sm border border-purple-400/30 rounded-full flex items-center justify-center text-white transition-all duration-200 shadow-lg hover:shadow-purple-500/25"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        aria-label="Open Family Monitoring"
      >
        <Monitor className="w-6 h-6" />
      </motion.button>

      <motion.button
        onClick={onOpenDictation}
        className="w-14 h-14 bg-purple-600/80 hover:bg-purple-500/90 backdrop-blur-sm border border-purple-400/30 rounded-full flex items-center justify-center text-white transition-all duration-200 shadow-lg hover:shadow-purple-500/25"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        aria-label="Open Voice Dictation"
      >
        <Mic className="w-6 h-6" />
      </motion.button>
    </div>
  );
};
