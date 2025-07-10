/**
 * Validation Mode Orchestrator
 *
 * 🧪 VALIDATION MODE: Test and verify that everything works as expected
 * Mission: Thoroughly test and validate all functionality before deployment
 */
import { BaseModeOrchestrator, DevelopmentMode, IModeAgent, ISuccessCriteria } from './BaseModeOrchestrator';
export declare class ValidationModeOrchestrator extends BaseModeOrchestrator {
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
//# sourceMappingURL=ValidationModeOrchestrator.d.ts.map