"use strict";
/**
 * Clean Project Analyzer - MVP Implementation
 * Focuses on core project analysis without over-engineering
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
exports.ProjectAnalyzer = void 0;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
// Constants for analysis thresholds and display
const analysisThresholds = {
    maxProgress: 95,
    progressIncrement: 5,
    lowComplexity: 30,
    mediumComplexity: 50,
    errorSeparatorLength: 50,
};
class ProjectAnalyzer {
    constructor(claudeCliManager, configManager) {
        this.claudeCliManager = claudeCliManager;
        this.configManager = configManager;
    }
    async analyzeProject() {
        return vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'TrueNorth Project Analysis',
            cancellable: true,
        }, async (progress, token) => {
            try {
                progress.report({ increment: 0, message: 'Initializing analysis...' });
                const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
                if (!workspaceFolder) {
                    throw new Error('No workspace folder found');
                }
                // Skip authentication checks - just proceed with analysis
                progress.report({ increment: 10, message: 'Starting project analysis...' });
                progress.report({ increment: 20, message: 'Scanning project structure...' });
                const projectInfo = await this.getProjectInfo(workspaceFolder.uri.fsPath);
                if (token.isCancellationRequested) {
                    return;
                }
                progress.report({ increment: 40, message: 'Running Claude analysis...' });
                // Set up progress reporting for long analysis
                let currentProgress = 40;
                const onProgress = (message) => {
                    if (currentProgress < analysisThresholds.maxProgress) {
                        currentProgress += analysisThresholds.progressIncrement;
                        progress.report({ increment: currentProgress, message: `Analysis: ${message}` });
                    }
                };
                // Use Claude CLI to analyze the project with extended timeout
                const analysis = await this.claudeCliManager.executeAnalysisCommand(`Perform a comprehensive analysis of this ${projectInfo.type} project. This analysis should include:
            - Detailed code architecture and structure evaluation
            - Potential improvements and optimization opportunities
            - Best practices compliance assessment
            - Code quality and maintainability review
            - Security considerations and recommendations
            - Performance optimization suggestions
            - Documentation and testing coverage analysis
            
            Project Details:
            - Files: ${projectInfo.files} files in ${projectInfo.directories} directories
            - Primary languages: ${projectInfo.languages.join(', ')}
            - Project type: ${projectInfo.type}
            
            Please provide detailed, actionable recommendations. This analysis may take 15-30 minutes to complete thoroughly.`, onProgress);
                if (token.isCancellationRequested) {
                    return;
                }
                progress.report({ increment: 100, message: 'Analysis complete!' });
                if (analysis && analysis.trim().length > 0) {
                    vscode.window.showInformationMessage('Project analysis completed successfully!');
                    // Show output in dedicated channel
                    const outputChannel = vscode.window.createOutputChannel('TrueNorth Analysis');
                    outputChannel.clear();
                    outputChannel.appendLine('='.repeat(analysisThresholds.mediumComplexity));
                    outputChannel.appendLine('TrueNorth Project Analysis Results');
                    outputChannel.appendLine('='.repeat(analysisThresholds.mediumComplexity));
                    outputChannel.appendLine(`Project: ${projectInfo.name}`);
                    outputChannel.appendLine(`Type: ${projectInfo.type}`);
                    outputChannel.appendLine(`Files: ${projectInfo.files}`);
                    outputChannel.appendLine(`Languages: ${projectInfo.languages.join(', ')}`);
                    outputChannel.appendLine('\nAnalysis Results:');
                    outputChannel.appendLine('-'.repeat(analysisThresholds.lowComplexity));
                    outputChannel.appendLine(analysis);
                    outputChannel.show();
                }
                else {
                    throw new Error('Analysis failed - no output received');
                }
            }
            catch (error) {
                const errorMessage = `Project analysis failed: ${error instanceof Error ? error.message : 'Unknown error'}`;
                vscode.window.showErrorMessage(errorMessage);
                // Log error details
                const outputChannel = vscode.window.createOutputChannel('TrueNorth Errors');
                outputChannel.clear();
                outputChannel.appendLine('='.repeat(analysisThresholds.errorSeparatorLength));
                outputChannel.appendLine('TrueNorth Analysis Error');
                outputChannel.appendLine('='.repeat(analysisThresholds.errorSeparatorLength));
                outputChannel.appendLine(errorMessage);
                outputChannel.appendLine('\nTroubleshooting:');
                outputChannel.appendLine('1. Ensure Claude CLI is installed: curl -sSL https://claude.ai/install | bash');
                outputChannel.appendLine('2. Test command: claude --dangerously-skip-permissions --model sonnet -p "test"');
                outputChannel.appendLine('3. Check authentication: claude auth login');
                outputChannel.show();
            }
        });
    }
    async getProjectInfo(projectPath) {
        const info = {
            name: path.basename(projectPath),
            type: 'unknown',
            files: 0,
            directories: 0,
            size: 0,
            languages: [],
        };
        // Detect project type
        if (fs.existsSync(path.join(projectPath, 'package.json'))) {
            info.type = 'Node.js/JavaScript';
            info.languages.push('JavaScript', 'TypeScript');
        }
        if (fs.existsSync(path.join(projectPath, 'Cargo.toml'))) {
            info.type = 'Rust';
            info.languages.push('Rust');
        }
        if (fs.existsSync(path.join(projectPath, 'go.mod'))) {
            info.type = 'Go';
            info.languages.push('Go');
        }
        if (fs.existsSync(path.join(projectPath, 'requirements.txt')) ||
            fs.existsSync(path.join(projectPath, 'pyproject.toml'))) {
            info.type = 'Python';
            info.languages.push('Python');
        }
        // Count files and directories
        await this.walkDirectory(projectPath, (filePath, stats) => {
            if (stats.isDirectory()) {
                info.directories++;
            }
            else {
                info.files++;
                info.size += stats.size;
                // Add language based on file extension
                const ext = path.extname(filePath);
                switch (ext) {
                    case '.ts':
                        if (!info.languages.includes('TypeScript')) {
                            info.languages.push('TypeScript');
                        }
                        break;
                    case '.js':
                        if (!info.languages.includes('JavaScript')) {
                            info.languages.push('JavaScript');
                        }
                        break;
                    case '.py':
                        if (!info.languages.includes('Python')) {
                            info.languages.push('Python');
                        }
                        break;
                    case '.rs':
                        if (!info.languages.includes('Rust')) {
                            info.languages.push('Rust');
                        }
                        break;
                    case '.go':
                        if (!info.languages.includes('Go')) {
                            info.languages.push('Go');
                        }
                        break;
                }
            }
        });
        return info;
    }
    async walkDirectory(dirPath, callback) {
        const items = fs.readdirSync(dirPath);
        for (const item of items) {
            // Skip common ignore patterns
            if (item.startsWith('.') ||
                item === 'node_modules' ||
                item === 'target' ||
                item === '__pycache__') {
                continue;
            }
            const fullPath = path.join(dirPath, item);
            const stats = fs.statSync(fullPath);
            callback(fullPath, stats);
            if (stats.isDirectory()) {
                await this.walkDirectory(fullPath, callback);
            }
        }
    }
    /**
     * Get project statistics
     */
    async getProjectStats() {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            return null;
        }
        return this.getProjectInfo(workspaceFolder.uri.fsPath);
    }
}
exports.ProjectAnalyzer = ProjectAnalyzer;
//# sourceMappingURL=ProjectAnalyzer.js.map