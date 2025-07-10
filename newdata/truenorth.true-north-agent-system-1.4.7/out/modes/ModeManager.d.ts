/**
 * Mode Manager - Universal Development Modes System
 *
 * Centralized manager for all development mode orchestrators.
 * Handles mode detection, switching, and coordination between modes.
 */
import { DevelopmentMode, BaseModeOrchestrator, IModeExecution, IModeTransition } from './BaseModeOrchestrator';
import { IModeRecommendation } from './ModeDetectionSystem';
import { ClaudeCliManager } from '../core/ClaudeCliManager';
import { ConfigManager } from '../core/ConfigManager';
export interface IModeManagerState {
    currentMode: DevelopmentMode;
    activeExecution?: IModeExecution;
    lastRecommendation?: IModeRecommendation;
    transitionHistory: IModeTransition[];
    modeStartTime: Date;
}
export declare class ModeManager {
    private claudeCliManager;
    private configManager;
    private errorHandler;
    private detectionSystem;
    private orchestrators;
    private state;
    private statusBarItem?;
    constructor(claudeCliManager: ClaudeCliManager, configManager: ConfigManager);
    /**
     * Initialize all mode orchestrators
     */
    private initializeOrchestrators;
    /**
     * Detect and recommend appropriate mode for current project
     */
    detectAndRecommendMode(): Promise<IModeRecommendation>;
    /**
     * Switch to a specific mode
     */
    switchToMode(mode: DevelopmentMode, reason?: string): Promise<void>;
    /**
     * Start execution in current mode
     */
    startCurrentModeExecution(): Promise<IModeExecution>;
    /**
     * Get current mode information
     */
    getCurrentMode(): DevelopmentMode;
    /**
     * Get current mode orchestrator
     */
    getCurrentOrchestrator(): BaseModeOrchestrator | undefined;
    /**
     * Get current execution status
     */
    getCurrentExecution(): IModeExecution | undefined;
    /**
     * Get all available modes
     */
    getAvailableModes(): DevelopmentMode[];
    /**
     * Get mode display information
     */
    getModeDisplayInfo(mode: DevelopmentMode): {
        icon: string;
        name: string;
    } | undefined;
    /**
     * Check if current mode's success criteria are met
     */
    checkCurrentModeCompletion(): Promise<boolean>;
    /**
     * Get recommended next modes
     */
    getRecommendedNextModes(): Promise<DevelopmentMode[]>;
    /**
     * Get transition history
     */
    getTransitionHistory(): IModeTransition[];
    /**
     * Get current state
     */
    getState(): IModeManagerState;
    /**
     * Create status bar item for mode display
     */
    private createStatusBarItem;
    /**
     * Update status bar item display
     */
    private updateStatusBarItem;
    /**
     * Dispose resources
     */
    dispose(): void;
}
//# sourceMappingURL=ModeManager.d.ts.map