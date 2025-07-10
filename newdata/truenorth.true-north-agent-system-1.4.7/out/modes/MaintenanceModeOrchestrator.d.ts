/**
 * Maintenance Mode Orchestrator
 *
 * 🔧 MAINTENANCE MODE: Maintain and improve existing stable codebase
 * Mission: Keep it running smoothly - ongoing maintenance, monitoring, and incremental improvements
 */
import { BaseModeOrchestrator, DevelopmentMode, IModeAgent, ISuccessCriteria } from './BaseModeOrchestrator';
export declare class MaintenanceModeOrchestrator extends BaseModeOrchestrator {
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
//# sourceMappingURL=MaintenanceModeOrchestrator.d.ts.map