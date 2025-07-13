// 💜 MAMA BEAR'S COLLAPSIBLE SIDEBAR - BEAUTIFUL & FUNCTIONAL! 🗂️
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ChevronLeft, 
  ChevronRight, 
  Files, 
  Search, 
  GitBranch, 
  Settings,
  MessageSquare,
  Terminal,
  Monitor,
  Mic
} from 'lucide-react';
import { cn } from '../../lib/utils';

interface SidebarItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  active?: boolean;
  badge?: string | number;
  onClick?: () => void;
}

interface CollapsibleSidebarProps {
  isCollapsed: boolean;
  onToggle: () => void;
  activePanel: string;
  onPanelChange: (panelId: string) => void;
  onOpenDictation?: () => void;
  onOpenMonitoring?: () => void;
}

export const CollapsibleSidebar: React.FC<CollapsibleSidebarProps> = ({
  isCollapsed,
  onToggle,
  activePanel,
  onPanelChange,
  onOpenDictation,
  onOpenMonitoring
}) => {
  const sidebarItems: SidebarItem[] = [
    {
      id: 'files',
      label: 'File Explorer',
      icon: <Files className="w-5 h-5" />,
      active: activePanel === 'files',
      onClick: () => onPanelChange('files')
    },
    {
      id: 'search',
      label: 'Search',
      icon: <Search className="w-5 h-5" />,
      active: activePanel === 'search',
      onClick: () => onPanelChange('search')
    },
    {
      id: 'git',
      label: 'Source Control',
      icon: <GitBranch className="w-5 h-5" />,
      active: activePanel === 'git',
      badge: '3',
      onClick: () => onPanelChange('git')
    },
    {
      id: 'chat',
      label: 'Family Chat',
      icon: <MessageSquare className="w-5 h-5" />,
      active: activePanel === 'chat',
      badge: '2',
      onClick: () => onPanelChange('chat')
    },
    {
      id: 'terminal',
      label: 'Terminal',
      icon: <Terminal className="w-5 h-5" />,
      active: activePanel === 'terminal',
      onClick: () => onPanelChange('terminal')
    },
    {
      id: 'monitoring',
      label: 'Family Monitor',
      icon: <Monitor className="w-5 h-5" />,
      onClick: onOpenMonitoring
    },
    {
      id: 'dictation',
      label: 'Voice Dictation',
      icon: <Mic className="w-5 h-5" />,
      onClick: onOpenDictation
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: <Settings className="w-5 h-5" />,
      active: activePanel === 'settings',
      onClick: () => onPanelChange('settings')
    }
  ];

  return (
    <motion.div 
      className={cn(
        "h-full bg-purple-900/30 backdrop-blur-sm border-r border-purple-500/20 relative",
        "flex flex-col transition-all duration-300 ease-in-out",
        isCollapsed ? "w-12" : "w-64"
      )}
      animate={{ width: isCollapsed ? 48 : 256 }}
      transition={{ duration: 0.3, ease: "easeInOut" }}
    >
      {/* Toggle Button */}
      <motion.button
        onClick={onToggle}
        className="absolute -right-3 top-4 z-10 w-6 h-6 bg-purple-600 hover:bg-purple-500 text-white rounded-full flex items-center justify-center transition-colors duration-200 shadow-lg"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        {isCollapsed ? (
          <ChevronRight className="w-3 h-3" />
        ) : (
          <ChevronLeft className="w-3 h-3" />
        )}
      </motion.button>

      {/* Header */}
      <div className="p-4 border-b border-purple-500/20">
        <AnimatePresence mode="wait">
          {!isCollapsed ? (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.2 }}
            >
              <h2 className="text-sm font-semibold text-purple-300 truncate">
                💜 Mama Bear IDE
              </h2>
              <p className="text-xs text-purple-400 truncate">
                Family Home
              </p>
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex justify-center"
            >
              <span className="text-lg">🐻</span>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Navigation Items */}
      <div className="flex-1 py-2 overflow-y-auto">
        {sidebarItems.map((item) => (
          <motion.button
            key={item.id}
            onClick={item.onClick}
            className={cn(
              "w-full flex items-center gap-3 px-3 py-2.5 text-left transition-all duration-200",
              "hover:bg-purple-500/20 relative group",
              item.active ? "bg-purple-500/30 text-purple-200 border-r-2 border-purple-400" : "text-purple-300"
            )}
            whileHover={{ x: 2 }}
            title={isCollapsed ? item.label : undefined}
          >
            <div className="flex-shrink-0 relative">
              {item.icon}
              {item.badge && (
                <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                  {item.badge}
                </span>
              )}
            </div>
            
            <AnimatePresence>
              {!isCollapsed && (
                <motion.span
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  transition={{ duration: 0.2 }}
                  className="text-sm font-medium truncate"
                >
                  {item.label}
                </motion.span>
              )}
            </AnimatePresence>

            {/* Tooltip for collapsed state */}
            {isCollapsed && (
              <div className="absolute left-full ml-2 px-2 py-1 bg-purple-800 text-purple-100 text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50">
                {item.label}
                <div className="absolute left-0 top-1/2 -translate-x-1 -translate-y-1/2 w-2 h-2 bg-purple-800 rotate-45" />
              </div>
            )}
          </motion.button>
        ))}
      </div>

      {/* Footer */}
      <div className="border-t border-purple-500/20 p-2">
        <AnimatePresence>
          {!isCollapsed && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              transition={{ duration: 0.2 }}
              className="text-xs text-purple-400 text-center"
            >
              <p>Built with 💜</p>
              <p>by Mama Bear</p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};
