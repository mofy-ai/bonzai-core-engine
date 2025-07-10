/**
 * Clean Project Analyzer - MVP Implementation
 * Focuses on core project analysis without over-engineering
 */
import { ClaudeCliManager } from './ClaudeCliManager';
import { ConfigManager } from './ConfigManager';
export interface IProjectInfo {
    name: string;
    type: string;
    files: number;
    directories: number;
    size: number;
    languages: string[];
}
export declare class ProjectAnalyzer {
    private claudeCliManager;
    private configManager;
    constructor(claudeCliManager: ClaudeCliManager, configManager: ConfigManager);
    analyzeProject(): Promise<void>;
    private getProjectInfo;
    private walkDirectory;
    /**
     * Get project statistics
     */
    getProjectStats(): Promise<IProjectInfo | null>;
}
//# sourceMappingURL=ProjectAnalyzer.d.ts.map