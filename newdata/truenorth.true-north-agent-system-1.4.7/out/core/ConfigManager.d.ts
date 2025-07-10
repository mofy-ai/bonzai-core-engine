/**
 * Clean Config Manager - MVP Implementation
 * Focuses on core configuration without over-engineering
 */
import * as vscode from 'vscode';
export declare class ConfigManager {
    private context;
    private config;
    constructor(context: vscode.ExtensionContext);
    private loadDefaultConfig;
    getConfig(key: string): unknown;
    setConfig(key: string, value: unknown): Promise<void>;
    getAllConfig(): Record<string, unknown>;
    /**
     * Get workspace folder path
     */
    getWorkspacePath(): string | undefined;
    /**
     * Dispose resources
     */
    dispose(): void;
}
//# sourceMappingURL=ConfigManager.d.ts.map