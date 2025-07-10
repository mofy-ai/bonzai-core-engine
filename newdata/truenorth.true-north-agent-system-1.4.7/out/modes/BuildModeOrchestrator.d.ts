/**
 * Build Mode Orchestrator
 *
 * 🔧 BUILD MODE: Rapidly create new features and functionality from scratch
 * Mission: Build new features quickly without worrying about polish or perfection
 */
import { BaseModeOrchestrator, DevelopmentMode, IModeAgent, ISuccessCriteria } from './BaseModeOrchestrator';
export declare class BuildModeOrchestrator extends BaseModeOrchestrator {
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
    private checkDevEnvironment;
}
//# sourceMappingURL=BuildModeOrchestrator.d.ts.map