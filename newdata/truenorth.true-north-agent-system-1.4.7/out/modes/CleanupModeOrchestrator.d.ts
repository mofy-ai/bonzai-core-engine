/**
 * Cleanup Mode Orchestrator
 *
 * 🧹 CLEANUP MODE: Organize, optimize, and clean messy but functional code
 * Mission: Improve code quality without changing functionality
 */
import { BaseModeOrchestrator, DevelopmentMode, IModeAgent, ISuccessCriteria } from './BaseModeOrchestrator';
export declare class CleanupModeOrchestrator extends BaseModeOrchestrator {
    getMode(): DevelopmentMode;
    getModeIcon(): string;
    getModeDisplayName(): string;
    getGuardQuestions(): string[];
    getAllowedActions(): string[];
    getForbiddenActions(): string[];
    getSuccessCriteria(): ISuccessCriteria[];
    getRecommendedNextModes(): DevelopmentMode[];
    createModeAgents(): IModeAgent[];
    protected validateModeEntry(): boolean;
}
//# sourceMappingURL=CleanupModeOrchestrator.d.ts.map