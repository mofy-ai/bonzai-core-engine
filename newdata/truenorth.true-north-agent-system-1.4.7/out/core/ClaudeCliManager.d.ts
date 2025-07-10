/**
 * Enhanced Claude CLI Manager - Phase 1A Implementation
 * Executes Claude CLI commands with VS Code terminal integration
 */
import { OutputManager } from '../output/OutputManager';
export interface IClaudeCliResult {
    success: boolean;
    output: string;
    error?: string;
    duration: number;
    command: string;
}
export interface ICommandOptions {
    timeout?: number;
    commandType?: 'quick' | 'analysis' | 'agent' | 'extended';
    onProgress?: (message: string) => void;
    useStreamingOutput?: boolean;
    enableProgressReporting?: boolean;
    useTTY?: boolean;
}
export declare class ClaudeCliManager {
    private outputManager?;
    private claudePath?;
    private errorHandler;
    private readonly timeouts;
    constructor(outputManager?: OutputManager);
    /**
     * Detect Claude CLI path across different systems
     */
    private detectClaudePath;
    /**
     * Enhanced environment setup for Claude CLI
     */
    private getEnhancedEnvironment;
    /**
     * Execute command using VS Code terminal for better integration
     */
    private executeWithVSCodeTerminal;
    /**
     * Execute command using standard subprocess (fallback)
     */
    private executeWithSubprocess;
    /**
     * Execute command with comprehensive error handling and recovery
     */
    executeCommand(prompt: string, options?: ICommandOptions): Promise<string>;
    /**
     * Execute command using shell/terminal - matches user's working environment
     */
    private executeWithTerminal;
    /**
     * Properly escape strings for shell execution
     */
    private escapeShellString;
    /**
     * Clean and normalize output
     */
    private cleanOutput;
    /**
     * Execute command with result information
     */
    executeCommandWithResult(prompt: string, options?: ICommandOptions): Promise<IClaudeCliResult>;
    /**
     * Test if Claude CLI is available with enhanced feedback
     */
    testConnection(): Promise<boolean>;
    /**
     * Get the detected Claude CLI path
     */
    getClaudePath(): string;
    /**
     * Validate Claude CLI installation
     */
    validateInstallation(): Promise<{
        valid: boolean;
        version?: string;
        path: string;
        error?: string;
    }>;
    /**
     * Execute an analysis command with VS Code terminal and streaming
     */
    executeAnalysisCommand(prompt: string, onProgress?: (message: string) => void): Promise<string>;
    /**
     * Execute an agent command with extended timeout
     */
    executeAgentCommand(prompt: string, onProgress?: (message: string) => void): Promise<string>;
    /**
     * Execute an extended operation command with maximum timeout
     */
    executeExtendedCommand(prompt: string, onProgress?: (message: string) => void): Promise<string>;
    /**
     * Get maximum retry attempts based on command type
     */
    private getMaxRetries;
    /**
     * Check if error should not be retried
     */
    private shouldNotRetry;
    /**
     * Enhanced error handling for executeWithTerminal
     */
    private executeWithTerminalSafe;
    /**
     * Add delay utility method
     */
    private delay;
    /**
     * Enhanced connection test with detailed diagnostics
     */
    testConnectionDetailed(): Promise<{
        success: boolean;
        diagnostics: {
            claudePathExists: boolean;
            claudeExecutable: boolean;
            networkConnectivity: boolean;
            authentication: boolean;
            version?: string;
            error?: string;
        };
    }>;
    /**
     * Get comprehensive health status
     */
    getHealthStatus(): Promise<{
        healthy: boolean;
        claudeCliAvailable: boolean;
        lastSuccessfulCommand?: string;
        errorCount: number;
        uptime: number;
        performance: {
            averageResponseTime: number;
            successRate: number;
        };
    }>;
    /**
     * Cleanup method
     */
    dispose(): void;
}
//# sourceMappingURL=ClaudeCliManager.d.ts.map