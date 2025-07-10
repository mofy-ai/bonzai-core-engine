"use strict";
/**
 * Centralized Error Handler for TrueNorth Agent System
 * Provides comprehensive error handling, recovery mechanisms, and reporting
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
exports.ErrorHandler = exports.ErrorCategory = exports.ErrorSeverity = void 0;
const vscode = __importStar(require("vscode"));
var ErrorSeverity;
(function (ErrorSeverity) {
    ErrorSeverity["LOW"] = "low";
    ErrorSeverity["MEDIUM"] = "medium";
    ErrorSeverity["HIGH"] = "high";
    ErrorSeverity["CRITICAL"] = "critical";
})(ErrorSeverity || (exports.ErrorSeverity = ErrorSeverity = {}));
var ErrorCategory;
(function (ErrorCategory) {
    ErrorCategory["CLAUDE_CLI"] = "claude_cli";
    ErrorCategory["NETWORK"] = "network";
    ErrorCategory["FILESYSTEM"] = "filesystem";
    ErrorCategory["AUTHENTICATION"] = "authentication";
    ErrorCategory["VALIDATION"] = "validation";
    ErrorCategory["SYSTEM"] = "system";
    ErrorCategory["USER_INPUT"] = "user_input";
    ErrorCategory["AGENT"] = "agent";
})(ErrorCategory || (exports.ErrorCategory = ErrorCategory = {}));
// Constants
const defaultMaxHistorySize = 100;
class ErrorHandler {
    constructor(outputManager) {
        this.errorHistory = [];
        this.activeRecoveryAttempts = new Map();
        this.maxHistorySize = defaultMaxHistorySize; // Configurable via constructor or config
        this.outputManager = outputManager;
    }
    static getInstance(outputManager) {
        if (!ErrorHandler.instance) {
            if (!outputManager) {
                throw new Error('OutputManager required for first initialization');
            }
            ErrorHandler.instance = new ErrorHandler(outputManager);
        }
        return ErrorHandler.instance;
    }
    /**
     * Handle any error with comprehensive error processing
     */
    async handleError(error, category, severity, context, recoveryActions = []) {
        const errorId = this.generateErrorId();
        const timestamp = new Date().toISOString();
        const originalError = error instanceof Error ? error : new Error(String(error));
        const message = this.extractErrorMessage(originalError);
        const trueNorthError = {
            id: errorId,
            message,
            originalError,
            severity,
            category,
            context: {
                component: context.component ?? 'unknown',
                operation: context.operation ?? 'unknown',
                timestamp,
                stackTrace: originalError.stack,
                ...context,
            },
            recoveryActions,
            isRecoverable: recoveryActions.length > 0,
            timestamp,
        };
        // Log the error
        this.logError(trueNorthError);
        // Add to history
        this.addToHistory(trueNorthError);
        // Attempt automatic recovery if possible
        if (trueNorthError.isRecoverable && severity !== ErrorSeverity.CRITICAL) {
            await this.attemptRecovery(trueNorthError);
        }
        // Show user notification based on severity
        this.showUserNotification(trueNorthError);
        return trueNorthError;
    }
    /**
     * Handle Claude CLI specific errors with specialized recovery
     */
    async handleClaudeCliError(error, operation, command) {
        const message = error instanceof Error ? error.message : String(error);
        // Analyze error type for specific recovery actions
        const recoveryActions = [];
        let severity = ErrorSeverity.MEDIUM;
        if (this.isAuthenticationError(message)) {
            severity = ErrorSeverity.HIGH;
            recoveryActions.push({
                type: 'manual_intervention',
                description: 'Claude CLI authentication required. Please run: claude auth login',
            });
        }
        else if (this.isNetworkError(message)) {
            severity = ErrorSeverity.MEDIUM;
            recoveryActions.push({
                type: 'retry',
                description: 'Retry operation with exponential backoff',
                maxAttempts: 3,
                retryDelay: 2000,
            }, {
                type: 'fallback',
                description: 'Switch to offline mode if available',
            });
        }
        else if (this.isTimeoutError(message)) {
            severity = ErrorSeverity.MEDIUM;
            recoveryActions.push({
                type: 'retry',
                description: 'Retry with increased timeout',
                maxAttempts: 2,
                retryDelay: 5000,
            });
        }
        else if (this.isCLINotFoundError(message)) {
            severity = ErrorSeverity.CRITICAL;
            recoveryActions.push({
                type: 'manual_intervention',
                description: 'Claude CLI not found. Please install Claude CLI: curl -sSL https://claude.ai/install | bash',
            });
        }
        return this.handleError(error, ErrorCategory.CLAUDE_CLI, severity, {
            component: 'ClaudeCliManager',
            operation,
            additionalData: { command },
        }, recoveryActions);
    }
    /**
     * Handle network-related errors with connection recovery
     */
    async handleNetworkError(error, component, operation) {
        const recoveryActions = [
            {
                type: 'retry',
                description: 'Retry with exponential backoff',
                maxAttempts: 5,
                retryDelay: 1000,
            },
            {
                type: 'fallback',
                description: 'Use cached data if available',
            },
            {
                type: 'manual_intervention',
                description: 'Check network connectivity and try again',
            },
        ];
        return this.handleError(error, ErrorCategory.NETWORK, ErrorSeverity.MEDIUM, { component, operation }, recoveryActions);
    }
    /**
     * Attempt automatic error recovery
     */
    async attemptRecovery(error) {
        const currentAttempts = this.activeRecoveryAttempts.get(error.id) ?? 0;
        for (const recoveryAction of error.recoveryActions) {
            if (recoveryAction.type === 'manual_intervention') {
                continue; // Skip manual interventions in automatic recovery
            }
            if (recoveryAction.maxAttempts && currentAttempts >= recoveryAction.maxAttempts) {
                continue; // Skip if max attempts reached
            }
            try {
                this.outputManager.log('info', `Attempting recovery: ${recoveryAction.description}`);
                // Apply retry delay if specified
                if (recoveryAction.retryDelay) {
                    await this.delay(recoveryAction.retryDelay * Math.pow(2, currentAttempts));
                }
                // Execute recovery action if provided
                if (recoveryAction.action) {
                    await recoveryAction.action();
                }
                // Mark as recovered
                error.resolved = true;
                error.resolutionTime = new Date().toISOString();
                this.outputManager.log('success', `Recovery successful for error: ${error.message}`);
                this.activeRecoveryAttempts.delete(error.id);
                return true;
            }
            catch (recoveryError) {
                this.activeRecoveryAttempts.set(error.id, currentAttempts + 1);
                this.outputManager.log('warning', `Recovery attempt failed: ${recoveryError instanceof Error ? recoveryError.message : String(recoveryError)}`);
            }
        }
        return false;
    }
    /**
     * Show appropriate user notification based on error severity
     */
    showUserNotification(error) {
        switch (error.severity) {
            case ErrorSeverity.CRITICAL:
                vscode.window
                    .showErrorMessage(`🚨 Critical Error: ${error.message}`, 'View Details', 'Restart Extension')
                    ?.then?.(selection => {
                    if (selection === 'View Details') {
                        this.outputManager?.show();
                    }
                    else if (selection === 'Restart Extension') {
                        vscode.commands.executeCommand('workbench.action.reloadWindow');
                    }
                });
                break;
            case ErrorSeverity.HIGH:
                vscode.window
                    .showErrorMessage(`❌ Error: ${error.message}`, 'View Details', 'Retry')
                    ?.then?.(selection => {
                    if (selection === 'View Details') {
                        this.outputManager?.show();
                    }
                    else if (selection === 'Retry') {
                        void this.attemptRecovery(error);
                    }
                });
                break;
            case ErrorSeverity.MEDIUM:
                vscode.window
                    .showWarningMessage(`⚠️ Warning: ${error.message}`, 'View Details')
                    ?.then?.(selection => {
                    if (selection === 'View Details') {
                        this.outputManager?.show();
                    }
                });
                break;
            case ErrorSeverity.LOW:
                // Log only for low severity errors
                break;
        }
    }
    /**
     * Get error statistics and summary
     */
    getErrorSummary() {
        const bySeverity = Object.values(ErrorSeverity).reduce((acc, severity) => {
            acc[severity] = this.errorHistory.filter(e => e.severity === severity).length;
            return acc;
        }, {});
        const byCategory = Object.values(ErrorCategory).reduce((acc, category) => {
            acc[category] = this.errorHistory.filter(e => e.category === category).length;
            return acc;
        }, {});
        const recentErrorsCount = 10;
        const recent = this.errorHistory.slice(-recentErrorsCount);
        const unresolved = this.errorHistory.filter(e => !e.resolved);
        return {
            total: this.errorHistory.length,
            bySeverity,
            byCategory,
            recent,
            unresolved,
        };
    }
    /**
     * Generate detailed error report
     */
    generateErrorReport() {
        const summary = this.getErrorSummary();
        const now = new Date().toISOString();
        let report = `# TrueNorth Error Report\n\n`;
        report += `Generated: ${now}\n\n`;
        report += `## Summary\n`;
        report += `- Total Errors: ${summary.total}\n`;
        report += `- Unresolved: ${summary.unresolved.length}\n\n`;
        report += `## By Severity\n`;
        Object.entries(summary.bySeverity).forEach(([severity, count]) => {
            report += `- ${severity}: ${count}\n`;
        });
        report += `\n## By Category\n`;
        Object.entries(summary.byCategory).forEach(([category, count]) => {
            report += `- ${category}: ${count}\n`;
        });
        report += `\n## Recent Errors\n`;
        summary.recent.forEach(error => {
            report += `### ${error.timestamp}\n`;
            report += `**Category:** ${error.category}\n`;
            report += `**Severity:** ${error.severity}\n`;
            report += `**Message:** ${error.message}\n`;
            report += `**Component:** ${error.context.component}\n`;
            report += `**Operation:** ${error.context.operation}\n`;
            report += `**Resolved:** ${error.resolved ? 'Yes' : 'No'}\n\n`;
        });
        return report;
    }
    // Helper methods
    generateErrorId() {
        const randomBase = 36;
        const randomStart = 2;
        const randomLength = 9;
        return `err_${Date.now()}_${Math.random().toString(randomBase).substr(randomStart, randomLength)}`;
    }
    extractErrorMessage(error) {
        let message = error.message;
        // Clean up common error message patterns
        message = message.replace(/^Error: /, '');
        message = message.replace(/\n[\s\S]*$/, ''); // Remove stack trace from message
        return message;
    }
    logError(error) {
        const logLevel = this.getLogLevel(error.severity);
        const logMessage = `[${error.category}] ${error.context.component}:${error.context.operation} - ${error.message}`;
        this.outputManager.log(logLevel, logMessage);
        if (error.severity === ErrorSeverity.CRITICAL || error.severity === ErrorSeverity.HIGH) {
            this.outputManager.logError(logMessage, error.originalError);
        }
    }
    getLogLevel(severity) {
        switch (severity) {
            case ErrorSeverity.LOW:
                return 'info';
            case ErrorSeverity.MEDIUM:
                return 'warning';
            case ErrorSeverity.HIGH:
            case ErrorSeverity.CRITICAL:
                return 'error';
            default:
                return 'warning';
        }
    }
    addToHistory(error) {
        this.errorHistory.push(error);
        // Maintain history size
        if (this.errorHistory.length > this.maxHistorySize) {
            this.errorHistory = this.errorHistory.slice(-this.maxHistorySize);
        }
    }
    isAuthenticationError(message) {
        const authPatterns = [
            /authentication/i,
            /unauthorized/i,
            /access.*denied/i,
            /invalid.*token/i,
            /login.*required/i,
            /credentials/i,
        ];
        return authPatterns.some(pattern => pattern.test(message));
    }
    isNetworkError(message) {
        const networkPatterns = [
            /network/i,
            /connection/i,
            /enotfound/i,
            /econnrefused/i,
            /timeout/i,
            /unreachable/i,
            /dns/i,
        ];
        return networkPatterns.some(pattern => pattern.test(message));
    }
    isTimeoutError(message) {
        const timeoutPatterns = [/timeout/i, /timed.*out/i, /request.*timeout/i, /operation.*timeout/i];
        return timeoutPatterns.some(pattern => pattern.test(message));
    }
    isCLINotFoundError(message) {
        const cliPatterns = [
            /command.*not.*found/i,
            /claude.*not.*found/i,
            /no.*such.*file/i,
            /enoent/i,
            /spawn.*enoent/i,
        ];
        return cliPatterns.some(pattern => pattern.test(message));
    }
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    /**
     * Clear error history
     */
    clearHistory() {
        this.errorHistory = [];
        this.activeRecoveryAttempts.clear();
        this.outputManager.log('info', 'Error history cleared');
    }
    /**
     * Get all unresolved errors
     */
    getUnresolvedErrors() {
        return this.errorHistory.filter(error => !error.resolved);
    }
    /**
     * Mark an error as resolved manually
     */
    markAsResolved(errorId) {
        const error = this.errorHistory.find(e => e.id === errorId);
        if (error) {
            error.resolved = true;
            error.resolutionTime = new Date().toISOString();
            this.outputManager.log('success', `Error ${errorId} marked as resolved`);
            return true;
        }
        return false;
    }
    /**
     * Dispose and cleanup
     */
    dispose() {
        this.errorHistory = [];
        this.activeRecoveryAttempts.clear();
    }
}
exports.ErrorHandler = ErrorHandler;
//# sourceMappingURL=ErrorHandler.js.map