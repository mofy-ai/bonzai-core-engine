/**
 * Deployment Mode Orchestrator
 *
 * 🚀 DEPLOYMENT MODE: Prepare stable code for production deployment
 * Mission: Polish for production - ensure release-ready quality and deployment preparation
 */
import { BaseModeOrchestrator, DevelopmentMode, IModeAgent, ISuccessCriteria } from './BaseModeOrchestrator';
export declare class DeploymentModeOrchestrator extends BaseModeOrchestrator {
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
//# sourceMappingURL=DeploymentModeOrchestrator.d.ts.map