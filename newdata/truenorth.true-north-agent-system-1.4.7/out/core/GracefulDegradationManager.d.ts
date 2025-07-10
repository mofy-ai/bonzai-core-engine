/**
 * Graceful Degradation Manager for TrueNorth Agent System
 * Handles fallback behaviors when non-critical features fail
 */
import { OutputManager } from '../output/OutputManager';
export declare enum FeatureType {
    DASHBOARD = "dashboard",
    AUTO_UPDATE = "auto_update",
    METRICS_TRACKING = "metrics_tracking",
    PROGRESS_REPORTING = "progress_reporting",
    SIDEBAR_PANEL = "sidebar_panel",
    STATUS_BAR = "status_bar",
    KEYBOARD_SHORTCUTS = "keyboard_shortcuts",
    FILE_LOGGING = "file_logging",
    PERFORMANCE_MONITORING = "performance_monitoring"
}
export interface IFeatureStatus {
    type: FeatureType;
    enabled: boolean;
    healthy: boolean;
    lastError?: string;
    lastErrorTime?: string;
    fallbackActive: boolean;
    fallbackDescription?: string;
    retryCount: number;
    maxRetries: number;
    nextRetryTime?: string;
}
export interface IFallbackStrategy {
    feature: FeatureType;
    priority: 'low' | 'medium' | 'high';
    fallbackAction: () => Promise<boolean>;
    description: string;
    requiresUserNotification: boolean;
    recoveryAction?: () => Promise<boolean>;
}
export declare class GracefulDegradationManager {
    private static instance;
    private outputManager;
    private errorHandler;
    private featureStatuses;
    private fallbackStrategies;
    private degradationMode;
    private notifiedFailures;
    private constructor();
    static getInstance(outputManager?: OutputManager): GracefulDegradationManager;
    /**
     * Initialize feature status tracking
     */
    private initializeFeatureStatuses;
    /**
     * Initialize fallback strategies for each feature
     */
    private initializeFallbackStrategies;
    /**
     * Handle feature failure and apply graceful degradation
     */
    handleFeatureFailure(feature: FeatureType, error: Error | string, context?: Record<string, unknown>): Promise<boolean>;
    /**
     * Apply fallback strategy for a feature
     */
    private applyFallback;
    /**
     * Show user notification for fallback activation
     */
    private showFallbackNotification;
    /**
     * Attempt to recover a failed feature
     */
    attemptFeatureRecovery(feature: FeatureType): Promise<boolean>;
    /**
     * Schedule retry for a failed feature
     */
    private scheduleRetry;
    /**
     * Update overall degradation mode status
     */
    private updateDegradationMode;
    /**
     * Get maximum retry attempts for a feature
     */
    private getMaxRetries;
    /**
     * Get display name for a feature
     */
    private getFeatureDisplayName;
    /**
     * Show comprehensive system status
     */
    showSystemStatus(): void;
    /**
     * Get current system health summary
     */
    getHealthSummary(): {
        degradationMode: boolean;
        healthyFeatures: number;
        totalFeatures: number;
        failedFeatures: FeatureType[];
        degradedFeatures: FeatureType[];
    };
    /**
     * Reset feature status (for testing or manual recovery)
     */
    resetFeatureStatus(feature: FeatureType): void;
    /**
     * Dispose and cleanup
     */
    dispose(): void;
}
//# sourceMappingURL=GracefulDegradationManager.d.ts.map