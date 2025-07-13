// 💜 MAMA BEAR'S VOICE DICTATION TOOL - MODULAR & BEAUTIFUL! 🎤
import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, X, Loader2, Check, Copy, Sparkles } from 'lucide-react';
import { cn, logWithLove } from '../../lib/utils';
import { useSpeechRecognition } from '../../hooks/useSpeechRecognition';

interface DictationToolProps {
  isOpen: boolean;
  onClose: () => void;
  onTextComplete: (text: string) => void;
}

export const DictationTool: React.FC<DictationToolProps> = ({ 
  isOpen, 
  onClose, 
  onTextComplete 
}) => {
  const [status, setStatus] = useState<'idle' | 'listening' | 'processing' | 'done'>('idle');
  const [duration, setDuration] = useState(0);
  const [result, setResult] = useState<{ correctedText: string; suggestedPrompt: string } | null>(null);
  const [copiedTextType, setCopiedTextType] = useState<'corrected' | 'suggested' | null>(null);
  
  const { transcript, isListening, startListening, stopListening } = useSpeechRecognition();
  const transcriptRef = useRef('');
  const timerRef = useRef<number | null>(null);

  // 🤖 AI Text Enhancement (simplified for demo)
  const enhanceText = async (text: string) => {
    return new Promise<{ correctedText: string; suggestedPrompt: string }>((resolve) => {
      setTimeout(() => {
        const correctedText = text.trim()
          .replace(/\s+/g, ' ')
          .replace(/^(\w)/, (match) => match.toUpperCase());
        
        const suggestedPrompt = `💜 Help me improve this code: "${correctedText}"`;
        
        resolve({ correctedText, suggestedPrompt });
      }, 1500);
    });
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
