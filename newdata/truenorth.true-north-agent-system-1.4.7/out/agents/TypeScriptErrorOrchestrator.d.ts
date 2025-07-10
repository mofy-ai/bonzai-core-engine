/**
 * TypeScript Error Resolution Agent System
 * Specialized 125-Agent System for TypeScript Error Resolution
 * 5-Phase Loop: Execute→Audit→Execute→Audit→Finalize until ALL errors resolved
 */
import { ClaudeCliManager } from '../core/ClaudeCliManager';
import { ConfigManager } from '../core/ConfigManager';
export interface ITypeScriptError {
    file: string;
    line: number;
    column: number;
    code: string;
    message: string;
    severity: 'error' | 'warning' | 'suggestion';
    category: string;
}
export interface ITypeScriptAgent {
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
    errorsAssigned?: ITypeScriptError[];
    errorsFixed?: ITypeScriptError[];
}
export interface ITypeScriptPhaseExecution {
    phase: number;
    name: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    agents: ITypeScriptAgent[];
    startTime?: Date;
    endTime?: Date;
    reportPath?: string;
    errorCount: number;
    errorsFixed: number;
}
export interface ITypeScriptExecution {
    id: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    currentPhase: number;
    completedPhases: number[];
    phases: ITypeScriptPhaseExecution[];
    wave: string;
    iteration: number;
    totalErrors: number;
    errorsRemaining: number;
    startTime?: Date;
    endTime?: Date;
}
export declare class TypeScriptErrorOrchestrator {
    private claudeCliManager;
    private configManager;
    private maxParallelAgents;
    private currentExecution?;
    private waveNumber;
    private logBasePath;
    private errorHandler;
    private workspacePath;
    constructor(claudeCliManager: ClaudeCliManager, configManager: ConfigManager);
    private ensureLogDirectories;
    /**
     * Launch the TypeScript Error Resolution System
     * Continues looping until ALL TypeScript errors are resolved
     */
    launchTypeScriptErrorResolution(progressCallback?: (message: string) => void): Promise<void>;
    /**
     * Get phase description for progress reporting
     */
    private getPhaseDescription;
    /**
     * Analyze errors that persist across multiple iterations
     */
    private analyzeStubornErrors;
    /**
     * Run TypeScript check and parse errors
     */
    private runTypeScriptCheck;
    /**
     * Parse TypeScript compiler errors from stderr output
     */
    private parseTypeScriptErrors;
    /**
     * Categorize TypeScript errors by type
     */
    private categorizeError;
    /**
     * Initialize execution structure for TypeScript error resolution
     */
    private initializeExecution;
    /**
     * Generate TypeScript-specific agents for a phase
     */
    private generatePhaseAgents;
    /**
     * Generate TypeScript-specific agent names
     */
    private generateAgentName;
    /**
     * Get phase number from agent number
     */
    private getPhaseFromAgentNumber;
    /**
     * Execute a specific phase for TypeScript error resolution
     */
    private executePhase;
    /**
     * Distribute TypeScript errors among agents
     */
    private distributeErrorsToAgents;
    /**
     * Execute individual TypeScript agent
     */
    private executeTypeScriptAgent;
    /**
     * Generate TypeScript-specific prompts for each phase
     */
    private generateTypeScriptPrompt;
    /**
     * Execute agent with specific prompt
     */
    private runAgentWithPrompt;
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
     * Generate final success report
     */
    private generateFinalSuccessReport;
    /**
     * Get current execution status
     */
    getCurrentExecution(): ITypeScriptExecution | undefined;
    /**
     * Get current phase information
     */
    getCurrentPhase(): ITypeScriptPhaseExecution | undefined;
    /**
     * Get execution summary
     */
    getExecutionSummary(): {
        totalErrors: number;
        errorsRemaining: number;
        iteration: number;
        currentPhase: number;
        overallProgress: number;
        status: string;
    };
    /**
     * Stop all TypeScript agents
     */
    stopAllAgents(): void;
    /**
     * Get quick TypeScript error check
     */
    getTypeScriptErrorCount(): Promise<number>;
}
//# sourceMappingURL=TypeScriptErrorOrchestrator.d.ts.map