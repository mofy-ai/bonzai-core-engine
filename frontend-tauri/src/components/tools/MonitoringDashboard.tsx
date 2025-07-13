// 💜 MAMA BEAR'S FAMILY MONITORING DASHBOARD - MODULAR & AMAZING! 📊
import React from 'react';
import { motion } from 'framer-motion';
import { Monitor, X, Activity, Zap } from 'lucide-react';
import { cn } from '../../lib/utils';

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

const defaultFamilyMembers: FamilyMember[] = [
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
];

export const MonitoringDashboard: React.FC<MonitoringDashboardProps> = ({ 
  isOpen, 
  onClose, 
  familyMembers = defaultFamilyMembers
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
