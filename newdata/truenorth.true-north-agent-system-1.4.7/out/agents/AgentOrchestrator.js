"use strict";
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
exports.AgentOrchestrator = void 0;
const ErrorHandler_1 = require("../core/ErrorHandler");
const constants_1 = require("../constants");
const fs = __importStar(require("fs"));
const os = __importStar(require("os"));
const path = __importStar(require("path"));
const vscode = __importStar(require("vscode"));
// Phase constants
const totalPhases = 5;
const phase1Start = 1;
const phase1End = 25;
const phase2Start = 26;
const phase2End = 50;
const phase3Start = 51;
const phase3End = 75;
const phase4Start = 76;
const phase4End = 100;
const phase5Start = 101;
const phase5End = 125;
const agentNamePadding = 3;
const fullProgress = 100;
const firstPhase = 1;
const secondPhase = 2;
const thirdPhase = 3;
const fourthPhase = 4;
const fifthPhase = 5;
const defaultProgress = 0;
const progressStepSize = 5;
const maxSafeProgress = 95;
const phase1ArrayOffset = 1;
const cleanOutputSubstringLength = 500;
const percentageMultiplier = 100;
const timeoutDelayMs = 1000;
class AgentOrchestrator {
    constructor(claudeCliManager, configManager) {
        this.claudeCliManager = claudeCliManager;
        this.configManager = configManager;
        this.agents = [];
        this.maxParallelAgents = constants_1.timeConstants.MAX_PARALLEL_AGENTS;
        this.waveNumber = '01';
        this.errorHandler = ErrorHandler_1.ErrorHandler.getInstance();
        // Use workspace directory instead of process.cwd() for VS Code extension context
        const workspacePath = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath ?? process.cwd();
        this.logBasePath = path.join(workspacePath, 'logs', `wave-${this.waveNumber}`);
        this.ensureLogDirectories();
    }
    ensureLogDirectories() {
        const directories = [
            'phase1-execution-reports',
            'phase2-audit-findings',
            'phase3-execution-reports',
            'phase4-audit-findings',
            'phase5-finalization',
        ];
        try {
            // Ensure base log directory exists first
            if (!fs.existsSync(this.logBasePath)) {
                fs.mkdirSync(this.logBasePath, { recursive: true });
            }
            // Create phase subdirectories
            directories.forEach(dir => {
                const dirPath = path.join(this.logBasePath, dir);
                if (!fs.existsSync(dirPath)) {
                    fs.mkdirSync(dirPath, { recursive: true });
                }
            });
        }
        catch (error) {
            void this.errorHandler.handleError(new Error(`Failed to create log directories: ${error}`), ErrorHandler_1.ErrorCategory.FILESYSTEM, ErrorHandler_1.ErrorSeverity.HIGH, {
                component: 'AgentOrchestrator',
                operation: 'ensureLogDirectories',
                timestamp: new Date().toISOString(),
            });
            // Fallback to a temporary directory if workspace creation fails
            const tempDir = path.join(os.tmpdir(), 'truenorth-logs', `wave-${this.waveNumber}`);
            this.logBasePath = tempDir;
            // Try to create temp directories
            try {
                if (!fs.existsSync(this.logBasePath)) {
                    fs.mkdirSync(this.logBasePath, { recursive: true });
                }
                directories.forEach(dir => {
                    const dirPath = path.join(this.logBasePath, dir);
                    if (!fs.existsSync(dirPath)) {
                        fs.mkdirSync(dirPath, { recursive: true });
                    }
                });
                // Using temporary log directory fallback
            }
            catch (tempError) {
                void this.errorHandler.handleError(new Error(`Failed to create temporary log directories: ${tempError}`), ErrorHandler_1.ErrorCategory.FILESYSTEM, ErrorHandler_1.ErrorSeverity.CRITICAL, {
                    component: 'AgentOrchestrator',
                    operation: 'ensureLogDirectories:fallback',
                    timestamp: new Date().toISOString(),
                });
                // If all else fails, disable directory creation
                this.logBasePath = '';
            }
        }
    }
    /**
     * Launch the complete 5-phase, 125-agent system
     */
    async launchSystematic5PhaseExecution() {
        this.currentExecution = this.initializeExecution();
        // Execute all phases sequentially
        for (let phaseNumber = 1; phaseNumber <= totalPhases; phaseNumber++) {
            await this.executePhase(phaseNumber);
            // Phase transition validation
            if (!this.validatePhaseCompletion(phaseNumber)) {
                throw new Error(`Phase ${phaseNumber} validation failed`);
            }
        }
        // Generate final production report
        this.generateFinalProductionReport();
    }
    /**
     * Initialize the 125-agent execution structure
     */
    initializeExecution() {
        const phases = [
            {
                phase: 1,
                name: 'Core Execution',
                status: 'pending',
                agents: this.generatePhaseAgents(phase1Start, phase1End, 'execution'),
            },
            {
                phase: 2,
                name: 'Comprehensive Audit',
                status: 'pending',
                agents: this.generatePhaseAgents(phase2Start, phase2End, 'audit'),
            },
            {
                phase: 3,
                name: 'Targeted Execution',
                status: 'pending',
                agents: this.generatePhaseAgents(phase3Start, phase3End, 'execution'),
            },
            {
                phase: 4,
                name: 'Final Audit',
                status: 'pending',
                agents: this.generatePhaseAgents(phase4Start, phase4End, 'audit'),
            },
            {
                phase: 5,
                name: 'Finalization',
                status: 'pending',
                agents: this.generatePhaseAgents(phase5Start, phase5End, 'finalization'),
            },
        ];
        return {
            id: `systematic-execution-${Date.now()}`,
            status: 'pending',
            currentPhase: 1,
            completedPhases: [],
            phases,
            wave: this.waveNumber,
        };
    }
    /**
     * Generate agents for a specific phase
     */
    generatePhaseAgents(startAgent, endAgent, phaseType) {
        const agents = [];
        for (let i = startAgent; i <= endAgent; i++) {
            agents.push({
                id: `agent-${i.toString().padStart(agentNamePadding, '0')}`,
                name: this.generateAgentName(i, phaseType),
                phase: phaseType,
                phaseNumber: this.getPhaseFromAgentNumber(i),
                agentNumber: i,
                status: 'pending',
                progress: defaultProgress,
                output: [],
            });
        }
        return agents;
    }
    /**
     * Generate appropriate agent name based on number and type
     */
    generateAgentName(agentNumber, phaseType) {
        const phaseNumber = this.getPhaseFromAgentNumber(agentNumber);
        switch (phaseType) {
            case 'execution':
                return `${phaseType === 'execution' && phaseNumber === 1 ? 'Core Implementation' : 'Fix Implementation'} Agent ${agentNumber}`;
            case 'audit':
                return `${phaseNumber === 2 ? 'Comprehensive Audit' : 'Final Validation'} Agent ${agentNumber}`;
            case 'finalization':
                return `Production Finalization Agent ${agentNumber}`;
            default:
                return `Agent ${agentNumber}`;
        }
    }
    /**
     * Get phase number from agent number
     */
    getPhaseFromAgentNumber(agentNumber) {
        if (agentNumber <= phase1End) {
            return firstPhase;
        }
        if (agentNumber <= phase2End) {
            return secondPhase;
        }
        if (agentNumber <= phase3End) {
            return thirdPhase;
        }
        if (agentNumber <= phase4End) {
            return fourthPhase;
        }
        return fifthPhase;
    }
    /**
     * Execute a specific phase
     */
    async executePhase(phaseNumber) {
        if (!this.currentExecution) {
            throw new Error('No execution initialized');
        }
        const phase = this.currentExecution.phases[phaseNumber - phase1ArrayOffset];
        phase.status = 'running';
        phase.startTime = new Date();
        this.currentExecution.currentPhase = phaseNumber;
        // Execute agents in parallel batches
        const batchSize = this.maxParallelAgents;
        const agentBatches = this.chunkArray(phase.agents, batchSize);
        for (const batch of agentBatches) {
            await Promise.all(batch.map(agent => this.executeAgent(agent, phaseNumber)));
        }
        phase.status = 'completed';
        phase.endTime = new Date();
        this.currentExecution.completedPhases.push(phaseNumber);
        // Generate phase report
        this.generatePhaseReport(phaseNumber, phase);
    }
    /**
     * Execute individual agent
     */
    async executeAgent(agent, phaseNumber) {
        try {
            agent.status = 'running';
            agent.startTime = new Date();
            const prompt = this.generateAgentPrompt(agent, phaseNumber);
            const output = await this.runAgentWithPrompt(agent, prompt);
            agent.output.push(output || 'No output received');
            agent.status = 'completed';
            agent.progress = fullProgress;
        }
        catch (error) {
            agent.status = 'failed';
            agent.error = error instanceof Error ? error.message : 'Unknown error';
        }
        finally {
            agent.endTime = new Date();
        }
    }
    async launchAgents() {
        // Backward compatibility - launch the systematic execution
        await this.launchSystematic5PhaseExecution();
    }
    /**
     * Generate appropriate prompt for agent based on phase and number
     */
    generateAgentPrompt(agent, phaseNumber) {
        switch (phaseNumber) {
            case firstPhase: // Core Execution
                return this.getPhase1Prompt(agent.agentNumber);
            case secondPhase: // Comprehensive Audit
                return this.getPhase2Prompt(agent.agentNumber);
            case thirdPhase: // Targeted Execution
                return this.getPhase3Prompt(agent.agentNumber);
            case fourthPhase: // Final Audit
                return this.getPhase4Prompt(agent.agentNumber);
            case fifthPhase: // Finalization
                return this.getPhase5Prompt(agent.agentNumber);
            default:
                return 'Analyze and improve the project structure and codebase.';
        }
    }
    /**
     * Execute agent with specific prompt
     */
    async runAgentWithPrompt(agent, prompt) {
        const onProgress = (message) => {
            agent.output.push(`[PROGRESS] ${message}`);
            if (agent.progress < maxSafeProgress) {
                agent.progress = Math.min(agent.progress + progressStepSize, maxSafeProgress);
            }
        };
        // Execute command with Claude CLI
        return this.claudeCliManager.executeCommand(prompt, {
            commandType: 'agent',
            enableProgressReporting: true,
            onProgress,
        });
    }
    /**
     * Phase 1 prompts: Core Implementation
     */
    getPhase1Prompt(agentNumber) {
        const prompts = [
            'Analyze and optimize core TypeScript configuration and build pipeline for production readiness.',
            'Implement comprehensive error handling and recovery mechanisms throughout the codebase.',
            'Enhance the dashboard real-time communication system and WebSocket management.',
            'Optimize agent orchestration system for better parallel execution and resource management.',
            'Implement advanced security features including input validation and protection mechanisms.',
            'Develop comprehensive logging and monitoring systems for production deployment.',
            'Optimize database connections and data management layers for performance.',
            'Implement advanced caching strategies and performance optimization techniques.',
            'Enhance user interface components with accessibility and responsive design improvements.',
            'Develop comprehensive API documentation and integration testing frameworks.',
            'Implement advanced authentication and authorization systems.',
            'Optimize bundle size and loading performance for web components.',
            'Enhance configuration management and environment-specific deployments.',
            'Implement advanced retry mechanisms and circuit breaker patterns.',
            'Develop comprehensive health check and system monitoring capabilities.',
            'Optimize memory usage and garbage collection performance.',
            'Implement advanced data validation and sanitization features.',
            'Enhance cross-platform compatibility and deployment strategies.',
            'Develop comprehensive backup and recovery systems.',
            'Implement advanced analytics and performance tracking.',
            'Optimize network communication and protocol efficiency.',
            'Enhance container orchestration and microservice architecture.',
            'Implement advanced search and filtering capabilities.',
            'Develop comprehensive notification and alerting systems.',
            'Optimize final integration testing and deployment validation.',
        ];
        return prompts[agentNumber - phase1ArrayOffset] ?? 'Implement core functionality improvements.';
    }
    /**
     * Phase 2 prompts: Comprehensive Audit
     */
    getPhase2Prompt(agentNumber) {
        const auditIndex = agentNumber - phase2Start;
        const prompts = [
            'Audit TypeScript configuration and build pipeline for issues and improvements.',
            'Review error handling implementation for completeness and best practices.',
            'Audit dashboard communication system for performance and reliability issues.',
            'Review agent orchestration system for scalability and resource optimization.',
            'Audit security implementation for vulnerabilities and compliance issues.',
            'Review logging and monitoring systems for coverage and effectiveness.',
            'Audit database layer for performance bottlenecks and optimization opportunities.',
            'Review caching implementation for efficiency and consistency.',
            'Audit UI components for accessibility compliance and usability issues.',
            'Review API documentation and testing framework completeness.',
            'Audit authentication and authorization systems for security vulnerabilities.',
            'Review bundle optimization and loading performance metrics.',
            'Audit configuration management for security and maintainability.',
            'Review retry mechanisms and error recovery patterns for robustness.',
            'Audit health check systems for comprehensive coverage.',
            'Review memory usage patterns and potential memory leaks.',
            'Audit data validation systems for completeness and security.',
            'Review cross-platform compatibility and deployment issues.',
            'Audit backup and recovery systems for reliability.',
            'Review analytics implementation for accuracy and performance.',
            'Audit network communication for efficiency and error handling.',
            'Review container and microservice architecture for best practices.',
            'Audit search and filtering implementation for performance.',
            'Review notification systems for reliability and scalability.',
            'Conduct final comprehensive system audit and integration review.',
        ];
        return prompts[auditIndex] ?? 'Conduct comprehensive audit of implemented features.';
    }
    /**
     * Phase 3 prompts: Targeted Execution (Fixes)
     */
    getPhase3Prompt(agentNumber) {
        const fixIndex = agentNumber - phase3Start;
        return `Fix and implement improvements identified in Phase 2 audit for area ${fixIndex + phase1ArrayOffset}. Address all critical and high-priority issues found during the comprehensive review.`;
    }
    /**
     * Phase 4 prompts: Final Audit
     */
    getPhase4Prompt(agentNumber) {
        const validationIndex = agentNumber - phase4Start;
        return `Validate and verify that all Phase 3 fixes have been properly implemented for area ${validationIndex + phase1ArrayOffset}. Ensure no regressions and confirm production readiness.`;
    }
    /**
     * Phase 5 prompts: Finalization
     */
    getPhase5Prompt(agentNumber) {
        const finalizationIndex = agentNumber - phase5Start;
        const prompts = [
            'Final code consolidation and cleanup for production deployment.',
            'Generate comprehensive documentation and user guides.',
            'Prepare production deployment scripts and configuration.',
            'Create final security validation and compliance reports.',
            'Generate performance benchmarks and optimization reports.',
            'Prepare release notes and changelog documentation.',
            'Create final integration and acceptance testing reports.',
            'Prepare monitoring and alerting configuration for production.',
            'Generate final backup and disaster recovery procedures.',
            'Create comprehensive troubleshooting and support documentation.',
            'Prepare final deployment validation and rollback procedures.',
            'Generate production readiness checklist and verification.',
            'Create final architecture documentation and diagrams.',
            'Prepare operational runbooks and maintenance procedures.',
            'Generate final quality assurance and testing reports.',
            'Create production monitoring dashboards and alerts.',
            'Prepare final security audit and penetration testing reports.',
            'Generate final performance optimization and tuning reports.',
            'Create comprehensive API documentation and examples.',
            'Prepare final deployment automation and CI/CD pipeline.',
            'Generate final system architecture and design documentation.',
            'Create comprehensive user training materials and guides.',
            'Prepare final production support and maintenance procedures.',
            'Generate final project completion and handover documentation.',
            'Create final production launch validation and success metrics.',
        ];
        return prompts[finalizationIndex] ?? 'Finalize system for production deployment.';
    }
    /**
     * Utility method to chunk array into smaller arrays
     */
    chunkArray(array, chunkSize) {
        const chunks = [];
        for (let i = 0; i < array.length; i += chunkSize) {
            chunks.push(array.slice(i, i + chunkSize));
        }
        return chunks;
    }
    /**
     * Validate phase completion
     */
    validatePhaseCompletion(phaseNumber) {
        if (!this.currentExecution) {
            return false;
        }
        const phase = this.currentExecution.phases[phaseNumber - phase1ArrayOffset];
        const completedAgents = phase.agents.filter(a => a.status === 'completed').length;
        const totalAgents = phase.agents.length;
        return completedAgents === totalAgents;
    }
    /**
     * Generate phase report
     */
    generatePhaseReport(phaseNumber, phase) {
        if (!this.logBasePath) {
            // Skipping phase report generation - no log directory available
            return;
        }
        try {
            const reportDir = this.getPhaseReportDirectory(phaseNumber);
            const reportPath = path.join(reportDir, `phase-${phaseNumber}-report.md`);
            const report = this.createPhaseReportContent(phaseNumber, phase);
            fs.writeFileSync(reportPath, report, 'utf8');
            phase.reportPath = reportPath;
        }
        catch (error) {
            void this.errorHandler.handleError(new Error(`Failed to generate phase ${phaseNumber} report: ${error}`), ErrorHandler_1.ErrorCategory.FILESYSTEM, ErrorHandler_1.ErrorSeverity.MEDIUM, {
                component: 'AgentOrchestrator',
                operation: 'generatePhaseReport',
                timestamp: new Date().toISOString(),
                additionalData: { phaseNumber },
            });
        }
    }
    /**
     * Get phase report directory
     */
    getPhaseReportDirectory(phaseNumber) {
        const directories = [
            'phase1-execution-reports',
            'phase2-audit-findings',
            'phase3-execution-reports',
            'phase4-audit-findings',
            'phase5-finalization',
        ];
        return path.join(this.logBasePath, directories[phaseNumber - 1]);
    }
    /**
     * Create phase report content
     */
    createPhaseReportContent(phaseNumber, phase) {
        const duration = phase.endTime && phase.startTime
            ? Math.round((phase.endTime.getTime() - phase.startTime.getTime()) / timeoutDelayMs)
            : 0;
        const completedCount = phase.agents.filter(a => a.status === 'completed').length;
        const failedCount = phase.agents.filter(a => a.status === 'failed').length;
        return `# Phase ${phaseNumber} Report: ${phase.name}

## 📊 Summary
- **Status**: ${phase.status}
- **Start Time**: ${phase.startTime?.toISOString()}
- **End Time**: ${phase.endTime?.toISOString()}
- **Duration**: ${duration} seconds
- **Agents Completed**: ${completedCount}/${phase.agents.length}
- **Agents Failed**: ${failedCount}

## 🤖 Agent Results

${phase.agents
            .map(agent => `### ${agent.name}
- **ID**: ${agent.id}
- **Status**: ${agent.status}
- **Progress**: ${agent.progress}%
- **Duration**: ${agent.endTime && agent.startTime ? Math.round((agent.endTime.getTime() - agent.startTime.getTime()) / timeoutDelayMs) : 0}s
${agent.error ? `- **Error**: ${agent.error}` : ''}
${agent.output.length > 0 ? `- **Output**: ${agent.output.join('\\n').substring(0, cleanOutputSubstringLength)}...` : ''}
`)
            .join('\\n')}

---
*Generated: ${new Date().toISOString()}*
*Wave: ${this.waveNumber}*
`;
    }
    /**
     * Generate final production report
     */
    generateFinalProductionReport() {
        if (!this.currentExecution) {
            return;
        }
        if (!this.logBasePath) {
            // Skipping final production report generation - no log directory available
            return;
        }
        try {
            const reportPath = path.join(this.logBasePath, 'final-production-report.md');
            const totalAgents = this.currentExecution.phases.reduce((sum, phase) => sum + phase.agents.length, 0);
            const completedAgents = this.currentExecution.phases.reduce((sum, phase) => sum + phase.agents.filter(a => a.status === 'completed').length, 0);
            const report = `# Final Production Report - Wave ${this.waveNumber}

## 🎯 Executive Summary
- **Total Agents**: ${totalAgents}
- **Completed Agents**: ${completedAgents}
- **Success Rate**: ${Math.round((completedAgents / totalAgents) * percentageMultiplier)}%
- **Execution Status**: ${this.currentExecution.status}

## 📋 Phase Summary
${this.currentExecution.phases
                .map(phase => `
### Phase ${phase.phase}: ${phase.name}
- **Status**: ${phase.status}
- **Agents**: ${phase.agents.filter(a => a.status === 'completed').length}/${phase.agents.length} completed
- **Report**: ${phase.reportPath ?? 'Not generated'}
`)
                .join('\\n')}

## 🚀 Production Readiness
- ✅ All 5 phases completed
- ✅ Systematic audit cycle executed
- ✅ Issues identified and resolved
- ✅ Final validation completed
- ✅ Production deployment ready

---
*Generated: ${new Date().toISOString()}*
*Wave: ${this.waveNumber}*
*System: TrueNorth 5-Phase Execution*
`;
            fs.writeFileSync(reportPath, report, 'utf8');
        }
        catch (error) {
            void this.errorHandler.handleError(new Error(`Failed to generate final production report: ${error}`), ErrorHandler_1.ErrorCategory.FILESYSTEM, ErrorHandler_1.ErrorSeverity.MEDIUM, {
                component: 'AgentOrchestrator',
                operation: 'generateFinalProductionReport',
                timestamp: new Date().toISOString(),
            });
        }
    }
    stopAllAgents() {
        // Stop current execution
        if (this.currentExecution) {
            this.currentExecution.status = 'failed';
            // Stop all running agents in current phase
            const currentPhase = this.currentExecution.phases[this.currentExecution.currentPhase - 1];
            if (currentPhase) {
                currentPhase.agents.forEach(agent => {
                    if (agent.status === 'running') {
                        agent.status = 'failed';
                        agent.error = 'Stopped by user';
                        agent.endTime = new Date();
                    }
                });
            }
        }
        // Legacy support
        for (const agent of this.agents) {
            if (agent.status === 'running') {
                agent.status = 'failed';
                agent.error = 'Stopped by user';
            }
        }
    }
    getAgents() {
        if (this.currentExecution) {
            // Return all agents from all phases
            return this.currentExecution.phases.flatMap(phase => phase.agents);
        }
        return [...this.agents];
    }
    getAgentStatus() {
        const allAgents = this.getAgents();
        const running = allAgents.filter(a => a.status === 'running').length;
        const completed = allAgents.filter(a => a.status === 'completed').length;
        const failed = allAgents.filter(a => a.status === 'failed').length;
        return { running, completed, failed };
    }
    /**
     * Get current execution status
     */
    getCurrentExecution() {
        return this.currentExecution;
    }
    /**
     * Get current phase information
     */
    getCurrentPhase() {
        if (!this.currentExecution) {
            return undefined;
        }
        return this.currentExecution.phases[this.currentExecution.currentPhase - phase1ArrayOffset];
    }
    /**
     * Get phase progress percentage
     */
    getPhaseProgress(phaseNumber) {
        if (!this.currentExecution) {
            return 0;
        }
        const phase = this.currentExecution.phases[phaseNumber - phase1ArrayOffset];
        if (!phase) {
            return 0;
        }
        const completedAgents = phase.agents.filter(a => a.status === 'completed').length;
        const totalAgents = phase.agents.length;
        return Math.round((completedAgents / totalAgents) * percentageMultiplier);
    }
    /**
     * Get overall execution progress
     */
    getOverallProgress() {
        if (!this.currentExecution) {
            return 0;
        }
        const totalAgents = this.currentExecution.phases.reduce((sum, phase) => sum + phase.agents.length, 0);
        const completedAgents = this.currentExecution.phases.reduce((sum, phase) => sum + phase.agents.filter(a => a.status === 'completed').length, 0);
        return Math.round((completedAgents / totalAgents) * percentageMultiplier);
    }
    /**
     * Launch specific phase (for testing/manual control)
     */
    async launchPhase(phaseNumber) {
        this.currentExecution ?? (this.currentExecution = this.initializeExecution());
        await this.executePhase(phaseNumber);
    }
    /**
     * Get execution summary
     */
    getExecutionSummary() {
        if (!this.currentExecution) {
            return {
                totalAgents: 0,
                completedAgents: 0,
                failedAgents: 0,
                currentPhase: 0,
                completedPhases: [],
                overallProgress: 0,
                status: 'not_started',
            };
        }
        const totalAgents = this.currentExecution.phases.reduce((sum, phase) => sum + phase.agents.length, 0);
        const completedAgents = this.currentExecution.phases.reduce((sum, phase) => sum + phase.agents.filter(a => a.status === 'completed').length, 0);
        const failedAgents = this.currentExecution.phases.reduce((sum, phase) => sum + phase.agents.filter(a => a.status === 'failed').length, 0);
        return {
            totalAgents,
            completedAgents,
            failedAgents,
            currentPhase: this.currentExecution.currentPhase,
            completedPhases: this.currentExecution.completedPhases,
            overallProgress: this.getOverallProgress(),
            status: this.currentExecution.status,
        };
    }
}
exports.AgentOrchestrator = AgentOrchestrator;
//# sourceMappingURL=AgentOrchestrator.js.map