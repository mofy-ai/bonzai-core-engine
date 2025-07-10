"use strict";
/**
 * Clean TrueNorth Orchestrator - MVP Implementation
 * Focuses on core task orchestration without over-engineering
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.TrueNorthOrchestrator = void 0;
const OutputManager_1 = require("../output/OutputManager");
// Constants for task progress and validation
const taskConstants = {
    maxProgress: 90,
    progressIncrement: 10,
    initialProgress: 25,
    completedProgress: 100,
    failedProgress: 0,
    minOutputLength: 20,
    descriptionMaxLength: 100,
};
class TrueNorthOrchestrator {
    constructor(claudeCliManager, configManager) {
        this.claudeCliManager = claudeCliManager;
        this.configManager = configManager;
        this.tasks = [];
        this.pausedTasks = new Map();
        this.outputManager = new OutputManager_1.OutputManager();
    }
    /**
     * Get available tasks for the current project
     */
    getAvailableTasks() {
        return [
            {
                id: 'analyze-project',
                name: 'Analyze Project',
                description: 'Analyze the current project structure and provide insights',
                icon: 'search',
                status: 'pending',
                progress: 0,
                output: [],
            },
            {
                id: 'cleanup-code',
                name: 'Clean Up Code',
                description: 'Clean up and optimize code structure',
                icon: 'tools',
                status: 'pending',
                progress: 0,
                output: [],
            },
            {
                id: 'find-duplicates',
                name: 'Find Duplicates',
                description: 'Find and suggest removal of duplicate code',
                icon: 'files',
                status: 'pending',
                progress: 0,
                output: [],
            },
        ];
    }
    /**
     * Execute a specific task
     */
    async executeTask(taskId) {
        const task = this.getAvailableTasks().find(t => t.id === taskId);
        if (!task) {
            throw new Error(`Task ${taskId} not found`);
        }
        task.status = 'running';
        task.startTime = new Date();
        task.progress = 0;
        this.currentTask = task;
        // Store task in tasks array for persistence
        const existingIndex = this.tasks.findIndex(t => t.id === taskId);
        if (existingIndex >= 0) {
            this.tasks[existingIndex] = task;
        }
        else {
            this.tasks.push(task);
        }
        this.notifyTaskUpdate(task);
        try {
            // Execute task based on type
            switch (taskId) {
                case 'analyze-project':
                    await this.analyzeProject(task);
                    break;
                case 'cleanup-code':
                    await this.cleanupCode(task);
                    break;
                case 'find-duplicates':
                    await this.findDuplicates(task);
                    break;
                default:
                    throw new Error(`Unknown task: ${taskId}`);
            }
            task.status = 'completed';
            task.endTime = new Date();
            task.progress = 100;
        }
        catch (error) {
            task.status = 'failed';
            task.error = error instanceof Error ? error.message : 'Unknown error';
            task.endTime = new Date();
        }
        this.currentTask = undefined;
        this.notifyTaskUpdate(task);
    }
    /**
     * Get current task status
     */
    getCurrentTask() {
        return this.currentTask;
    }
    /**
     * Get all tasks including completed ones
     */
    getAllTasks() {
        return [...this.tasks];
    }
    /**
     * Set callback for task updates
     */
    onUpdate(callback) {
        this.onTaskUpdate = callback;
    }
    /**
     * Stop current running task
     */
    stopCurrentTask() {
        if (this.currentTask && this.currentTask.status === 'running') {
            this.currentTask.status = 'failed';
            this.currentTask.error = 'Stopped by user';
            this.currentTask.endTime = new Date();
            this.notifyTaskUpdate(this.currentTask);
            this.currentTask = undefined;
        }
    }
    /**
     * Pause a specific task
     */
    pauseTask(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (task && task.status === 'running') {
            task.status = 'paused';
            task.pausedTime = new Date();
            this.pausedTasks.set(taskId, task);
            // If this is the current task, stop it
            if (this.currentTask?.id === taskId) {
                this.currentTask = undefined;
            }
            this.notifyTaskUpdate(task);
            this.outputManager.log('info', `Task ${taskId} paused`, 'TrueNorth Orchestrator');
        }
    }
    /**
     * Resume a paused task
     */
    async resumeTask(taskId) {
        const task = this.pausedTasks.get(taskId);
        if (task && task.status === 'paused') {
            task.status = 'running';
            task.resumedTime = new Date();
            this.pausedTasks.delete(taskId);
            this.currentTask = task;
            this.notifyTaskUpdate(task);
            this.outputManager.log('info', `Task ${taskId} resumed`, 'TrueNorth Orchestrator');
            // Continue execution from where it left off
            try {
                await this.continueTaskExecution(task);
            }
            catch (error) {
                task.status = 'failed';
                task.error = error instanceof Error ? error.message : 'Unknown error';
                task.endTime = new Date();
                this.currentTask = undefined;
                this.notifyTaskUpdate(task);
            }
        }
    }
    /**
     * Kill a specific task
     */
    killTask(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (task && (task.status === 'running' || task.status === 'paused')) {
            task.status = 'failed';
            task.error = 'Killed by user';
            task.endTime = new Date();
            // Remove from paused tasks if it was paused
            this.pausedTasks.delete(taskId);
            // If this is the current task, clear it
            if (this.currentTask?.id === taskId) {
                this.currentTask = undefined;
            }
            this.notifyTaskUpdate(task);
            this.outputManager.log('info', `Task ${taskId} killed`, 'TrueNorth Orchestrator');
        }
    }
    /**
     * Clear completed tasks from history
     */
    clearCompletedTasks() {
        const initialCount = this.tasks.length;
        this.tasks = this.tasks.filter(task => task.status !== 'completed');
        const removedCount = initialCount - this.tasks.length;
        this.outputManager.log('info', `Removed ${removedCount} completed tasks`, 'TrueNorth Orchestrator');
    }
    /**
     * Get task by ID
     */
    getTaskById(taskId) {
        return this.tasks.find(t => t.id === taskId);
    }
    /**
     * Continue execution of a resumed task
     */
    async continueTaskExecution(task) {
        // This is a simplified continuation - in a real implementation,
        // you would need to save and restore the execution state
        switch (task.id) {
            case 'analyze-project':
                await this.analyzeProject(task);
                break;
            case 'cleanup-code':
                await this.cleanupCode(task);
                break;
            case 'find-duplicates':
                await this.findDuplicates(task);
                break;
            default:
                if (task.id.startsWith('custom-')) {
                    // For custom tasks, we'll need to re-execute from the beginning
                    // as we don't have saved state
                    task.progress = 0;
                    task.output = [];
                    await this.executeCustomTaskContinuation(task);
                }
                else {
                    throw new Error(`Unknown task type for continuation: ${task.id}`);
                }
        }
        task.status = 'completed';
        task.endTime = new Date();
        task.progress = taskConstants.completedProgress;
        this.currentTask = undefined;
        this.notifyTaskUpdate(task);
    }
    /**
     * Continue execution of a custom task
     */
    async executeCustomTaskContinuation(task) {
        const onProgress = (message) => {
            task.progress = Math.min(taskConstants.maxProgress, task.progress + taskConstants.progressIncrement);
            task.output.push(message);
            this.notifyTaskUpdate(task);
        };
        const output = await this.claudeCliManager.executeExtendedCommand(`Continue this custom mission for the TrueNorth project: ${task.description}. Provide detailed analysis and recommendations.`, onProgress);
        if (output && output.trim().length > taskConstants.minOutputLength) {
            task.output.push(output);
        }
        else {
            throw new Error('Claude CLI command produced insufficient output');
        }
    }
    /**
     * Execute a custom user-defined mission
     */
    async executeCustomTask(mission) {
        const customTask = {
            id: `custom-${Date.now()}`,
            name: 'Custom Mission',
            description: mission.substring(0, taskConstants.descriptionMaxLength) +
                (mission.length > taskConstants.descriptionMaxLength ? '...' : ''),
            icon: 'target',
            status: 'running',
            progress: 0,
            startTime: new Date(),
            output: [],
        };
        this.outputManager.log('info', `Starting custom mission: ${mission}`, 'TrueNorth Orchestrator');
        this.currentTask = customTask;
        this.tasks.push(customTask);
        this.notifyTaskUpdate(customTask);
        try {
            customTask.progress = taskConstants.initialProgress;
            this.notifyTaskUpdate(customTask);
            const onProgress = (message) => {
                // Extract progress from message or use default increments
                customTask.progress = Math.min(taskConstants.maxProgress, customTask.progress + taskConstants.progressIncrement);
                customTask.output.push(message);
                this.notifyTaskUpdate(customTask);
            };
            const output = await this.claudeCliManager.executeExtendedCommand(`Execute this custom mission for the TrueNorth project: ${mission}. Provide detailed analysis and recommendations.`, onProgress);
            // Check if Claude CLI produced meaningful output
            if (output && output.trim().length > taskConstants.minOutputLength) {
                customTask.output.push(output);
                customTask.status = 'completed';
                customTask.endTime = new Date();
                customTask.progress = taskConstants.completedProgress;
                this.outputManager.log('success', `Custom mission completed successfully with ${output.length} chars of output`, 'TrueNorth Orchestrator');
            }
            else {
                const errorMsg = 'Claude CLI command produced insufficient output';
                customTask.error = errorMsg;
                customTask.status = 'failed';
                customTask.endTime = new Date();
                customTask.progress = taskConstants.failedProgress;
                this.outputManager.log('error', `Custom mission failed: ${customTask.error}`, 'TrueNorth Orchestrator');
                throw new Error(customTask.error);
            }
        }
        catch (error) {
            customTask.status = 'failed';
            customTask.error = error instanceof Error ? error.message : 'Unknown error';
            customTask.endTime = new Date();
        }
        this.currentTask = undefined;
        this.notifyTaskUpdate(customTask);
    }
    async analyzeProject(task) {
        const onProgress = (message) => {
            // Extract progress from message or use default increments
            task.progress = Math.min(taskConstants.maxProgress, task.progress + taskConstants.progressIncrement);
            task.output.push(message);
            this.notifyTaskUpdate(task);
        };
        task.progress = taskConstants.initialProgress;
        this.notifyTaskUpdate(task);
        const output = await this.claudeCliManager.executeAnalysisCommand('Analyze this TrueNorth VS Code extension project. List the main TypeScript files in src/ directory and briefly describe what each one does.', onProgress);
        // Check if Claude CLI produced meaningful output
        if (output && output.trim().length > 0) {
            task.output.push(output);
            task.progress = taskConstants.completedProgress;
            this.outputManager.log('success', `Analyze task completed successfully with ${output.length} chars of output`, 'TrueNorth Orchestrator');
        }
        else {
            const errorMsg = 'Claude CLI command failed or produced no output';
            task.error = errorMsg;
            task.progress = taskConstants.failedProgress;
            this.outputManager.log('error', `Analyze task failed: ${task.error}`, 'TrueNorth Orchestrator');
            throw new Error(task.error);
        }
        this.notifyTaskUpdate(task);
    }
    async cleanupCode(task) {
        const onProgress = (message) => {
            // Extract progress from message or use default increments
            task.progress = Math.min(taskConstants.maxProgress, task.progress + taskConstants.progressIncrement);
            task.output.push(message);
            this.notifyTaskUpdate(task);
        };
        task.progress = taskConstants.initialProgress;
        this.notifyTaskUpdate(task);
        const output = await this.claudeCliManager.executeAgentCommand('Review this TrueNorth extension codebase. Suggest 3 simple code improvements you can see.', onProgress);
        // Check if Claude CLI produced meaningful output
        if (output && output.trim().length > taskConstants.minOutputLength) {
            task.output.push(output);
            task.progress = taskConstants.completedProgress;
            this.outputManager.log('success', `Cleanup task completed successfully with ${output.length} chars of output`, 'TrueNorth Orchestrator');
        }
        else {
            const errorMsg = 'Claude CLI command failed or produced insufficient output';
            task.error = errorMsg;
            task.progress = taskConstants.failedProgress;
            this.outputManager.log('error', `Cleanup task failed: ${task.error}`, 'TrueNorth Orchestrator');
            throw new Error(task.error);
        }
        this.notifyTaskUpdate(task);
    }
    async findDuplicates(task) {
        const onProgress = (message) => {
            // Extract progress from message or use default increments
            task.progress = Math.min(taskConstants.maxProgress, task.progress + taskConstants.progressIncrement);
            task.output.push(message);
            this.notifyTaskUpdate(task);
        };
        task.progress = taskConstants.initialProgress;
        this.notifyTaskUpdate(task);
        const output = await this.claudeCliManager.executeAgentCommand('Scan this TrueNorth extension project for duplicate code. Find any similar functions or repeated patterns.', onProgress);
        // Check if Claude CLI produced meaningful output
        if (output && output.trim().length > taskConstants.minOutputLength) {
            task.output.push(output);
            task.progress = taskConstants.completedProgress;
            this.outputManager.log('success', `Find duplicates task completed successfully with ${output.length} chars of output`, 'TrueNorth Orchestrator');
        }
        else {
            const errorMsg = 'Claude CLI command failed or produced insufficient output';
            task.error = errorMsg;
            task.progress = taskConstants.failedProgress;
            this.outputManager.log('error', `Find duplicates task failed: ${task.error}`, 'TrueNorth Orchestrator');
            throw new Error(task.error);
        }
        this.notifyTaskUpdate(task);
    }
    notifyTaskUpdate(task) {
        this.outputManager.log('info', `Notifying task update: ${task.id} (${task.status}, ${task.progress}%)`, 'TrueNorth Orchestrator');
        if (this.onTaskUpdate) {
            this.onTaskUpdate(task);
        }
        else {
            this.outputManager.log('warning', 'No onTaskUpdate callback registered', 'TrueNorth Orchestrator');
        }
    }
    /**
     * Get paused tasks
     */
    getPausedTasks() {
        return Array.from(this.pausedTasks.values());
    }
    /**
     * Dispose resources
     */
    dispose() {
        if (this.currentTask?.status === 'running') {
            void this.stopCurrentTask();
        }
        // Kill all paused tasks
        for (const taskId of this.pausedTasks.keys()) {
            void this.killTask(taskId);
        }
    }
}
exports.TrueNorthOrchestrator = TrueNorthOrchestrator;
//# sourceMappingURL=TrueNorthOrchestrator.js.map