// 💜 MAMA BEAR'S INTEGRATED TOOLS - PROFESSIONAL MODULAR ARCHITECTURE! 🎯✨
import React, { useState } from 'react';
import { DictationModal, MonitoringDashboard } from './features';
import { FloatingActionButton } from './shared';
import type { FloatingAction } from './shared';
import { cn } from '../lib/utils';

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
