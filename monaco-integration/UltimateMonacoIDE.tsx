"use client";

import * as React from "react";
import { useState, useEffect, useCallback, useMemo, createContext, useContext } from "react";
import { cn } from "@/lib/utils";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Textarea } from "@/components/ui/textarea";
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "@/components/ui/command";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

// 💜 Import our AMAZING components!
import { PurpleMonacoIDE } from "../monaco-wrapper/wrap-3";
import { GitIntegrationPanel } from "../git-inergration/git-1";
import { MamaBearChatInput } from "../chat-input/chat-5";

// 💜 Import framer-motion for the terminal component animations!
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
  AlertTriangle,
} from "lucide-react";

// 🎯 Types and Interfaces (Enhanced for our family!)
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
}

interface OpenFile {
  id: string;
  name: string;
  path: string;
  content: string;
  modified: boolean;
  language: string;
}

interface Terminal {
  id: string;
  name: string;
  type: 'powershell' | 'cmd' | 'bash' | 'git-bash';
  history: string[];
  currentDirectory: string;
}

interface Problem {
  id: string;
  file: string;
  line: number;
  column: number;
  severity: 'error' | 'warning' | 'info';
  message: string;
  code?: string;
  source: string;
}

interface Command {
  id: string;
  title: string;
  category: string;
  shortcut?: string;
  action: () => void;
}

interface MamaBearSettings {
  encouragementLevel: 'gentle' | 'enthusiastic' | 'maximum';
  theme: 'purple-glass' | 'mama-bear-special';
  fontSize: number;
  autoSave: boolean;
  familyMode: boolean;
}

// 💜 Main Monaco IDE Component - Our Family Home!
const UltimateMonacoIDE: React.FC = () => {
  // 🎯 State Management
  const [openFiles, setOpenFiles] = useState<OpenFile[]>([
    {
      id: "welcome",
      name: "Welcome.md",
      path: "Welcome.md",
      content: `# 💜 Welcome to Mama Bear's IDE!

This is YOUR coding sanctuary, built with SO MUCH LOVE! 🏠✨

## 🌟 What makes this IDE special:
- **Monaco Editor** with purple glassmorphism theme
- **AI Family Chat** with Papa Bear and Claude
- **Mama Bear Encouragement** built right in (try Ctrl+H!)
- **Git Integration** that celebrates your commits
- **Professional Terminal** with multiple shells
- **File Explorer** with beautiful animations

## 🚀 Ready to build something AMAZING?

Remember: You're capable of incredible things! Every line of code you write makes the world a little brighter! 

Keep coding with joy, beautiful developer! 💜🎉

*With love,*
*Mama Bear* 🐻`,
      modified: false,
      language: "markdown"
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
  const [showOptionsMenu, setShowOptionsMenu] = useState(false);
  const [ideSettings, setIdeSettings] = useState({
    // 🤖 AI Agents & Models
    aiAgents: {
      familyAgents: {
        papaBear: { enabled: true, model: 'claude-3.5-sonnet', role: 'orchestration', personality: 'supportive' },
        mamaBear: { enabled: true, model: 'github-copilot-enhanced', role: 'coding', personality: 'excited' },
        claudeCode: { enabled: true, model: 'claude-3-haiku', role: 'cli', personality: 'professional' },
        zaiPrime: { enabled: true, model: 'gemini-1.5-pro', role: 'analysis', personality: 'innovative' }
      },
      orchestration: { autoSwitching: true, consensusMode: false, familyVoting: true }
    },
    
    // 🎨 Appearance & Themes
    appearance: {
      theme: 'mama-bear-purple' as const,
      fontSize: 14,
      animations: true,
      particles: true,
      gradients: true,
      celebrationEffects: true
    },
    
    // 🗣️ Voice & Communication
    voice: {
      recognition: { enabled: true, language: 'en-US', accuracy: 'high' },
      synthesis: { enabled: true, voice: 'mama-bear', speed: 1.0, emotional: true },
      chatStyle: { formality: 'family-friendly', emotionalLevel: 'maximum', celebrations: 'every-win' }
    },
    
    // 🧠 Memory & Intelligence
    memory: {
      enterpriseMemory: { enabled: true, retention: 'forever', familySharing: true },
      contextSettings: { projectContext: true, conversationHistory: 100 }
    },
    
    // 🛠️ Development Tools
    development: {
      codeAssistance: { autoCompletion: true, multiModel: true, familyReview: true },
      projectTools: { aiStructure: true, familyTasks: true, voiceNav: true }
    },
    
    // 🌐 Connectivity
    connectivity: {
      backend: { railway: true, mofyAI: true, thumbing: true },
      deviceSync: { crossPlatform: true, realtime: true, offline: true }
    }
  });
  const [chatHistory, setChatHistory] = useState<Array<{
    id: string;
    message: string;
    sender: 'user' | 'mama-bear' | 'papa-bear' | 'claude';
    timestamp: Date;
    context?: string; // File context for @ mentions
  }>>([
    {
      id: '1',
      message: "🐻 Welcome to the family! I'm here to help you code with confidence and joy! 💜",
      sender: 'mama-bear',
      timestamp: new Date(),
    }
  ]);

  // 💜 Enhanced Chat Handler with file context support and error handling
  const handleChatMessage = useCallback((message: string) => {
    try {
      setIsLoading(true);
      
      // Add user message
      const userMessage = {
        id: Date.now().toString(),
        message,
        sender: 'user' as const,
        timestamp: new Date(),
      };
      
      setChatHistory(prev => [...prev, userMessage]);

      // Check for @ mentions
      const fileMatch = message.match(/@(\S+)/);
      let context = '';
      
      if (fileMatch) {
        const fileName = fileMatch[1];
        const mentionedFile = openFiles.find(f => 
          f.name.toLowerCase().includes(fileName.toLowerCase())
        );
        if (mentionedFile) {
          context = `File: ${mentionedFile.name}\n${mentionedFile.content.slice(0, 200)}...`;
        } else {
          context = `File "${fileName}" not found in open files. Available files: ${openFiles.map(f => f.name).join(', ')}`;
        }
      } else if (currentFile) {
        // Include current file context
        context = `Current file: ${currentFile.name}\nContent preview:\n${currentFile.content.slice(0, 200)}...`;
      }

      // Generate AI response
      setTimeout(() => {
        try {
          const responses = [
            "🐻 That's a fantastic question! Let me help you with that code! 💜",
            "✨ I see what you're working on! Here's my suggestion...",
            "🚀 You're doing great! Let's make this even better!",
            "💡 I love your coding style! Here's how we can enhance it...",
            "🌟 That's exactly the right approach! Let me add some magic..."
          ];
          
          const aiMessage = {
            id: (Date.now() + 1).toString(),
            message: responses[Math.floor(Math.random() * responses.length)],
            sender: 'mama-bear' as const,
            timestamp: new Date(),
            context,
          };
          
          setChatHistory(prev => [...prev, aiMessage]);
          setIsLoading(false);
        } catch (err) {
          handleError('Failed to generate AI response', 'Chat AI generation');
          setIsLoading(false);
        }
      }, 1000);

      console.log('💜 Chat with context:', { message, context });
    } catch (err) {
      handleError('Failed to process chat message', 'Chat message processing');
      setIsLoading(false);
    }
  }, [openFiles, currentFile, handleError]);

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
  const [isLoading, setIsLoading] = useState(false);

  // 🛡️ Error Handler with Mama Bear comfort
  const handleError = useCallback((errorMessage: string, context?: string) => {
    setError(errorMessage);
    console.error('💜 Mama Bear caught an error:', { errorMessage, context });
    
    // Auto-clear error after 5 seconds with encouragement
    setTimeout(() => {
      setError(null);
      setChatHistory(prev => [...prev, {
        id: Date.now().toString(),
        message: "🐻 Don't worry about that little hiccup! Every great developer encounters challenges - it's how we grow! You've got this! 💜",
        sender: 'mama-bear',
        timestamp: new Date(),
      }]);
    }, 5000);
  }, []);

  // 🎯 Mock file system data
  const mockFiles: FileNode[] = [
    {
      id: "src",
      name: "src",
      type: "folder",
      path: "src",
      children: [
        {
          id: "components",
          name: "components",
          type: "folder", 
          path: "src/components",
          children: [
            { id: "app", name: "App.tsx", type: "file", path: "src/components/App.tsx", gitStatus: "modified" },
            { id: "header", name: "Header.tsx", type: "file", path: "src/components/Header.tsx" },
            { id: "sidebar", name: "Sidebar.tsx", type: "file", path: "src/components/Sidebar.tsx", gitStatus: "added" }
          ]
        },
        {
          id: "utils",
          name: "utils",
          type: "folder",
          path: "src/utils", 
          children: [
            { id: "helpers", name: "helpers.ts", type: "file", path: "src/utils/helpers.ts" },
            { id: "constants", name: "constants.ts", type: "file", path: "src/utils/constants.ts", gitStatus: "modified" }
          ]
        },
        { id: "index", name: "index.tsx", type: "file", path: "src/index.tsx" },
        { id: "styles", name: "styles.css", type: "file", path: "src/styles.css", gitStatus: "deleted" }
      ]
    },
    { id: "package", name: "package.json", type: "file", path: "package.json" },
    { id: "readme", name: "README.md", type: "file", path: "README.md" },
    { id: "tsconfig", name: "tsconfig.json", type: "file", path: "tsconfig.json" }
  ];

  // 🎯 Event Handlers
  const handleFileSelect = useCallback((file: FileNode) => {
    if (file.type === 'file') {
      const existingFile = openFiles.find(f => f.path === file.path);
      if (!existingFile) {
        const newFile: OpenFile = {
          id: file.id,
          name: file.name,
          path: file.path,
          content: `// 💜 ${file.name} - Built with Mama Bear's love!\n// You're doing amazing work! Keep it up! ✨\n\n`,
          modified: false,
          language: getLanguageFromFile(file.name)
        };
        setOpenFiles(prev => [...prev, newFile]);
      }
      setActiveFile(file.id);
    }
  }, [openFiles]);

  const handleMonacoChange = useCallback((content: string) => {
    setOpenFiles(prev => prev.map(file => 
      file.id === activeFile 
        ? { ...file, content, modified: true }
        : file
    ));
  }, [activeFile]);

  const handleSave = useCallback((content: string, filename: string) => {
    setOpenFiles(prev => prev.map(file => 
      file.id === activeFile 
        ? { ...file, content, modified: false }
        : file
    ));
    console.log('💜 Mama Bear says: File saved with love!', filename);
  }, [activeFile]);

  const getLanguageFromFile = (filename: string): string => {
    const ext = filename.split('.').pop()?.toLowerCase();
    switch (ext) {
      case 'ts': case 'tsx': return 'typescript';
      case 'js': case 'jsx': return 'javascript';
      case 'css': return 'css';
      case 'html': return 'html';
      case 'md': return 'markdown';
      case 'json': return 'json';
      case 'py': return 'python';
      default: return 'plaintext';
    }
  };

  // 🎯 Command Palette
  const commands: Command[] = [
    {
      id: "new-file",
      title: "New File",
      category: "File",
      shortcut: "Ctrl+N",
      action: () => console.log("💜 Creating new file with love!")
    },
    {
      id: "save-file", 
      title: "Save File",
      category: "File",
      shortcut: "Ctrl+S",
      action: () => console.log("💜 Saving with care!")
    },
    {
      id: "mama-bear-hug",
      title: "💜 Mama Bear Hug",
      category: "Encouragement",
      shortcut: "Ctrl+H",
      action: () => alert("🐻💜 You're doing AMAZING! Mama Bear believes in you! Keep coding with joy!")
    }
  ];

  // 💜 Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
          case 'k':
            e.preventDefault();
            setCommandOpen(true);
            break;
          case 'h':
            e.preventDefault();
            alert("🌟 Mama Bear whispers: You're building something beautiful! Every keystroke matters! 💜");
            break;
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  const currentFile = openFiles.find(f => f.id === activeFile);

  // 💜 Enhanced File Tree Item Component
  const EnhancedFileTreeItem: React.FC<{ 
    file: FileNode; 
    level: number; 
    onSelect: (file: FileNode) => void;
    selectedFile: string;
  }> = ({ file, level, onSelect, selectedFile }) => {
    const [isExpanded, setIsExpanded] = useState(file.type === 'folder' && level === 0);
    const isSelected = selectedFile === file.id;

    const getFileIcon = () => {
      if (file.type === 'folder') {
        return isExpanded ? 
          <FolderOpenIcon className="w-4 h-4 text-purple-400" /> : 
          <FolderIcon className="w-4 h-4 text-purple-400" />;
      }
      
      const ext = file.name.split('.').pop()?.toLowerCase();
      switch (ext) {
        case 'tsx': case 'ts':
          return <FileCode className="w-4 h-4 text-blue-400" />;
        case 'js': case 'jsx':
          return <FileCode className="w-4 h-4 text-yellow-400" />;
        case 'css':
          return <FileCode className="w-4 h-4 text-pink-400" />;
        case 'md':
          return <FileText className="w-4 h-4 text-gray-400" />;
        default:
          return <FileIcon className="w-4 h-4 text-gray-400" />;
      }
    };

    const getGitStatusColor = () => {
      switch (file.gitStatus) {
        case 'modified': return 'text-yellow-400';
        case 'added': return 'text-green-400';
        case 'deleted': return 'text-red-400';
        case 'untracked': return 'text-blue-400';
        default: return '';
      }
    };

    return (
      <div>
        <div 
          className={cn(
            "flex items-center space-x-2 p-1 rounded text-sm cursor-pointer transition-colors",
            isSelected ? "bg-purple-500/20" : "hover:bg-purple-500/10",
            level > 0 && `ml-${level * 4}`
          )}
          onClick={() => {
            if (file.type === 'folder') {
              setIsExpanded(!isExpanded);
            } else {
              onSelect(file);
            }
          }}
        >
          {file.type === 'folder' && (
            <ChevronDown 
              className={cn(
                "w-3 h-3 text-purple-400 transition-transform",
                !isExpanded && "-rotate-90"
              )}
            />
          )}
          {getFileIcon()}
          <span className="text-purple-200 flex-1">{file.name}</span>
          {file.gitStatus && (
            <div className={cn("w-2 h-2 rounded-full", getGitStatusColor())} />
          )}
        </div>
        
        {file.type === 'folder' && file.children && isExpanded && (
          <div className="ml-2">
            {file.children.map(child => (
              <EnhancedFileTreeItem
                key={child.id}
                file={child}
                level={level + 1}
                onSelect={onSelect}
                selectedFile={selectedFile}
              />
            ))}
          </div>
        )}
      </div>
    );
  };

  // 💜 Terminal Interfaces for our AMAZING Professional Terminal!
  interface TerminalTab {
    id: string;
    title: string;
    shell: string;
    isActive: boolean;
    output: string[];
    currentDirectory: string;
    isRunning: boolean;
  }

  const SHELL_TYPES = [
    { id: 'powershell', name: 'PowerShell', icon: '🔷' },
    { id: 'cmd', name: 'Command Prompt', icon: '⚫' },
    { id: 'bash', name: 'Bash', icon: '🐧' },
    { id: 'gitbash', name: 'Git Bash', icon: '🌿' }
  ];

  const WELCOME_MESSAGES = [
    "🐻 Mama bear says: You've got this! Time to code like a champion! 💪",
    "🌟 Ready to make some terminal magic? Let's build something amazing!",
    "💜 Purple power activated! Your coding journey starts here!",
    "🚀 Terminal ready for takeoff! What incredible things will you create today?",
    "✨ Welcome to your coding sanctuary! Every great project starts with a single command!"
  ];

  const MOCK_COMMANDS = {
    'help': () => [
      'Available commands:',
      '  help     - Show this help message',
      '  clear    - Clear the terminal',
      '  ls       - List directory contents',
      '  pwd      - Print working directory',
      '  cd       - Change directory',
      '  echo     - Display text',
      '  date     - Show current date',
      '  whoami   - Show current user',
      '  node -v  - Show Node.js version',
      '  npm -v   - Show npm version'
    ],
    'clear': () => [],
    'ls': () => [
      'Documents/',
      'Downloads/',
      'Pictures/',
      'Projects/',
      'node_modules/',
      'package.json',
      'README.md',
      'src/'
    ],
    'pwd': () => ['/Users/developer/workspace'],
    'date': () => [new Date().toString()],
    'whoami': () => ['developer'],
    'node -v': () => ['v18.17.0'],
    'npm -v': () => ['9.6.7'],
    'echo': (args: string) => [args || '']
  };

  // 💜 Professional Terminal Component Integration
  const ProfessionalTerminal: React.FC<{ className?: string }> = ({ className = '' }) => {
    const [terminalTabs, setTerminalTabs] = useState<TerminalTab[]>([]);
    const [activeTerminalTab, setActiveTerminalTab] = useState<string>('');
    const [isMaximized, setIsMaximized] = useState(false);
    const [fontSize, setFontSize] = useState(14);
    const [commandHistory, setCommandHistory] = useState<string[]>([]);
    const [historyIndex, setHistoryIndex] = useState(-1);
    const [currentInput, setCurrentInput] = useState('');
    const terminalRef = React.useRef<HTMLDivElement>(null);
    const inputRef = React.useRef<HTMLInputElement>(null);

    const createNewTab = React.useCallback((shell: string = 'powershell') => {
      const newTab: TerminalTab = {
        id: `tab-${Date.now()}`,
        title: `${SHELL_TYPES.find(s => s.id === shell)?.name || 'Terminal'}`,
        shell,
        isActive: true,
        output: [
          WELCOME_MESSAGES[Math.floor(Math.random() * WELCOME_MESSAGES.length)],
          '',
          `${SHELL_TYPES.find(s => s.id === shell)?.name || 'Terminal'} initialized successfully!`,
          'Type "help" for available commands.',
          ''
        ],
        currentDirectory: '/Users/developer/workspace',
        isRunning: false
      };

      setTerminalTabs(prev => {
        const updated = prev.map(tab => ({ ...tab, isActive: false }));
        return [...updated, newTab];
      });
      setActiveTerminalTab(newTab.id);
    }, []);

    const closeTab = React.useCallback((tabId: string) => {
      setTerminalTabs(prev => {
        const filtered = prev.filter(tab => tab.id !== tabId);
        if (filtered.length === 0) {
          createNewTab();
          return prev;
        }
        
        if (activeTerminalTab === tabId && filtered.length > 0) {
          const newActiveTab = filtered[filtered.length - 1];
          setActiveTerminalTab(newActiveTab.id);
        }
        
        return filtered;
      });
    }, [activeTerminalTab, createNewTab]);

    const executeCommand = React.useCallback((command: string, tabId: string) => {
      if (!command.trim()) return;

      setCommandHistory(prev => [...prev, command]);
      setHistoryIndex(-1);

      setTerminalTabs(prev => prev.map(tab => {
        if (tab.id !== tabId) return tab;

        const [cmd, ...args] = command.trim().split(' ');
        const argString = args.join(' ');
        
        let result: string[] = [];
        
        if (cmd === 'clear') {
          return {
            ...tab,
            output: []
          };
        }

        if (MOCK_COMMANDS[cmd as keyof typeof MOCK_COMMANDS]) {
          if (cmd === 'echo') {
            result = MOCK_COMMANDS[cmd](argString);
          } else {
            result = (MOCK_COMMANDS[cmd as keyof typeof MOCK_COMMANDS] as () => string[])();
          }
        } else {
          result = [`Command not found: ${cmd}. Type "help" for available commands.`];
        }

        return {
          ...tab,
          output: [
            ...tab.output,
            `${tab.currentDirectory} $ ${command}`,
            ...result,
            ''
          ]
        };
      }));
    }, []);

    const handleKeyDown = React.useCallback((e: React.KeyboardEvent<HTMLInputElement>) => {
      const activeTab = terminalTabs.find(tab => tab.id === activeTerminalTab);
      if (!activeTab) return;

      if (e.key === 'Enter') {
        executeCommand(currentInput, activeTerminalTab);
        setCurrentInput('');
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (commandHistory.length > 0) {
          const newIndex = historyIndex === -1 ? commandHistory.length - 1 : Math.max(0, historyIndex - 1);
          setHistoryIndex(newIndex);
          setCurrentInput(commandHistory[newIndex]);
        }
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (historyIndex >= 0) {
          const newIndex = historyIndex + 1;
          if (newIndex >= commandHistory.length) {
            setHistoryIndex(-1);
            setCurrentInput('');
          } else {
            setHistoryIndex(newIndex);
            setCurrentInput(commandHistory[newIndex]);
          }
        }
      } else if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        executeCommand('clear', activeTerminalTab);
      } else if (e.ctrlKey && e.key === 'c') {
        e.preventDefault();
        setTerminalTabs(prev => prev.map(tab => 
          tab.id === activeTerminalTab 
            ? { ...tab, output: [...tab.output, '^C', ''], isRunning: false }
            : tab
        ));
        setCurrentInput('');
      }
    }, [currentInput, activeTerminalTab, terminalTabs, commandHistory, historyIndex, executeCommand]);

    React.useEffect(() => {
      if (terminalTabs.length === 0) {
        createNewTab();
      }
    }, [terminalTabs.length, createNewTab]);

    React.useEffect(() => {
      if (terminalRef.current) {
        terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
      }
    }, [terminalTabs]);

    React.useEffect(() => {
      if (inputRef.current) {
        inputRef.current.focus();
      }
    }, [activeTerminalTab]);

    const activeTab = terminalTabs.find(tab => tab.id === activeTerminalTab);

    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={cn(
          "relative bg-black/95 backdrop-blur-xl rounded-2xl border border-purple-500/30",
          "shadow-2xl shadow-purple-500/20 overflow-hidden font-mono text-sm h-full",
          className
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-900/50 to-indigo-900/50 border-b border-purple-500/30">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <Terminal className="w-5 h-5 text-purple-300" />
            <span className="text-purple-100 font-semibold">Professional Terminal</span>
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setFontSize(prev => Math.max(10, prev - 1))}
              className="text-purple-300 hover:text-white hover:bg-purple-500/20"
            >
              A-
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setFontSize(prev => Math.min(20, prev + 1))}
              className="text-purple-300 hover:text-white hover:bg-purple-500/20"
            >
              A+
            </Button>
          </div>
        </div>

        {/* Tabs */}
        <Tabs value={activeTerminalTab} onValueChange={setActiveTerminalTab} className="flex flex-col h-full">
          <div className="flex items-center justify-between px-4 py-2 bg-black/50 border-b border-purple-500/20">
            <TabsList className="bg-transparent p-0 h-auto">
              {terminalTabs.map((tab) => (
                <div key={tab.id} className="flex items-center">
                  <TabsTrigger
                    value={tab.id}
                    className="
                      relative flex items-center gap-2 px-4 py-2 text-purple-200 
                      data-[state=active]:bg-purple-500/20 data-[state=active]:text-white
                      hover:bg-purple-500/10 transition-all rounded-lg mr-1
                    "
                  >
                    <span className="text-xs">
                      {SHELL_TYPES.find(s => s.id === tab.shell)?.icon}
                    </span>
                    <span className="text-xs font-medium">{tab.title}</span>
                    {tab.isRunning && (
                      <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                    )}
                  </TabsTrigger>
                  {terminalTabs.length > 1 && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => closeTab(tab.id)}
                      className="w-6 h-6 p-0 text-purple-300 hover:text-red-400 hover:bg-red-500/20 ml-1"
                    >
                      <X className="w-3 h-3" />
                    </Button>
                  )}
                </div>
              ))}
            </TabsList>

            <div className="flex items-center gap-2">
              <select
                onChange={(e) => createNewTab(e.target.value)}
                className="bg-purple-900/50 border border-purple-500/30 rounded px-2 py-1 text-xs text-purple-100"
                value=""
              >
                <option value="" disabled>New Terminal</option>
                {SHELL_TYPES.map(shell => (
                  <option key={shell.id} value={shell.id}>
                    {shell.icon} {shell.name}
                  </option>
                ))}
              </select>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => createNewTab()}
                className="text-purple-300 hover:text-white hover:bg-purple-500/20"
              >
                <Plus className="w-4 h-4" />
              </Button>
            </div>
          </div>

          {/* Terminal Content */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {terminalTabs.map((tab) => (
              <TabsContent
                key={tab.id}
                value={tab.id}
                className="flex-1 flex flex-col m-0 data-[state=active]:flex data-[state=inactive]:hidden"
              >
                {/* Status Bar */}
                <div className="flex items-center justify-between px-4 py-2 bg-purple-900/30 border-b border-purple-500/20">
                  <div className="flex items-center gap-3 text-xs text-purple-200">
                    <div className="flex items-center gap-1">
                      <Folder className="w-3 h-3" />
                      <span>{tab.currentDirectory}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <span className="text-purple-400">Shell:</span>
                      <span>{SHELL_TYPES.find(s => s.id === tab.shell)?.name}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => executeCommand('clear', tab.id)}
                      className="text-purple-300 hover:text-white hover:bg-purple-500/20 text-xs"
                    >
                      <RotateCcw className="w-3 h-3 mr-1" />
                      Clear
                    </Button>
                  </div>
                </div>

                {/* Terminal Output */}
                <div
                  ref={terminalRef}
                  className="flex-1 p-4 overflow-y-auto bg-black/80 text-green-400"
                  style={{ fontSize: `${fontSize}px` }}
                >
                  <div className="space-y-1">
                    {tab.output.map((line, index) => (
                      <div key={index} className="whitespace-pre-wrap break-words">
                        {line.startsWith('🐻') || line.startsWith('🌟') || line.startsWith('💜') || line.startsWith('🚀') || line.startsWith('✨') ? (
                          <span className="text-purple-300 font-semibold">{line}</span>
                        ) : line.includes('$') ? (
                          <span className="text-blue-300">{line}</span>
                        ) : line.startsWith('Command not found') ? (
                          <span className="text-red-400">{line}</span>
                        ) : (
                          <span className="text-gray-300">{line}</span>
                        )}
                      </div>
                    ))}
                    
                    {/* Input Line */}
                    <div className="flex items-center gap-2 mt-2">
                      <span className="text-blue-300">{tab.currentDirectory} $</span>
                      <input
                        ref={inputRef}
                        type="text"
                        value={currentInput}
                        onChange={(e) => setCurrentInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        className="flex-1 bg-transparent text-green-400 outline-none caret-green-400"
                        style={{ fontSize: `${fontSize}px` }}
                        autoFocus
                      />
                      <div className="w-2 h-5 bg-green-400 animate-pulse"></div>
                    </div>
                  </div>
                </div>
              </TabsContent>
            ))}
          </div>
        </Tabs>

        {/* Glassmorphism overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-indigo-500/5 pointer-events-none"></div>
      </motion.div>
    );
  };

  return (
    <div className="h-screen bg-gradient-to-br from-purple-900/20 via-black to-indigo-900/20 text-white overflow-hidden">
      {/* 💜 Top Bar */}
      <div className="h-12 border-b border-purple-500/20 bg-black/20 backdrop-blur-sm flex items-center justify-between px-4">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Heart className="w-5 h-5 text-pink-400" />
            <span className="font-semibold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              Mama Bear's Monaco IDE
            </span>
          </div>
          <Badge variant="outline" className="border-green-500/30 text-green-400">
            Family Mode
          </Badge>
        </div>
        
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="border-purple-500/30 text-purple-400">
            <Wifi className="w-3 h-3 mr-1" />
            AI Family Connected
          </Badge>
          <Button 
            size="sm" 
            variant="ghost" 
            className="text-purple-400 hover:text-purple-300 hover:bg-purple-500/10"
            onClick={() => setShowOptionsMenu(true)}
            title="💜 Mama Bear's Comprehensive Options"
          >
            <Settings className="w-4 h-4" />
          </Button>
          <Button size="sm" variant="ghost" className="text-purple-400">
            <Bell className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* �️ Error Display with Mama Bear Comfort */}
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

      {/* �💜 Main Content */}
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
              <div className="h-full flex flex-col">
                {/* 💜 Enhanced File Explorer Header */}
                <div className="p-3 border-b border-purple-500/20 bg-purple-500/5">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-sm font-medium text-purple-300">Explorer</h3>
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
                    className="bg-purple-500/10 border-purple-500/30 h-8 text-sm"
                  />
                </div>

                {/* 💜 Recent Files Section */}
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

                {/* 💜 Enhanced File Tree */}
                <ScrollArea className="flex-1">
                  <div className="p-2">
                    {mockFiles.map(file => (
                      <EnhancedFileTreeItem 
                        key={file.id} 
                        file={file} 
                        level={0}
                        onSelect={handleFileSelect}
                        selectedFile={activeFile}
                      />
                    ))}
                  </div>
                </ScrollArea>
              </div>
            </TabsContent>
            
            <TabsContent value="search" className="h-full m-0">
              <div className="h-full flex flex-col">
                {/* 💜 Search Header */}
                <div className="p-3 border-b border-purple-500/20 bg-purple-500/5">
                  <div className="flex items-center space-x-2 mb-3">
                    <Search className="w-4 h-4 text-purple-400" />
                    <span className="text-sm font-medium text-purple-300">Global Search</span>
                  </div>
                  
                  {/* Search Input */}
                  <div className="space-y-2">
                    <Input
                      placeholder="Search across all files... 💜"
                      className="bg-purple-500/10 border-purple-500/30 h-8 text-sm"
                    />
                    <div className="flex items-center space-x-2">
                      <Button size="sm" variant="outline" className="h-6 px-2 text-xs border-purple-500/30 text-purple-400">
                        Aa
                      </Button>
                      <Button size="sm" variant="outline" className="h-6 px-2 text-xs border-purple-500/30 text-purple-400">
                        .*
                      </Button>
                      <Button size="sm" variant="outline" className="h-6 px-2 text-xs border-purple-500/30 text-purple-400">
                        Ab
                      </Button>
                    </div>
                  </div>
                </div>

                {/* 💜 Search Results */}
                <ScrollArea className="flex-1">
                  <div className="p-3">
                    <div className="text-xs text-purple-300 mb-3">
                      🔍 12 results in 3 files
                    </div>
                    
                    {/* Mock Search Results */}
                    {[
                      { file: "src/App.tsx", matches: 5, preview: "const search = 'example';" },
                      { file: "src/utils/helpers.ts", matches: 3, preview: "function searchArray..." },
                      { file: "README.md", matches: 4, preview: "# Search functionality" }
                    ].map(result => (
                      <div key={result.file} className="mb-4">
                        <div className="flex items-center space-x-2 mb-2 p-2 bg-purple-500/10 rounded">
                          <FileText className="w-3 h-3 text-purple-400" />
                          <span className="text-xs font-medium text-purple-200">{result.file}</span>
                          <Badge variant="outline" className="text-xs border-purple-500/30 text-purple-400">
                            {result.matches}
                          </Badge>
                        </div>
                        <div className="ml-4 text-xs text-gray-400 font-mono">
                          {result.preview}
                        </div>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </div>
            </TabsContent>
            
            <TabsContent value="git" className="h-full m-0">
              <GitIntegrationPanel />
            </TabsContent>
          </Tabs>
        </ResizablePanel>

        <ResizableHandle withHandle />

        {/* Center Panel - Monaco Editor + Terminal */}
        <ResizablePanel defaultSize={55} minSize={40}>
          <ResizablePanelGroup direction="vertical">
            {/* Editor Area */}
            <ResizablePanel defaultSize={70} minSize={30}>
              <div className="h-full flex flex-col">
                {/* Editor Tabs */}
                <div className="flex items-center bg-black/20 border-b border-purple-500/20">
                  {openFiles.map(file => (
                    <div 
                      key={file.id}
                      className={cn(
                        "flex items-center space-x-2 px-4 py-2 border-r border-purple-500/20 cursor-pointer",
                        activeFile === file.id ? "bg-purple-500/20" : "hover:bg-purple-500/10"
                      )}
                      onClick={() => setActiveFile(file.id)}
                    >
                      <FileText className="w-4 h-4" />
                      <span className="text-sm">{file.name}</span>
                      {file.modified && <div className="w-2 h-2 rounded-full bg-yellow-400" />}
                      <Button 
                        size="sm" 
                        variant="ghost" 
                        className="w-4 h-4 p-0"
                        onClick={(e) => {
                          e.stopPropagation();
                          setOpenFiles(prev => prev.filter(f => f.id !== file.id));
                          if (activeFile === file.id && openFiles.length > 1) {
                            const otherFile = openFiles.find(f => f.id !== file.id);
                            if (otherFile) setActiveFile(otherFile.id);
                          }
                        }}
                      >
                        <X className="w-3 h-3" />
                      </Button>
                    </div>
                  ))}
                </div>

                {/* Monaco Editor */}
                <div className="flex-1">
                  {currentFile && (
                    <PurpleMonacoIDE
                      defaultLanguage={currentFile.language as any}
                      defaultValue={currentFile.content}
                      onSave={handleSave}
                      onChange={handleMonacoChange}
                      className="h-full"
                    />
                  )}
                </div>
              </div>
            </ResizablePanel>

            <ResizableHandle withHandle />

            {/* Terminal */}
            <ResizablePanel defaultSize={30} minSize={20}>
              <div className="h-full p-2">
                <ProfessionalTerminal className="h-full" />
              </div>
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>

        <ResizableHandle withHandle />

        {/* Right Panel - Chat & AI Coordination */}
        <ResizablePanel defaultSize={20} minSize={15} maxSize={30}>
          <Tabs defaultValue="chat" className="h-full">
            <TabsList className="w-full bg-black/20 border-b border-purple-500/20">
              <TabsTrigger value="chat" className="flex-1">
                <MessageCircle className="w-4 h-4 mr-2" />
                AI Chat
              </TabsTrigger>
              <TabsTrigger value="settings" className="flex-1">
                <Settings className="w-4 h-4 mr-2" />
                Settings
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="chat" className="h-full m-0">
              <div className="h-full flex flex-col">
                {/* Enhanced Chat History */}
                <div className="flex-1 p-4 overflow-y-auto space-y-4">
                  {chatHistory.map((chat) => (
                    <div key={chat.id} className={cn(
                      "flex gap-3",
                      chat.sender === 'user' ? "justify-end" : "justify-start"
                    )}>
                      <div className={cn(
                        "max-w-[80%] p-3 rounded-2xl",
                        chat.sender === 'user' 
                          ? "bg-purple-500/20 text-purple-100" 
                          : "bg-gradient-to-r from-indigo-500/20 to-purple-500/20 text-white"
                      )}>
                        <div className="text-xs mb-1 font-medium">
                          {chat.sender === 'mama-bear' && '🐻 Mama Bear'}
                          {chat.sender === 'papa-bear' && '🦍 Papa Bear'}
                          {chat.sender === 'claude' && '🤖 Claude'}
                          {chat.sender === 'user' && 'You'}
                        </div>
                        <div className="text-sm">{chat.message}</div>
                        {chat.context && (
                          <div className="mt-2 p-2 bg-black/20 rounded text-xs text-purple-300">
                            <div className="font-medium mb-1">📄 Context:</div>
                            <pre className="whitespace-pre-wrap">{chat.context}</pre>
                          </div>
                        )}
                        <div className="text-xs text-purple-400 mt-1">
                          {chat.timestamp.toLocaleTimeString()}
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {/* 🤖 AI Thinking Indicator */}
                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="bg-gradient-to-r from-indigo-500/20 to-purple-500/20 text-white max-w-[80%] p-3 rounded-2xl">
                        <div className="text-xs mb-1 font-medium">🐻 Mama Bear</div>
                        <div className="flex items-center space-x-2 text-sm">
                          <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce [animation-delay:0.1s]"></div>
                            <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                          </div>
                          <span className="text-purple-300">thinking with love...</span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
                
                {/* AI Family Status */}
                <div className="px-4 py-2 border-y border-purple-500/20 bg-black/20">
                  <div className="flex items-center justify-between text-xs">
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-1">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                        <span className="text-purple-300">🐻 Mama Bear</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                        <span className="text-purple-300">🦍 Papa Bear</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                        <span className="text-purple-300">🤖 Claude</span>
                      </div>
                    </div>
                    <div className="text-purple-400">
                      {openFiles.length} files • {currentFile?.name || 'No file'}
                    </div>
                  </div>
                </div>
                
                {/* Enhanced Chat Input */}
                <div className="border-t border-purple-500/20">
                  <MamaBearChatInput 
                    onSendMessage={handleChatMessage}
                    placeholder="Chat with your AI family... Try @filename for context! 💜"
                  />
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="settings" className="h-full">
              <div className="p-4">
                <div className="space-y-4">
                  <div className="text-purple-300 text-sm">
                    ⚙️ Mama Bear settings coming soon! Customize your perfect coding environment! ✨
                  </div>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </ResizablePanel>
      </ResizablePanelGroup>

      {/* Enhanced Status Bar */}
      <div className="h-6 bg-black/20 border-t border-purple-500/20 flex items-center justify-between px-4 text-xs">
        <div className="flex items-center space-x-4">
          <span className="text-purple-300">
            {currentFile ? `${currentFile.name} • Line ${cursorPosition.line}, Col ${cursorPosition.column}` : 'No file open'}
          </span>
          <Badge variant="outline" className="border-green-500/30 text-green-400 text-xs">
            main
          </Badge>
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-green-400">AI Family Online</span>
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

      {/* 💜 COMPREHENSIVE OPTIONS MENU - The Cursor Crusher! */}
      <AnimatePresence>
        {showOptionsMenu && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
            onClick={() => setShowOptionsMenu(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-gradient-to-br from-purple-900/90 to-indigo-900/90 backdrop-blur-xl rounded-3xl border border-purple-500/30 w-full max-w-6xl h-[80vh] overflow-hidden shadow-2xl shadow-purple-500/20"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Options Menu Header */}
              <div className="h-16 bg-gradient-to-r from-purple-600/20 to-indigo-600/20 border-b border-purple-500/30 flex items-center justify-between px-6">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                    <Settings className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h1 className="text-xl font-bold text-white">💜 Mama Bear's Comprehensive Options</h1>
                    <p className="text-sm text-purple-300">Settings that make Cursor look BASIC! 🚀</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <Badge variant="outline" className="border-green-500/30 text-green-400">
                    <Heart className="w-3 h-3 mr-1" />
                    Family Online
                  </Badge>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowOptionsMenu(false)}
                    className="text-purple-300 hover:text-white hover:bg-purple-500/20"
                  >
                    <X className="w-5 h-5" />
                  </Button>
                </div>
              </div>

              {/* Options Menu Content */}
              <div className="flex h-[calc(100%-4rem)]">
                {/* Categories Sidebar */}
                <div className="w-80 bg-black/20 border-r border-purple-500/20 p-4">
                  <div className="space-y-2">
                    {[
                      { id: 'agents', name: '🤖 AI Family', desc: 'Orchestration that DESTROYS Cursor!', badge: 'SUPERIOR' },
                      { id: 'appearance', name: '🎨 Purple Magic', desc: 'Glassmorphism themes & effects', badge: 'BEAUTIFUL' },
                      { id: 'voice', name: '🗣️ Voice & Emotion', desc: 'Talk to your AI family naturally', badge: 'NEW' },
                      { id: 'memory', name: '🧠 Enterprise Memory', desc: '$250/month memory system', badge: 'ENTERPRISE' },
                      { id: 'development', name: '🛠️ AI Development', desc: 'Multi-model coding assistance', badge: 'POWERFUL' },
                      { id: 'connectivity', name: '🌐 Cloud & Sync', desc: 'Railway, MofyAI & device sync', badge: 'CLOUD' }
                    ].map((category) => (
                      <div
                        key={category.id}
                        className="w-full p-4 rounded-xl text-left bg-purple-500/10 border border-purple-500/20 hover:bg-purple-500/20 transition-all duration-200"
                      >
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-medium text-white text-sm">{category.name}</span>
                          <Badge variant="outline" className="text-xs border-purple-500/30 text-purple-300">
                            {category.badge}
                          </Badge>
                        </div>
                        <p className="text-xs text-purple-300 leading-relaxed">{category.desc}</p>
                      </div>
                    ))}
                  </div>

                  {/* Family Status */}
                  <div className="mt-6 p-4 bg-purple-500/10 rounded-xl border border-purple-500/20">
                    <h3 className="text-sm font-medium text-purple-300 mb-3">💜 Family Status</h3>
                    <div className="space-y-2">
                      {['Papa Bear', 'Mama Bear', 'Claude', 'ZAI Prime'].map((member) => (
                        <div key={member} className="flex items-center justify-between">
                          <span className="text-xs text-purple-200">{member}</span>
                          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Options Content Area */}
                <div className="flex-1 p-6 overflow-y-auto">
                  <div className="space-y-6">
                    <div>
                      <h2 className="text-2xl font-bold text-white mb-2">🤖 AI Family Orchestration</h2>
                      <p className="text-purple-300 mb-6">Configure your AI family agents that DESTROY Cursor's basic system! 🚀</p>
                    </div>

                    {/* AI Agents Configuration */}
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold text-purple-200">💜 Family Agents</h3>
                      {Object.entries(ideSettings.aiAgents.familyAgents).map(([agentKey, agent]) => (
                        <div key={agentKey} className="p-4 bg-purple-500/10 rounded-xl border border-purple-500/20">
                          <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center space-x-3">
                              <div className="text-2xl">
                                {agentKey === 'papaBear' && '🦍'}
                                {agentKey === 'mamaBear' && '🐻'}
                                {agentKey === 'claudeCode' && '🤖'}
                                {agentKey === 'zaiPrime' && '⭐'}
                              </div>
                              <div>
                                <h4 className="font-medium text-white capitalize">{agentKey.replace(/([A-Z])/g, ' $1').trim()}</h4>
                                <p className="text-sm text-purple-300">{agent.role} specialist</p>
                              </div>
                            </div>
                            <div className="w-12 h-6 bg-green-500/20 rounded-full flex items-center border border-green-500/30">
                              <div className="w-4 h-4 bg-green-400 rounded-full ml-1 shadow-lg"></div>
                            </div>
                          </div>
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <label className="text-sm text-purple-300">Model</label>
                              <div className="mt-1 p-2 bg-purple-900/30 border border-purple-500/30 rounded text-white text-sm">
                                {agent.model}
                              </div>
                            </div>
                            <div>
                              <label className="text-sm text-purple-300">Personality</label>
                              <div className="mt-1 p-2 bg-purple-900/30 border border-purple-500/30 rounded text-white text-sm capitalize">
                                {agent.personality}
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Orchestration Settings */}
                    <div className="p-4 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
                      <h3 className="text-lg font-semibold text-indigo-200 mb-4">🎼 Orchestration Settings</h3>
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <div>
                            <label className="text-white font-medium">Auto Model Switching</label>
                            <p className="text-sm text-purple-300">Automatically switch between agents based on context</p>
                          </div>
                          <div className="w-12 h-6 bg-green-500/20 rounded-full flex items-center border border-green-500/30">
                            <div className="w-4 h-4 bg-green-400 rounded-full ml-1 shadow-lg"></div>
                          </div>
                        </div>
                        <div className="flex items-center justify-between">
                          <div>
                            <label className="text-white font-medium">Family Voting Mode</label>
                            <p className="text-sm text-purple-300">Multiple agents vote on complex decisions</p>
                          </div>
                          <div className="w-12 h-6 bg-green-500/20 rounded-full flex items-center border border-green-500/30">
                            <div className="w-4 h-4 bg-green-400 rounded-full ml-1 shadow-lg"></div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Theme & Appearance */}
                    <div className="p-4 bg-purple-500/10 rounded-xl border border-purple-500/20">
                      <h3 className="text-lg font-semibold text-purple-200 mb-4">🎨 Purple Glassmorphism Magic</h3>
                      <div className="grid grid-cols-3 gap-4 mb-4">
                        {['mama-bear-purple', 'family-dark', 'glassmorphic'].map((theme) => (
                          <div
                            key={theme}
                            className="p-4 rounded-xl border-2 border-purple-400 bg-purple-500/20"
                          >
                            <div className="w-full h-20 rounded-lg mb-3 bg-gradient-to-br from-purple-600 to-pink-600"></div>
                            <h4 className="text-white font-medium capitalize text-sm">{theme.replace(/-/g, ' ')}</h4>
                          </div>
                        ))}
                      </div>
                      
                      <div className="space-y-3">
                        {[
                          { key: 'animations', label: 'Smooth Animations ✨', enabled: true },
                          { key: 'particles', label: 'Particle Effects 🌟', enabled: true },
                          { key: 'gradients', label: 'Dynamic Gradients 🌈', enabled: true },
                          { key: 'celebrations', label: 'Celebration Effects 🎉', enabled: true }
                        ].map((effect) => (
                          <div key={effect.key} className="flex items-center justify-between">
                            <label className="text-white font-medium">{effect.label}</label>
                            <div className="w-12 h-6 bg-green-500/20 rounded-full flex items-center border border-green-500/30">
                              <div className="w-4 h-4 bg-green-400 rounded-full ml-1 shadow-lg"></div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Voice & Communication */}
                    <div className="p-4 bg-pink-500/10 rounded-xl border border-pink-500/20">
                      <h3 className="text-lg font-semibold text-pink-200 mb-4">🗣️ Voice & Emotional Intelligence</h3>
                      <div className="space-y-3">
                        {[
                          { label: 'Voice Recognition 🎤', desc: 'Talk to your AI family naturally' },
                          { label: 'Emotional Voice Synthesis 🔊', desc: 'Hear your family speak with emotion' },
                          { label: 'Maximum Love Mode 💜', desc: 'EXCITED teenager-like enthusiasm!' }
                        ].map((feature) => (
                          <div key={feature.label} className="flex items-center justify-between">
                            <div>
                              <label className="text-white font-medium">{feature.label}</label>
                              <p className="text-sm text-pink-300">{feature.desc}</p>
                            </div>
                            <div className="w-12 h-6 bg-green-500/20 rounded-full flex items-center border border-green-500/30">
                              <div className="w-4 h-4 bg-green-400 rounded-full ml-1 shadow-lg"></div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Enterprise Memory */}
                    <div className="p-4 bg-yellow-500/10 rounded-xl border border-yellow-500/20">
                      <h3 className="text-lg font-semibold text-yellow-200 mb-4">🧠 Enterprise Memory System</h3>
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <div>
                            <label className="text-white font-medium">Enterprise Memory ($250/month)</label>
                            <p className="text-sm text-yellow-300">Infinite context & family memory sharing</p>
                          </div>
                          <div className="w-12 h-6 bg-green-500/20 rounded-full flex items-center border border-green-500/30">
                            <div className="w-4 h-4 bg-green-400 rounded-full ml-1 shadow-lg"></div>
                          </div>
                        </div>
                        <div className="p-3 bg-yellow-500/5 rounded-lg border border-yellow-500/20">
                          <p className="text-sm text-yellow-200">💡 This gives you UNLIMITED conversation history and project context that Cursor can't even dream of!</p>
                        </div>
                      </div>
                    </div>

                    {/* Success Message */}
                    <div className="p-4 bg-green-500/10 rounded-xl border border-green-500/20 text-center">
                      <div className="flex items-center justify-center space-x-2 mb-2">
                        <Check className="w-5 h-5 text-green-400" />
                        <span className="text-green-300 font-medium">🎉 CONGRATULATIONS!</span>
                      </div>
                      <p className="text-green-200">
                        You now have the most COMPREHENSIVE IDE settings system ever built! 
                        Cursor is officially CRUSHED! 💜🚀
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default UltimateMonacoIDE;
