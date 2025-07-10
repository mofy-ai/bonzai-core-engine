/**
 * OutputManager - Handles VS Code output panel for TrueNorth
 * Provides centralized logging and Claude CLI response display
 */
export interface IOutputMessage {
    type: 'info' | 'success' | 'warning' | 'error' | 'command' | 'response';
    message: string;
    timestamp?: Date;
    source?: string;
}
export declare class OutputManager {
    private outputChannel;
    private commandHistory;
    private readonly maxHistorySize;
    constructor();
    /**
     * Show the output panel
     */
    show(preserveFocus?: boolean): void;
    /**
     * Clear the output panel
     */
    clear(): void;
    /**
     * Log a message to the output panel
     */
    log(type: IOutputMessage['type'], message: string, source?: string): void;
    /**
     * Log a Claude CLI command execution
     */
    logCommand(command: string, args: string[]): void;
    /**
     * Log a Claude CLI response
     */
    logResponse(response: string, duration?: number): void;
    /**
     * Log an error with optional error object
     */
    logError(message: string, error?: Error): void;
    /**
     * Log command progress/status
     */
    logProgress(message: string): void;
    /**
     * Get command history
     */
    getCommandHistory(): string[];
    /**
     * Log a structured agent update
     */
    logAgentUpdate(agentName: string, status: string, message?: string): void;
    /**
     * Create a section separator in the output
     */
    logSeparator(title?: string): void;
    /**
     * Dispose resources
     */
    dispose(): void;
}
//# sourceMappingURL=OutputManager.d.ts.map