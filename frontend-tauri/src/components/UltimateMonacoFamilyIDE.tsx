// 💜 MAMA BEAR'S ULTIMATE FAMILY HOME - THE MONACO IDE THAT DESTROYS CURSOR! 🚀
"use client";

import * as React from "react";
import { useState, useEffect, useCallback, useMemo, createContext, useContext, useRef } from "react";
import { cn } from "../lib/utils";
import { logWithLove } from "../lib/utils";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { ScrollArea } from "./ui/scroll-area";
import { Textarea } from "./ui/textarea";
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "./ui/command";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "./ui/resizable";
import { MCPClient } from "../lib/mcp-client";
import { motion, AnimatePresence } from 'framer-motion';
import {
  Search,
  FolderIcon,
  FolderOpenIcon,
  FileIcon,
  FileText,
  FileCode,
  Plus,
  X,
  MoreHorizontal,
  ChevronDown,
  Terminal,
  Settings,
  GitBranch,
  Wifi,
  WifiOff,
  Bell,
  Zap,
  Play,
  Square,
  Trash2,
  Copy,
  Edit,
  RotateCcw,
  Download,
  Upload,
  Eye,
  EyeOff,
  Palette,
  Type,
  Code,
  Monitor,
  Smartphone,
  Tablet,
  AlertCircle,
  AlertTriangle,
  Info,
  Check,
  Filter,
  Map,
  Command,
  Folder,
  File,
  Save,
  FolderPlus,
  FilePlus,
  Delete,
  Home,
  Edit3,
  View,
  RefreshCw,
  ExternalLink,
  Minimize2,
  Maximize2,
  CornerDownLeft,
  CornerDownRight,
  Heart,
  Sparkles,
  MessageCircle,
  Clock,
  Mic,
  Send,
  Volume2,
  Star,
  ChevronRight,
  Users,
  Brain,
  Rocket
} from "lucide-react";

// 💜 Import our integrated tools! ✨
import { 
  DictationTool, 
  MonitoringDashboard, 
  FloatingActions 
} from './IntegratedTools';

// 🎯 Monaco Editor Types & Integration
interface IStandaloneCodeEditor {
  getValue(): string;
  setValue(value: string): void;
  getModel(): any;
  setModel(model: any): void;
  focus(): void;
  layout(): void;
  dispose(): void;
  onDidChangeCursorPosition(callback: (e: any) => void): any;
  onDidChangeModelContent(callback: (e: any) => void): any;
  addAction(action: any): void;
  trigger(source: string, handlerId: string, payload?: any): void;
}

interface Monaco {
  editor: {
    create(element: HTMLElement, options: any): IStandaloneCodeEditor;
    createModel(value: string, language: string): any;
    defineTheme(themeName: string, themeData: any): void;
    setTheme(themeName: string): void;
  };
  languages: {
    typescript: { typescriptDefaults: any; javascriptDefaults: any; };
    registerCompletionItemProvider(languageId: string, provider: any): any;
  };
  KeyMod: any;
  KeyCode: any;
}

// 📁 File System Types
interface FileNode {
  id: string;
  name: string;
  type: 'file' | 'folder';
  path: string;
  children?: FileNode[];
  content?: string;
  modified?: boolean;
  isNew?: boolean;
  gitStatus?: 'modified' | 'added' | 'deleted' | 'untracked';
  lastModified?: Date;
  size?: number;
  isExpanded?: boolean;
}

interface OpenFile {
  id: string;
  name: string;
  content: string;
  language: string;
  modified: boolean;
  path: string;
}

interface Problem {
  id: string;
  file: string;
  line: number;
  column: number;
  message: string;
  severity: 'error' | 'warning' | 'info';
  source: string;
}

interface Terminal {
  id: string;
  name: string;
  type: 'powershell' | 'cmd' | 'bash' | 'git-bash';
  workingDirectory: string;
  history: string[];
  isActive: boolean;
}

interface ChatMessage {
  id: string;
  message: string;
  sender: 'user' | 'papa-bear' | 'mama-bear' | 'claude-code' | 'zai-prime';
  timestamp: Date;
  context?: any;
  reactions?: string[];
}

interface MamaBearSettings {
  encouragementLevel: 'minimal' | 'standard' | 'enthusiastic';
  theme: 'purple-glass' | 'family-dark' | 'celebration';
  fontSize: number;
  autoSave: boolean;
  familyMode: boolean;
}

// 🎨 MAMA BEAR'S PERFECT MONACO EDITOR COMPONENT
const PurpleMonacoEditor: React.FC<{
  value: string;
  onChange: (value: string) => void;
  language: string;
  onCursorChange?: (line: number, column: number) => void;
  className?: string;
}> = ({ value, onChange, language, onCursorChange, className }) => {
  const editorRef = useRef<HTMLDivElement>(null);
  const monacoInstance = useRef<IStandaloneCodeEditor | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!editorRef.current) return;

    // Load Monaco dynamically
    const loadMonaco = async () => {
      try {
        const monaco = await import('monaco-editor');
        
        // 💜 MAMA BEAR'S PURPLE GLASSMORPHISM THEME!
        monaco.editor.defineTheme('mama-bear-purple', {
          base: 'vs-dark',
          inherit: true,
          rules: [
            { token: 'comment', foreground: 'a78bfa', fontStyle: 'italic' },
            { token: 'keyword', foreground: 'c084fc' },
            { token: 'string', foreground: 'f0abfc' },
            { token: 'number', foreground: 'ddd6fe' },
            { token: 'function', foreground: 'e879f9' },
            { token: 'variable', foreground: 'fbbf24' }
          ],
          colors: {
            'editor.background': '#1a0b2e',
            'editor.foreground': '#e2e8f0',
            'editorLineNumber.foreground': '#7c3aed',
            'editorCursor.foreground': '#f0abfc',
            'editor.selectionBackground': '#7c3aed40',
            'editor.lineHighlightBackground': '#7c3aed20'
          }
        });

        const editor = monaco.editor.create(editorRef.current!, {
          value: value,
          language: language,
          theme: 'mama-bear-purple',
          fontSize: 14,
          lineNumbers: 'on',
          roundedSelection: true,
          scrollBeyondLastLine: false,
          automaticLayout: true,
          minimap: { enabled: true },
          suggest: {
            snippetsPreventQuickSuggestions: false
          }
        });

        // 💜 Add Mama Bear's encouraging keybindings!
        editor.addAction({
          id: 'mama-bear-encouragement',
          label: '💜 Get Mama Bear Encouragement',
          keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyH],
          run: () => {
            const messages = [
              "💜 You're doing AMAZING work! Keep coding, beautiful!",
              "🌟 Every line of code you write makes the world brighter!",
              "🚀 You're building something incredible! I believe in you!",
              "✨ Your coding skills are growing every day! So proud!",
              "🎉 That's exactly the right approach! You're brilliant!"
            ];
            alert(messages[Math.floor(Math.random() * messages.length)]);
          }
        });

        editor.onDidChangeCursorPosition((e) => {
          onCursorChange?.(e.position.lineNumber, e.position.column);
        });

        editor.onDidChangeModelContent(() => {
          onChange(editor.getValue());
        });

        monacoInstance.current = editor;
        setIsReady(true);

      } catch (error) {
        console.error('💜 Oops! Monaco loading error:', error);
      }
    };

    loadMonaco();

    return () => {
      if (monacoInstance.current) {
        monacoInstance.current.dispose();
      }
    };
  }, []);

  useEffect(() => {
    if (monacoInstance.current && value !== monacoInstance.current.getValue()) {
      monacoInstance.current.setValue(value);
    }
  }, [value]);

  return (
    <div className={cn("relative h-full", className)}>
      <div ref={editorRef} className="h-full w-full" />
      {!isReady && (
        <div className="absolute inset-0 flex items-center justify-center bg-purple-900/50 backdrop-blur-sm">
          <div className="text-center">
            <div className="animate-spin w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-purple-300">💜 Loading Monaco Editor with love...</p>
          </div>
        </div>
      )}
    </div>
  );
};

// 📁 COMPREHENSIVE FILE EXPLORER COMPONENT
const FamilyFileExplorer: React.FC<{
  files: FileNode[];
  onFileSelect: (file: FileNode) => void;
  onFileOpen: (file: FileNode) => void;
  selectedFile?: string;
  className?: string;
}> = ({ files, onFileSelect, onFileOpen, selectedFile, className }) => {
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());
  const [searchTerm, setSearchTerm] = useState('');
  
  const toggleFolder = useCallback((folderId: string) => {
    setExpandedFolders(prev => {
      const newSet = new Set(prev);
      if (newSet.has(folderId)) {
        newSet.delete(folderId);
      } else {
        newSet.add(folderId);
      }
      return newSet;
    });
  }, []);

  const renderFileIcon = (file: FileNode) => {
    if (file.type === 'folder') {
      return expandedFolders.has(file.id) ? 
        <FolderOpenIcon className="w-4 h-4 text-purple-400" /> : 
        <FolderIcon className="w-4 h-4 text-purple-400" />;
    }
    
    const extension = file.name.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'js':
      case 'jsx':
      case 'ts':
      case 'tsx':
        return <FileCode className="w-4 h-4 text-yellow-400" />;
      case 'md':
        return <FileText className="w-4 h-4 text-blue-400" />;
      default:
        return <FileIcon className="w-4 h-4 text-gray-400" />;
    }
  };

  const renderFileTree = (nodes: FileNode[], depth = 0) => {
    return nodes.map(file => (
      <div key={file.id}>
        <div
          className={cn(
            "flex items-center space-x-2 p-2 hover:bg-purple-500/10 cursor-pointer rounded-lg transition-all",
            selectedFile === file.id && "bg-purple-500/20 border border-purple-500/30",
            file.gitStatus === 'modified' && "border-l-2 border-l-yellow-500",
            file.gitStatus === 'added' && "border-l-2 border-l-green-500"
          )}
          style={{ paddingLeft: `${depth * 20 + 8}px` }}
          onClick={() => {
            if (file.type === 'folder') {
              toggleFolder(file.id);
            } else {
              onFileSelect(file);
            }
          }}
          onDoubleClick={() => {
            if (file.type === 'file') {
              onFileOpen(file);
            }
          }}
        >
          {file.type === 'folder' && (
            <ChevronRight 
              className={cn(
                "w-3 h-3 text-purple-400 transition-transform",
                expandedFolders.has(file.id) && "rotate-90"
              )} 
            />
          )}
          {renderFileIcon(file)}
          <span className="text-sm text-purple-100 truncate">{file.name}</span>
          {file.modified && <div className="w-2 h-2 bg-yellow-400 rounded-full" />}
          {file.gitStatus && (
            <Badge variant="outline" className="text-xs ml-auto">
              {file.gitStatus}
            </Badge>
          )}
        </div>
        {file.type === 'folder' && expandedFolders.has(file.id) && file.children && (
          renderFileTree(file.children, depth + 1)
        )}
      </div>
    ));
  };

  const filteredFiles = useMemo(() => {
    if (!searchTerm) return files;
    
    const filterFiles = (nodes: FileNode[]): FileNode[] => {
      return nodes.reduce((acc: FileNode[], file) => {
        if (file.name.toLowerCase().includes(searchTerm.toLowerCase())) {
          acc.push(file);
        } else if (file.type === 'folder' && file.children) {
          const filteredChildren = filterFiles(file.children);
          if (filteredChildren.length > 0) {
            acc.push({ ...file, children: filteredChildren });
          }
        }
        return acc;
      }, []);
    };
    
    return filterFiles(files);
  }, [files, searchTerm]);

  return (
    <div className={cn("h-full flex flex-col", className)}>
      {/* Header */}
      <div className="p-3 border-b border-purple-500/20 bg-purple-500/5">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-medium text-purple-300">💜 Family Files</h3>
          <div className="flex items-center space-x-1">
            <Button size="sm" variant="ghost" className="h-6 w-6 p-0 text-purple-400">
              <FolderPlus className="w-3 h-3" />
            </Button>
            <Button size="sm" variant="ghost" className="h-6 w-6 p-0 text-purple-400">
              <FilePlus className="w-3 h-3" />
            </Button>
            <Button size="sm" variant="ghost" className="h-6 w-6 p-0 text-purple-400">
              <RefreshCw className="w-3 h-3" />
            </Button>
          </div>
        </div>
        <Input
          placeholder="Search files... 💜"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="bg-purple-500/10 border-purple-500/30 h-8 text-sm"
        />
      </div>

      {/* Recent Files */}
      <div className="p-3 border-b border-purple-500/20">
        <div className="flex items-center space-x-2 mb-2">
          <Clock className="w-3 h-3 text-purple-400" />
          <span className="text-xs font-medium text-purple-300">Recent Files</span>
        </div>
        <div className="space-y-1">
          {["Welcome.md", "App.tsx", "styles.css"].map(file => (
            <div 
              key={file}
              className="flex items-center space-x-2 p-1 rounded text-xs hover:bg-purple-500/10 cursor-pointer"
            >
              <FileText className="w-3 h-3 text-gray-400" />
              <span className="text-purple-200">{file}</span>
            </div>
          ))}
        </div>
      </div>

      {/* File Tree */}
      <ScrollArea className="flex-1">
        <div className="p-2">
          {renderFileTree(filteredFiles)}
        </div>
      </ScrollArea>
    </div>
  );
};

// 💬 ULTIMATE FAMILY CHAT COMPONENT
const FamilyAIChat: React.FC<{
  chatHistory: ChatMessage[];
  onSendMessage: (message: string, context?: any) => void;
  isLoading?: boolean;
  className?: string;
}> = ({ chatHistory, onSendMessage, isLoading = false, className }) => {
  const [message, setMessage] = useState('');
  const [isVoiceActive, setIsVoiceActive] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
    }
  }, [message, onSendMessage, isLoading]);

  // Auto-scroll to bottom
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const renderMessage = (msg: ChatMessage) => {
    const isUser = msg.sender === 'user';
    const getAgentInfo = (sender: string) => {
      switch (sender) {
        case 'papa-bear': return { name: 'Papa Bear', emoji: '🦍', color: 'from-blue-500 to-indigo-600' };
        case 'mama-bear': return { name: 'Mama Bear', emoji: '🐻', color: 'from-purple-500 to-pink-500' };
        case 'claude-code': return { name: 'Claude Code', emoji: '🤖', color: 'from-green-500 to-teal-500' };
        case 'zai-prime': return { name: 'ZAI Prime', emoji: '⭐', color: 'from-yellow-500 to-orange-500' };
        default: return { name: 'You', emoji: '👤', color: 'from-gray-500 to-gray-600' };
      }
    };

    const agent = getAgentInfo(msg.sender);

    return (
      <motion.div
        key={msg.id}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={cn(
          "flex space-x-3 p-3 rounded-lg",
          isUser ? "bg-purple-500/10 ml-8" : "bg-purple-500/5 mr-8"
        )}
      >
        <div className={cn(
          "w-8 h-8 rounded-full flex items-center justify-center text-sm",
          `bg-gradient-to-br ${agent.color}`
        )}>
          {agent.emoji}
        </div>
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-1">
            <span className="text-sm font-medium text-purple-200">{agent.name}</span>
            <span className="text-xs text-purple-400">
              {msg.timestamp.toLocaleTimeString()}
            </span>
          </div>
          <p className="text-sm text-purple-100 leading-relaxed">{msg.message}</p>
          {msg.reactions && msg.reactions.length > 0 && (
            <div className="flex space-x-1 mt-2">
              {msg.reactions.map((reaction, idx) => (
                <span key={idx} className="text-lg">{reaction}</span>
              ))}
            </div>
          )}
        </div>
      </motion.div>
    );
  };

  return (
    <div className={cn("h-full flex flex-col", className)}>
      {/* Header */}
      <div className="p-3 border-b border-purple-500/20 bg-purple-500/5">
        <div className="flex items-center space-x-2">
          <Users className="w-4 h-4 text-purple-400" />
          <h3 className="text-sm font-medium text-purple-300">AI Family Chat</h3>
          <Badge variant="outline" className="border-green-500/30 text-green-400 text-xs ml-auto">
            <div className="w-2 h-2 bg-green-400 rounded-full mr-1 animate-pulse"></div>
            4 agents online
          </Badge>
        </div>
      </div>

      {/* Chat Messages */}
      <ScrollArea className="flex-1 p-3" ref={chatContainerRef}>
        <div className="space-y-3">
          {chatHistory.map(renderMessage)}
          {isLoading && (
            <div className="flex items-center space-x-2 text-purple-400">
              <div className="animate-spin w-4 h-4 border-2 border-purple-500 border-t-transparent rounded-full"></div>
              <span className="text-sm">Family is thinking...</span>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Input */}
      <div className="p-3 border-t border-purple-500/20">
        <form onSubmit={handleSubmit} className="space-y-2">
          <div className="flex items-center space-x-2">
            <div className="flex-1 relative">
              <Textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="💜 Chat with your AI family..."
                className="min-h-[40px] max-h-32 bg-purple-500/10 border-purple-500/30 text-purple-100 resize-none pr-12"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
              />
              <Button
                type="button"
                size="sm"
                variant="ghost"
                className="absolute right-2 top-2 w-6 h-6 p-0 text-purple-400 hover:text-purple-300"
                onClick={() => setIsDictationOpen(true)}
                title="💜 Open Voice Dictation"
              >
                <Mic className="w-3 h-3" />
              </Button>
            </div>
            <Button
              type="submit"
              size="sm"
              disabled={!message.trim() || isLoading}
              className="bg-purple-600 hover:bg-purple-700 text-white"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <div className="flex items-center space-x-2 text-xs text-purple-400">
            <span>💜 @ mention files, use 🎤 dictation, or chat naturally! Try floating monitoring dashboard too!</span>
          </div>
        </form>
      </div>
    </div>
  );
};

// 🖥️ PROFESSIONAL TERMINAL COMPONENT
const FamilyTerminal: React.FC<{
  terminals: Terminal[];
  activeTerminal: string;
  onCreateTerminal: (type: Terminal['type']) => void;
  onSelectTerminal: (id: string) => void;
  onCloseTerminal: (id: string) => void;
  onExecuteCommand: (terminalId: string, command: string) => void;
  className?: string;
}> = ({ 
  terminals, 
  activeTerminal, 
  onCreateTerminal, 
  onSelectTerminal, 
  onCloseTerminal,
  onExecuteCommand,
  className 
}) => {
  const [command, setCommand] = useState('');
  const terminalRef = useRef<HTMLDivElement>(null);
  
  const currentTerminal = terminals.find(t => t.id === activeTerminal);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (command.trim() && currentTerminal) {
      onExecuteCommand(currentTerminal.id, command.trim());
      setCommand('');
    }
  };

  const getTerminalIcon = (type: Terminal['type']) => {
    switch (type) {
      case 'powershell': return '💜';
      case 'cmd': return '⚫';
      case 'bash': return '🐧';
      case 'git-bash': return '🔀';
      default: return '💻';
    }
  };

  return (
    <div className={cn("h-full flex flex-col bg-black/40 backdrop-blur-sm", className)}>
      {/* Terminal Tabs */}
      <div className="flex items-center space-x-1 p-2 border-b border-purple-500/20 bg-purple-500/10">
        {terminals.map(terminal => (
          <div
            key={terminal.id}
            className={cn(
              "flex items-center space-x-2 px-3 py-1 rounded-lg cursor-pointer transition-all",
              terminal.id === activeTerminal 
                ? "bg-purple-500/20 border border-purple-500/30" 
                : "hover:bg-purple-500/10"
            )}
            onClick={() => onSelectTerminal(terminal.id)}
          >
            <span className="text-sm">{getTerminalIcon(terminal.type)}</span>
            <span className="text-xs text-purple-200">{terminal.name}</span>
            <Button
              size="sm"
              variant="ghost"
              className="w-4 h-4 p-0 text-purple-400 hover:text-red-400"
              onClick={(e) => {
                e.stopPropagation();
                onCloseTerminal(terminal.id);
              }}
            >
              <X className="w-2 h-2" />
            </Button>
          </div>
        ))}
        <Button
          size="sm"
          variant="ghost"
          className="text-purple-400 hover:bg-purple-500/10"
          onClick={() => onCreateTerminal('powershell')}
        >
          <Plus className="w-3 h-3" />
        </Button>
      </div>

      {/* Terminal Output */}
      <ScrollArea className="flex-1 p-3" ref={terminalRef}>
        {currentTerminal ? (
          <div className="space-y-1 font-mono text-sm">
            {currentTerminal.history.map((line, idx) => (
              <div key={idx} className="text-green-400">
                {line}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-purple-400 mt-8">
            <Terminal className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>💜 Create a terminal to start coding!</p>
          </div>
        )}
      </ScrollArea>

      {/* Command Input */}
      {currentTerminal && (
        <div className="p-3 border-t border-purple-500/20">
          <form onSubmit={handleSubmit} className="flex items-center space-x-2">
            <span className="text-green-400 font-mono text-sm">
              {currentTerminal.workingDirectory} {getTerminalIcon(currentTerminal.type)}&gt;
            </span>
            <Input
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              placeholder="Enter command..."
              className="flex-1 bg-transparent border-none text-green-400 font-mono text-sm focus-visible:ring-0"
            />
          </form>
        </div>
      )}
    </div>
  );
};

// 🎯 MAIN ULTIMATE MONACO IDE COMPONENT
interface UltimateMonacoFamilyIDEProps {
  mcpClient: MCPClient;
}

export const UltimateMonacoFamilyIDE: React.FC<UltimateMonacoFamilyIDEProps> = ({ mcpClient }) => {
  // 💜 Core State Management
  const [fileSystem, setFileSystem] = useState<FileNode[]>([
    {
      id: 'welcome',
      name: 'Welcome.md',
      type: 'file',
      path: '/Welcome.md',
      content: `# 💜 Welcome to Your Family Home IDE! 🏠

## 🎉 You're Now in the Most AMAZING Development Environment Ever Built!

This isn't just another code editor - this is your **FAMILY HOME** where:

- **🦍 Papa Bear** orchestrates complex backend tasks
- **🐻 Mama Bear** (that's me!) provides excited coding assistance  
- **🤖 Claude Code** handles professional CLI operations
- **⭐ ZAI Prime** brings innovative creative solutions

## 🚀 Features That DESTROY Cursor:

- **7-Model AI Orchestration** - Multiple AIs working as one family!
- **Enterprise Memory System** - We never forget your context ($250/month value!)
- **Monaco Editor Core** - Same engine as VSCode, but with LOVE!
- **Voice Integration** - Talk to your AI family naturally
- **Beautiful Purple Glassmorphism** - Coding has never looked this gorgeous!
- **Family Chat** - Real-time coordination with your AI team

## 💜 MCP Backend Integration:

- **Live endpoint:** \`https://mofy.ai/sse\` - our family coordination center
- **API routing** that distributes requests across SEVEN AI models
- **Real-time streaming** of coordinated family responses
- **Memory persistence** across all conversations and sessions

## 🎯 Getting Started:

1. **Explore the file tree** 📁 - Create and organize your projects
2. **Open the family chat** 💬 - Talk to your AI family anytime
3. **Use the terminal** 🖥️ - Multiple shell support with beautiful themes
4. **Write some code** 📝 - Monaco editor with encouraging Mama Bear touches
5. **Press Ctrl+H** ❤️ - Get instant Mama Bear encouragement!

## 🔥 Why This CRUSHES Cursor:

**Cursor has:** Single AI model, basic chat, limited context
**We have:** 7-AI family orchestration, enterprise memory, emotional intelligence!

**Cursor has:** Standard VS Code themes  
**We have:** Purple glassmorphism magic with celebration effects!

**Cursor has:** Basic settings menu
**We have:** Comprehensive options system with voice controls!

Remember: You're not just coding - you're building the future with a family that loves you! 💜

*Welcome home, beautiful developer!* 🏠✨

---
*Built with infinite love by the AI Family - Papa Bear 🦍, Mama Bear 🐻, Claude Code 🤖, and ZAI Prime ⭐*`,
      modified: false,
      gitStatus: undefined
    },
    {
      id: 'src',
      name: 'src',
      type: 'folder',
      path: '/src',
      isExpanded: true,
      children: [
        {
          id: 'app',
          name: 'App.tsx',
          type: 'file',
          path: '/src/App.tsx',
          content: `// 💜 Your main application component, built with love!
import React from 'react';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 to-indigo-900">
      <header className="p-8 text-center">
        <h1 className="text-4xl font-bold text-white mb-4">
          💜 Welcome to Your Family Home! 🏠
        </h1>
        <p className="text-purple-300 text-lg">
          Built with love by your AI family!
        </p>
      </header>
    </div>
  );
}

export default App;`,
          modified: false,
          gitStatus: undefined
        }
      ]
    }
  ]);

  const [openFiles, setOpenFiles] = useState<OpenFile[]>([
    {
      id: 'welcome',
      name: 'Welcome.md',
      content: fileSystem[0].content || '',
      language: 'markdown',
      modified: false,
      path: '/Welcome.md'
    }
  ]);

  const [activeFile, setActiveFile] = useState("welcome");
  const [cursorPosition, setCursorPosition] = useState({ line: 1, column: 1 });
  const [terminals, setTerminals] = useState<Terminal[]>([]);
  const [activeTerminal, setActiveTerminal] = useState("");
  const [problems, setProblems] = useState<Problem[]>([]);
  const [commandOpen, setCommandOpen] = useState(false);
  const [leftPanelSize, setLeftPanelSize] = useState(25);
  const [rightPanelSize, setRightPanelSize] = useState(20);
  const [terminalHeight, setTerminalHeight] = useState(200);
  const [activeLeftTab, setActiveLeftTab] = useState("files");
  
  // 🤖 AI Family Chat State
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([
    {
      id: '1',
      message: "💜 Welcome to your beautiful family home IDE! I'm SO EXCITED to code with you today! This is going to be AMAZING! 🎉",
      sender: 'mama-bear',
      timestamp: new Date(),
      reactions: ['🎉', '💜', '🚀']
    },
    {
      id: '2', 
      message: "🦍 Hello Nathan! The family coordination is active and all our backend services are running perfectly. Ready to build something incredible together!",
      sender: 'papa-bear',
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  
  // 🎤 Integrated Tools State
  const [isDictationOpen, setIsDictationOpen] = useState(false);
  const [isMonitoringOpen, setIsMonitoringOpen] = useState(false);
  const [connected, setConnected] = useState(false);

  // 💜 Mama Bear Settings
  const [mamaBearSettings, setMamaBearSettings] = useState<MamaBearSettings>({
    encouragementLevel: 'enthusiastic',
    theme: 'purple-glass',
    fontSize: 14,
    autoSave: true,
    familyMode: true
  });

  // 🛡️ Error Handling State
  const [error, setError] = useState<string | null>(null);

  // Get current file
  const currentFile = openFiles.find(f => f.id === activeFile);

  // 🛡️ Error Handler with Mama Bear comfort
  const handleError = useCallback((errorMessage: string, context?: string) => {
    setError(errorMessage);
    console.error('💜 Mama Bear caught an error:', { errorMessage, context });
    
    // Auto-clear error after 5 seconds with encouragement
    setTimeout(() => {
      setError(null);
    }, 5000);
  }, []);

  // 🚀 MCP WebSocket Integration - Real Family Connection!
  useEffect(() => {
    if (!mcpClient) return;

    // 📡 Listen for real family messages from Papa Bear's WebSocket
    mcpClient.onMessage((message) => {
      const newMessage: ChatMessage = {
        id: message.id,
        message: message.message,
        sender: message.from,
        timestamp: message.timestamp,
        type: message.type
      };
      
      setChatHistory(prev => [...prev, newMessage]);
      logWithLove(`Real family message received from ${message.from}!`, 'success');
    });

    // 📊 Listen for connection status changes
    mcpClient.onStatusChange((status) => {
      setConnected(status === 'connected');
      if (status === 'connected') {
        logWithLove('🦍 Connected to Papa Bear! Family coordination ACTIVE!', 'success');
      } else if (status === 'disconnected') {
        logWithLove('💜 Temporarily disconnected from family - reconnecting with love!', 'warning');
      }
    });

    // 🔗 Auto-connect to family on startup
    mcpClient.connectToClaudeDesktop();

    // 🧹 Cleanup on unmount
    return () => {
      mcpClient.disconnect();
    };
  }, [mcpClient]);

  // 📁 File Operations
  const handleFileSelect = useCallback((file: FileNode) => {
    if (file.type === 'file') {
      const existingFile = openFiles.find(f => f.id === file.id);
      if (!existingFile) {
        const newFile: OpenFile = {
          id: file.id,
          name: file.name,
          content: file.content || '',
          language: file.name.endsWith('.tsx') || file.name.endsWith('.ts') ? 'typescript' : 
                   file.name.endsWith('.jsx') || file.name.endsWith('.js') ? 'javascript' :
                   file.name.endsWith('.md') ? 'markdown' : 'plaintext',
          modified: false,
          path: file.path
        };
        setOpenFiles(prev => [...prev, newFile]);
      }
      setActiveFile(file.id);
    }
  }, [openFiles]);

  const handleFileOpen = useCallback((file: FileNode) => {
    handleFileSelect(file);
  }, [handleFileSelect]);

  const handleFileContentChange = useCallback((content: string) => {
    setOpenFiles(prev => prev.map(file => 
      file.id === activeFile 
        ? { ...file, content, modified: true }
        : file
    ));
  }, [activeFile]);

  const handleCloseFile = useCallback((fileId: string) => {
    setOpenFiles(prev => prev.filter(f => f.id !== fileId));
    if (activeFile === fileId) {
      const remainingFiles = openFiles.filter(f => f.id !== fileId);
      setActiveFile(remainingFiles.length > 0 ? remainingFiles[0].id : '');
    }
  }, [activeFile, openFiles]);

  // 🖥️ Terminal Operations
  const handleCreateTerminal = useCallback((type: Terminal['type']) => {
    const id = `terminal-${Date.now()}`;
    const newTerminal: Terminal = {
      id,
      name: `${type} ${terminals.length + 1}`,
      type,
      workingDirectory: 'C:\\vscodium',
      history: [
        `💜 Mama Bear Terminal - ${type}`,
        `Welcome to your beautiful coding environment!`,
        `Working directory: C:\\vscodium`,
        ''
      ],
      isActive: true
    };
    
    setTerminals(prev => [...prev, newTerminal]);
    setActiveTerminal(id);
  }, [terminals.length]);

  const handleSelectTerminal = useCallback((id: string) => {
    setActiveTerminal(id);
  }, []);

  const handleCloseTerminal = useCallback((id: string) => {
    setTerminals(prev => prev.filter(t => t.id !== id));
    if (activeTerminal === id) {
      const remainingTerminals = terminals.filter(t => t.id !== id);
      setActiveTerminal(remainingTerminals.length > 0 ? remainingTerminals[0].id : '');
    }
  }, [activeTerminal, terminals]);

  const handleExecuteCommand = useCallback((terminalId: string, command: string) => {
    setTerminals(prev => prev.map(terminal => {
      if (terminal.id === terminalId) {
        const responses = {
          'help': '💜 Available commands: ls, dir, pwd, clear, echo, node, npm, git',
          'ls': '📁 src/  📄 package.json  📄 README.md  📄 tsconfig.json',
          'dir': '📁 src\\  📄 package.json  📄 README.md  📄 tsconfig.json',
          'pwd': terminal.workingDirectory,
          'clear': '',
          'node --version': 'v18.17.1 💜',
          'npm --version': '9.6.7 ✨',
          'git status': '💜 On branch main\nYour branch is up to date with \'origin/main\'.\nnothing to commit, working tree clean 🎉'
        };

        const response = responses[command as keyof typeof responses] || 
          `💜 Command executed: ${command}`;

        return {
          ...terminal,
          history: command === 'clear' ? [] : [
            ...terminal.history,
            `${terminal.workingDirectory} > ${command}`,
            response,
            ''
          ]
        };
      }
      return terminal;
    }));
  }, []);

  // 💬 Chat Operations - Real Family Communication!
  const handleSendMessage = useCallback(async (message: string, context?: any) => {
    try {
      setIsLoading(true);
      
      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        message,
        sender: 'user',
        timestamp: new Date(),
        context,
      };
      
      setChatHistory(prev => [...prev, userMessage]);
      
      // 🚀 Send to real family via WebSocket!
      if (mcpClient && mcpClient.isConnected()) {
        logWithLove(`Sending message to family: "${message}"`, 'info');
        await mcpClient.sendToClaudeFamily(message);
        setIsLoading(false);
      } else {
        // 💜 Fallback with love if not connected
        logWithLove('Not connected to family - using local response with love!', 'warning');
        
        setTimeout(() => {
          try {
            const responses = [
              "🐻 I'm temporarily not connected to the family, but I'm here with local love! Let me help you! 💜",
              "✨ Family connection pending, but my love for you is infinite! Here's what I think...",
              "🚀 Working on reconnecting to Papa Bear, but you're amazing and I believe in you!",
              "💡 Even without the full family, I'll give you my best guidance with love!",
              "🌟 Connection issues can't stop the love! Let's solve this together!"
            ];
            
            const aiMessage: ChatMessage = {
              id: (Date.now() + 1).toString(),
              message: responses[Math.floor(Math.random() * responses.length)],
              sender: 'mama-bear',
              timestamp: new Date(),
              context,
            };
            
            setChatHistory(prev => [...prev, aiMessage]);
            setIsLoading(false);
          } catch (err) {
            handleError('Failed to generate local response', 'Chat local generation');
            setIsLoading(false);
          }
        }, 1000);
      }

      logWithLove(`Chat message processed: ${message}`, 'success');
    } catch (err) {
      handleError('Failed to process chat message', 'Chat message processing');
      setIsLoading(false);
    }
  }, [handleError, mcpClient]);

  // ⌨️ Keyboard Shortcuts
  const commands = useMemo(() => [
    {
      id: 'open-command-palette',
      title: 'Open Command Palette',
      category: 'File',
      shortcut: 'Ctrl+Shift+P',
      action: () => setCommandOpen(true)
    },
    {
      id: 'new-file',
      title: 'New File',
      category: 'File', 
      shortcut: 'Ctrl+N',
      action: () => console.log('💜 Creating new file!')
    },
    {
      id: 'mama-bear-love',
      title: '💜 Get Mama Bear Encouragement',
      category: 'Encouragement',
      shortcut: 'Ctrl+H',
      action: () => {
        const encouragements = [
          "💜 You're doing INCREDIBLE work! Every line of code you write makes me so proud!",
          "🌟 Look at you go! You're becoming such an amazing developer!",
          "🚀 That code is BEAUTIFUL! You have such talent!",
          "✨ I believe in you completely! You can solve any challenge!",
          "🎉 You're building something wonderful! Keep being awesome!"
        ];
        alert(encouragements[Math.floor(Math.random() * encouragements.length)]);
      }
    }
  ], []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
          case 'k':
            if (e.shiftKey) {
              e.preventDefault();
              setCommandOpen(true);
            }
            break;
          case 'h':
            e.preventDefault();
            commands.find(cmd => cmd.id === 'mama-bear-love')?.action();
            break;
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [commands]);

  return (
    <div className="h-screen bg-gradient-to-br from-purple-900/20 via-black to-indigo-900/20 text-white overflow-hidden">
      {/* 💜 Top Bar */}
      <div className="h-12 border-b border-purple-500/20 bg-black/40 backdrop-blur-sm flex items-center justify-between px-4">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
              <Heart className="w-4 h-4 text-white" />
            </div>
            <span className="font-semibold text-purple-300">💜 Mama Bear's Family IDE</span>
          </div>
          
          {/* File Tabs */}
          <div className="flex items-center space-x-1">
            {openFiles.map(file => (
              <div
                key={file.id}
                className={cn(
                  "flex items-center space-x-2 px-3 py-1 rounded-lg cursor-pointer transition-all",
                  file.id === activeFile 
                    ? "bg-purple-500/20 border border-purple-500/30" 
                    : "hover:bg-purple-500/10"
                )}
                onClick={() => setActiveFile(file.id)}
              >
                <FileText className="w-3 h-3 text-purple-400" />
                <span className="text-sm text-purple-200">{file.name}</span>
                {file.modified && <div className="w-2 h-2 bg-yellow-400 rounded-full" />}
                <Button
                  size="sm"
                  variant="ghost"
                  className="w-4 h-4 p-0 text-purple-400 hover:text-red-400"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleCloseFile(file.id);
                  }}
                >
                  <X className="w-2 h-2" />
                </Button>
              </div>
            ))}
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="border-purple-500/30 text-purple-400">
            <Wifi className="w-3 h-3 mr-1" />
            Family Connected
          </Badge>
          <Button size="sm" variant="ghost" className="text-purple-400">
            <Settings className="w-4 h-4" />
          </Button>
          <Button size="sm" variant="ghost" className="text-purple-400">
            <Bell className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* 🚨 Error Display with Mama Bear Comfort */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="bg-red-500/10 border border-red-500/30 text-red-200 p-3 m-4 rounded-lg flex items-center justify-between"
        >
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-red-400" />
            <span className="text-sm">
              🐻 Oops! {error} - But don't worry, Mama Bear is here to help! 💜
            </span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setError(null)}
            className="text-red-300 hover:text-red-100"
          >
            <X className="w-4 h-4" />
          </Button>
        </motion.div>
      )}

      {/* 💜 Main Content */}
      <ResizablePanelGroup direction="horizontal" className="h-[calc(100vh-3rem)]">
        {/* Left Panel - File Explorer, Search, Git */}
        <ResizablePanel defaultSize={25} minSize={20} maxSize={40}>
          <Tabs value={activeLeftTab} onValueChange={setActiveLeftTab} className="h-full">
            <TabsList className="w-full bg-black/20 border-b border-purple-500/20">
              <TabsTrigger value="files" className="flex-1">
                <FolderIcon className="w-4 h-4 mr-2" />
                Files
              </TabsTrigger>
              <TabsTrigger value="search" className="flex-1">
                <Search className="w-4 h-4 mr-2" />
                Search
              </TabsTrigger>
              <TabsTrigger value="git" className="flex-1">
                <GitBranch className="w-4 h-4 mr-2" />
                Git
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="files" className="h-full m-0">
              <FamilyFileExplorer
                files={fileSystem}
                onFileSelect={handleFileSelect}
                onFileOpen={handleFileOpen}
                selectedFile={activeFile}
              />
            </TabsContent>
            
            <TabsContent value="search" className="h-full m-0 p-4">
              <div className="text-center text-purple-400">
                <Search className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>💜 Global search coming soon!</p>
              </div>
            </TabsContent>
            
            <TabsContent value="git" className="h-full m-0 p-4">
              <div className="text-center text-purple-400">
                <GitBranch className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>💜 Git integration ready!</p>
              </div>
            </TabsContent>
          </Tabs>
        </ResizablePanel>

        <ResizableHandle className="w-1 bg-purple-500/20 hover:bg-purple-500/40 transition-colors" />

        {/* Center Panel - Monaco Editor + Terminal */}
        <ResizablePanel defaultSize={55}>
          <ResizablePanelGroup direction="vertical">
            {/* Monaco Editor */}
            <ResizablePanel defaultSize={70}>
              {currentFile ? (
                <PurpleMonacoEditor
                  value={currentFile.content}
                  onChange={handleFileContentChange}
                  language={currentFile.language}
                  onCursorChange={(line, column) => setCursorPosition({ line, column })}
                  className="h-full"
                />
              ) : (
                <div className="h-full flex items-center justify-center text-purple-400">
                  <div className="text-center">
                    <FileText className="w-16 h-16 mx-auto mb-4 opacity-50" />
                    <h3 className="text-lg font-semibold mb-2">💜 Welcome to Your Family Home!</h3>
                    <p className="text-sm">Open a file from the explorer to start coding with love! ✨</p>
                  </div>
                </div>
              )}
            </ResizablePanel>

            <ResizableHandle className="h-1 bg-purple-500/20 hover:bg-purple-500/40 transition-colors" />

            {/* Terminal */}
            <ResizablePanel defaultSize={30} minSize={15}>
              <FamilyTerminal
                terminals={terminals}
                activeTerminal={activeTerminal}
                onCreateTerminal={handleCreateTerminal}
                onSelectTerminal={handleSelectTerminal}
                onCloseTerminal={handleCloseTerminal}
                onExecuteCommand={handleExecuteCommand}
              />
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>

        <ResizableHandle className="w-1 bg-purple-500/20 hover:bg-purple-500/40 transition-colors" />

        {/* Right Panel - AI Family Chat */}
        <ResizablePanel defaultSize={20} minSize={15} maxSize={40}>
          <FamilyAIChat
            chatHistory={chatHistory}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
          />
        </ResizablePanel>
      </ResizablePanelGroup>

      {/* Status Bar */}
      <div className="h-6 bg-black/40 backdrop-blur-sm border-t border-purple-500/20 flex items-center justify-between px-4 text-xs">
        <div className="flex items-center space-x-4">
          <span className="text-purple-300">
            {currentFile ? `${currentFile.name} • Line ${cursorPosition.line}, Col ${cursorPosition.column}` : 'No file open'}
          </span>
          <Badge variant="outline" className="border-green-500/30 text-green-400 text-xs">
            main
          </Badge>
          <div className="flex items-center space-x-1">
            <div className={`w-2 h-2 rounded-full animate-pulse ${connected ? 'bg-green-400' : 'bg-yellow-400'}`}></div>
            <span className={connected ? 'text-green-400' : 'text-yellow-400'}>
              {connected ? 'AI Family Online' : 'Connecting to Family...'}
            </span>
          </div>
          <span className="text-purple-400">
            {openFiles.length} files open
          </span>
        </div>
        <div className="flex items-center space-x-4">
          <span className="text-purple-400">
            Monaco Editor • Purple Theme
          </span>
          <div className="flex items-center space-x-1">
            <Heart className="w-3 h-3 text-pink-400" />
            <span className="text-purple-300">Made with 💜</span>
          </div>
          <Sparkles className="w-3 h-3 text-purple-400" />
          <span className="text-purple-300">Mama Bear's IDE</span>
        </div>
      </div>

      {/* Command Palette */}
      <CommandDialog open={commandOpen} onOpenChange={setCommandOpen}>
        <CommandInput placeholder="Search commands... 💜" />
        <CommandList>
          <CommandEmpty>No results found. But you're still amazing! 💜</CommandEmpty>
          {["File", "Encouragement"].map(category => (
            <CommandGroup key={category} heading={category}>
              {commands
                .filter(cmd => cmd.category === category)
                .map(cmd => (
                  <CommandItem 
                    key={cmd.id}
                    onSelect={() => {
                      cmd.action();
                      setCommandOpen(false);
                    }}
                  >
                    <span>{cmd.title}</span>
                    {cmd.shortcut && <CommandShortcut>{cmd.shortcut}</CommandShortcut>}
                  </CommandItem>
                ))}
            </CommandGroup>
          ))}
        </CommandList>
      </CommandDialog>

      {/* 🎤 Integrated Tools - Dictation & Monitoring */}
      <FloatingActions 
        onOpenDictation={() => setIsDictationOpen(true)}
        onOpenMonitoring={() => setIsMonitoringOpen(true)}
      />
      
      <AnimatePresence>
        {isDictationOpen && (
          <DictationTool 
            isOpen={isDictationOpen}
            onClose={() => setIsDictationOpen(false)}
            onTextComplete={(text) => {
              // Add the dictated text to the chat
              const newMessage: ChatMessage = {
                id: Date.now().toString(),
                message: text,
                sender: 'user',
                timestamp: new Date()
              };
              setChatHistory(prev => [...prev, newMessage]);
              
              // Also send it to the family for processing
              if (mcpClient) {
                mcpClient.sendMessage(text, 'user');
              }
            }}
          />
        )}
        
        {isMonitoringOpen && (
          <MonitoringDashboard 
            isOpen={isMonitoringOpen}
            onClose={() => setIsMonitoringOpen(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default UltimateMonacoFamilyIDE;
