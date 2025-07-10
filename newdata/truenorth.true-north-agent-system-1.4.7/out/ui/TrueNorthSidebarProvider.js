"use strict";
/**
 * TrueNorth Sidebar Tree View Provider
 *
 * Provides a custom sidebar panel with agent launcher, project status,
 * and quick actions for a vibe coder-friendly experience.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.TrueNorthWebviewProvider = exports.TrueNorthSidebarProvider = void 0;
const vscode = __importStar(require("vscode"));
const modes_1 = require("../modes");
class TrueNorthSidebarProvider {
    constructor(context) {
        this.context = context;
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
        this.projectStatus = {
            health: 'good', // good, warning, error
            agents: {
                running: 0,
                completed: 0,
                failed: 0,
            },
            lastAnalysis: null,
        };
    }
    setModeManager(modeManager) {
        this.modeManager = modeManager;
        this.refresh();
    }
    updateModeStatus() {
        this.refresh();
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        const item = new vscode.TreeItem(element.label, element.collapsibleState ?? vscode.TreeItemCollapsibleState.None);
        if (element.icon) {
            item.iconPath = new vscode.ThemeIcon(element.icon);
        }
        if (element.description) {
            item.description = element.description;
        }
        if (element.command) {
            item.command = {
                command: element.command,
                title: element.label,
                arguments: [element],
            };
        }
        if (element.contextValue) {
            item.contextValue = element.contextValue;
        }
        if (element.tooltip) {
            item.tooltip = element.tooltip;
        }
        return item;
    }
    getChildren(element) {
        if (!element) {
            return Promise.resolve(this.getRootItems());
        }
        if (element.children) {
            return Promise.resolve(element.children);
        }
        return Promise.resolve([]);
    }
    getRootItems() {
        const items = [];
        // Add Development Mode section
        if (this.modeManager) {
            items.push({
                id: 'development-mode',
                label: 'Development Mode',
                icon: 'target',
                collapsibleState: vscode.TreeItemCollapsibleState.Expanded,
                children: this.getModeChildren(),
            });
        }
        items.push({
            id: 'project-status',
            label: 'Project Status',
            icon: this.getHealthIcon(),
            description: this.getHealthDescription(),
            collapsibleState: vscode.TreeItemCollapsibleState.Expanded,
            children: this.getProjectStatusChildren(),
        }, {
            id: 'quick-actions',
            label: 'Quick Actions',
            icon: 'zap',
            collapsibleState: vscode.TreeItemCollapsibleState.Expanded,
            children: this.getQuickActionChildren(),
        }, {
            id: 'analysis-agents',
            label: '🔍 Analysis',
            icon: 'search',
            collapsibleState: vscode.TreeItemCollapsibleState.Expanded,
            children: this.getAnalysisAgentChildren(),
        }, {
            id: 'improvement-agents',
            label: '✨ Improvement',
            icon: 'tools',
            collapsibleState: vscode.TreeItemCollapsibleState.Expanded,
            children: this.getImprovementAgentChildren(),
        }, {
            id: 'deployment-agents',
            label: '🚀 Deployment',
            icon: 'rocket',
            collapsibleState: vscode.TreeItemCollapsibleState.Expanded,
            children: this.getDeploymentAgentChildren(),
        }, {
            id: 'recent-activity',
            label: 'Recent Activity',
            icon: 'history',
            collapsibleState: vscode.TreeItemCollapsibleState.Collapsed,
            children: this.getRecentActivityChildren(),
        });
        return items;
    }
    getHealthIcon() {
        switch (this.projectStatus.health) {
            case 'good':
                return 'pass';
            case 'warning':
                return 'warning';
            case 'error':
                return 'error';
            default:
                return 'question';
        }
    }
    getHealthDescription() {
        const { running, completed, failed } = this.projectStatus.agents;
        const total = running + completed + failed;
        if (total === 0) {
            return 'Ready';
        }
        if (running > 0) {
            return `${running} running`;
        }
        if (failed > 0) {
            return `${failed} failed`;
        }
        return `${completed} completed`;
    }
    getProjectStatusChildren() {
        const { running, completed, failed } = this.projectStatus.agents;
        const items = [];
        if (running > 0) {
            items.push({
                id: 'running-agents',
                label: `${running} Running`,
                icon: 'loading~spin',
                description: 'agents',
                command: 'truenorth.showRunningAgents',
                contextValue: 'running-agents',
            });
        }
        if (completed > 0) {
            items.push({
                id: 'completed-agents',
                label: `${completed} Completed`,
                icon: 'check',
                description: 'agents',
                command: 'truenorth.showCompletedAgents',
                contextValue: 'completed-agents',
            });
        }
        if (failed > 0) {
            items.push({
                id: 'failed-agents',
                label: `${failed} Failed`,
                icon: 'x',
                description: 'agents',
                command: 'truenorth.showFailedAgents',
                contextValue: 'failed-agents',
            });
        }
        if (items.length === 0) {
            items.push({
                id: 'no-agents',
                label: 'No active agents',
                icon: 'info',
                description: 'Click Quick Actions to start',
                contextValue: 'no-agents',
            });
        }
        return items;
    }
    getQuickActionChildren() {
        return [
            {
                id: 'quick-analyze',
                label: 'Quick Analysis',
                icon: 'search',
                description: 'Analyze & generate agents',
                command: 'truenorth.analyzeProject',
                contextValue: 'quick-action',
                tooltip: 'Analyze your project and generate intelligent agents',
            },
            {
                id: 'open-dashboard',
                label: 'Open Dashboard',
                icon: 'dashboard',
                description: 'Launch control center',
                command: 'truenorth.openDashboard',
                contextValue: 'quick-action',
                tooltip: 'Open the TrueNorth dashboard in your browser',
            },
            {
                id: 'clean-code',
                label: 'Clean Codebase',
                icon: 'sparkle',
                description: 'Remove unused code',
                command: 'truenorth.cleanCodebase',
                contextValue: 'quick-action',
                tooltip: 'Clean up unused code and optimize imports',
            },
        ];
    }
    getAnalysisAgentChildren() {
        return [
            {
                id: 'analyze-project',
                label: 'Analyze Project',
                icon: 'search',
                description: 'Generate comprehensive agents',
                command: 'truenorth.analyzeProject',
                contextValue: 'agent-launcher',
                tooltip: 'Analyze project structure and generate optimization agents',
            },
            {
                id: 'security-scan',
                label: 'Security Scan',
                icon: 'shield',
                description: 'Find vulnerabilities',
                command: 'truenorth.analyzeSecurity',
                contextValue: 'agent-launcher',
                tooltip: 'Scan for security vulnerabilities and compliance issues',
            },
            {
                id: 'sustainability-analysis',
                label: 'Sustainability Analysis',
                icon: 'globe',
                description: 'Optimize resource usage',
                command: 'truenorth.analyzeSustainability',
                contextValue: 'agent-launcher',
                tooltip: 'Analyze and optimize resource consumption',
            },
        ];
    }
    getImprovementAgentChildren() {
        return [
            {
                id: 'clean-codebase',
                label: 'Clean Codebase',
                icon: 'sparkle',
                description: 'Remove unused code',
                command: 'truenorth.cleanCodebase',
                contextValue: 'agent-launcher',
                tooltip: 'Remove unused code and optimize imports',
            },
            {
                id: 'optimize-performance',
                label: 'Optimize Performance',
                icon: 'zap',
                description: 'Improve speed',
                command: 'truenorth.optimizePerformance',
                contextValue: 'agent-launcher',
                tooltip: 'Identify and fix performance bottlenecks',
            },
            {
                id: 'fix-issues',
                label: 'Auto-Fix Issues',
                icon: 'tools',
                description: 'Resolve problems',
                command: 'truenorth.autoFixIssues',
                contextValue: 'agent-launcher',
                tooltip: 'Automatically detect and fix common issues',
            },
        ];
    }
    getDeploymentAgentChildren() {
        return [
            {
                id: 'deploy-agents',
                label: 'Deploy All Agents',
                icon: 'rocket',
                description: 'Run generated agents',
                command: 'truenorth.startDeployment',
                contextValue: 'agent-launcher',
                tooltip: 'Deploy and run all generated agents',
            },
            {
                id: 'retry-failed',
                label: 'Retry Failed',
                icon: 'refresh',
                description: 'Re-run failed agents',
                command: 'truenorth.retryFailed',
                contextValue: 'agent-launcher',
                tooltip: 'Retry agents that failed during execution',
            },
            {
                id: 'stop-all',
                label: 'Stop All Agents',
                icon: 'stop-circle',
                description: 'Cancel execution',
                command: 'truenorth.stopDeployment',
                contextValue: 'agent-launcher',
                tooltip: 'Stop all running agents immediately',
            },
        ];
    }
    getRecentActivityChildren() {
        // This would be populated with actual recent activity data
        return [
            {
                id: 'no-activity',
                label: 'No recent activity',
                icon: 'info',
                description: 'Start using TrueNorth',
                contextValue: 'no-activity',
            },
        ];
    }
    // Public methods to update status
    updateProjectStatus(status) {
        this.projectStatus = { ...this.projectStatus, ...status };
        this.refresh();
    }
    updateAgentCounts(running, completed, failed) {
        this.projectStatus.agents = { running, completed, failed };
        this.refresh();
    }
    setProjectHealth(health) {
        this.projectStatus.health = health;
        this.refresh();
    }
    getModeChildren() {
        if (!this.modeManager) {
            return [];
        }
        const currentMode = this.modeManager.getCurrentMode();
        const modeInfo = modes_1.ModeInfo[currentMode];
        const execution = this.modeManager.getCurrentExecution();
        const children = [
            {
                id: 'current-mode',
                label: `${modeInfo.icon} ${modeInfo.name}`,
                description: execution ? `${execution.progress}%` : 'Ready',
                icon: execution?.status === 'running' ? 'loading~spin' : 'target',
                tooltip: modeInfo.description,
                command: execution ? undefined : 'truenorth.startModeExecution',
            },
            {
                id: 'mode-actions',
                label: 'Mode Actions',
                icon: 'list-selection',
                collapsibleState: vscode.TreeItemCollapsibleState.Expanded,
                children: this.getModeActionChildren(),
            },
        ];
        return children;
    }
    getModeActionChildren() {
        if (!this.modeManager) {
            return [];
        }
        const actions = [
            {
                id: 'detect-mode',
                label: 'Detect Recommended Mode',
                icon: 'search',
                command: 'truenorth.detectMode',
                tooltip: 'Analyze project and recommend appropriate mode',
            },
            {
                id: 'switch-mode',
                label: 'Switch Mode',
                icon: 'arrow-swap',
                command: 'truenorth.showModeSelector',
                tooltip: 'Manually switch to different development mode',
            },
            {
                id: 'mode-help',
                label: 'Mode Guide',
                icon: 'question',
                command: 'truenorth.showModeGuide',
                tooltip: 'Learn about development modes',
            },
        ];
        const execution = this.modeManager.getCurrentExecution();
        if (execution && execution.status === 'running') {
            actions.unshift({
                id: 'stop-execution',
                label: 'Stop Execution',
                icon: 'stop-circle',
                command: 'truenorth.stopModeExecution',
                tooltip: 'Stop current mode execution',
            });
        }
        else {
            actions.unshift({
                id: 'start-execution',
                label: 'Start Mode Execution',
                icon: 'play',
                command: 'truenorth.startModeExecution',
                tooltip: 'Start executing current mode agents',
            });
        }
        return actions;
    }
}
exports.TrueNorthSidebarProvider = TrueNorthSidebarProvider;
/**
 * Enhanced webview provider for the TrueNorth sidebar with comprehensive dashboard UI
 */
class TrueNorthWebviewProvider {
    constructor(_context) {
        this._context = _context;
        this._statusData = {
            running: 0,
            completed: 0,
            failed: 0,
            health: 'good',
            lastActivity: 'No recent activity',
            currentPhase: 'Ready',
            totalAgents: 125,
            progress: 0,
        };
    }
    setModeManager(modeManager) {
        this.modeManager = modeManager;
    }
    resolveWebviewView(webviewView) {
        this._view = webviewView;
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._context.extensionUri],
        };
        webviewView.webview.html = this._getHtmlForWebview();
        // Handle messages from the webview
        webviewView.webview.onDidReceiveMessage(message => {
            switch (message.type) {
                case 'launchAgent':
                    void vscode.commands.executeCommand(message.command);
                    break;
                case 'openDashboard':
                    // Focus the webview instead of opening browser
                    if (this._view) {
                        this._view.show();
                    }
                    break;
                case 'showStatus':
                    void vscode.window.showInformationMessage(`TrueNorth Status: ${message.status}`);
                    break;
                case 'showOutput':
                    void vscode.commands.executeCommand('truenorth.showOutput');
                    break;
                case 'testClaude':
                    void vscode.commands.executeCommand('truenorth.testClaude');
                    break;
            }
        }, undefined, this._context.subscriptions);
    }
    _getHtmlForWebview() {
        const projectName = vscode.workspace.workspaceFolders?.[0]?.name ?? 'Unknown Project';
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrueNorth Dashboard - ${projectName}</title>
    <meta name="description" content="TrueNorth AI agent launcher and project status dashboard for VS Code">
    <style>
        /* Premium Design System - Tesla/Apple Inspired */
        :root {
            /* Spacing System - 8px base unit */
            --space-xs: 4px;
            --space-sm: 8px;
            --space-md: 16px;
            --space-lg: 24px;
            --space-xl: 32px;
            
            /* Premium Color System */
            --color-bg-primary: var(--vscode-editor-background);
            --color-bg-secondary: var(--vscode-sideBar-background);
            --color-bg-card: var(--vscode-editor-inactiveSelectionBackground);
            --color-border: var(--vscode-panel-border);
            --color-text: var(--vscode-editor-foreground);
            --color-text-secondary: var(--vscode-descriptionForeground);
            
            /* Tesla/Apple Inspired Accents */
            --color-accent-primary: #00d4ff;
            --color-accent-secondary: #ff6b35;
            --color-success: #00ff88;
            --color-warning: #ffb800;
            --color-error: #ff3333;
            
            /* Shadows & Effects */
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.15);
            
            /* Transitions */
            --transition-fast: 150ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
            --transition-base: 300ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
            --transition-slow: 500ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }
        
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        
        body {
            font-family: var(--vscode-font-family), -apple-system, BlinkMacSystemFont, 'SF Pro Display', Inter, system-ui, sans-serif;
            font-size: var(--vscode-font-size);
            background: var(--color-bg-primary);
            color: var(--color-text);
            padding: 0;
            margin: 0;
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        .container {
            padding: var(--space-md);
            min-height: 100vh;
        }
        
        /* Premium Header */
        .header {
            text-align: center;
            padding: var(--space-lg) 0 var(--space-md) 0;
            margin-bottom: var(--space-md);
            border-bottom: 1px solid var(--color-border);
        }
        
        .header h1 {
            font-size: 18px;
            font-weight: 600;
            background: linear-gradient(135deg, var(--color-accent-primary) 0%, var(--color-accent-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: var(--space-xs);
            letter-spacing: -0.01em;
        }
        
        .project-badge {
            display: inline-block;
            background: rgba(0, 212, 255, 0.1);
            border: 1px solid rgba(0, 212, 255, 0.3);
            color: var(--color-accent-primary);
            padding: var(--space-xs) var(--space-sm);
            border-radius: 6px;
            font-size: 11px;
            font-weight: 500;
        }
        
        /* Status Cards */
        .status-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: var(--space-sm);
            margin-bottom: var(--space-lg);
        }
        
        .status-card {
            background: var(--color-bg-card);
            border: 1px solid var(--color-border);
            border-radius: 8px;
            padding: var(--space-md);
            text-align: center;
            transition: all var(--transition-base);
            position: relative;
            overflow: hidden;
        }
        
        .status-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
            border-color: var(--color-accent-primary);
        }
        
        .status-card.success {
            border-left: 3px solid var(--color-success);
        }
        
        .status-card.warning {
            border-left: 3px solid var(--color-warning);
        }
        
        .status-card.error {
            border-left: 3px solid var(--color-error);
        }
        
        .status-number {
            font-size: 24px;
            font-weight: 700;
            line-height: 1;
            margin-bottom: var(--space-xs);
        }
        
        .status-label {
            font-size: 11px;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .section {
            margin-bottom: var(--space-lg);
        }
        
        .section-title {
            font-size: 13px;
            font-weight: 600;
            margin-bottom: var(--space-md);
            color: var(--color-text);
            display: flex;
            align-items: center;
            gap: var(--space-xs);
            padding-bottom: var(--space-xs);
            border-bottom: 1px solid var(--color-border);
        }
        
        .action-grid {
            display: grid;
            gap: var(--space-sm);
        }
        
        .action-button {
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            padding: var(--space-md);
            background: var(--color-bg-card);
            color: var(--color-text);
            border: 1px solid var(--color-border);
            border-radius: 8px;
            cursor: pointer;
            transition: all var(--transition-base);
            text-align: left;
            width: 100%;
            font-size: 12px;
            min-height: 44px;
            position: relative;
            overflow: hidden;
        }
        
        .action-button:hover {
            background: var(--vscode-button-hoverBackground);
            transform: translateY(-1px) scale(1.02);
            box-shadow: var(--shadow-md);
            border-color: var(--color-accent-primary);
        }
        
        .action-button:active {
            transform: translateY(0) scale(0.98);
            transition: all var(--transition-fast);
        }
        
        .action-button:focus {
            outline: 2px solid var(--vscode-focusBorder);
            outline-offset: 2px;
        }
        
        .action-button.primary {
            background: linear-gradient(135deg, var(--color-accent-primary), #0099cc);
            color: white;
            border-color: var(--color-accent-primary);
            font-weight: 600;
        }
        
        .action-button.primary:hover {
            background: linear-gradient(135deg, #00b8e6, var(--color-accent-primary));
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
        }
        
        .action-button.secondary {
            background: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
            border-color: var(--color-border);
        }
        
        .action-button.secondary:hover {
            background: var(--vscode-button-secondaryHoverBackground);
        }
        
        .action-button.danger {
            border-color: var(--color-error);
            color: var(--color-error);
        }
        
        .action-button.danger:hover {
            background: rgba(255, 51, 51, 0.1);
            border-color: var(--color-error);
        }
        
        .action-icon {
            font-size: 16px;
            min-width: 20px;
            text-align: center;
            opacity: 0.8;
        }
        
        .action-info {
            flex: 1;
        }
        
        .action-name {
            font-weight: 600;
            margin-bottom: 2px;
            line-height: 1.2;
        }
        
        .action-description {
            font-size: 10px;
            opacity: 0.7;
            line-height: 1.3;
        }
        
        /* Progress Indicators */
        .progress-bar {
            width: 100%;
            height: 4px;
            background: var(--color-border);
            border-radius: 2px;
            overflow: hidden;
            margin-top: var(--space-xs);
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--color-accent-primary), var(--color-success));
            border-radius: 2px;
            transition: width var(--transition-base);
            width: 0%;
        }
        
        /* Pulse Animation for Active Status */
        .pulse {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.5;
            }
        }
        
        /* Activity Indicator */
        .activity-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: var(--space-xs);
        }
        
        .activity-indicator.active {
            background: var(--color-success);
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        .activity-indicator.warning {
            background: var(--color-warning);
        }
        
        .activity-indicator.error {
            background: var(--color-error);
        }
        
        .activity-indicator.idle {
            background: var(--color-text-secondary);
            opacity: 0.5;
        }
        
    
    </style>
</head>
<body>
    <div class="container">
        <!-- Premium Header -->
        <header class="header">
            <h1>🧭 TrueNorth</h1>
            <div class="project-badge">${projectName}</div>
        </header>
        
        <!-- Status Grid -->
        <div class="status-grid">
            <div class="status-card success">
                <div class="status-number" id="running-count">0</div>
                <div class="status-label">Running</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="running-progress"></div>
                </div>
            </div>
            <div class="status-card">
                <div class="status-number" id="completed-count">0</div>
                <div class="status-label">Completed</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="completed-progress"></div>
                </div>
            </div>
            <div class="status-card error">
                <div class="status-number" id="failed-count">0</div>
                <div class="status-label">Failed</div>
            </div>
            <div class="status-card">
                <div class="status-number" id="progress-percent">0%</div>
                <div class="status-label">Progress</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="overall-progress"></div>
                </div>
            </div>
        </div>
        
        <!-- Current Status -->
        <div class="section">
            <h3 class="section-title">
                <span class="activity-indicator idle" id="status-indicator"></span>
                Status
            </h3>
            <div style="padding: var(--space-sm); background: var(--color-bg-card); border-radius: 6px; border: 1px solid var(--color-border);">
                <div id="current-status" style="font-size: 12px; opacity: 0.8;">Ready to launch agents</div>
                <div id="current-phase" style="font-size: 11px; opacity: 0.6; margin-top: 4px;">Phase: Standby</div>
            </div>
        </div>
        
        <!-- Quick Actions -->
        <div class="section">
            <h3 class="section-title">⚡ Quick Actions</h3>
            <div class="action-grid">
                <button class="action-button primary" onclick="launchAgent('truenorth.analyzeProject')">
                    <span class="action-icon">🎯</span>
                    <div class="action-info">
                        <div class="action-name">Analyze Project</div>
                        <div class="action-description">Generate intelligent agents</div>
                    </div>
                </button>
                <button class="action-button secondary" onclick="testClaude()">
                    <span class="action-icon">🤖</span>
                    <div class="action-info">
                        <div class="action-name">Test Claude CLI</div>
                        <div class="action-description">Verify connection</div>
                    </div>
                </button>
                <button class="action-button secondary" onclick="showOutput()">
                    <span class="action-icon">📄</span>
                    <div class="action-info">
                        <div class="action-name">Show Output</div>
                        <div class="action-description">View logs & results</div>
                    </div>
                </button>
            </div>
        </div>
        
        <!-- TypeScript Error Resolution -->
        <div class="section">
            <h3 class="section-title">🔧 TypeScript</h3>
            <div class="action-grid">
                <button class="action-button primary" onclick="launchAgent('truenorth.launchTypeScriptFixer')">
                    <span class="action-icon">🔥</span>
                    <div class="action-info">
                        <div class="action-name">Fix TypeScript Errors</div>
                        <div class="action-description">125-agent error resolution</div>
                    </div>
                </button>
                <button class="action-button secondary" onclick="launchAgent('truenorth.checkTypeScriptErrors')">
                    <span class="action-icon">🔍</span>
                    <div class="action-info">
                        <div class="action-name">Check Errors</div>
                        <div class="action-description">Run type check</div>
                    </div>
                </button>
                <button class="action-button secondary" onclick="launchAgent('truenorth.showTypeScriptStatus')">
                    <span class="action-icon">📊</span>
                    <div class="action-info">
                        <div class="action-name">Status Report</div>
                        <div class="action-description">View progress</div>
                    </div>
                </button>
            </div>
        </div>
        
        <!-- 5-Phase System -->
        <div class="section">
            <h3 class="section-title">🎯 5-Phase System</h3>
            <div class="action-grid">
                <button class="action-button primary" onclick="launchAgent('truenorth.launch5PhaseSystem')">
                    <span class="action-icon">🚀</span>
                    <div class="action-info">
                        <div class="action-name">Launch 5-Phase System</div>
                        <div class="action-description">Complete systematic execution</div>
                    </div>
                </button>
                <button class="action-button secondary" onclick="launchAgent('truenorth.show5PhaseStatus')">
                    <span class="action-icon">📊</span>
                    <div class="action-info">
                        <div class="action-name">Phase Status</div>
                        <div class="action-description">View current progress</div>
                    </div>
                </button>
            </div>
        </div>
        
        <!-- Control Actions -->
        <div class="section">
            <h3 class="section-title">🎮 Control</h3>
            <div class="action-grid">
                <button class="action-button secondary" onclick="launchAgent('truenorth.launchAgents')">
                    <span class="action-icon">🚀</span>
                    <div class="action-info">
                        <div class="action-name">Launch Agents</div>
                        <div class="action-description">Start agent execution</div>
                    </div>
                </button>
                <button class="action-button danger" onclick="launchAgent('truenorth.stopAllAgents')">
                    <span class="action-icon">🛑</span>
                    <div class="action-info">
                        <div class="action-name">Stop All</div>
                        <div class="action-description">Cancel execution</div>
                    </div>
                </button>
            </div>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        // Global state
        let currentData = {
            running: 0,
            completed: 0,
            failed: 0,
            progress: 0,
            status: 'Ready',
            phase: 'Standby'
        };
        
        // Enhanced Dashboard Controller
        class TrueNorthDashboard {
            constructor() {
                this.init();
            }
            
            init() {
                this.setupEventListeners();
                this.updateDisplay();
                // Dashboard initialized
            }
            
            setupEventListeners() {
                // Button click handlers with enhanced feedback
                document.querySelectorAll('.action-button').forEach(button => {
                    button.addEventListener('click', (e) => {
                        this.handleButtonClick(e);
                    });
                    
                    // Enhanced hover effects
                    button.addEventListener('mouseenter', (e) => {
                        this.animateButton(e.target, 'hover');
                    });
                    
                    button.addEventListener('mouseleave', (e) => {
                        this.animateButton(e.target, 'leave');
                    });
                });
                
                // Keyboard navigation
                document.addEventListener('keydown', (e) => {
                    this.handleKeyboard(e);
                });
            }
            
            handleButtonClick(event) {
                const button = event.currentTarget;
                const actionName = button.querySelector('.action-name')?.textContent || 'Action';
                
                // Visual feedback
                this.animateButton(button, 'click');
                
                // Update status
                this.updateStatus(\`Launching \${actionName}...\`, 'active');
                
                // Action triggered
            }
            
            animateButton(button, type) {
                switch (type) {
                    case 'click':
                        button.style.transform = 'translateY(1px) scale(0.98)';
                        setTimeout(() => {
                            button.style.transform = '';
                        }, 150);
                        break;
                    case 'hover':
                        if (!button.classList.contains('primary')) {
                            button.style.borderColor = 'var(--color-accent-primary)';
                        }
                        break;
                    case 'leave':
                        if (!button.classList.contains('primary')) {
                            button.style.borderColor = '';
                        }
                        break;
                }
            }
            
            handleKeyboard(event) {
                // Quick shortcuts - Alt+Number for section navigation
                if (event.altKey) {
                    switch (event.key) {
                        case '1':
                            event.preventDefault();
                            this.focusSection('quick-actions');
                            this.announceShortcut('Quick Actions section focused');
                            break;
                        case '2':
                            event.preventDefault();
                            this.focusSection('typescript');
                            this.announceShortcut('TypeScript section focused');
                            break;
                        case '3':
                            event.preventDefault();
                            this.focusSection('5-phase');
                            this.announceShortcut('5-Phase System section focused');
                            break;
                        case '4':
                            event.preventDefault();
                            this.focusSection('control');
                            this.announceShortcut('Control section focused');
                            break;
                    }
                }
                
                // Enter and Space for button activation
                if (event.target.classList.contains('action-button')) {
                    if (event.key === 'Enter' || event.key === ' ') {
                        event.preventDefault();
                        event.target.click();
                    }
                }
            }
            
            announceShortcut(message) {
                // Visual feedback for keyboard navigation
                const notification = document.createElement('div');
                notification.textContent = message;
                notification.style.cssText = \`
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: var(--color-accent-primary);
                    color: white;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: 600;
                    z-index: 1000;
                    opacity: 0;
                    transform: translateY(-10px);
                    transition: all 0.3s ease;
                \`;
                
                document.body.appendChild(notification);
                
                // Animate in
                setTimeout(() => {
                    notification.style.opacity = '1';
                    notification.style.transform = 'translateY(0)';
                }, 10);
                
                // Animate out and remove
                setTimeout(() => {
                    notification.style.opacity = '0';
                    notification.style.transform = 'translateY(-10px)';
                    setTimeout(() => {
                        if (notification.parentNode) {
                            notification.parentNode.removeChild(notification);
                        }
                    }, 300);
                }, 2000);
            }
            
            focusSection(section) {
                const element = document.querySelector(\`[data-section="\${section}"]\`) ?? 
                              document.querySelector('.section');
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    const firstButton = element.querySelector('.action-button');
                    if (firstButton) {
                        firstButton.focus();
                    }
                }
            }
            
            updateDisplay() {
                this.updateCounts(currentData.running, currentData.completed, currentData.failed);
                this.updateProgress(currentData.progress);
                this.updateStatus(currentData.status, this.getStatusType());
                this.updatePhase(currentData.phase);
            }
            
            updateCounts(running, completed, failed) {
                const total = running + completed + failed;
                
                // Update numbers with animation
                this.animateNumber('running-count', running);
                this.animateNumber('completed-count', completed);
                this.animateNumber('failed-count', failed);
                
                // Update progress bars
                if (total > 0) {
                    const runningPercent = (running / total) * 100;
                    const completedPercent = (completed / total) * 100;
                    
                    this.updateProgressBar('running-progress', runningPercent);
                    this.updateProgressBar('completed-progress', completedPercent);
                }
                
                // Update overall progress
                const overallPercent = total > 0 ? (completed / total) * 100 : 0;
                this.updateProgressBar('overall-progress', overallPercent);
                document.getElementById('progress-percent').textContent = \`\${Math.round(overallPercent)}%\`;
                
                // Update status cards classes
                this.updateStatusCardClasses(running, completed, failed);
                
                // Store current data
                currentData.running = running;
                currentData.completed = completed;
                currentData.failed = failed;
                currentData.progress = overallPercent;
            }
            
            animateNumber(elementId, newValue) {
                const element = document.getElementById(elementId);
                if (!element) return;
                
                const currentValue = parseInt(element.textContent) || 0;
                if (currentValue === newValue) return;
                
                // Simple number animation
                element.style.transform = 'scale(1.1)';
                element.style.color = 'var(--color-accent-primary)';
                
                setTimeout(() => {
                    element.textContent = newValue;
                    element.style.transform = '';
                    element.style.color = '';
                }, 150);
            }
            
            updateProgressBar(elementId, percent) {
                const element = document.getElementById(elementId);
                if (element) {
                    element.style.width = \`\${Math.min(100, Math.max(0, percent))}%\`;
                }
            }
            
            updateStatusCardClasses(running, completed, failed) {
                const runningCard = document.querySelector('.status-card.success');
                const failedCard = document.querySelector('.status-card.error');
                
                if (runningCard) {
                    runningCard.classList.toggle('pulse', running > 0);
                }
                
                if (failedCard) {
                    failedCard.style.display = failed > 0 ? 'block' : 'block'; // Always show
                }
            }
            
            updateStatus(status, type = 'idle') {
                const statusElement = document.getElementById('current-status');
                const indicatorElement = document.getElementById('status-indicator');
                
                if (statusElement) {
                    statusElement.textContent = status;
                }
                
                if (indicatorElement) {
                    indicatorElement.className = \`activity-indicator \${type}\`;
                }
                
                currentData.status = status;
            }
            
            updatePhase(phase) {
                const phaseElement = document.getElementById('current-phase');
                if (phaseElement) {
                    phaseElement.textContent = \`Phase: \${phase}\`;
                }
                currentData.phase = phase;
            }
            
            getStatusType() {
                if (currentData.running > 0) return 'active';
                if (currentData.failed > 0) return 'error';
                if (currentData.completed > 0) return 'warning';
                return 'idle';
            }
        }
        
        // Command handlers
        function launchAgent(command) {
            vscode.postMessage({
                type: 'launchAgent',
                command: command
            });
        }
        
        function testClaude() {
            vscode.postMessage({
                type: 'testClaude'
            });
        }
        
        function showOutput() {
            vscode.postMessage({
                type: 'showOutput'
            });
        }
        
        // Message handling from extension
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.type) {
                case 'updateCounts':
                    dashboard?.updateCounts(message.running, message.completed, message.failed);
                    break;
                case 'updateStatus':
                    dashboard?.updateStatus(message.status, message.statusType);
                    break;
                case 'updatePhase':
                    dashboard?.updatePhase(message.phase);
                    break;
                case 'updateProgress':
                    dashboard?.updateProgress(message.progress);
                    break;
            }
        });
        
        // Initialize dashboard
        let dashboard;
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                dashboard = new TrueNorthDashboard();
            });
        } else {
            dashboard = new TrueNorthDashboard();
        }
    </script>
</body>
</html>`;
    }
    // Public methods to update the webview data
    updateCounts(running, completed, failed) {
        this._statusData.running = running;
        this._statusData.completed = completed;
        this._statusData.failed = failed;
        if (this._view) {
            void this._view.webview.postMessage({
                type: 'updateCounts',
                running,
                completed,
                failed,
            });
        }
    }
    updateStatus(status, type) {
        this._statusData.lastActivity = status;
        if (this._view) {
            void this._view.webview.postMessage({
                type: 'updateStatus',
                status,
                statusType: type ?? 'info',
            });
        }
    }
    updatePhase(phase) {
        this._statusData.currentPhase = phase;
        if (this._view) {
            void this._view.webview.postMessage({
                type: 'updatePhase',
                phase,
            });
        }
    }
    updateProgress(progress) {
        this._statusData.progress = progress;
        if (this._view) {
            void this._view.webview.postMessage({
                type: 'updateProgress',
                progress,
            });
        }
    }
    setProjectHealth(health) {
        this._statusData.health = health;
        // You could add visual updates based on health status
    }
    show() {
        if (this._view) {
            this._view.show();
        }
    }
}
exports.TrueNorthWebviewProvider = TrueNorthWebviewProvider;
TrueNorthWebviewProvider.viewType = 'truenorth-sidebar';
//# sourceMappingURL=TrueNorthSidebarProvider.js.map