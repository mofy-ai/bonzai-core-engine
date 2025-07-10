/**
 * Clean TrueNorth Orchestrator - MVP Implementation
 * Focuses on core task orchestration without over-engineering
 */
import { ClaudeCliManager } from './ClaudeCliManager';
import { ConfigManager } from './ConfigManager';
export interface ITrueNorthTask {
    id: string;
    name: string;
    description: string;
    icon: string;
    status: 'pending' | 'running' | 'completed' | 'failed' | 'paused';
    progress: number;
    startTime?: Date;
    endTime?: Date;
    pausedTime?: Date;
    resumedTime?: Date;
    output: string[];
    error?: string;
}
export declare class TrueNorthOrchestrator {
    private claudeCliManager;
    private configManager;
    private tasks;
    private currentTask?;
    private pausedTasks;
    private onTaskUpdate?;
    private outputManager;
    constructor(claudeCliManager: ClaudeCliManager, configManager: ConfigManager);
    /**
     * Get available tasks for the current project
     */
    getAvailableTasks(): ITrueNorthTask[];
    /**
     * Execute a specific task
     */
    executeTask(taskId: string): Promise<void>;
    /**
     * Get current task status
     */
    getCurrentTask(): ITrueNorthTask | undefined;
    /**
     * Get all tasks including completed ones
     */
    getAllTasks(): ITrueNorthTask[];
    /**
     * Set callback for task updates
     */
    onUpdate(callback: (task: ITrueNorthTask) => void): void;
    /**
     * Stop current running task
     */
    stopCurrentTask(): void;
    /**
     * Pause a specific task
     */
    pauseTask(taskId: string): void;
    /**
     * Resume a paused task
     */
    resumeTask(taskId: string): Promise<void>;
    /**
     * Kill a specific task
     */
    killTask(taskId: string): void;
    /**
     * Clear completed tasks from history
     */
    clearCompletedTasks(): void;
    /**
     * Get task by ID
     */
    getTaskById(taskId: string): ITrueNorthTask | undefined;
    /**
     * Continue execution of a resumed task
     */
    private continueTaskExecution;
    /**
     * Continue execution of a custom task
     */
    private executeCustomTaskContinuation;
    /**
     * Execute a custom user-defined mission
     */
    executeCustomTask(mission: string): Promise<void>;
    private analyzeProject;
    private cleanupCode;
    private findDuplicates;
    private notifyTaskUpdate;
    /**
     * Get paused tasks
     */
    getPausedTasks(): ITrueNorthTask[];
    /**
     * Dispose resources
     */
    dispose(): void;
}
//# sourceMappingURL=TrueNorthOrchestrator.d.ts.map