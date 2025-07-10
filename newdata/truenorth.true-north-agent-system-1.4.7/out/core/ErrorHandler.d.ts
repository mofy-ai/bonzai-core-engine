/**
 * Centralized Error Handler for TrueNorth Agent System
 * Provides comprehensive error handling, recovery mechanisms, and reporting
 */
import { OutputManager } from '../output/OutputManager';
export declare enum ErrorSeverity {
    LOW = "low",
    MEDIUM = "medium",
    HIGH = "high",
    CRITICAL = "critical"
}
export declare enum ErrorCategory {
    CLAUDE_CLI = "claude_cli",
    NETWORK = "network",
    FILESYSTEM = "filesystem",
    AUTHENTICATION = "authentication",
    VALIDATION = "validation",
    SYSTEM = "system",
    USER_INPUT = "user_input",
    AGENT = "agent"
}
export interface IErrorContext {
    component: string;
    operation: string;
    userId?: string;
    sessionId?: string;
    timestamp: string;
    stackTrace?: string;
    additionalData?: Record<string, unknown>;
}
export interface IRecoveryAction {
    type: 'retry' | 'fallback' | 'abort' | 'manual_intervention' | 'restart_service';
    description: string;
    maxAttempts?: number;
    retryDelay?: number;
    action?: () => Promise<void>;
}
export interface ITrueNorthError {
    id: string;
    message: string;
    originalError?: Error;
    severity: ErrorSeverity;
    category: ErrorCategory;
    context: IErrorContext;
    recoveryActions: IRecoveryAction[];
    isRecoverable: boolean;
    timestamp: string;
    resolved?: boolean;
    resolutionTime?: string;
}
export declare class ErrorHandler {
    private static instance;
    private outputManager;
    private errorHistory;
    private activeRecoveryAttempts;
    private maxHistorySize;
    private constructor();
    static getInstance(outputManager?: OutputManager): ErrorHandler;
    /**
     * Handle any error with comprehensive error processing
     */
    handleError(error: Error | string, category: ErrorCategory, severity: ErrorSeverity, context: Partial<IErrorContext>, recoveryActions?: IRecoveryAction[]): Promise<ITrueNorthError>;
    /**
     * Handle Claude CLI specific errors with specialized recovery
     */
    handleClaudeCliError(error: Error | string, operation: string, command?: string): Promise<ITrueNorthError>;
    /**
     * Handle network-related errors with connection recovery
     */
    handleNetworkError(error: Error | string, component: string, operation: string): Promise<ITrueNorthError>;
    /**
     * Attempt automatic error recovery
     */
    private attemptRecovery;
    /**
     * Show appropriate user notification based on error severity
     */
    private showUserNotification;
    /**
     * Get error statistics and summary
     */
    getErrorSummary(): {
        total: number;
        bySeverity: Record<ErrorSeverity, number>;
        byCategory: Record<ErrorCategory, number>;
        recent: ITrueNorthError[];
        unresolved: ITrueNorthError[];
    };
    /**
     * Generate detailed error report
     */
    generateErrorReport(): string;
    private generateErrorId;
    private extractErrorMessage;
    private logError;
    private getLogLevel;
    private addToHistory;
    private isAuthenticationError;
    private isNetworkError;
    private isTimeoutError;
    private isCLINotFoundError;
    private delay;
    /**
     * Clear error history
     */
    clearHistory(): void;
    /**
     * Get all unresolved errors
     */
    getUnresolvedErrors(): ITrueNorthError[];
    /**
     * Mark an error as resolved manually
     */
    markAsResolved(errorId: string): boolean;
    /**
     * Dispose and cleanup
     */
    dispose(): void;
}
//# sourceMappingURL=ErrorHandler.d.ts.map