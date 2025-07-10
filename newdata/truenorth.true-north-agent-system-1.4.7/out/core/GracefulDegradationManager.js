"use strict";
/**
 * Graceful Degradation Manager for TrueNorth Agent System
 * Handles fallback behaviors when non-critical features fail
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.GracefulDegradationManager = exports.FeatureType = void 0;
const vscode = __importStar(require("vscode"));
// Constants for timeouts and delays
const monitoringIntervalMs = 1000;
const systemRecoveryTimeoutMs = 60000;
const maxRetries = 3;
const ErrorHandler_1 = require("./ErrorHandler");
var FeatureType;
(function (FeatureType) {
    FeatureType["DASHBOARD"] = "dashboard";
    FeatureType["AUTO_UPDATE"] = "auto_update";
    FeatureType["METRICS_TRACKING"] = "metrics_tracking";
    FeatureType["PROGRESS_REPORTING"] = "progress_reporting";
    FeatureType["SIDEBAR_PANEL"] = "sidebar_panel";
    FeatureType["STATUS_BAR"] = "status_bar";
    FeatureType["KEYBOARD_SHORTCUTS"] = "keyboard_shortcuts";
    FeatureType["FILE_LOGGING"] = "file_logging";
    FeatureType["PERFORMANCE_MONITORING"] = "performance_monitoring";
})(FeatureType || (exports.FeatureType = FeatureType = {}));
class GracefulDegradationManager {
    constructor(outputManager) {
        this.featureStatuses = new Map();
        this.fallbackStrategies = new Map();
        this.degradationMode = false;
        this.notifiedFailures = new Set();
        this.outputManager = outputManager;
        this.errorHandler = ErrorHandler_1.ErrorHandler.getInstance(outputManager);
        this.initializeFeatureStatuses();
        this.initializeFallbackStrategies();
    }
    static getInstance(outputManager) {
        if (!GracefulDegradationManager.instance) {
            if (!outputManager) {
                throw new Error('OutputManager required for first initialization');
            }
            GracefulDegradationManager.instance = new GracefulDegradationManager(outputManager);
        }
        return GracefulDegradationManager.instance;
    }
    /**
     * Initialize feature status tracking
     */
    initializeFeatureStatuses() {
        const features = Object.values(FeatureType);
        features.forEach(feature => {
            this.featureStatuses.set(feature, {
                type: feature,
                enabled: true,
                healthy: true,
                fallbackActive: false,
                retryCount: 0,
                maxRetries: this.getMaxRetries(feature),
            });
        });
    }
    /**
     * Initialize fallback strategies for each feature
     */
    initializeFallbackStrategies() {
        // Dashboard fallback - use basic command palette
        this.fallbackStrategies.set(FeatureType.DASHBOARD, {
            feature: FeatureType.DASHBOARD,
            priority: 'medium',
            fallbackAction: async () => {
                const selection = await vscode.window.showInformationMessage('Dashboard unavailable. Use Command Palette (Ctrl+Shift+P) for TrueNorth commands.', 'Show Commands');
                if (selection === 'Show Commands') {
                    await vscode.commands.executeCommand('workbench.action.showCommands', 'TrueNorth');
                }
                return true;
            },
            description: 'Using command palette instead of dashboard',
            requiresUserNotification: true,
        });
        // Auto-update fallback - manual update notifications
        this.fallbackStrategies.set(FeatureType.AUTO_UPDATE, {
            feature: FeatureType.AUTO_UPDATE,
            priority: 'low',
            fallbackAction: () => {
                this.outputManager.log('info', 'Auto-update disabled. Check manually for updates periodically.');
                return Promise.resolve(true);
            },
            description: 'Manual update checking only',
            requiresUserNotification: false,
        });
        // Metrics tracking fallback - basic logging
        this.fallbackStrategies.set(FeatureType.METRICS_TRACKING, {
            feature: FeatureType.METRICS_TRACKING,
            priority: 'low',
            fallbackAction: () => {
                this.outputManager.log('info', 'Metrics tracking unavailable. Using basic operation logging.');
                return Promise.resolve(true);
            },
            description: 'Basic logging without detailed metrics',
            requiresUserNotification: false,
        });
        // Progress reporting fallback - simple status messages
        this.fallbackStrategies.set(FeatureType.PROGRESS_REPORTING, {
            feature: FeatureType.PROGRESS_REPORTING,
            priority: 'medium',
            fallbackAction: () => {
                this.outputManager.log('info', 'Progress reporting simplified due to technical issues.');
                return Promise.resolve(true);
            },
            description: 'Basic status messages instead of detailed progress',
            requiresUserNotification: false,
        });
        // Sidebar panel fallback - output panel
        this.fallbackStrategies.set(FeatureType.SIDEBAR_PANEL, {
            feature: FeatureType.SIDEBAR_PANEL,
            priority: 'high',
            fallbackAction: async () => {
                const selection = await vscode.window.showInformationMessage('Sidebar panel unavailable. View TrueNorth output in Output panel.', 'Show Output');
                if (selection === 'Show Output') {
                    this.outputManager.show();
                }
                return true;
            },
            description: 'Using output panel instead of sidebar',
            requiresUserNotification: true,
        });
        // Status bar fallback - output messages
        this.fallbackStrategies.set(FeatureType.STATUS_BAR, {
            feature: FeatureType.STATUS_BAR,
            priority: 'low',
            fallbackAction: () => {
                this.outputManager.log('info', 'Status bar unavailable. Check output panel for status updates.');
                return Promise.resolve(true);
            },
            description: 'Status updates via output panel',
            requiresUserNotification: false,
        });
        // Keyboard shortcuts fallback - command palette
        this.fallbackStrategies.set(FeatureType.KEYBOARD_SHORTCUTS, {
            feature: FeatureType.KEYBOARD_SHORTCUTS,
            priority: 'medium',
            fallbackAction: async () => {
                const selection = await vscode.window.showInformationMessage('Keyboard shortcuts unavailable. Use Command Palette for TrueNorth commands.', 'Show Commands');
                if (selection === 'Show Commands') {
                    await vscode.commands.executeCommand('workbench.action.showCommands', 'TrueNorth');
                }
                return true;
            },
            description: 'Command palette access only',
            requiresUserNotification: true,
        });
        // File logging fallback - console logging
        this.fallbackStrategies.set(FeatureType.FILE_LOGGING, {
            feature: FeatureType.FILE_LOGGING,
            priority: 'low',
            fallbackAction: () => {
                // File logging unavailable. Using console and output panel only.
                this.outputManager.log('warning', 'File logging disabled. Logs available in output panel only.');
                return Promise.resolve(true);
            },
            description: 'Console and output panel logging only',
            requiresUserNotification: false,
        });
        // Performance monitoring fallback - basic error tracking
        this.fallbackStrategies.set(FeatureType.PERFORMANCE_MONITORING, {
            feature: FeatureType.PERFORMANCE_MONITORING,
            priority: 'low',
            fallbackAction: () => {
                this.outputManager.log('info', 'Performance monitoring simplified.');
                return Promise.resolve(true);
            },
            description: 'Basic error tracking only',
            requiresUserNotification: false,
        });
    }
    /**
     * Handle feature failure and apply graceful degradation
     */
    async handleFeatureFailure(feature, error, context) {
        const status = this.featureStatuses.get(feature);
        if (!status) {
            this.outputManager.log('error', `Unknown feature type: ${feature}`);
            return false;
        }
        // Update feature status
        status.healthy = false;
        status.lastError = error instanceof Error ? error.message : String(error);
        status.lastErrorTime = new Date().toISOString();
        status.retryCount++;
        // Log the failure
        await this.errorHandler.handleError(error, ErrorHandler_1.ErrorCategory.SYSTEM, ErrorHandler_1.ErrorSeverity.MEDIUM, {
            component: 'GracefulDegradationManager',
            operation: 'handleFeatureFailure',
            additionalData: { feature, context },
        });
        // Apply fallback if available and not already active
        if (!status.fallbackActive) {
            const success = await this.applyFallback(feature);
            if (success) {
                status.fallbackActive = true;
                this.outputManager.log('info', `Fallback activated for ${feature}`);
            }
        }
        // Check if we should enter degradation mode
        this.updateDegradationMode();
        // Schedule retry if appropriate
        if (status.retryCount < status.maxRetries) {
            this.scheduleRetry(feature);
        }
        return status.fallbackActive;
    }
    /**
     * Apply fallback strategy for a feature
     */
    async applyFallback(feature) {
        const strategy = this.fallbackStrategies.get(feature);
        if (!strategy) {
            return false;
        }
        try {
            const success = await strategy.fallbackAction();
            if (success) {
                const status = this.featureStatuses.get(feature);
                if (status) {
                    status.fallbackDescription = strategy.description;
                }
                // Show user notification if required
                if (strategy.requiresUserNotification && !this.notifiedFailures.has(feature)) {
                    this.showFallbackNotification(feature, strategy);
                    this.notifiedFailures.add(feature);
                }
                this.outputManager.log('success', `Fallback applied for ${feature}: ${strategy.description}`);
                return true;
            }
        }
        catch (fallbackError) {
            this.outputManager.log('error', `Fallback failed for ${feature}: ${fallbackError instanceof Error ? fallbackError.message : String(fallbackError)}`);
        }
        return false;
    }
    /**
     * Show user notification for fallback activation
     */
    showFallbackNotification(feature, strategy) {
        const message = `${this.getFeatureDisplayName(feature)} is temporarily unavailable. ${strategy.description}`;
        switch (strategy.priority) {
            case 'high':
                vscode.window.showWarningMessage(message, 'View Details').then(selection => {
                    if (selection === 'View Details') {
                        this.outputManager.show();
                    }
                });
                break;
            case 'medium':
                vscode.window.showInformationMessage(message);
                break;
            case 'low':
                // No notification for low priority fallbacks
                break;
        }
    }
    /**
     * Attempt to recover a failed feature
     */
    async attemptFeatureRecovery(feature) {
        const status = this.featureStatuses.get(feature);
        const strategy = this.fallbackStrategies.get(feature);
        if (!status || !strategy) {
            return false;
        }
        // Try recovery action if available
        if (strategy.recoveryAction) {
            try {
                const recovered = await strategy.recoveryAction();
                if (recovered) {
                    status.healthy = true;
                    status.fallbackActive = false;
                    status.retryCount = 0;
                    status.lastError = undefined;
                    status.lastErrorTime = undefined;
                    status.nextRetryTime = undefined;
                    this.notifiedFailures.delete(feature);
                    this.updateDegradationMode();
                    this.outputManager.log('success', `Feature ${feature} recovered successfully`);
                    return true;
                }
            }
            catch (recoveryError) {
                this.outputManager.log('warning', `Recovery failed for ${feature}: ${recoveryError instanceof Error ? recoveryError.message : String(recoveryError)}`);
            }
        }
        return false;
    }
    /**
     * Schedule retry for a failed feature
     */
    scheduleRetry(feature) {
        const status = this.featureStatuses.get(feature);
        if (!status) {
            return;
        }
        const delay = Math.min(monitoringIntervalMs * Math.pow(2, status.retryCount), systemRecoveryTimeoutMs); // Max 1 minute
        const retryTime = new Date(Date.now() + delay);
        status.nextRetryTime = retryTime.toISOString();
        setTimeout(() => {
            if (status.retryCount < maxRetries && !status.healthy) {
                this.outputManager.log('info', `Attempting recovery for ${feature} (attempt ${status.retryCount + 1}/${maxRetries})`);
                void this.attemptFeatureRecovery(feature);
            }
        }, delay);
    }
    /**
     * Update overall degradation mode status
     */
    updateDegradationMode() {
        const criticalFeatures = [FeatureType.DASHBOARD, FeatureType.SIDEBAR_PANEL];
        const criticalFailures = criticalFeatures.filter(feature => {
            const status = this.featureStatuses.get(feature);
            return status && !status.healthy;
        });
        const wasInDegradationMode = this.degradationMode;
        this.degradationMode = criticalFailures.length > 0;
        if (this.degradationMode !== wasInDegradationMode) {
            if (this.degradationMode) {
                this.outputManager.log('warning', 'TrueNorth entered degradation mode due to critical feature failures');
                vscode.window
                    .showWarningMessage('TrueNorth is running in degradation mode. Some features may be limited.', 'View Status')
                    .then(selection => {
                    if (selection === 'View Status') {
                        this.showSystemStatus();
                    }
                });
            }
            else {
                this.outputManager.log('success', 'TrueNorth exited degradation mode - all critical features restored');
            }
        }
    }
    /**
     * Get maximum retry attempts for a feature
     */
    getMaxRetries(feature) {
        switch (feature) {
            case FeatureType.DASHBOARD:
            case FeatureType.SIDEBAR_PANEL:
                return maxRetries;
            case FeatureType.AUTO_UPDATE:
            case FeatureType.METRICS_TRACKING:
                return 1;
            default:
                return 2;
        }
    }
    /**
     * Get display name for a feature
     */
    getFeatureDisplayName(feature) {
        switch (feature) {
            case FeatureType.DASHBOARD:
                return 'Dashboard';
            case FeatureType.AUTO_UPDATE:
                return 'Auto-update';
            case FeatureType.METRICS_TRACKING:
                return 'Metrics tracking';
            case FeatureType.PROGRESS_REPORTING:
                return 'Progress reporting';
            case FeatureType.SIDEBAR_PANEL:
                return 'Sidebar panel';
            case FeatureType.STATUS_BAR:
                return 'Status bar';
            case FeatureType.KEYBOARD_SHORTCUTS:
                return 'Keyboard shortcuts';
            case FeatureType.FILE_LOGGING:
                return 'File logging';
            case FeatureType.PERFORMANCE_MONITORING:
                return 'Performance monitoring';
            default:
                return feature;
        }
    }
    /**
     * Show comprehensive system status
     */
    showSystemStatus() {
        const healthyFeatures = Array.from(this.featureStatuses.values()).filter(s => s.healthy).length;
        const totalFeatures = this.featureStatuses.size;
        const degradedFeatures = Array.from(this.featureStatuses.values()).filter(s => s.fallbackActive);
        let statusMessage = `TrueNorth System Status:\n`;
        statusMessage += `Mode: ${this.degradationMode ? 'Degraded' : 'Normal'}\n`;
        statusMessage += `Features: ${healthyFeatures}/${totalFeatures} healthy\n\n`;
        if (degradedFeatures.length > 0) {
            statusMessage += `Degraded Features:\n`;
            degradedFeatures.forEach(feature => {
                statusMessage += `• ${this.getFeatureDisplayName(feature.type)}: ${feature.fallbackDescription}\n`;
            });
        }
        this.outputManager.log('info', statusMessage);
        this.outputManager.show();
    }
    /**
     * Get current system health summary
     */
    getHealthSummary() {
        const failed = Array.from(this.featureStatuses.values())
            .filter(s => !s.healthy)
            .map(s => s.type);
        const degraded = Array.from(this.featureStatuses.values())
            .filter(s => s.fallbackActive)
            .map(s => s.type);
        const healthy = Array.from(this.featureStatuses.values()).filter(s => s.healthy).length;
        return {
            degradationMode: this.degradationMode,
            healthyFeatures: healthy,
            totalFeatures: this.featureStatuses.size,
            failedFeatures: failed,
            degradedFeatures: degraded,
        };
    }
    /**
     * Reset feature status (for testing or manual recovery)
     */
    resetFeatureStatus(feature) {
        const status = this.featureStatuses.get(feature);
        if (status) {
            status.healthy = true;
            status.fallbackActive = false;
            status.retryCount = 0;
            status.lastError = undefined;
            status.lastErrorTime = undefined;
            status.nextRetryTime = undefined;
            this.notifiedFailures.delete(feature);
            this.updateDegradationMode();
            this.outputManager.log('info', `Feature ${feature} status reset`);
        }
    }
    /**
     * Dispose and cleanup
     */
    dispose() {
        this.featureStatuses.clear();
        this.fallbackStrategies.clear();
        this.notifiedFailures.clear();
        this.degradationMode = false;
    }
}
exports.GracefulDegradationManager = GracefulDegradationManager;
//# sourceMappingURL=GracefulDegradationManager.js.map