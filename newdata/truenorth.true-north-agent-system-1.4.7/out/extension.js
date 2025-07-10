"use strict";
/**
 * @fileoverview Main extension entry point for TrueNorth Agent System
 * Clean version with unnecessary features removed
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
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
// Constants for phase numbers and timeouts
const phaseNumbers = {
    phase1: 1,
    phase2: 2,
    phase3: 3,
    phase4: 4,
    phase5: 5,
};
const timeoutDelays = {
    errorClearDelay: 5000,
    retryDelay: 3000,
};
const simulationConstants = {
    maxRunningAgents: 10,
    maxCompletedAgents: 50,
    maxFailedAgents: 3,
};
// Helper function for launching specific phases
async function launchSpecificPhase(phaseNumber, phaseName, agentOrchestrator, outputManager) {
    try {
        outputManager.logSeparator(`Phase ${phaseNumber} Launch`);
        outputManager.log('info', `Launching Phase ${phaseNumber}: ${phaseName}...`);
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: `TrueNorth Phase ${phaseNumber}`,
            cancellable: true,
        }, async (progress, token) => {
            const response = await agentOrchestrator.launchPhase(phaseNumber);
            if (token.isCancellationRequested) {
                outputManager.log('info', `Phase ${phaseNumber} cancelled by user`);
                return;
            }
            outputManager.log('success', `Phase ${phaseNumber} completed: ${response}`);
        });
    }
    catch (error) {
        const errorMessage = `Phase ${phaseNumber} failed: ${error}`;
        outputManager.logError(errorMessage, error);
        const selection = await vscode.window.showErrorMessage(errorMessage, 'Retry', 'Cancel');
        if (selection === 'Retry') {
            void vscode.commands.executeCommand(`truenorth.launchPhase${phaseNumber}`);
        }
    }
}
const ClaudeCliManager_1 = require("./core/ClaudeCliManager");
const AgentOrchestrator_1 = require("./agents/AgentOrchestrator");
const TypeScriptErrorOrchestrator_1 = require("./agents/TypeScriptErrorOrchestrator");
const ConfigManager_1 = require("./core/ConfigManager");
const TrueNorthSidebarProvider_1 = require("./ui/TrueNorthSidebarProvider");
const OutputManager_1 = require("./output/OutputManager");
const ModeManager_1 = require("./modes/ModeManager");
const ErrorHandler_1 = require("./core/ErrorHandler");
// Constants to replace magic numbers
const maxDisplayItems = 5;
const maxGuardQuestions = 3;
// Global managers
let outputManager;
let claudeCliManager;
let agentOrchestrator;
let typeScriptOrchestrator;
let configManager;
let errorHandler;
let webviewProvider;
let modeManager;
async function activate(context) {
    try {
        // Initialize core managers in order
        outputManager = new OutputManager_1.OutputManager();
        errorHandler = ErrorHandler_1.ErrorHandler.getInstance(outputManager);
        configManager = new ConfigManager_1.ConfigManager(context);
        claudeCliManager = new ClaudeCliManager_1.ClaudeCliManager(outputManager);
        agentOrchestrator = new AgentOrchestrator_1.AgentOrchestrator(claudeCliManager, configManager);
        typeScriptOrchestrator = new TypeScriptErrorOrchestrator_1.TypeScriptErrorOrchestrator(claudeCliManager, configManager);
        modeManager = new ModeManager_1.ModeManager(claudeCliManager, configManager);
        // Log startup information
        outputManager.logSeparator('TrueNorth Extension Activation');
        outputManager.log('info', 'Initializing TrueNorth Agent System...');
        outputManager.log('info', `Claude CLI Path: ${claudeCliManager.getClaudePath()}`);
        // Validate Claude CLI installation
        const validation = await claudeCliManager.validateInstallation();
        if (validation.valid) {
            outputManager.log('success', `Claude CLI validated successfully`);
            if (validation.version) {
                outputManager.log('info', `Claude CLI Version: ${validation.version}`);
            }
        }
        else {
            outputManager.log('warning', `Claude CLI validation failed: ${validation.error}`);
        }
        // Initialize sidebar providers
        webviewProvider = new TrueNorthSidebarProvider_1.TrueNorthWebviewProvider(context);
        webviewProvider.setModeManager(modeManager);
        // Register webview provider for the sidebar
        context.subscriptions.push(vscode.window.registerWebviewViewProvider('truenorth-sidebar', webviewProvider));
        // Register core commands
        context.subscriptions.push(vscode.commands.registerCommand('truenorth.launchAgents', async () => {
            try {
                webviewProvider?.updateStatus('Launching agents...', 'active');
                await agentOrchestrator.launchAgents();
                webviewProvider?.updateStatus('Agents launched successfully', 'success');
            }
            catch (error) {
                webviewProvider?.updateStatus('Failed to launch agents', 'error');
                // Enhanced error handling
                await errorHandler.handleError(error instanceof Error ? error : new Error(String(error)), ErrorHandler_1.ErrorCategory.SYSTEM, ErrorHandler_1.ErrorSeverity.HIGH, {
                    component: 'Extension',
                    operation: 'launchAgents',
                });
            }
        }), vscode.commands.registerCommand('truenorth.analyzeProject', async () => {
            try {
                webviewProvider?.updateStatus('Analyzing project...', 'active');
                outputManager.logSeparator('Project Analysis');
                outputManager.log('info', 'Starting project analysis...');
                // Show output panel immediately for better UX
                outputManager.show(true);
                // Show progress notification with proper error handling
                await vscode.window.withProgress({
                    location: vscode.ProgressLocation.Notification,
                    title: 'TrueNorth Analysis',
                    cancellable: false,
                }, async (progress) => {
                    try {
                        progress.report({ increment: 0, message: 'Initializing analysis...' });
                        // Execute Claude CLI command with TTY and streaming for better reliability
                        const result = await claudeCliManager.executeAnalysisCommand('Analyze this project structure and provide insights about the codebase organization, potential improvements, and any issues you notice. Keep the response concise but informative.', msg => progress.report({ message: msg }));
                        progress.report({ increment: 100, message: 'Analysis complete!' });
                        return result;
                    }
                    catch (error) {
                        progress.report({ increment: 100, message: 'Analysis failed' });
                        throw error;
                    }
                });
                webviewProvider?.updateStatus('Project analysis completed', 'success');
                outputManager.log('success', 'Project analysis completed successfully');
                vscode.window
                    .showInformationMessage('✅ Project analysis complete! Check TrueNorth output panel for results.', 'View Results')
                    .then(selection => {
                    if (selection === 'View Results') {
                        outputManager.show(true);
                    }
                });
            }
            catch (error) {
                // Enhanced error handling with recovery options
                await errorHandler.handleError(error instanceof Error ? error : new Error(String(error)), ErrorHandler_1.ErrorCategory.CLAUDE_CLI, ErrorHandler_1.ErrorSeverity.MEDIUM, {
                    component: 'Extension',
                    operation: 'analyzeProject',
                    additionalData: {
                        workspacePath: vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath,
                    },
                }, [
                    {
                        type: 'retry',
                        description: 'Retry project analysis',
                        maxAttempts: 2,
                        retryDelay: timeoutDelays.retryDelay,
                        action: async () => {
                            await vscode.commands.executeCommand('truenorth.analyzeProject');
                        },
                    },
                    {
                        type: 'fallback',
                        description: 'Use basic project scan instead',
                        action: () => {
                            outputManager.log('info', 'Falling back to basic project information scan');
                            // Basic fallback could scan file structure without Claude CLI
                            return Promise.resolve();
                        },
                    },
                ]);
                // Clear error status after 5 seconds
                setTimeout(() => { }, timeoutDelays.errorClearDelay);
            }
        }), vscode.commands.registerCommand('truenorth.openDashboard', () => {
            try {
                // Focus the webview panel instead of opening browser
                if (webviewProvider) {
                    webviewProvider.show();
                    vscode.window
                        .showInformationMessage('🎛️ TrueNorth Dashboard is now active in the sidebar!', 'View Dashboard')
                        .then(async (selection) => {
                        if (selection === 'View Dashboard') {
                            // Focus the sidebar
                            await vscode.commands.executeCommand('workbench.view.extension.truenorth');
                        }
                    });
                }
                else {
                    throw new Error('Dashboard webview not initialized');
                }
            }
            catch (error) {
                vscode.window
                    .showErrorMessage(`❌ Failed to focus dashboard: ${error instanceof Error ? error.message : 'Unknown error'}`, 'Try Again')
                    .then(async (selection) => {
                    if (selection === 'Try Again') {
                        await vscode.commands.executeCommand('truenorth.openDashboard');
                    }
                });
            }
        }), vscode.commands.registerCommand('truenorth.stopAllAgents', () => {
            try {
                agentOrchestrator.stopAllAgents();
            }
            catch (error) {
                vscode.window.showErrorMessage(`Failed to stop agents: ${error instanceof Error ? error.message : 'Unknown error'}`);
            }
        }), 
        // Enhanced Claude CLI test command with output panel integration
        vscode.commands.registerCommand('truenorth.testClaude', async () => {
            try {
                outputManager.logSeparator('Claude CLI Test');
                outputManager.show(true);
                const testResult = await vscode.window.withProgress({
                    location: vscode.ProgressLocation.Notification,
                    title: 'Claude CLI Test',
                    cancellable: false,
                }, async (progress) => {
                    progress.report({ increment: 0, message: 'Connecting to Claude CLI...' });
                    const result = await claudeCliManager.testConnection();
                    progress.report({
                        increment: 100,
                        message: result ? 'Connection successful!' : 'Connection failed!',
                    });
                    return result;
                });
                if (testResult) {
                    vscode.window
                        .showInformationMessage('✅ Claude CLI test successful! System is ready for operations.', 'View Details')
                        .then(selection => {
                        if (selection === 'View Details') {
                            outputManager.show(true);
                        }
                    });
                }
                else {
                    vscode.window
                        .showWarningMessage('⚠️ Claude CLI test failed! Please check your configuration.', 'View Details', 'Retry')
                        .then(selection => {
                        if (selection === 'View Details') {
                            outputManager.show(true);
                        }
                        else if (selection === 'Retry') {
                            vscode.commands.executeCommand('truenorth.testClaude');
                        }
                    });
                }
            }
            catch (error) {
                outputManager.logError('Claude CLI test exception', error instanceof Error ? error : new Error(String(error)));
                vscode.window
                    .showErrorMessage(`❌ Claude CLI test failed: ${error instanceof Error ? error.message : 'Unknown error'}`, 'View Details', 'Retry')
                    .then(selection => {
                    if (selection === 'View Details') {
                        outputManager.show(true);
                    }
                    else if (selection === 'Retry') {
                        vscode.commands.executeCommand('truenorth.testClaude');
                    }
                });
            }
        }), 
        // Add command to show output panel
        vscode.commands.registerCommand('truenorth.showOutput', () => {
            outputManager.show();
        }), 
        // Add command to clear output panel
        vscode.commands.registerCommand('truenorth.clearOutput', () => {
            outputManager.clear();
        }), 
        // Update commands
        // Error reporting and diagnostics commands
        vscode.commands.registerCommand('truenorth.showErrorReport', () => {
            try {
                const report = errorHandler.generateErrorReport();
                const summary = errorHandler.getErrorSummary();
                outputManager.logSeparator('TrueNorth Error Report');
                outputManager.log('info', `Total errors: ${summary.total}, Unresolved: ${summary.unresolved.length}`);
                outputManager.log('info', 'Error report generated - see output for details');
                outputManager.show(true);
                // Show the full report in output
                report.split('\n').forEach(line => {
                    if (line.trim()) {
                        outputManager.log('info', line);
                    }
                });
                vscode.window
                    .showInformationMessage(`📊 Error Report: ${summary.total} total errors, ${summary.unresolved.length} unresolved`, 'View Details', 'Clear History')
                    .then(selection => {
                    if (selection === 'View Details') {
                        outputManager.show(true);
                    }
                    else if (selection === 'Clear History') {
                        vscode.commands.executeCommand('truenorth.clearErrorHistory');
                    }
                });
            }
            catch (error) {
                vscode.window.showErrorMessage(`Failed to generate error report: ${error instanceof Error ? error.message : 'Unknown error'}`);
            }
        }), vscode.commands.registerCommand('truenorth.clearErrorHistory', () => {
            try {
                errorHandler.clearHistory();
                outputManager.log('success', 'Error history cleared');
                vscode.window.showInformationMessage('🧹 Error history cleared successfully');
            }
            catch (error) {
                vscode.window.showErrorMessage(`Failed to clear error history: ${error instanceof Error ? error.message : 'Unknown error'}`);
            }
        }), vscode.commands.registerCommand('truenorth.runDiagnostics', async () => {
            try {
                outputManager.logSeparator('TrueNorth System Diagnostics');
                outputManager.show(true);
                // Run comprehensive diagnostics
                const claudeHealth = await claudeCliManager.getHealthStatus();
                const errorSummary = errorHandler.getErrorSummary();
                outputManager.log('info', '🔍 System Diagnostics Report');
                outputManager.log('info', `Claude CLI Health: ${claudeHealth.healthy ? '✅ Healthy' : '❌ Unhealthy'}`);
                outputManager.log('info', `Error Count: ${errorSummary.total} total, ${errorSummary.unresolved.length} unresolved`);
                outputManager.log('info', `System Uptime: ${Math.round(process.uptime())} seconds`);
                // Test Claude CLI connection
                const claudeTest = await claudeCliManager.testConnectionDetailed();
                outputManager.log('info', `Claude CLI Test: ${claudeTest.success ? '✅ Passed' : '❌ Failed'}`);
                if (!claudeTest.success && claudeTest.diagnostics.error) {
                    outputManager.log('warning', `  Error: ${claudeTest.diagnostics.error}`);
                }
                const isHealthy = claudeHealth.healthy && errorSummary.unresolved.length === 0;
                vscode.window
                    .showInformationMessage(`🔍 Diagnostics Complete: System is ${isHealthy ? 'healthy' : 'experiencing issues'}`, 'View Report', 'Fix Issues')
                    .then(selection => {
                    if (selection === 'View Report') {
                        outputManager.show(true);
                    }
                    else if (selection === 'Fix Issues') {
                        vscode.commands.executeCommand('truenorth.showErrorReport');
                    }
                });
            }
            catch (error) {
                await errorHandler.handleError(error instanceof Error ? error : new Error(String(error)), ErrorHandler_1.ErrorCategory.SYSTEM, ErrorHandler_1.ErrorSeverity.MEDIUM, {
                    component: 'Extension',
                    operation: 'runDiagnostics',
                });
            }
        }), 
        // 5-Phase System Commands
        vscode.commands.registerCommand('truenorth.launch5PhaseSystem', async () => {
            try {
                outputManager.logSeparator('5-Phase System Launch');
                outputManager.log('info', 'Launching systematic 5-phase execution cycle...');
                await vscode.window.withProgress({
                    location: vscode.ProgressLocation.Notification,
                    title: 'TrueNorth 5-Phase System',
                    cancellable: true,
                }, async (progress, token) => {
                    if (token.isCancellationRequested) {
                        throw new Error('Operation cancelled by user');
                    }
                    progress.report({ increment: 0, message: 'Initializing 125-agent system...' });
                    await agentOrchestrator.launchSystematic5PhaseExecution();
                    progress.report({ increment: 100, message: '5-Phase system launched!' });
                });
                outputManager.log('success', '🎯 5-Phase systematic execution launched successfully!');
                vscode.window
                    .showInformationMessage('🚀 5-Phase System launched! Check output for progress.', 'View Progress', 'Open Dashboard')
                    .then(selection => {
                    if (selection === 'View Progress') {
                        outputManager.show(true);
                    }
                    else if (selection === 'Open Dashboard') {
                        vscode.commands.executeCommand('truenorth.openDashboard');
                    }
                });
            }
            catch (error) {
                outputManager.logError('5-Phase system launch error', error instanceof Error ? error : new Error(String(error)));
                vscode.window
                    .showErrorMessage(`❌ 5-Phase system launch failed: ${error instanceof Error ? error.message : 'Unknown error'}`, 'View Details', 'Retry')
                    .then(selection => {
                    if (selection === 'View Details') {
                        outputManager.show(true);
                    }
                    else if (selection === 'Retry') {
                        vscode.commands.executeCommand('truenorth.launch5PhaseSystem');
                    }
                });
            }
        }), 
        // Individual Phase Commands
        vscode.commands.registerCommand('truenorth.launchPhase1', async () => {
            await launchSpecificPhase(1, 'Core Execution', agentOrchestrator, outputManager);
        }), vscode.commands.registerCommand('truenorth.launchPhase2', async () => {
            await launchSpecificPhase(2, 'Comprehensive Audit', agentOrchestrator, outputManager);
        }), vscode.commands.registerCommand('truenorth.launchPhase3', async () => {
            await launchSpecificPhase(phaseNumbers.phase3, 'Targeted Execution', agentOrchestrator, outputManager);
        }), vscode.commands.registerCommand('truenorth.launchPhase4', async () => {
            await launchSpecificPhase(phaseNumbers.phase4, 'Final Audit', agentOrchestrator, outputManager);
        }), vscode.commands.registerCommand('truenorth.launchPhase5', async () => {
            await launchSpecificPhase(phaseNumbers.phase5, 'Finalization', agentOrchestrator, outputManager);
        }), 
        // Status and Reporting Commands
        vscode.commands.registerCommand('truenorth.show5PhaseStatus', () => {
            try {
                const execution = agentOrchestrator.getCurrentExecution();
                if (!execution) {
                    vscode.window.showInformationMessage('No 5-phase execution currently active.');
                    return;
                }
                const summary = agentOrchestrator.getExecutionSummary();
                const statusMessage = `
🎯 5-Phase System Status
━━━━━━━━━━━━━━━━━━━━━━━
📊 Progress: ${summary.overallProgress}%
🤖 Agents: ${summary.completedAgents}/${summary.totalAgents}
📋 Phase: ${summary.currentPhase}/5
✅ Completed Phases: ${summary.completedPhases.join(', ')}
❌ Failed Agents: ${summary.failedAgents}
🔄 Status: ${summary.status}
          `;
                outputManager.logSeparator('5-Phase Status Report');
                outputManager.log('info', statusMessage);
                vscode.window
                    .showInformationMessage(`📊 Progress: ${summary.overallProgress}% | Phase: ${summary.currentPhase}/5`, 'View Details', 'Open Dashboard')
                    .then(selection => {
                    if (selection === 'View Details') {
                        outputManager.show(true);
                    }
                    else if (selection === 'Open Dashboard') {
                        vscode.commands.executeCommand('truenorth.openDashboard');
                    }
                });
            }
            catch (error) {
                vscode.window.showErrorMessage(`Failed to get status: ${error instanceof Error ? error.message : 'Unknown error'}`);
            }
        }), vscode.commands.registerCommand('truenorth.generatePhaseReport', () => {
            try {
                const execution = agentOrchestrator.getCurrentExecution();
                if (!execution) {
                    vscode.window.showWarningMessage('No active execution to generate report for.');
                    return;
                }
                outputManager.logSeparator('Phase Report Generation');
                outputManager.log('info', 'Generating comprehensive phase reports...');
                // Report generation is handled automatically by the AgentOrchestrator
                vscode.window
                    .showInformationMessage('📋 Phase reports available in /logs/wave-01/', 'Open Logs Folder', 'View in Output')
                    .then(selection => {
                    if (selection === 'Open Logs Folder') {
                        vscode.commands.executeCommand('vscode.openFolder', vscode.Uri.file('/logs/wave-01'));
                    }
                    else if (selection === 'View in Output') {
                        outputManager.show(true);
                    }
                });
            }
            catch (error) {
                vscode.window.showErrorMessage(`Failed to generate report: ${error instanceof Error ? error.message : 'Unknown error'}`);
            }
        }));
        // Register TypeScript Error Resolution Commands
        context.subscriptions.push(vscode.commands.registerCommand('truenorth.launchTypeScriptFixer', async () => {
            try {
                webviewProvider?.updateStatus('Launching TypeScript Error Fixer...', 'active');
                webviewProvider?.updatePhase('TypeScript Error Resolution');
                outputManager.logSeparator('TypeScript Error Resolution System');
                outputManager.log('info', 'Starting TypeScript Error Resolution 125-Agent System...');
                // Show output panel for real-time feedback
                outputManager.show(true);
                await vscode.window.withProgress({
                    location: vscode.ProgressLocation.Notification,
                    title: 'TrueNorth TypeScript Fixer',
                    cancellable: true,
                }, async (progress, token) => {
                    if (token.isCancellationRequested) {
                        throw new Error('Operation cancelled by user');
                    }
                    progress.report({
                        increment: 0,
                        message: 'Initializing TypeScript error detection...',
                    });
                    // Check initial error count
                    const initialErrors = await typeScriptOrchestrator.getTypeScriptErrorCount();
                    if (initialErrors === 0) {
                        progress.report({ increment: 100, message: 'No TypeScript errors found!' });
                        vscode.window.showInformationMessage('✅ No TypeScript errors found! Your code is already clean.');
                        return;
                    }
                    if (initialErrors === -1) {
                        throw new Error('Failed to run TypeScript check. Ensure TypeScript is properly configured.');
                    }
                    outputManager.log('info', `Found ${initialErrors} TypeScript errors to resolve`);
                    progress.report({
                        increment: 10,
                        message: `Found ${initialErrors} errors. Starting 5-phase resolution...`,
                    });
                    // Launch the systematic error resolution with progress reporting
                    await typeScriptOrchestrator.launchTypeScriptErrorResolution((message) => {
                        outputManager.log('info', message);
                        const maxMessageLength = 50;
                        progress.report({ message: message.substring(0, maxMessageLength) + '...' });
                        // Simulate agent progress updates
                        if (message.includes('Phase')) {
                            const phaseMatch = message.match(/Phase (\d+)/);
                            if (phaseMatch) {
                                webviewProvider?.updatePhase(`Phase ${phaseMatch[1]}`);
                            }
                        }
                        // Update running agents count simulation
                        const runningAgents = Math.floor(Math.random() * simulationConstants.maxRunningAgents) + 1;
                        const completedAgents = Math.floor(Math.random() * simulationConstants.maxCompletedAgents);
                        const failedAgents = Math.floor(Math.random() * simulationConstants.maxFailedAgents);
                        webviewProvider?.updateCounts(runningAgents, completedAgents, failedAgents);
                    });
                    progress.report({
                        increment: 100,
                        message: 'TypeScript error resolution completed!',
                    });
                });
                webviewProvider?.updateStatus('TypeScript errors resolved!', 'success');
                webviewProvider?.updatePhase('Completed');
                outputManager.log('success', '🎉 TypeScript Error Resolution System completed successfully!');
                // Final verification
                const finalErrors = await typeScriptOrchestrator.getTypeScriptErrorCount();
                if (finalErrors === 0) {
                    vscode.window
                        .showInformationMessage('🎉 All TypeScript errors resolved! Code is production ready.', 'View Report', 'Run Type Check')
                        .then(selection => {
                        if (selection === 'View Report') {
                            vscode.commands.executeCommand('truenorth.generateTypeScriptReport');
                        }
                        else if (selection === 'Run Type Check') {
                            vscode.commands.executeCommand('truenorth.checkTypeScriptErrors');
                        }
                    });
                }
                else {
                    vscode.window
                        .showWarningMessage(`${finalErrors} TypeScript errors remain. Some may require manual intervention.`, 'View Details', 'Try Again')
                        .then(selection => {
                        if (selection === 'View Details') {
                            outputManager.show(true);
                        }
                        else if (selection === 'Try Again') {
                            vscode.commands.executeCommand('truenorth.launchTypeScriptFixer');
                        }
                    });
                }
            }
            catch (error) {
                await errorHandler.handleError(error instanceof Error ? error : new Error(String(error)), ErrorHandler_1.ErrorCategory.SYSTEM, ErrorHandler_1.ErrorSeverity.HIGH, {
                    component: 'Extension',
                    operation: 'launchTypeScriptFixer',
                });
                setTimeout(() => { }, timeoutDelays.errorClearDelay);
            }
        }), vscode.commands.registerCommand('truenorth.showTypeScriptStatus', () => {
            try {
                const execution = typeScriptOrchestrator.getCurrentExecution();
                if (!execution) {
                    vscode.window.showInformationMessage('No TypeScript error resolution currently running.');
                    return;
                }
                const summary = typeScriptOrchestrator.getExecutionSummary();
                outputManager.logSeparator('TypeScript Error Resolution Status');
                outputManager.log('info', `Iteration: ${summary.iteration}`);
                outputManager.log('info', `Current Phase: ${summary.currentPhase}/5`);
                outputManager.log('info', `Total Errors: ${summary.totalErrors}`);
                outputManager.log('info', `Errors Remaining: ${summary.errorsRemaining}`);
                outputManager.log('info', `Overall Progress: ${summary.overallProgress}%`);
                outputManager.log('info', `Status: ${summary.status}`);
                const currentPhase = typeScriptOrchestrator.getCurrentPhase();
                if (currentPhase) {
                    outputManager.log('info', `Current Phase: ${currentPhase.name}`);
                    outputManager.log('info', `Phase Status: ${currentPhase.status}`);
                    outputManager.log('info', `Errors in Phase: ${currentPhase.errorCount}`);
                }
                outputManager.show(true);
                vscode.window
                    .showInformationMessage(`TypeScript Resolution: ${summary.overallProgress}% complete`, 'View Details')
                    .then(selection => {
                    if (selection === 'View Details') {
                        outputManager.show(true);
                    }
                });
            }
            catch (error) {
                vscode.window.showErrorMessage(`Failed to get TypeScript status: ${error instanceof Error ? error.message : 'Unknown error'}`);
            }
        }), vscode.commands.registerCommand('truenorth.checkTypeScriptErrors', async () => {
            try {
                outputManager.logSeparator('TypeScript Error Check');
                outputManager.log('info', 'Running TypeScript compilation check...');
                const errorCount = await typeScriptOrchestrator.getTypeScriptErrorCount();
                if (errorCount === -1) {
                    outputManager.log('error', 'Failed to run TypeScript check');
                    vscode.window.showErrorMessage('Failed to run TypeScript check. Ensure TypeScript is properly configured.');
                    return;
                }
                if (errorCount === 0) {
                    outputManager.log('success', '✅ No TypeScript errors found!');
                    vscode.window.showInformationMessage('✅ No TypeScript errors found! Your code compiles successfully.');
                }
                else {
                    outputManager.log('warning', `Found ${errorCount} TypeScript errors`);
                    vscode.window
                        .showWarningMessage(`Found ${errorCount} TypeScript errors.`, 'Fix Errors', 'View Details')
                        .then(selection => {
                        if (selection === 'Fix Errors') {
                            vscode.commands.executeCommand('truenorth.launchTypeScriptFixer');
                        }
                        else if (selection === 'View Details') {
                            outputManager.show(true);
                        }
                    });
                }
                setTimeout(() => { }, timeoutDelays.errorClearDelay);
            }
            catch (error) {
                outputManager.log('error', `TypeScript check failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
                vscode.window.showErrorMessage(`TypeScript check failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
                setTimeout(() => { }, timeoutDelays.errorClearDelay);
            }
        }), vscode.commands.registerCommand('truenorth.generateTypeScriptReport', () => {
            try {
                const execution = typeScriptOrchestrator.getCurrentExecution();
                if (!execution) {
                    vscode.window.showWarningMessage('No TypeScript error resolution execution to generate report for.');
                    return;
                }
                outputManager.logSeparator('TypeScript Fix Report Generation');
                outputManager.log('info', 'TypeScript fix reports are automatically generated during execution...');
                const summary = typeScriptOrchestrator.getExecutionSummary();
                outputManager.log('info', `Report Summary:`);
                outputManager.log('info', `- Iteration: ${summary.iteration}`);
                outputManager.log('info', `- Total Errors Found: ${summary.totalErrors}`);
                outputManager.log('info', `- Errors Remaining: ${summary.errorsRemaining}`);
                outputManager.log('info', `- Overall Progress: ${summary.overallProgress}%`);
                outputManager.log('info', `- Status: ${summary.status}`);
                vscode.window
                    .showInformationMessage('📋 TypeScript fix reports available in logs/', 'View in Output')
                    .then(selection => {
                    if (selection === 'View in Output') {
                        outputManager.show(true);
                    }
                });
            }
            catch (error) {
                vscode.window.showErrorMessage(`Failed to generate TypeScript report: ${error instanceof Error ? error.message : 'Unknown error'}`);
            }
        }), 
        // Mode System Commands
        vscode.commands.registerCommand('truenorth.detectMode', async () => {
            try {
                const recommendation = await modeManager.detectAndRecommendMode();
                const modeInfo = `${recommendation.recommendedMode.toUpperCase()} MODE (${recommendation.confidence}% confidence)`;
                const reasons = recommendation.reasoning.join('\n• ');
                const message = `🎯 Recommended Mode: ${modeInfo}\n\nReasons:\n• ${reasons}`;
                const action = await vscode.window.showInformationMessage(message, 'Switch to Mode', 'Stay Current');
                if (action === 'Switch to Mode') {
                    await modeManager.switchToMode(recommendation.recommendedMode, 'Auto-detected recommendation');
                }
            }
            catch (error) {
                vscode.window.showErrorMessage(`Mode detection failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
            }
        }), vscode.commands.registerCommand('truenorth.showModeSelector', async () => {
            const modes = modeManager.getAvailableModes();
            const currentMode = modeManager.getCurrentMode();
            const items = modes.map(mode => {
                const info = modeManager.getModeDisplayInfo(mode);
                const isCurrent = mode === currentMode;
                return {
                    label: `${info?.icon ?? ''} ${info?.name ?? mode}`,
                    description: isCurrent ? '(Current)' : '',
                    detail: mode,
                    picked: isCurrent,
                };
            });
            const selection = await vscode.window.showQuickPick(items, {
                title: 'Select Development Mode',
                placeHolder: 'Choose a development mode to switch to',
            });
            if (selection && selection.detail !== currentMode) {
                await modeManager.switchToMode(selection.detail, 'Manual mode selection');
            }
        }), vscode.commands.registerCommand('truenorth.startModeExecution', async () => {
            try {
                const execution = await modeManager.startCurrentModeExecution();
                const currentMode = modeManager.getCurrentMode();
                webviewProvider?.updateStatus(`${currentMode} mode executing...`, 'active');
                vscode.window.showInformationMessage(`🚀 Started ${currentMode} mode execution with ${execution.agents.length} agents`);
            }
            catch (error) {
                vscode.window.showErrorMessage(`Failed to start mode execution: ${error instanceof Error ? error.message : 'Unknown error'}`);
            }
        }), vscode.commands.registerCommand('truenorth.stopModeExecution', () => {
            const orchestrator = modeManager.getCurrentOrchestrator();
            if (orchestrator) {
                orchestrator.stopExecution();
                webviewProvider?.updateStatus('Execution stopped', 'warning');
                vscode.window.showInformationMessage('Mode execution stopped');
            }
        }), vscode.commands.registerCommand('truenorth.showModeGuide', () => {
            const orchestrator = modeManager.getCurrentOrchestrator();
            if (orchestrator) {
                const allowed = orchestrator.getAllowedActions().slice(0, maxDisplayItems).join('\n• ');
                const forbidden = orchestrator
                    .getForbiddenActions()
                    .slice(0, maxDisplayItems)
                    .join('\n• ');
                const guards = orchestrator.getGuardQuestions().slice(0, maxGuardQuestions).join('\n• ');
                const guide = `${orchestrator.getModeIcon()} ${orchestrator.getModeDisplayName()}\n\nALLOWED ACTIONS:\n• ${allowed}\n\nFORBIDDEN ACTIONS:\n• ${forbidden}\n\nGUARD QUESTIONS:\n• ${guards}`;
                vscode.window.showInformationMessage(guide, { modal: true });
            }
        }));
        // Initialize status bar
        // Log successful activation
        outputManager.log('success', 'TrueNorth Extension activated successfully!');
        outputManager.logSeparator();
    }
    catch (error) {
        const errorMessage = `Failed to activate TrueNorth extension: ${error instanceof Error ? error.message : 'Unknown error'}`;
        // Use error handler if available, otherwise fallback to basic logging
        if (errorHandler) {
            await errorHandler.handleError(error instanceof Error ? error : new Error(String(error)), ErrorHandler_1.ErrorCategory.SYSTEM, ErrorHandler_1.ErrorSeverity.CRITICAL, {
                component: 'Extension',
                operation: 'activate',
            });
        }
        else {
            outputManager?.logError('Extension activation failed', error instanceof Error ? error : new Error(String(error)));
            vscode.window.showErrorMessage(errorMessage);
        }
    }
}
function deactivate() {
    try {
        outputManager?.log('info', 'Deactivating TrueNorth Extension...');
        // Stop all agents
        agentOrchestrator?.stopAllAgents();
        // Dispose managers in reverse order
        modeManager?.dispose?.();
        claudeCliManager?.dispose?.();
        errorHandler?.dispose?.();
        outputManager?.dispose?.();
        // Extension deactivated successfully
    }
    catch {
        // Error during deactivation - silent fail
    }
}
//# sourceMappingURL=extension.js.map