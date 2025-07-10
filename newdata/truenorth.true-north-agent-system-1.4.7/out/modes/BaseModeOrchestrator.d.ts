/**
 * Base Mode Orchestrator - Universal Development Modes System
 *
 * Abstract base class for all development mode orchestrators.
 * Implements the Universal Development Modes framework with mode-specific
 * guard questions, success criteria, and transition logic.
 */
import { ClaudeCliManager } from '../core/ClaudeCliManager';
import { ConfigManager } from '../core/ConfigManager';
import { ErrorHandler } from '../core/ErrorHandler';
export declare enum DevelopmentMode {
    FOUNDATION = "foundation",
    BUILD = "build",
    COMPLETION = "completion",
    CLEANUP = "cleanup",
    VALIDATION = "validation",
    DEPLOYMENT = "deployment",
    MAINTENANCE = "maintenance",
    ENHANCEMENT = "enhancement"
}
export interface IModeAgent {
    id: string;
    name: string;
    description: string;
    mode: DevelopmentMode;
    status: 'pending' | 'running' | 'completed' | 'failed';
    startTime?: Date;
    endTime?: Date;
    progress: number;
    output: string[];
    error?: string;
    guardQuestions: string[];
    allowedActions: string[];
    forbiddenActions: string[];
}
export interface IModeExecution {
    id: string;
    mode: DevelopmentMode;
    startTime: Date;
    endTime?: Date;
    status: 'running' | 'completed' | 'failed';
    agents: IModeAgent[];
    successCriteria: ISuccessCriteria[];
    progress: number;
    currentAgent?: IModeAgent;
}
export interface ISuccessCriteria {
    id: string;
    description: string;
    completed: boolean;
    required: boolean;
    validator?: () => Promise<boolean>;
}
export interface IModeTransition {
    fromMode: DevelopmentMode;
    toMode: DevelopmentMode;
    reason: string;
    completedCriteria: string[];
    timestamp: Date;
}
export declare abstract class BaseModeOrchestrator {
    protected claudeCliManager: ClaudeCliManager;
    protected configManager: ConfigManager;
    protected errorHandler: ErrorHandler;
    protected currentExecution?: IModeExecution;
    protected transitions: IModeTransition[];
    constructor(claudeCliManager: ClaudeCliManager, configManager: ConfigManager);
    abstract getMode(): DevelopmentMode;
    abstract getModeIcon(): string;
    abstract getModeDisplayName(): string;
    abstract getGuardQuestions(): string[];
    abstract getAllowedActions(): string[];
    abstract getForbiddenActions(): string[];
    abstract getSuccessCriteria(): ISuccessCriteria[];
    abstract createModeAgents(): IModeAgent[];
    abstract getRecommendedNextModes(): DevelopmentMode[];
    /**
     * Start the mode execution with specialized agents
     */
    startModeExecution(): Promise<IModeExecution>;
    /**
     * Execute a single agent with mode-specific constraints
     */
    protected executeAgent(agent: IModeAgent): Promise<void>;
    /**
     * Create mode-aware prompt with guard questions and constraints
     */
    protected createModeAwarePrompt(agent: IModeAgent): string;
    /**
     * Validate if we can enter this mode
     */
    protected validateModeEntry(): boolean;
    /**
     * Validate agent action against mode constraints
     */
    protected validateAgentAction(agent: IModeAgent): void;
    /**
     * Update execution progress
     */
    protected updateProgress(): void;
    /**
     * Check if all success criteria are met
     */
    checkSuccessCriteria(): Promise<boolean>;
    /**
     * Get recommended next modes based on current state
     */
    getNextModeRecommendations(): Promise<DevelopmentMode[]>;
    /**
     * Record mode transition
     */
    recordTransition(toMode: DevelopmentMode, reason: string): void;
    /**
     * Get current execution status
     */
    getCurrentExecution(): IModeExecution | undefined;
    /**
     * Get execution history
     */
    getTransitionHistory(): IModeTransition[];
    /**
     * Stop current execution
     */
    stopExecution(): void;
}
//# sourceMappingURL=BaseModeOrchestrator.d.ts.map