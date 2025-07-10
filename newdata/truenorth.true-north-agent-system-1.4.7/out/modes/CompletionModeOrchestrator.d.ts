/**
 * Completion Mode Orchestrator
 *
 * 🏁 COMPLETION MODE: Complete existing partial implementations - finish what was started
 * Mission: Polish and complete existing features without adding new scope
 */
import { BaseModeOrchestrator, DevelopmentMode, IModeAgent, ISuccessCriteria } from './BaseModeOrchestrator';
export declare class CompletionModeOrchestrator extends BaseModeOrchestrator {
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
    private checkForPartialFeatures;
    private countTodoComments;
    private findIncompletePatterns;
    private findStubImplementations;
    private getAllSourceFiles;
}
//# sourceMappingURL=CompletionModeOrchestrator.d.ts.map