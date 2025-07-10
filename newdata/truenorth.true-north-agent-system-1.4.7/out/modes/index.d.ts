/**
 * Universal Development Modes System - Entry Point
 *
 * Exports all mode orchestrators and management classes
 */
export { DevelopmentMode, BaseModeOrchestrator } from './BaseModeOrchestrator';
export type { IModeAgent, ISuccessCriteria, IModeExecution, IModeTransition, } from './BaseModeOrchestrator';
export { ModeDetectionSystem } from './ModeDetectionSystem';
export type { IProjectAssessment, IModeRecommendation } from './ModeDetectionSystem';
export { ModeManager } from './ModeManager';
export type { IModeManagerState } from './ModeManager';
export { FoundationModeOrchestrator } from './FoundationModeOrchestrator';
export { BuildModeOrchestrator } from './BuildModeOrchestrator';
export { CompletionModeOrchestrator } from './CompletionModeOrchestrator';
export { CleanupModeOrchestrator } from './CleanupModeOrchestrator';
export { ValidationModeOrchestrator } from './ValidationModeOrchestrator';
export { DeploymentModeOrchestrator } from './DeploymentModeOrchestrator';
export { MaintenanceModeOrchestrator } from './MaintenanceModeOrchestrator';
export { EnhancementModeOrchestrator } from './EnhancementModeOrchestrator';
export declare const ModeInfo: {
    readonly foundation: {
        readonly icon: "🏗️";
        readonly name: "Foundation Mode";
        readonly description: "Get the basic development environment working from broken or new state";
        readonly color: "#8B4513";
    };
    readonly build: {
        readonly icon: "🔧";
        readonly name: "Build Mode";
        readonly description: "Rapidly create new features and functionality from scratch";
        readonly color: "#1E90FF";
    };
    readonly completion: {
        readonly icon: "🏁";
        readonly name: "Completion Mode";
        readonly description: "Complete existing partial implementations - finish what was started";
        readonly color: "#32CD32";
    };
    readonly cleanup: {
        readonly icon: "🧹";
        readonly name: "Cleanup Mode";
        readonly description: "Organize, optimize, and clean messy but functional code";
        readonly color: "#FFD700";
    };
    readonly validation: {
        readonly icon: "🧪";
        readonly name: "Validation Mode";
        readonly description: "Test and verify that everything works as expected";
        readonly color: "#9932CC";
    };
    readonly deployment: {
        readonly icon: "🚀";
        readonly name: "Deployment Mode";
        readonly description: "Get the application live in production successfully";
        readonly color: "#FF4500";
    };
    readonly maintenance: {
        readonly icon: "🔄";
        readonly name: "Maintenance Mode";
        readonly description: "Keep production application running smoothly and address issues";
        readonly color: "#708090";
    };
    readonly enhancement: {
        readonly icon: "🎨";
        readonly name: "Enhancement Mode";
        readonly description: "Add new features and capabilities to existing working system";
        readonly color: "#FF1493";
    };
};
//# sourceMappingURL=index.d.ts.map