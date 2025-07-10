"use strict";
/**
 * Base Mode Orchestrator - Universal Development Modes System
 *
 * Abstract base class for all development mode orchestrators.
 * Implements the Universal Development Modes framework with mode-specific
 * guard questions, success criteria, and transition logic.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.BaseModeOrchestrator = exports.DevelopmentMode = void 0;
const ErrorHandler_1 = require("../core/ErrorHandler");
// vscode not used in base class
var DevelopmentMode;
(function (DevelopmentMode) {
    DevelopmentMode["FOUNDATION"] = "foundation";
    DevelopmentMode["BUILD"] = "build";
    DevelopmentMode["COMPLETION"] = "completion";
    DevelopmentMode["CLEANUP"] = "cleanup";
    DevelopmentMode["VALIDATION"] = "validation";
    DevelopmentMode["DEPLOYMENT"] = "deployment";
    DevelopmentMode["MAINTENANCE"] = "maintenance";
    DevelopmentMode["ENHANCEMENT"] = "enhancement";
})(DevelopmentMode || (exports.DevelopmentMode = DevelopmentMode = {}));
class BaseModeOrchestrator {
    constructor(claudeCliManager, configManager) {
        this.transitions = [];
        this.claudeCliManager = claudeCliManager;
        this.configManager = configManager;
        this.errorHandler = ErrorHandler_1.ErrorHandler.getInstance();
    }
    /**
     * Start the mode execution with specialized agents
     */
    async startModeExecution() {
        try {
            const agents = this.createModeAgents();
            this.currentExecution = {
                id: `${this.getMode()}_${Date.now()}`,
                mode: this.getMode(),
                startTime: new Date(),
                status: 'running',
                agents,
                successCriteria: this.getSuccessCriteria(),
                progress: 0,
            };
            // Validate mode entry with guard questions
            const canProceed = this.validateModeEntry();
            if (!canProceed) {
                throw new Error(`Cannot enter ${this.getMode()} mode: guard questions failed`);
            }
            // Execute agents sequentially
            for (const agent of agents) {
                await this.executeAgent(agent);
                this.updateProgress();
            }
            this.currentExecution.status = 'completed';
            this.currentExecution.endTime = new Date();
            return this.currentExecution;
        }
        catch (error) {
            await this.errorHandler.handleError(error instanceof Error ? error : new Error(String(error)), ErrorHandler_1.ErrorCategory.SYSTEM, ErrorHandler_1.ErrorSeverity.HIGH, {
                component: 'ModeOrchestrator',
                operation: 'startModeExecution',
            });
            if (this.currentExecution) {
                this.currentExecution.status = 'failed';
                this.currentExecution.endTime = new Date();
            }
            throw error;
        }
    }
    /**
     * Execute a single agent with mode-specific constraints
     */
    async executeAgent(agent) {
        agent.status = 'running';
        agent.startTime = new Date();
        if (this.currentExecution) {
            this.currentExecution.currentAgent = agent;
        }
        try {
            // Validate agent action against mode constraints
            this.validateAgentAction(agent);
            // Create mode-specific prompt with guard questions
            const prompt = this.createModeAwarePrompt(agent);
            // Execute with Claude CLI
            const result = await this.claudeCliManager.executeCommand(prompt, {
                timeout: 180000, // 3 minutes per agent
                commandType: 'agent',
            });
            agent.output.push(result);
            agent.status = 'completed';
            agent.endTime = new Date();
            agent.progress = 100;
        }
        catch (error) {
            agent.status = 'failed';
            agent.endTime = new Date();
            agent.error = error instanceof Error ? error.message : String(error);
            throw error;
        }
    }
    /**
     * Create mode-aware prompt with guard questions and constraints
     */
    createModeAwarePrompt(agent) {
        const guardQuestions = this.getGuardQuestions().join('\n- ');
        const allowedActions = this.getAllowedActions().join('\n✅ ');
        const forbiddenActions = this.getForbiddenActions().join('\n❌ ');
        return `${this.getModeIcon()} ${this.getModeDisplayName().toUpperCase()} MODE ACTIVE

MISSION: ${agent.description}
CONTEXT: Working on ${agent.name} in ${this.getMode()} mode

ALLOWED ACTIONS:
✅ ${allowedActions}

STRICTLY FORBIDDEN:
❌ ${forbiddenActions}

GUARD QUESTIONS (Ask yourself before any action):
- ${guardQuestions}

TASK: ${agent.description}

Important: Only perform actions that align with ${this.getMode()} mode objectives. 
Always validate your approach against the guard questions above.
Focus on the specific mission and avoid scope creep.`;
    }
    /**
     * Validate if we can enter this mode
     */
    validateModeEntry() {
        // Each mode can override this for specific validation
        return true;
    }
    /**
     * Validate agent action against mode constraints
     */
    validateAgentAction(agent) {
        // Basic implementation - each mode can add specific validation
        // For now, we trust the prompt engineering to enforce constraints
        // Log agent validation for future enhancement
        // Future: implement detailed agent validation logic
        void agent; // Use parameter to prevent warning
    }
    /**
     * Update execution progress
     */
    updateProgress() {
        if (!this.currentExecution) {
            return;
        }
        const totalAgents = this.currentExecution.agents.length;
        const completedAgents = this.currentExecution.agents.filter(a => a.status === 'completed').length;
        const percentageMultiplier = 100;
        this.currentExecution.progress = Math.round((completedAgents / totalAgents) * percentageMultiplier);
    }
    /**
     * Check if all success criteria are met
     */
    async checkSuccessCriteria() {
        if (!this.currentExecution) {
            return false;
        }
        for (const criteria of this.currentExecution.successCriteria) {
            if (criteria.required && !criteria.completed) {
                // Try to validate with custom validator if available
                if (criteria.validator) {
                    criteria.completed = await criteria.validator();
                }
                if (!criteria.completed) {
                    return false;
                }
            }
        }
        return true;
    }
    /**
     * Get recommended next modes based on current state
     */
    async getNextModeRecommendations() {
        const criteriasMet = await this.checkSuccessCriteria();
        if (criteriasMet) {
            return this.getRecommendedNextModes();
        }
        // If criteria not met, recommend staying in current mode
        return [this.getMode()];
    }
    /**
     * Record mode transition
     */
    recordTransition(toMode, reason) {
        const completedCriteria = this.currentExecution?.successCriteria.filter(c => c.completed).map(c => c.description) ?? [];
        const transition = {
            fromMode: this.getMode(),
            toMode,
            reason,
            completedCriteria,
            timestamp: new Date(),
        };
        this.transitions.push(transition);
    }
    /**
     * Get current execution status
     */
    getCurrentExecution() {
        return this.currentExecution;
    }
    /**
     * Get execution history
     */
    getTransitionHistory() {
        return [...this.transitions];
    }
    /**
     * Stop current execution
     */
    stopExecution() {
        if (this.currentExecution && this.currentExecution.status === 'running') {
            this.currentExecution.status = 'failed';
            this.currentExecution.endTime = new Date();
        }
    }
}
exports.BaseModeOrchestrator = BaseModeOrchestrator;
//# sourceMappingURL=BaseModeOrchestrator.js.map