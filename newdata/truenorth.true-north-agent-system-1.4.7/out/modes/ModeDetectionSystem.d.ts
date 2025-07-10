/**
 * Mode Detection System - Universal Development Modes
 *
 * Automatically detects current project state and recommends appropriate
 * development mode based on the Universal Development Modes framework.
 */
import { DevelopmentMode } from './BaseModeOrchestrator';
export interface IProjectAssessment {
    canRunDevServer: boolean;
    hasAllFeatures: boolean;
    featuresPartiallyComplete: boolean;
    codeIsClean: boolean;
    hasTestedThoroughly: boolean;
    isLiveInProduction: boolean;
    productionIsStable: boolean;
    needsNewFeatures: boolean;
}
export interface IModeRecommendation {
    recommendedMode: DevelopmentMode;
    confidence: number;
    reasoning: string[];
    assessment: IProjectAssessment;
    alternativeModes: DevelopmentMode[];
}
export declare class ModeDetectionSystem {
    private workspaceRoot;
    constructor();
    /**
     * Perform comprehensive project assessment
     */
    assessProject(): IProjectAssessment;
    /**
     * Get mode recommendation based on assessment
     */
    recommendMode(): IModeRecommendation;
    /**
     * Check if development server can start
     */
    private checkDevServerStatus;
    /**
     * Check for TypeScript/compilation errors
     */
    private checkCompilationErrors;
    /**
     * Check for other project types (Python, etc.)
     */
    private checkOtherProjectTypes;
    /**
     * Check if all required features exist
     */
    private checkFeatureCompleteness;
    /**
     * Check if features are partially complete
     */
    private checkPartialFeatures;
    /**
     * Check code quality and organization
     */
    private checkCodeQuality;
    /**
     * Check test coverage and validation
     */
    private checkTestCoverage;
    /**
     * Check if application is deployed to production
     */
    private checkProductionStatus;
    /**
     * Check production stability
     */
    private checkProductionStability;
    /**
     * Check if new features are needed
     */
    private checkFeatureRequests;
    private countTodoComments;
    private countIncompleteFeatures;
    private countDuplicateCode;
    private checkFileOrganization;
    private checkForProductionEnv;
    private countFeatureRequests;
    private findSourceFiles;
}
//# sourceMappingURL=ModeDetectionSystem.d.ts.map