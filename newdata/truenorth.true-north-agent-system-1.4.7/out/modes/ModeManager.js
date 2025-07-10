"use strict";
/**
 * Mode Manager - Universal Development Modes System
 *
 * Centralized manager for all development mode orchestrators.
 * Handles mode detection, switching, and coordination between modes.
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
exports.ModeManager = void 0;
const BaseModeOrchestrator_1 = require("./BaseModeOrchestrator");
const ModeDetectionSystem_1 = require("./ModeDetectionSystem");
const FoundationModeOrchestrator_1 = require("./FoundationModeOrchestrator");
const BuildModeOrchestrator_1 = require("./BuildModeOrchestrator");
const CompletionModeOrchestrator_1 = require("./CompletionModeOrchestrator");
const CleanupModeOrchestrator_1 = require("./CleanupModeOrchestrator");
const ValidationModeOrchestrator_1 = require("./ValidationModeOrchestrator");
const DeploymentModeOrchestrator_1 = require("./DeploymentModeOrchestrator");
const MaintenanceModeOrchestrator_1 = require("./MaintenanceModeOrchestrator");
const EnhancementModeOrchestrator_1 = require("./EnhancementModeOrchestrator");
const ErrorHandler_1 = require("../core/ErrorHandler");
const vscode = __importStar(require("vscode"));
// Constants
const modeStatusPriority = 100;
class ModeManager {
    constructor(claudeCliManager, configManager) {
        this.claudeCliManager = claudeCliManager;
        this.configManager = configManager;
        this.errorHandler = ErrorHandler_1.ErrorHandler.getInstance();
        this.detectionSystem = new ModeDetectionSystem_1.ModeDetectionSystem();
        // Initialize orchestrators
        this.orchestrators = new Map();
        this.initializeOrchestrators();
        // Initialize state
        this.state = {
            currentMode: BaseModeOrchestrator_1.DevelopmentMode.FOUNDATION, // Default starting mode
            transitionHistory: [],
            modeStartTime: new Date(),
        };
        this.createStatusBarItem();
    }
    /**
     * Initialize all mode orchestrators
     */
    initializeOrchestrators() {
        this.orchestrators.set(BaseModeOrchestrator_1.DevelopmentMode.FOUNDATION, new FoundationModeOrchestrator_1.FoundationModeOrchestrator(this.claudeCliManager, this.configManager));
        this.orchestrators.set(BaseModeOrchestrator_1.DevelopmentMode.BUILD, new BuildModeOrchestrator_1.BuildModeOrchestrator(this.claudeCliManager, this.configManager));
        this.orchestrators.set(BaseModeOrchestrator_1.DevelopmentMode.COMPLETION, new CompletionModeOrchestrator_1.CompletionModeOrchestrator(this.claudeCliManager, this.configManager));
        this.orchestrators.set(BaseModeOrchestrator_1.DevelopmentMode.CLEANUP, new CleanupModeOrchestrator_1.CleanupModeOrchestrator(this.claudeCliManager, this.configManager));
        this.orchestrators.set(BaseModeOrchestrator_1.DevelopmentMode.VALIDATION, new ValidationModeOrchestrator_1.ValidationModeOrchestrator(this.claudeCliManager, this.configManager));
        this.orchestrators.set(BaseModeOrchestrator_1.DevelopmentMode.DEPLOYMENT, new DeploymentModeOrchestrator_1.DeploymentModeOrchestrator(this.claudeCliManager, this.configManager));
        this.orchestrators.set(BaseModeOrchestrator_1.DevelopmentMode.MAINTENANCE, new MaintenanceModeOrchestrator_1.MaintenanceModeOrchestrator(this.claudeCliManager, this.configManager));
        this.orchestrators.set(BaseModeOrchestrator_1.DevelopmentMode.ENHANCEMENT, new EnhancementModeOrchestrator_1.EnhancementModeOrchestrator(this.claudeCliManager, this.configManager));
    }
    /**
     * Detect and recommend appropriate mode for current project
     */
    async detectAndRecommendMode() {
        try {
            const recommendation = this.detectionSystem.recommendMode();
            this.state.lastRecommendation = recommendation;
            return recommendation;
        }
        catch (error) {
            await this.errorHandler.handleError(error instanceof Error ? error : new Error(String(error)), ErrorHandler_1.ErrorCategory.SYSTEM, ErrorHandler_1.ErrorSeverity.MEDIUM, {
                component: 'ModeManager',
                operation: 'detectAndRecommendMode',
            });
            // Return fallback recommendation
            return {
                recommendedMode: BaseModeOrchestrator_1.DevelopmentMode.FOUNDATION,
                confidence: 50,
                reasoning: ['Failed to analyze project, defaulting to Foundation mode'],
                assessment: {
                    canRunDevServer: false,
                    hasAllFeatures: false,
                    featuresPartiallyComplete: false,
                    codeIsClean: false,
                    hasTestedThoroughly: false,
                    isLiveInProduction: false,
                    productionIsStable: false,
                    needsNewFeatures: false,
                },
                alternativeModes: [],
            };
        }
    }
    /**
     * Switch to a specific mode
     */
    async switchToMode(mode, reason) {
        try {
            const previousMode = this.state.currentMode;
            // Stop current execution if running
            const currentOrchestrator = this.orchestrators.get(this.state.currentMode);
            if (currentOrchestrator && this.state.activeExecution) {
                currentOrchestrator.stopExecution();
            }
            // Record transition
            const transition = {
                fromMode: previousMode,
                toMode: mode,
                reason: reason ?? 'Manual mode switch',
                completedCriteria: [],
                timestamp: new Date(),
            };
            this.state.transitionHistory.push(transition);
            this.state.currentMode = mode;
            this.state.modeStartTime = new Date();
            this.state.activeExecution = undefined;
            // Update UI
            this.updateStatusBarItem();
            // Show mode switch notification
            const orchestrator = this.orchestrators.get(mode);
            if (orchestrator) {
                vscode.window
                    .showInformationMessage(`${orchestrator.getModeIcon()} Switched to ${orchestrator.getModeDisplayName()}`, 'Start Execution')
                    .then(selection => {
                    if (selection === 'Start Execution') {
                        void this.startCurrentModeExecution();
                    }
                });
            }
        }
        catch (error) {
            await this.errorHandler.handleError(error instanceof Error ? error : new Error(String(error)), ErrorHandler_1.ErrorCategory.SYSTEM, ErrorHandler_1.ErrorSeverity.HIGH, {
                component: 'ModeManager',
                operation: 'switchToMode',
            });
            throw error;
        }
    }
    /**
     * Start execution in current mode
     */
    async startCurrentModeExecution() {
        const orchestrator = this.orchestrators.get(this.state.currentMode);
        if (!orchestrator) {
            throw new Error(`No orchestrator found for mode: ${this.state.currentMode}`);
        }
        try {
            this.state.activeExecution = await orchestrator.startModeExecution();
            this.updateStatusBarItem();
            return this.state.activeExecution;
        }
        catch (error) {
            await this.errorHandler.handleError(error instanceof Error ? error : new Error(String(error)), ErrorHandler_1.ErrorCategory.SYSTEM, ErrorHandler_1.ErrorSeverity.HIGH, {
                component: 'ModeManager',
                operation: 'startCurrentModeExecution',
            });
            throw error;
        }
    }
    /**
     * Get current mode information
     */
    getCurrentMode() {
        return this.state.currentMode;
    }
    /**
     * Get current mode orchestrator
     */
    getCurrentOrchestrator() {
        return this.orchestrators.get(this.state.currentMode);
    }
    /**
     * Get current execution status
     */
    getCurrentExecution() {
        return this.state.activeExecution;
    }
    /**
     * Get all available modes
     */
    getAvailableModes() {
        return Array.from(this.orchestrators.keys());
    }
    /**
     * Get mode display information
     */
    getModeDisplayInfo(mode) {
        const orchestrator = this.orchestrators.get(mode);
        if (!orchestrator) {
            return undefined;
        }
        return {
            icon: orchestrator.getModeIcon(),
            name: orchestrator.getModeDisplayName(),
        };
    }
    /**
     * Check if current mode's success criteria are met
     */
    async checkCurrentModeCompletion() {
        const orchestrator = this.orchestrators.get(this.state.currentMode);
        if (!orchestrator) {
            return false;
        }
        return orchestrator.checkSuccessCriteria();
    }
    /**
     * Get recommended next modes
     */
    async getRecommendedNextModes() {
        const orchestrator = this.orchestrators.get(this.state.currentMode);
        if (!orchestrator) {
            return [];
        }
        return orchestrator.getNextModeRecommendations();
    }
    /**
     * Get transition history
     */
    getTransitionHistory() {
        return [...this.state.transitionHistory];
    }
    /**
     * Get current state
     */
    getState() {
        return { ...this.state };
    }
    /**
     * Create status bar item for mode display
     */
    createStatusBarItem() {
        this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, modeStatusPriority);
        this.statusBarItem.command = 'truenorth.showModeSelector';
        this.updateStatusBarItem();
        this.statusBarItem.show();
    }
    /**
     * Update status bar item display
     */
    updateStatusBarItem() {
        if (!this.statusBarItem) {
            return;
        }
        const orchestrator = this.orchestrators.get(this.state.currentMode);
        if (!orchestrator) {
            return;
        }
        const icon = orchestrator.getModeIcon();
        const name = orchestrator.getModeDisplayName();
        let status = '';
        if (this.state.activeExecution) {
            switch (this.state.activeExecution.status) {
                case 'running':
                    status = ` (${this.state.activeExecution.progress}%)`;
                    break;
                case 'completed':
                    status = ' ✅';
                    break;
                case 'failed':
                    status = ' ❌';
                    break;
            }
        }
        this.statusBarItem.text = `${icon} ${name}${status}`;
        this.statusBarItem.tooltip = `Current Mode: ${name}\nClick to switch modes`;
    }
    /**
     * Dispose resources
     */
    dispose() {
        // Stop any running executions
        if (this.state.activeExecution) {
            const orchestrator = this.orchestrators.get(this.state.currentMode);
            orchestrator?.stopExecution();
        }
        // Dispose status bar item
        this.statusBarItem?.dispose();
    }
}
exports.ModeManager = ModeManager;
//# sourceMappingURL=ModeManager.js.map