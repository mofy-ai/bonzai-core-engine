// 💜 MAMA BEAR'S FLOATING ACTION BUTTON - PROFESSIONAL & EXCITED! 🎉
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, X, Settings, Monitor, Mic, FileText, Terminal, Search, GitBranch, Command } from 'lucide-react';
import { cn } from '../../../lib/utils';

export interface FloatingAction {
  id: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  onClick: () => void;
  color?: string;
  disabled?: boolean;
}

export interface FloatingActionButtonProps {
  actions?: FloatingAction[];
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const defaultActions: FloatingAction[] = [
  {
    id: 'dictation',
    label: '🎤 Voice Input',
    icon: Mic,
    onClick: () => console.log('Dictation opened'),
    color: 'purple'
  },
  {
    id: 'monitoring',
    label: '📊 Family Monitor',
    icon: Monitor,
    onClick: () => console.log('Monitoring opened'),
    color: 'blue'
  },
  {
    id: 'terminal',
    label: '🔧 Terminal',
    icon: Terminal,
    onClick: () => console.log('Terminal opened'),
    color: 'green'
  },
  {
    id: 'search',
    label: '🔍 Global Search',
    icon: Search,
    onClick: () => console.log('Search opened'),
    color: 'yellow'
  },
  {
    id: 'git',
    label: '🌿 Git Status',
    icon: GitBranch,
    onClick: () => console.log('Git opened'),
    color: 'orange'
  },
  {
    id: 'settings',
    label: '⚙️ Settings',
    icon: Settings,
    onClick: () => console.log('Settings opened'),
    color: 'gray'
  }
];

const positionClasses = {
  'bottom-right': 'bottom-6 right-6',
  'bottom-left': 'bottom-6 left-6',
  'top-right': 'top-6 right-6',
  'top-left': 'top-6 left-6'
};

const sizeClasses = {
  sm: 'w-12 h-12',
  md: 'w-14 h-14',
  lg: 'w-16 h-16'
};

const actionSizeClasses = {
  sm: 'w-10 h-10',
  md: 'w-12 h-12',
  lg: 'w-14 h-14'
};

export const FloatingActionButton: React.FC<FloatingActionButtonProps> = ({
  actions = defaultActions,
  position = 'bottom-right',
  size = 'md',
  className
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getColorClasses = (color: string = 'purple') => {
    const colors = {
      purple: 'bg-purple-600 hover:bg-purple-700 text-white',
      blue: 'bg-blue-600 hover:bg-blue-700 text-white',
      green: 'bg-green-600 hover:bg-green-700 text-white',
      yellow: 'bg-yellow-600 hover:bg-yellow-700 text-white',
      orange: 'bg-orange-600 hover:bg-orange-700 text-white',
      gray: 'bg-gray-600 hover:bg-gray-700 text-white'
    };
    return colors[color as keyof typeof colors] || colors.purple;
  };

  const handleMainButtonClick = () => {
    setIsExpanded(!isExpanded);
  };

  const handleActionClick = (action: FloatingAction) => {
    action.onClick();
    setIsExpanded(false);
  };

  return (
    <div className={cn("fixed z-50", positionClasses[position], className)}>
      <div className="relative">
        {/* 💜 ACTION BUTTONS */}
        <AnimatePresence>
          {isExpanded && (
            <div className="absolute bottom-16 right-0 space-y-3">
              {actions.map((action, index) => (
                <motion.button
                  key={action.id}
                  className={cn(
                    "flex items-center justify-center rounded-full shadow-lg backdrop-blur-sm transition-all duration-200 group",
                    actionSizeClasses[size],
                    getColorClasses(action.color),
                    action.disabled && "opacity-50 cursor-not-allowed"
                  )}
                  onClick={() => !action.disabled && handleActionClick(action)}
                  disabled={action.disabled}
                  initial={{ 
                    scale: 0, 
                    opacity: 0,
                    x: 20
                  }}
                  animate={{ 
                    scale: 1, 
                    opacity: 1,
                    x: 0
                  }}
                  exit={{ 
                    scale: 0, 
                    opacity: 0,
                    x: 20
                  }}
                  transition={{ 
                    delay: index * 0.05,
                    type: "spring",
                    stiffness: 400,
                    damping: 25
                  }}
                  whileHover={{ 
                    scale: 1.1,
                    rotate: 5
                  }}
                  whileTap={{ scale: 0.95 }}
                >
                  <action.icon className={cn(
                    size === 'sm' ? 'w-4 h-4' :
                    size === 'md' ? 'w-5 h-5' :
                    'w-6 h-6'
                  )} />
                  
                  {/* 💜 TOOLTIP */}
                  <div className="absolute right-full mr-3 opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none">
                    <div className="bg-gray-900 text-white text-sm px-2 py-1 rounded whitespace-nowrap">
                      {action.label}
                    </div>
                  </div>
                </motion.button>
              ))}
            </div>
          )}
        </AnimatePresence>

        {/* 💜 MAIN FLOATING BUTTON */}
        <motion.button
          className={cn(
            "flex items-center justify-center rounded-full shadow-lg transition-all duration-300",
            sizeClasses[size],
            isExpanded 
              ? "bg-red-600 hover:bg-red-700 rotate-45" 
              : "bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700",
            "text-white border-2 border-white/20"
          )}
          onClick={handleMainButtonClick}
          whileHover={{ 
            scale: 1.05,
            boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
          }}
          whileTap={{ scale: 0.95 }}
        >
          <AnimatePresence mode="wait">
            {isExpanded ? (
              <motion.div
                key="close"
                initial={{ rotate: -90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: 90, opacity: 0 }}
                transition={{ duration: 0.2 }}
              >
                <X className={cn(
                  size === 'sm' ? 'w-5 h-5' :
                  size === 'md' ? 'w-6 h-6' :
                  'w-7 h-7'
                )} />
              </motion.div>
            ) : (
              <motion.div
                key="plus"
                initial={{ rotate: 90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: -90, opacity: 0 }}
                transition={{ duration: 0.2 }}
              >
                <Plus className={cn(
                  size === 'sm' ? 'w-5 h-5' :
                  size === 'md' ? 'w-6 h-6' :
                  'w-7 h-7'
                )} />
              </motion.div>
            )}
          </AnimatePresence>
        </motion.button>

        {/* 💜 PULSING RING WHEN EXPANDED */}
        {isExpanded && (
          <motion.div
            className="absolute inset-0 rounded-full border-2 border-purple-400 pointer-events-none"
            initial={{ scale: 1, opacity: 0.5 }}
            animate={{ 
              scale: [1, 1.2, 1],
              opacity: [0.5, 0, 0.5]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
        )}
      </div>
    </div>
  );
};
