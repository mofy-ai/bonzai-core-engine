import { ClaudeCliManager } from '../core/ClaudeCliManager';
import { ConfigManager } from '../core/ConfigManager';
export interface IAgent {
    id: string;
    name: string;
    phase: string;
    phaseNumber: number;
    agentNumber: number;
    status: 'pending' | 'running' | 'completed' | 'failed';
    startTime?: Date;
    endTime?: Date;
    progress: number;
    output: string[];
    error?: string;
}
export interface IPhaseExecution {
    phase: number;
    name: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    agents: IAgent[];
    startTime?: Date;
    endTime?: Date;
    reportPath?: string;
}
export interface IAgentExecution {
    id: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    currentPhase: number;
    completedPhases: number[];
    phases: IPhaseExecution[];
    wave: string;
}
export declare class AgentOrchestrator {
    private claudeCliManager;
    private configManager;
    private agents;
    private maxParallelAgents;
    private currentExecution?;
    private waveNumber;
    private logBasePath;
    private errorHandler;
    constructor(claudeCliManager: ClaudeCliManager, configManager: ConfigManager);
    private ensureLogDirectories;
    /**
     * Launch the complete 5-phase, 125-agent system
     */
    launchSystematic5PhaseExecution(): Promise<void>;
    /**
     * Initialize the 125-agent execution structure
     */
    private initializeExecution;
    /**
     * Generate agents for a specific phase
     */
    private generatePhaseAgents;
    /**
     * Generate appropriate agent name based on number and type
     */
    private generateAgentName;
    /**
     * Get phase number from agent number
     */
    private getPhaseFromAgentNumber;
    /**
     * Execute a specific phase
     */
    private executePhase;
    /**
     * Execute individual agent
     */
    private executeAgent;
    launchAgents(): Promise<void>;
    /**
     * Generate appropriate prompt for agent based on phase and number
     */
    private generateAgentPrompt;
    /**
     * Execute agent with specific prompt
     */
    private runAgentWithPrompt;
    /**
     * Phase 1 prompts: Core Implementation
     */
    private getPhase1Prompt;
    /**
     * Phase 2 prompts: Comprehensive Audit
     */
    private getPhase2Prompt;
    /**
     * Phase 3 prompts: Targeted Execution (Fixes)
     */
    private getPhase3Prompt;
    /**
     * Phase 4 prompts: Final Audit
     */
    private getPhase4Prompt;
    /**
     * Phase 5 prompts: Finalization
     */
    private getPhase5Prompt;
    /**
     * Utility method to chunk array into smaller arrays
     */
    private chunkArray;
    /**
     * Validate phase completion
     */
    private validatePhaseCompletion;
    /**
     * Generate phase report
     */
    private generatePhaseReport;
    /**
     * Get phase report directory
     */
    private getPhaseReportDirectory;
    /**
     * Create phase report content
     */
    private createPhaseReportContent;
    /**
     * Generate final production report
     */
    private generateFinalProductionReport;
    stopAllAgents(): void;
    getAgents(): IAgent[];
    getAgentStatus(): {
        running: number;
        completed: number;
        failed: number;
    };
    /**
     * Get current execution status
     */
    getCurrentExecution(): IAgentExecution | undefined;
    /**
     * Get current phase information
     */
    getCurrentPhase(): IPhaseExecution | undefined;
    /**
     * Get phase progress percentage
     */
    getPhaseProgress(phaseNumber: number): number;
    /**
     * Get overall execution progress
     */
    getOverallProgress(): number;
    /**
     * Launch specific phase (for testing/manual control)
     */
    launchPhase(phaseNumber: number): Promise<void>;
    /**
     * Get execution summary
     */
    getExecutionSummary(): {
        totalAgents: number;
        completedAgents: number;
        failedAgents: number;
        currentPhase: number;
        completedPhases: number[];
        overallProgress: number;
        status: string;
    };
}
//# sourceMappingURL=AgentOrchestrator.d.ts.map