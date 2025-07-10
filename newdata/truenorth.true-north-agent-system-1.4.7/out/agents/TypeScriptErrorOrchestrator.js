"use strict";
/**
 * TypeScript Error Resolution Agent System
 * Specialized 125-Agent System for TypeScript Error Resolution
 * 5-Phase Loop: Execute→Audit→Execute→Audit→Finalize until ALL errors resolved
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
exports.TypeScriptErrorOrchestrator = void 0;
const ErrorHandler_1 = require("../core/ErrorHandler");
const constants_1 = require("../constants");
const fs = __importStar(require("fs"));
const os = __importStar(require("os"));
const path = __importStar(require("path"));
const vscode = __importStar(require("vscode"));
const child_process_1 = require("child_process");
const util_1 = require("util");
const execAsync = (0, util_1.promisify)(child_process_1.exec);
// TypeScript-specific phase constants
const totalPhases = 5;
const phaseNumbers = {
    ERROR_DETECTION: 3,
    FIX_VALIDATION: 4,
    COMPLETION_VERIFICATION: 5,
};
const phase1Start = 1;
const phase1End = 25;
const phase2Start = 26;
const phase2End = 50;
const phase3Start = 51;
const phase3End = 75;
const phase4Start = 76;
const phase4End = 100;
const phase5Start = 101;
const phase5End = 125;
const agentNamePadding = 3;
const fullProgress = 100;
const firstPhase = 1;
const secondPhase = 2;
const thirdPhase = 3;
const fourthPhase = 4;
const fifthPhase = 5;
const defaultProgress = 0;
const progressStepSize = 5;
const maxSafeProgress = 95;
const phase1ArrayOffset = 1;
const cleanOutputSubstringLength = 500;
const percentageMultiplier = 100;
const timeoutDelayMs = 1000;
const maxIterations = 10; // Prevent infinite loops
class TypeScriptErrorOrchestrator {
    constructor(claudeCliManager, configManager) {
        this.claudeCliManager = claudeCliManager;
        this.configManager = configManager;
        this.maxParallelAgents = constants_1.timeConstants.MAX_PARALLEL_AGENTS;
        this.waveNumber = '01';
        this.errorHandler = ErrorHandler_1.ErrorHandler.getInstance();
        this.workspacePath = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath ?? process.cwd();
        this.logBasePath = path.join(this.workspacePath, 'logs', 'typescript-fixes', `wave-${this.waveNumber}`);
        this.ensureLogDirectories();
    }
    ensureLogDirectories() {
        const directories = [
            'phase1-error-detection',
            'phase2-error-analysis',
            'phase3-error-fixes',
            'phase4-fix-validation',
            'phase5-completion',
        ];
        try {
            if (!fs.existsSync(this.logBasePath)) {
                fs.mkdirSync(this.logBasePath, { recursive: true });
            }
            directories.forEach(dir => {
                const dirPath = path.join(this.logBasePath, dir);
                if (!fs.existsSync(dirPath)) {
                    fs.mkdirSync(dirPath, { recursive: true });
                }
            });
        }
        catch (error) {
            void this.errorHandler.handleError(new Error(`Failed to create TypeScript log directories: ${error}`), ErrorHandler_1.ErrorCategory.FILESYSTEM, ErrorHandler_1.ErrorSeverity.HIGH, {
                component: 'TypeScriptErrorOrchestrator',
                operation: 'ensureLogDirectories',
                timestamp: new Date().toISOString(),
            });
            // Fallback to temp directory
            const tempDir = path.join(os.tmpdir(), 'truenorth-typescript-logs', `wave-${this.waveNumber}`);
            this.logBasePath = tempDir;
            try {
                if (!fs.existsSync(this.logBasePath)) {
                    fs.mkdirSync(this.logBasePath, { recursive: true });
                }
                directories.forEach(dir => {
                    const dirPath = path.join(this.logBasePath, dir);
                    if (!fs.existsSync(dirPath)) {
                        fs.mkdirSync(dirPath, { recursive: true });
                    }
                });
            }
            catch {
                this.logBasePath = '';
            }
        }
    }
    /**
     * Launch the TypeScript Error Resolution System
     * Continues looping until ALL TypeScript errors are resolved
     */
    async launchTypeScriptErrorResolution(progressCallback) {
        let iteration = 1;
        let errorsRemaining = 0;
        let previousErrorCount = 0;
        const reportProgress = (message) => {
            if (progressCallback) {
                progressCallback(message);
            }
        };
        reportProgress('Initializing TypeScript Error Resolution System...');
        do {
            this.currentExecution = this.initializeExecution(iteration);
            reportProgress(`Iteration ${iteration}: Scanning for TypeScript errors...`);
            // Check current TypeScript errors
            const errors = await this.runTypeScriptCheck();
            this.currentExecution.totalErrors = errors.length;
            this.currentExecution.errorsRemaining = errors.length;
            if (errors.length === 0) {
                this.currentExecution.status = 'completed';
                reportProgress('🎉 No TypeScript errors found! System completed successfully.');
                this.generateFinalSuccessReport();
                break;
            }
            reportProgress(`Found ${errors.length} TypeScript errors. Starting 5-phase resolution...`);
            // Check for progress (if we're not making progress, we might be stuck)
            if (iteration > 1 && errors.length >= previousErrorCount) {
                const warningMsg = `Iteration ${iteration}: Error count not decreasing (${errors.length} errors). Some errors may require manual intervention.`;
                reportProgress(warningMsg);
                const maxIterationsBeforeAnalysis = 3;
                if (iteration >= maxIterationsBeforeAnalysis) {
                    // After 3 iterations without progress, provide detailed error analysis
                    reportProgress('Analyzing stubborn errors for manual intervention requirements...');
                    this.analyzeStubornErrors(errors);
                }
            }
            previousErrorCount = errors.length;
            // Execute all 5 phases with progress reporting
            for (let phaseNumber = 1; phaseNumber <= totalPhases; phaseNumber++) {
                reportProgress(`Iteration ${iteration}, Phase ${phaseNumber}: ${this.getPhaseDescription(phaseNumber)}`);
                await this.executePhase(phaseNumber, errors);
                if (!this.validatePhaseCompletion(phaseNumber)) {
                    throw new Error(`Phase ${phaseNumber} validation failed in iteration ${iteration}`);
                }
                reportProgress(`Phase ${phaseNumber} completed successfully!`);
            }
            // Check if errors are resolved after this iteration
            reportProgress(`Iteration ${iteration}: Validating TypeScript compilation...`);
            const remainingErrors = await this.runTypeScriptCheck();
            errorsRemaining = remainingErrors.length;
            this.currentExecution.errorsRemaining = errorsRemaining;
            if (errorsRemaining === 0) {
                this.currentExecution.status = 'completed';
                reportProgress('🎉 All TypeScript errors resolved! Compilation successful!');
                this.generateFinalSuccessReport();
                break;
            }
            const resolved = errors.length - errorsRemaining;
            if (resolved > 0) {
                reportProgress(`Iteration ${iteration} completed: ${resolved} errors resolved, ${errorsRemaining} remaining.`);
            }
            else {
                reportProgress(`Iteration ${iteration} completed: No errors resolved, ${errorsRemaining} still need attention.`);
            }
            iteration++;
            if (iteration > maxIterations) {
                const errorMsg = `Maximum iterations (${maxIterations}) reached. ${errorsRemaining} TypeScript errors may require manual intervention.`;
                this.currentExecution.status = 'failed';
                throw new Error(errorMsg);
            }
        } while (errorsRemaining > 0 && iteration <= maxIterations);
        reportProgress(`TypeScript Error Resolution completed after ${iteration - 1} iterations.`);
    }
    /**
     * Get phase description for progress reporting
     */
    getPhaseDescription(phaseNumber) {
        switch (phaseNumber) {
            case 1:
                return 'Error Detection & Categorization';
            case 2:
                return 'Error Analysis & Root Cause Investigation';
            case phaseNumbers.ERROR_DETECTION:
                return 'Error Resolution Implementation';
            case phaseNumbers.FIX_VALIDATION:
                return 'Fix Validation & Regression Testing';
            case phaseNumbers.COMPLETION_VERIFICATION:
                return 'Completion Verification & Documentation';
            default:
                return `Phase ${phaseNumber}`;
        }
    }
    /**
     * Analyze errors that persist across multiple iterations
     */
    analyzeStubornErrors(errors) {
        const errorAnalysis = {
            typeAssignment: errors.filter(e => e.category === 'Type Assignment').length,
            unknownType: errors.filter(e => e.category === 'Unknown Type').length,
            nullUndefined: errors.filter(e => e.category === 'Null/Undefined').length,
            importModule: errors.filter(e => e.category === 'Import/Module').length,
            generics: errors.filter(e => e.category === 'Generics').length,
            other: errors.filter(e => e.category === 'Other').length,
        };
        // Log analysis for manual intervention guidance
        const analysisPath = path.join(this.logBasePath, 'stubborn-errors-analysis.md');
        const analysisContent = `# Stubborn TypeScript Errors Analysis

## Error Category Breakdown
- Type Assignment: ${errorAnalysis.typeAssignment}
- Unknown Type: ${errorAnalysis.unknownType}
- Null/Undefined: ${errorAnalysis.nullUndefined}
- Import/Module: ${errorAnalysis.importModule}
- Generics: ${errorAnalysis.generics}
- Other: ${errorAnalysis.other}

## Detailed Errors Requiring Manual Attention
${errors
            .map((error, index) => `
### Error ${index + 1}: ${error.code}
- **File**: ${error.file}
- **Location**: Line ${error.line}, Column ${error.column}
- **Category**: ${error.category}
- **Message**: ${error.message}
- **Severity**: ${error.severity}
`)
            .join('\n')}

## Recommended Manual Actions
1. Review complex type definitions and interfaces
2. Add explicit type annotations where inference fails
3. Update import statements and module declarations
4. Consider refactoring complex generic types
5. Add proper null checks and type guards

---
*Generated: ${new Date().toISOString()}*
*TrueNorth TypeScript Error Resolution System*
`;
        try {
            fs.writeFileSync(analysisPath, analysisContent, 'utf8');
        }
        catch {
            // Silent fail for analysis file creation
        }
    }
    /**
     * Run TypeScript check and parse errors
     */
    async runTypeScriptCheck() {
        try {
            const { stderr } = await execAsync('npx tsc --noEmit', {
                cwd: this.workspacePath,
                timeout: 30000,
            });
            // If no errors, stdout will be empty and stderr might contain success info
            if (!stderr || stderr.trim() === '') {
                return [];
            }
            return this.parseTypeScriptErrors(stderr);
        }
        catch (error) {
            // TypeScript compiler exits with non-zero code when there are errors
            if (error && typeof error === 'object' && 'stderr' in error) {
                return this.parseTypeScriptErrors(error.stderr);
            }
            throw error;
        }
    }
    /**
     * Parse TypeScript compiler errors from stderr output
     */
    parseTypeScriptErrors(stderr) {
        const errors = [];
        const lines = stderr.split('\n');
        for (const line of lines) {
            // Match TypeScript error format: file(line,column): error TS####: message
            const match = line.match(/^(.+?)\((\d+),(\d+)\):\s+(error|warning)\s+TS(\d+):\s+(.+)$/);
            if (match) {
                const [, file, lineStr, columnStr, severity, code, message] = match;
                errors.push({
                    file: file.trim(),
                    line: parseInt(lineStr, 10),
                    column: parseInt(columnStr, 10),
                    code: `TS${code}`,
                    message: message.trim(),
                    severity: severity,
                    category: this.categorizeError(code),
                });
            }
        }
        return errors;
    }
    /**
     * Categorize TypeScript errors by type
     */
    categorizeError(code) {
        const typeErrors = ['2345', '2322', '2339', '2571', '2551', '2304'];
        const nullErrors = ['2531', '2532', '2533', '2538'];
        const importErrors = ['2307', '2306', '2305', '2309'];
        const genericErrors = ['2314', '2315', '2344'];
        if (typeErrors.includes(code)) {
            return 'Type Assignment';
        }
        if (nullErrors.includes(code)) {
            return 'Null/Undefined';
        }
        if (importErrors.includes(code)) {
            return 'Import/Module';
        }
        if (genericErrors.includes(code)) {
            return 'Generics';
        }
        if (code === '18046') {
            return 'Unknown Type';
        }
        return 'Other';
    }
    /**
     * Initialize execution structure for TypeScript error resolution
     */
    initializeExecution(iteration) {
        const phases = [
            {
                phase: 1,
                name: 'TypeScript Error Detection',
                status: 'pending',
                agents: this.generatePhaseAgents(phase1Start, phase1End, 'detection'),
                errorCount: 0,
                errorsFixed: 0,
            },
            {
                phase: 2,
                name: 'Error Analysis & Audit',
                status: 'pending',
                agents: this.generatePhaseAgents(phase2Start, phase2End, 'analysis'),
                errorCount: 0,
                errorsFixed: 0,
            },
            {
                phase: 3,
                name: 'Error Resolution Implementation',
                status: 'pending',
                agents: this.generatePhaseAgents(phase3Start, phase3End, 'resolution'),
                errorCount: 0,
                errorsFixed: 0,
            },
            {
                phase: 4,
                name: 'Fix Validation & Audit',
                status: 'pending',
                agents: this.generatePhaseAgents(phase4Start, phase4End, 'validation'),
                errorCount: 0,
                errorsFixed: 0,
            },
            {
                phase: 5,
                name: 'Completion Verification',
                status: 'pending',
                agents: this.generatePhaseAgents(phase5Start, phase5End, 'completion'),
                errorCount: 0,
                errorsFixed: 0,
            },
        ];
        return {
            id: `typescript-resolution-${Date.now()}`,
            status: 'pending',
            currentPhase: 1,
            completedPhases: [],
            phases,
            wave: this.waveNumber,
            iteration,
            totalErrors: 0,
            errorsRemaining: 0,
            startTime: new Date(),
        };
    }
    /**
     * Generate TypeScript-specific agents for a phase
     */
    generatePhaseAgents(startAgent, endAgent, phaseType) {
        const agents = [];
        for (let i = startAgent; i <= endAgent; i++) {
            agents.push({
                id: `ts-agent-${i.toString().padStart(agentNamePadding, '0')}`,
                name: this.generateAgentName(i, phaseType),
                phase: phaseType,
                phaseNumber: this.getPhaseFromAgentNumber(i),
                agentNumber: i,
                status: 'pending',
                progress: defaultProgress,
                output: [],
                errorsAssigned: [],
                errorsFixed: [],
            });
        }
        return agents;
    }
    /**
     * Generate TypeScript-specific agent names
     */
    generateAgentName(agentNumber, phaseType) {
        switch (phaseType) {
            case 'detection':
                return `TypeScript Error Detection Agent ${agentNumber}`;
            case 'analysis':
                return `Error Analysis & Audit Agent ${agentNumber}`;
            case 'resolution':
                return `TypeScript Fix Implementation Agent ${agentNumber}`;
            case 'validation':
                return `Fix Validation & Audit Agent ${agentNumber}`;
            case 'completion':
                return `Completion Verification Agent ${agentNumber}`;
            default:
                return `TypeScript Agent ${agentNumber}`;
        }
    }
    /**
     * Get phase number from agent number
     */
    getPhaseFromAgentNumber(agentNumber) {
        if (agentNumber <= phase1End) {
            return firstPhase;
        }
        if (agentNumber <= phase2End) {
            return secondPhase;
        }
        if (agentNumber <= phase3End) {
            return thirdPhase;
        }
        if (agentNumber <= phase4End) {
            return fourthPhase;
        }
        return fifthPhase;
    }
    /**
     * Execute a specific phase for TypeScript error resolution
     */
    async executePhase(phaseNumber, errors) {
        if (!this.currentExecution) {
            throw new Error('No execution initialized');
        }
        const phase = this.currentExecution.phases[phaseNumber - phase1ArrayOffset];
        phase.status = 'running';
        phase.startTime = new Date();
        phase.errorCount = errors.length;
        this.currentExecution.currentPhase = phaseNumber;
        // Distribute errors among agents
        this.distributeErrorsToAgents(phase.agents, errors);
        // Execute agents in parallel batches
        const batchSize = this.maxParallelAgents;
        const agentBatches = this.chunkArray(phase.agents, batchSize);
        for (const batch of agentBatches) {
            await Promise.all(batch.map(agent => this.executeTypeScriptAgent(agent, phaseNumber)));
        }
        phase.status = 'completed';
        phase.endTime = new Date();
        this.currentExecution.completedPhases.push(phaseNumber);
        // Generate phase report
        this.generatePhaseReport(phaseNumber, phase);
    }
    /**
     * Distribute TypeScript errors among agents
     */
    distributeErrorsToAgents(agents, errors) {
        if (errors.length === 0 || agents.length === 0) {
            return;
        }
        const errorsPerAgent = Math.ceil(errors.length / agents.length);
        for (let i = 0; i < agents.length; i++) {
            const startIndex = i * errorsPerAgent;
            const endIndex = Math.min(startIndex + errorsPerAgent, errors.length);
            agents[i].errorsAssigned = errors.slice(startIndex, endIndex);
        }
    }
    /**
     * Execute individual TypeScript agent
     */
    async executeTypeScriptAgent(agent, phaseNumber) {
        try {
            agent.status = 'running';
            agent.startTime = new Date();
            const prompt = this.generateTypeScriptPrompt(agent, phaseNumber);
            const output = await this.runAgentWithPrompt(agent, prompt);
            agent.output.push(output || 'No output received');
            agent.status = 'completed';
            agent.progress = fullProgress;
        }
        catch (error) {
            agent.status = 'failed';
            agent.error = error instanceof Error ? error.message : 'Unknown error';
        }
        finally {
            agent.endTime = new Date();
        }
    }
    /**
     * Generate TypeScript-specific prompts for each phase
     */
    generateTypeScriptPrompt(agent, phaseNumber) {
        const errorDetails = agent.errorsAssigned
            ?.map(err => `${err.file}(${err.line},${err.column}): ${err.code} - ${err.message}`)
            .join('\n') ?? '';
        if (!errorDetails) {
            return `Agent ${agent.agentNumber}: No specific errors assigned. Perform general TypeScript quality analysis.`;
        }
        const baseContext = `You are TypeScript Agent ${agent.agentNumber} in the TrueNorth 125-agent error resolution system.`;
        switch (phaseNumber) {
            case firstPhase: // Detection
                return `${baseContext}

PHASE 1: ERROR DETECTION & CATEGORIZATION
Analyze these TypeScript errors and provide detailed categorization:

${errorDetails}

Your tasks:
1. Categorize each error by type (Type Assignment, Null/Undefined, Unknown Type, etc.)
2. Assess severity and potential impact on compilation
3. Identify any error dependencies or relationships
4. Suggest priority order for resolution
5. Flag any errors that might cascade or create additional issues

Provide structured analysis for systematic resolution in subsequent phases.`;
            case secondPhase: // Analysis
                return `${baseContext}

PHASE 2: ERROR ANALYSIS & ROOT CAUSE INVESTIGATION
Perform deep analysis on these TypeScript errors:

${errorDetails}

Your tasks:
1. Identify root causes for each error
2. Determine if errors are isolated or part of larger type system issues
3. Analyze code context and suggest optimal fix strategies
4. Check for patterns that might indicate architectural issues
5. Recommend specific TypeScript features or patterns to use for fixes

Focus on understanding WHY these errors exist and HOW to fix them systematically.`;
            case thirdPhase: // Resolution
                return `${baseContext}

PHASE 3: ERROR RESOLUTION IMPLEMENTATION
Implement specific fixes for these TypeScript errors:

${errorDetails}

Your tasks:
1. Provide exact code changes needed to fix each error
2. Ensure type safety and follow TypeScript best practices
3. Consider backwards compatibility and minimal disruption
4. Add proper type annotations, interfaces, or type guards as needed
5. Verify that fixes don't introduce new errors

Provide concrete, implementable solutions with before/after code examples.`;
            case fourthPhase: // Validation
                return `${baseContext}

PHASE 4: FIX VALIDATION & REGRESSION TESTING
Validate the implemented fixes for these TypeScript errors:

${errorDetails}

Your tasks:
1. Verify that each error has been properly resolved
2. Check for any new errors introduced by the fixes
3. Validate that type safety has been maintained or improved
4. Test edge cases and potential regression scenarios
5. Confirm that the fixes align with project coding standards

Ensure quality and stability of the implemented solutions.`;
            case fifthPhase: // Completion
                return `${baseContext}

PHASE 5: COMPLETION VERIFICATION & DOCUMENTATION
Final verification and documentation for these TypeScript errors:

${errorDetails}

Your tasks:
1. Confirm successful resolution of all assigned errors
2. Verify no regressions or side effects from fixes
3. Document the changes made and their rationale
4. Generate completion report with before/after summary
5. Validate overall TypeScript compilation success

Ensure production readiness and provide clear documentation of changes.`;
            default:
                return `${baseContext}\n\nProcess these TypeScript errors: ${errorDetails}`;
        }
    }
    /**
     * Execute agent with specific prompt
     */
    async runAgentWithPrompt(agent, prompt) {
        const onProgress = (message) => {
            agent.output.push(`[PROGRESS] ${message}`);
            if (agent.progress < maxSafeProgress) {
                agent.progress = Math.min(agent.progress + progressStepSize, maxSafeProgress);
            }
        };
        return this.claudeCliManager.executeCommand(prompt, {
            commandType: 'agent',
            enableProgressReporting: true,
            onProgress,
        });
    }
    /**
     * Utility method to chunk array into smaller arrays
     */
    chunkArray(array, chunkSize) {
        const chunks = [];
        for (let i = 0; i < array.length; i += chunkSize) {
            chunks.push(array.slice(i, i + chunkSize));
        }
        return chunks;
    }
    /**
     * Validate phase completion
     */
    validatePhaseCompletion(phaseNumber) {
        if (!this.currentExecution) {
            return false;
        }
        const phase = this.currentExecution.phases[phaseNumber - phase1ArrayOffset];
        const completedAgents = phase.agents.filter(a => a.status === 'completed').length;
        const totalAgents = phase.agents.length;
        return completedAgents === totalAgents;
    }
    /**
     * Generate phase report
     */
    generatePhaseReport(phaseNumber, phase) {
        if (!this.logBasePath) {
            return;
        }
        try {
            const reportDir = this.getPhaseReportDirectory(phaseNumber);
            const reportPath = path.join(reportDir, `typescript-phase-${phaseNumber}-report.md`);
            const report = this.createPhaseReportContent(phaseNumber, phase);
            fs.writeFileSync(reportPath, report, 'utf8');
            phase.reportPath = reportPath;
        }
        catch (error) {
            void this.errorHandler.handleError(new Error(`Failed to generate TypeScript phase ${phaseNumber} report: ${error}`), ErrorHandler_1.ErrorCategory.FILESYSTEM, ErrorHandler_1.ErrorSeverity.MEDIUM, {
                component: 'TypeScriptErrorOrchestrator',
                operation: 'generatePhaseReport',
                timestamp: new Date().toISOString(),
                additionalData: { phaseNumber },
            });
        }
    }
    /**
     * Get phase report directory
     */
    getPhaseReportDirectory(phaseNumber) {
        const directories = [
            'phase1-error-detection',
            'phase2-error-analysis',
            'phase3-error-fixes',
            'phase4-fix-validation',
            'phase5-completion',
        ];
        return path.join(this.logBasePath, directories[phaseNumber - 1]);
    }
    /**
     * Create phase report content
     */
    createPhaseReportContent(phaseNumber, phase) {
        const duration = phase.endTime && phase.startTime
            ? Math.round((phase.endTime.getTime() - phase.startTime.getTime()) / timeoutDelayMs)
            : 0;
        const completedCount = phase.agents.filter(a => a.status === 'completed').length;
        const failedCount = phase.agents.filter(a => a.status === 'failed').length;
        return `# TypeScript Phase ${phaseNumber} Report: ${phase.name}

## 📊 Summary
- **Status**: ${phase.status}
- **Start Time**: ${phase.startTime?.toISOString()}
- **End Time**: ${phase.endTime?.toISOString()}
- **Duration**: ${duration} seconds
- **Agents Completed**: ${completedCount}/${phase.agents.length}
- **Agents Failed**: ${failedCount}
- **Errors Processed**: ${phase.errorCount}
- **Errors Fixed**: ${phase.errorsFixed}

## 🤖 Agent Results

${phase.agents
            .map(agent => `### ${agent.name}
- **ID**: ${agent.id}
- **Status**: ${agent.status}
- **Progress**: ${agent.progress}%
- **Errors Assigned**: ${agent.errorsAssigned?.length ?? 0}
- **Errors Fixed**: ${agent.errorsFixed?.length ?? 0}
- **Duration**: ${agent.endTime && agent.startTime ? Math.round((agent.endTime.getTime() - agent.startTime.getTime()) / timeoutDelayMs) : 0}s
${agent.error ? `- **Error**: ${agent.error}` : ''}
${agent.output.length > 0 ? `- **Output**: ${agent.output.join('\\n').substring(0, cleanOutputSubstringLength)}...` : ''}
`)
            .join('\\n')}

---
*Generated: ${new Date().toISOString()}*
*Wave: ${this.waveNumber}*
*Iteration: ${this.currentExecution?.iteration ?? 1}*
`;
    }
    /**
     * Generate final success report
     */
    generateFinalSuccessReport() {
        if (!this.currentExecution || !this.logBasePath) {
            return;
        }
        try {
            const reportPath = path.join(this.logBasePath, 'typescript-success-report.md');
            const totalAgents = this.currentExecution.phases.reduce((sum, phase) => sum + phase.agents.length, 0);
            const completedAgents = this.currentExecution.phases.reduce((sum, phase) => sum + phase.agents.filter(a => a.status === 'completed').length, 0);
            const report = `# 🎉 TypeScript Error Resolution Success Report

## 🏆 Mission Accomplished
All TypeScript errors have been successfully resolved!

## 📊 Execution Summary
- **Iteration**: ${this.currentExecution.iteration}
- **Total Agents**: ${totalAgents}
- **Completed Agents**: ${completedAgents}
- **Success Rate**: ${Math.round((completedAgents / totalAgents) * percentageMultiplier)}%
- **Initial Errors**: ${this.currentExecution.totalErrors}
- **Errors Remaining**: ${this.currentExecution.errorsRemaining}
- **Start Time**: ${this.currentExecution.startTime?.toISOString()}
- **End Time**: ${new Date().toISOString()}

## ✅ TypeScript Compilation Status
\`\`\`
npx tsc --noEmit
\`\`\`
**Result**: ✅ SUCCESS - No TypeScript errors found!

## 📋 Phase Summary
${this.currentExecution.phases
                .map(phase => `
### Phase ${phase.phase}: ${phase.name}
- **Status**: ${phase.status}
- **Agents**: ${phase.agents.filter(a => a.status === 'completed').length}/${phase.agents.length} completed
- **Errors Processed**: ${phase.errorCount}
- **Report**: ${phase.reportPath ?? 'Generated'}
`)
                .join('\\n')}

## 🚀 Production Ready
- ✅ All TypeScript errors resolved
- ✅ 5-Phase systematic execution completed
- ✅ Type safety validation passed
- ✅ Code compilation successful
- ✅ Ready for production deployment

---
*Generated: ${new Date().toISOString()}*
*Wave: ${this.waveNumber}*
*System: TrueNorth TypeScript Error Resolution System*
*125-Agent Specialized System: SUCCESS*
`;
            fs.writeFileSync(reportPath, report, 'utf8');
            this.currentExecution.endTime = new Date();
        }
        catch (error) {
            void this.errorHandler.handleError(new Error(`Failed to generate TypeScript success report: ${error}`), ErrorHandler_1.ErrorCategory.FILESYSTEM, ErrorHandler_1.ErrorSeverity.MEDIUM, {
                component: 'TypeScriptErrorOrchestrator',
                operation: 'generateFinalSuccessReport',
                timestamp: new Date().toISOString(),
            });
        }
    }
    // Public API methods for external access
    /**
     * Get current execution status
     */
    getCurrentExecution() {
        return this.currentExecution;
    }
    /**
     * Get current phase information
     */
    getCurrentPhase() {
        if (!this.currentExecution) {
            return undefined;
        }
        return this.currentExecution.phases[this.currentExecution.currentPhase - phase1ArrayOffset];
    }
    /**
     * Get execution summary
     */
    getExecutionSummary() {
        if (!this.currentExecution) {
            return {
                totalErrors: 0,
                errorsRemaining: 0,
                iteration: 0,
                currentPhase: 0,
                overallProgress: 0,
                status: 'not_started',
            };
        }
        const totalAgents = this.currentExecution.phases.reduce((sum, phase) => sum + phase.agents.length, 0);
        const completedAgents = this.currentExecution.phases.reduce((sum, phase) => sum + phase.agents.filter(a => a.status === 'completed').length, 0);
        return {
            totalErrors: this.currentExecution.totalErrors,
            errorsRemaining: this.currentExecution.errorsRemaining,
            iteration: this.currentExecution.iteration,
            currentPhase: this.currentExecution.currentPhase,
            overallProgress: Math.round((completedAgents / totalAgents) * percentageMultiplier),
            status: this.currentExecution.status,
        };
    }
    /**
     * Stop all TypeScript agents
     */
    stopAllAgents() {
        if (this.currentExecution) {
            this.currentExecution.status = 'failed';
            const currentPhase = this.currentExecution.phases[this.currentExecution.currentPhase - 1];
            if (currentPhase) {
                currentPhase.agents.forEach(agent => {
                    if (agent.status === 'running') {
                        agent.status = 'failed';
                        agent.error = 'Stopped by user';
                        agent.endTime = new Date();
                    }
                });
            }
        }
    }
    /**
     * Get quick TypeScript error check
     */
    async getTypeScriptErrorCount() {
        try {
            const errors = await this.runTypeScriptCheck();
            return errors.length;
        }
        catch {
            return -1; // Error in checking
        }
    }
}
exports.TypeScriptErrorOrchestrator = TypeScriptErrorOrchestrator;
//# sourceMappingURL=TypeScriptErrorOrchestrator.js.map