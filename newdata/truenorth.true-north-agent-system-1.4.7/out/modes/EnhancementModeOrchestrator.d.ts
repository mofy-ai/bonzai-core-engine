/**
 * Enhancement Mode Orchestrator
 *
 * 🚀 ENHANCEMENT MODE: Explore new technologies and proof-of-concepts
 * Mission: Explore without breaking - enhance existing features with new capabilities
 */
import { BaseModeOrchestrator, DevelopmentMode, IModeAgent, ISuccessCriteria } from './BaseModeOrchestrator';
export declare class EnhancementModeOrchestrator extends BaseModeOrchestrator {
    getMode(): DevelopmentMode;
    getModeIcon(): string;
    getModeDisplayName(): string;
    getGuardQuestions(): string[];
    getAllowedActions(): string[];
    getForbiddenActions(): string[];
    getSuccessCriteria(): ISuccessCriteria[];
    getRecommendedNextModes(): DevelopmentMode[];
    createModeAgents(): IModeAgent[];
}
//# sourceMappingURL=EnhancementModeOrchestrator.d.ts.map