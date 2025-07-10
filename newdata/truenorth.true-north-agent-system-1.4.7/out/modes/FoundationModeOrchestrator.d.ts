/**
 * Foundation Mode Orchestrator
 *
 * 🏗️ FOUNDATION MODE: Get the basic development environment working from broken or new state
 * Mission: Establish a working development foundation before building features
 */
import { BaseModeOrchestrator, DevelopmentMode, IModeAgent, ISuccessCriteria } from './BaseModeOrchestrator';
export declare class FoundationModeOrchestrator extends BaseModeOrchestrator {
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
    private validateDevServerStarts;
    private validateHotReload;
    private validateNoCompilationErrors;
}
//# sourceMappingURL=FoundationModeOrchestrator.d.ts.map