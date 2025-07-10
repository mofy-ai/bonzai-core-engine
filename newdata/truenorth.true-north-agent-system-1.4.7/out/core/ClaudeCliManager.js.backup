"use strict";
/**
 * Enhanced Claude CLI Manager - Phase 1A Implementation
 * Executes Claude CLI commands with VS Code terminal integration
 * FIXED FOR WINDOWS COMPATIBILITY
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
exports.ClaudeCliManager = void 0;
const child_process_1 = require("child_process");
const fs_1 = require("fs");
const os = __importStar(require("os"));
const vscode = __importStar(require("vscode"));
const constants_1 = require("../constants");
const ErrorHandler_1 = require("./ErrorHandler");
// ANSI color code regex pattern as constant to avoid control character in source
const ansiEscapeChar = 27;
const ansiEsc = String.fromCharCode(ansiEscapeChar);
const ansiColorRegex = new RegExp(`${ansiEsc}\\[[0-9;]*m`, 'gu');
// Constants for timeouts and delays
const progressIntervalMs = 1000;
const outputSubstringLength = 100;
const progressStringLength = 200;
const forceKillDelayMs = 5000;
const progressIntervalLongMs = 30000;
const progressIntervalShortMs = 5000;
const minutesToMs = 60000;
const retryBaseDelayMs = 1000;
const maxRetryDelayMs = 10000;
const defaultTimeoutMs = 30000;
const promptSizeLimit = 50000;
const tempKillDelayMs = 2000;
const maxRetriesDefault = 3;
const percentageBase = 100;
const uptimeMultiplier = 1000;
const errorPenalty = 10;

// WINDOWS COMPATIBILITY FIX
const isWindows = os.platform() === 'win32';

class ClaudeCliManager {
    constructor(outputManager) {
        // Timeout configurations for different command types
        this.timeouts = {
            quick: constants_1.timeConstants.CLAUDE_QUICK_TIMEOUT_MS,
            analysis: constants_1.timeConstants.CLAUDE_ANALYSIS_TIMEOUT_MS,
            agent: constants_1.timeConstants.CLAUDE_AGENT_TIMEOUT_MS,
            extended: constants_1.timeConstants.CLAUDE_EXTENDED_TIMEOUT_MS,
        };
        this.outputManager = outputManager;
        this.claudePath = this.detectClaudePath();
        this.errorHandler = ErrorHandler_1.ErrorHandler.getInstance(outputManager);
    }
    /**
     * Detect Claude CLI path across different systems
     */
    detectClaudePath() {
        const possiblePaths = isWindows ? [
            'claude.exe', // Windows PATH fallback (preferred)
            'claude', // PATH fallback without extension
            'C:\\Program Files\\Claude CLI\\claude.exe', // Windows Program Files
            'C:\\Users\\' + os.userInfo().username + '\\AppData\\Local\\Claude CLI\\claude.exe', // User local
            'C:\\tools\\claude.exe', // Common tools directory
        ] : [
            'claude', // PATH fallback (preferred)
            '/opt/homebrew/bin/claude', // macOS Homebrew
            '/usr/local/bin/claude', // macOS/Linux standard
            '/usr/bin/claude', // Linux system-wide
        ];
        
        for (const claudePath of possiblePaths) {
            if (claudePath === 'claude' || claudePath === 'claude.exe' || (0, fs_1.existsSync)(claudePath)) {
                this.outputManager?.log('success', `Found Claude CLI at: ${claudePath}`);
                return claudePath;
            }
        }
        this.outputManager?.log('warning', 'Claude CLI not found in standard locations, using PATH fallback');
        return isWindows ? 'claude.exe' : 'claude';
    }
    /**
     * Enhanced environment setup for Claude CLI - WINDOWS COMPATIBLE
     */
    getEnhancedEnvironment() {
        const env = { ...process.env };
        // Ensure essential environment variables are set
        env.HOME ?? (env.HOME = os.homedir());
        env.USER ?? (env.USER = os.userInfo().username);
        
        // WINDOWS FIX: Set appropriate shell based on platform
        if (isWindows) {
            env.COMSPEC ?? (env.COMSPEC = 'C:\\Windows\\System32\\cmd.exe');
            // Add common Windows PATH locations
            const commonPaths = ['C:\\Windows\\System32', 'C:\\Windows', 'C:\\Program Files\\Claude CLI'];
            const currentPath = env.PATH ?? '';
            const missingPaths = commonPaths.filter(p => !currentPath.includes(p));
            if (missingPaths.length > 0) {
                env.PATH = `${currentPath};${missingPaths.join(';')}`;
            }
        } else {
            env.SHELL ?? (env.SHELL = '/bin/bash');
            // Add common PATH locations for Unix/Linux
            const commonPaths = ['/opt/homebrew/bin', '/usr/local/bin', '/usr/bin', '/bin'];
            const currentPath = env.PATH ?? '';
            const missingPaths = commonPaths.filter(p => !currentPath.includes(p));
            if (missingPaths.length > 0) {
                env.PATH = `${currentPath}:${missingPaths.join(':')}`;
            }
        }
        
        return env;
    }
    /**
     * Execute command using VS Code terminal for better integration
     */
    async executeWithVSCodeTerminal(prompt, options = {}) {
        const startTime = Date.now();
        const claudePath = this.claudePath ?? (isWindows ? 'claude.exe' : 'claude');
        const commandType = options.commandType ?? 'analysis';
        const timeout = options.timeout ?? this.timeouts[commandType];
        this.outputManager?.log('info', `Using VS Code terminal execution for ${commandType} command (timeout: ${timeout / progressIntervalMs}s)`);
        return new Promise((resolve, reject) => {
            const args = ['--dangerously-skip-permissions', '--model', 'sonnet', '--print', prompt];
            this.outputManager?.logCommand(claudePath, args);
            this.outputManager?.log('info', `Starting Claude CLI with prompt: ${prompt.substring(0, outputSubstringLength)}...`);
            // Use standard subprocess for reliable execution
            const child = (0, child_process_1.spawn)(claudePath, args, {
                stdio: ['pipe', 'pipe', 'pipe'],
                env: this.getEnhancedEnvironment(),
                cwd: process.cwd(),
                shell: isWindows, // Use shell on Windows for better compatibility
            });
            let output = '';
            let error = '';
            let hasStarted = false;
            child.stdout.on('data', data => {
                hasStarted = true;
                output += data.toString();
                // Always log some output to show progress
                const cleanData = data.toString().replace(ansiColorRegex, '');
                if (cleanData.trim()) {
                    this.outputManager?.log('info', `Claude output received: ${cleanData.substring(0, progressStringLength)}...`);
                }
                // Show streaming output if enabled
                if (options.useStreamingOutput) {
                    if (cleanData.trim()) {
                        this.outputManager?.logProgress(`Streaming: ${cleanData.trim()}`);
                    }
                }
            });
            child.stderr.on('data', data => {
                error += data.toString();
                this.outputManager?.log('warning', `Claude stderr: ${data.toString()}`);
            });
            child.on('close', exitCode => {
                const duration = Date.now() - startTime;
                if (exitCode === 0) {
                    // Clean up output formatting
                    const cleanOutput = output
                        .replace(ansiColorRegex, '') // Remove ANSI color codes
                        .replace(/\r\n/g, '\n') // Normalize line endings
                        .replace(/\r/g, '\n') // Convert remaining \r to \n
                        .trim();
                    this.outputManager?.logResponse(cleanOutput, duration);
                    this.outputManager?.log('success', `VS Code terminal command completed in ${duration}ms`);
                    resolve(cleanOutput);
                }
                else {
                    const errorMsg = `Command failed with exit code ${exitCode}${error ? `: ${error}` : ''}`;
                    this.outputManager?.logError(`VS Code terminal command failed (${duration}ms)`, new Error(errorMsg));
                    reject(new Error(errorMsg));
                }
            });
            child.on('error', err => {
                const errorMessage = `Failed to start Claude CLI: ${err.message}`;
                this.outputManager?.logError(errorMessage, err);
                reject(new Error(errorMessage));
            });
            // Progressive timeout handling
            const timeoutId = setTimeout(() => {
                const duration = Date.now() - startTime;
                this.outputManager?.logError(`VS Code terminal command timed out after ${duration}ms`);
                child.kill('SIGTERM');
                // Force kill after additional delay
                setTimeout(() => {
                    child.kill('SIGKILL');
                }, forceKillDelayMs);
                reject(new Error(`Command timed out after ${timeout / progressIntervalMs} seconds`));
            }, timeout);
            child.on('close', () => {
                clearTimeout(timeoutId);
            });
            // Enhanced progress reporting for long operations
            const progressInterval = commandType === 'agent' || commandType === 'extended' || commandType === 'analysis'
                ? progressIntervalLongMs
                : progressIntervalShortMs;
            const progressTimer = setInterval(() => {
                if (!hasStarted) {
                    this.outputManager?.log('warning', 'Command startup seems slow, this may indicate authentication or environment issues');
                }
                else if (options.enableProgressReporting) {
                    const elapsed = Date.now() - startTime;
                    const minutes = Math.floor(elapsed / minutesToMs);
                    const seconds = Math.floor((elapsed % minutesToMs) / progressIntervalMs);
                    this.outputManager?.log('info', `Operation running for ${minutes}m ${seconds}s...`);
                    if (options.onProgress) {
                        options.onProgress(`Running for ${minutes}m ${seconds}s`);
                    }
                }
            }, progressInterval);
            child.on('close', () => {
                clearInterval(progressTimer);
            });
        });
    }
    /**
     * Execute command using standard subprocess (fallback)
     */
    async executeWithSubprocess(prompt, options = {}) {
        const startTime = Date.now();
        const claudePath = this.claudePath ?? (isWindows ? 'claude.exe' : 'claude');
        const commandType = options.commandType ?? 'quick';
        const timeout = options.timeout ?? this.timeouts[commandType];
        const args = ['--dangerously-skip-permissions', '--model', 'sonnet', '--print', prompt];
        this.outputManager?.logCommand(claudePath, args);
        this.outputManager?.log('info', `Subprocess starting with timeout: ${timeout}ms`);
        return new Promise((resolve, reject) => {
            const child = (0, child_process_1.spawn)(claudePath, args, {
                stdio: ['pipe', 'pipe', 'pipe'],
                env: this.getEnhancedEnvironment(),
                detached: false, // Ensure child process is properly managed
                shell: isWindows, // Use shell on Windows
            });
            let output = '';
            let error = '';
            let hasOutput = false;
            child.stdout.on('data', data => {
                hasOutput = true;
                output += data.toString();
                this.outputManager?.log('info', `Subprocess output received: ${data.toString().substring(0, outputSubstringLength)}...`);
                if (options.useStreamingOutput) {
                    this.outputManager?.logProgress(`Output: ${data.toString().trim()}`);
                }
            });
            child.stderr.on('data', data => {
                error += data.toString();
            });
            child.on('close', code => {
                const duration = Date.now() - startTime;
                if (code === 0) {
                    const cleanOutput = output.trim();
                    this.outputManager?.logResponse(cleanOutput, duration);
                    this.outputManager?.log('success', `Subprocess command completed in ${duration}ms`);
                    resolve(cleanOutput);
                }
                else {
                    const errorMessage = error || `Command failed with exit code ${code}`;
                    this.outputManager?.logError(`Subprocess command failed (${duration}ms)`, new Error(errorMessage));
                    reject(new Error(errorMessage));
                }
            });
            child.on('error', err => {
                const errorMessage = `Failed to start Claude CLI: ${err.message}`;
                this.outputManager?.logError(errorMessage, err);
                reject(new Error(errorMessage));
            });
            const timeoutId = setTimeout(() => {
                const duration = Date.now() - startTime;
                this.outputManager?.logError(`Subprocess command timed out after ${duration}ms. HasOutput: ${hasOutput}`);
                child.kill('SIGTERM');
                // Force kill after delay if SIGTERM doesn't work
                setTimeout(() => {
                    if (!child.killed) {
                        this.outputManager?.log('warning', 'Force killing stuck process with SIGKILL');
                        child.kill('SIGKILL');
                    }
                }, tempKillDelayMs);
                reject(new Error(`Command timed out after ${timeout / progressIntervalMs} seconds. HasOutput: ${hasOutput}`));
            }, timeout);
            child.on('close', () => {
                clearTimeout(timeoutId);
            });
        });
    }
    /**
     * Execute command with comprehensive error handling and recovery
     */
    async executeCommand(prompt, options = {}) {
        const commandType = options.commandType ?? 'analysis';
        const operation = `execute_${commandType}_command`;
        this.outputManager?.log('info', `Executing ${commandType} command with Claude CLI`);
        try {
            // Validate inputs
            if (!prompt || prompt.trim().length === 0) {
                throw new Error('Command prompt cannot be empty');
            }
            if (prompt.length > promptSizeLimit) {
                throw new Error('Command prompt too large (max 50KB)');
            }
            // Check if Claude CLI is available
            if (!this.claudePath) {
                await this.errorHandler.handleClaudeCliError('Claude CLI path not detected', operation);
                throw new Error('Claude CLI not available');
            }
            // Execute with retry logic
            let lastError = null;
            const maxRetries = this.getMaxRetries(commandType);
            for (let attempt = 1; attempt <= maxRetries; attempt++) {
                try {
                    this.outputManager?.log('info', `Attempt ${attempt}/${maxRetries} for ${commandType} command`);
                    const result = await this.executeWithTerminal(prompt, {
                        timeout: options.timeout ?? this.timeouts[commandType],
                        ...options,
                    });
                    // Validate result
                    if (!result || result.trim().length === 0) {
                        throw new Error('Claude CLI returned empty response');
                    }
                    this.outputManager?.log('success', `${commandType} command completed successfully`);
                    return result;
                }
                catch (error) {
                    lastError = error instanceof Error ? error : new Error(String(error));
                    // Handle specific error types
                    await this.errorHandler.handleClaudeCliError(lastError, operation, this.claudePath);
                    // Don't retry for certain error types
                    if (this.shouldNotRetry(lastError.message)) {
                        break;
                    }
                    // Apply exponential backoff for retries
                    if (attempt < maxRetries) {
                        const delay = Math.min(retryBaseDelayMs * Math.pow(2, attempt - 1), maxRetryDelayMs);
                        this.outputManager?.log('warning', `Retrying in ${delay}ms...`);
                        await this.delay(delay);
                    }
                }
            }
            // All retries failed
            throw lastError ?? new Error('Command execution failed after all retries');
        }
        catch (error) {
            const finalError = error instanceof Error ? error : new Error(String(error));
            // Log the final error
            await this.errorHandler.handleClaudeCliError(finalError, operation, this.claudePath);
            throw finalError;
        }
    }
    /**
     * WINDOWS COMPATIBLE: Execute command using shell/terminal - matches user's working environment
     */
    async executeWithTerminal(prompt, options = {}) {
        const startTime = Date.now();
        const claudePath = this.claudePath ?? (isWindows ? 'claude.exe' : 'claude');
        const timeout = options.timeout ?? defaultTimeoutMs;
        // Basic validation
        if (!prompt || prompt.trim().length === 0) {
            throw new Error('Prompt cannot be empty');
        }
        // Build the command exactly like user types it in terminal
        const escapedPrompt = this.escapeShellString(prompt);
        const command = isWindows 
            ? `${claudePath} --dangerously-skip-permissions --model sonnet -p "${escapedPrompt}"`
            : `${claudePath} --dangerously-skip-permissions --model sonnet -p '${escapedPrompt}'`;
        
        // Get workspace path from VS Code
        const workspacePath = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath ?? (isWindows ? 'C:\\' : '/Users/truenorth');
        this.outputManager?.log('info', `Shell command: ${command.substring(0, outputSubstringLength)}...`);
        this.outputManager?.log('info', `Working directory: ${workspacePath}`);
        return new Promise((resolve, reject) => {
            // WINDOWS FIX: Execute via appropriate shell
            const shellCommand = isWindows ? 'cmd.exe' : '/bin/bash';
            const shellArgs = isWindows ? ['/c', command] : ['-c', command];
            
            const child = (0, child_process_1.spawn)(shellCommand, shellArgs, {
                cwd: workspacePath,
                env: { ...process.env }, // Inherit ALL environment variables
                stdio: ['ignore', 'pipe', 'pipe'], // Don't inherit stdin, capture stdout/stderr
                shell: false, // We're already using the shell explicitly
            });
            const stdoutChunks = [];
            const stderrChunks = [];
            let hasCompleted = false;
            let hasReceivedData = false;
            // Set up timeout
            const timeoutId = setTimeout(() => {
                if (!hasCompleted) {
                    hasCompleted = true;
                    child.kill('SIGTERM');
                    const duration = Date.now() - startTime;
                    const stdoutLength = stdoutChunks.reduce((sum, chunk) => sum + chunk.length, 0);
                    const stderrLength = stderrChunks.reduce((sum, chunk) => sum + chunk.length, 0);
                    const timeoutError = new Error(`Command timed out after ${timeout / progressIntervalMs}s. ` +
                        `Received data: ${hasReceivedData}. ` +
                        `Stdout length: ${stdoutLength}, Stderr length: ${stderrLength}`);
                    this.outputManager?.logError(`Shell command timed out after ${duration}ms`, timeoutError);
                    reject(timeoutError);
                }
            }, timeout);
            // Capture stdout efficiently using buffers
            child.stdout.on('data', (data) => {
                hasReceivedData = true;
                stdoutChunks.push(data);
                if (options.onProgress) {
                    options.onProgress('Receiving data...');
                }
            });
            // Capture stderr efficiently using buffers
            child.stderr.on('data', (data) => {
                hasReceivedData = true;
                stderrChunks.push(data);
                this.outputManager?.log('warning', `Claude stderr: ${data.toString().substring(0, progressStringLength)}`);
            });
            // Handle process completion
            child.on('close', (code) => {
                if (hasCompleted) {
                    return;
                }
                hasCompleted = true;
                clearTimeout(timeoutId);
                const duration = Date.now() - startTime;
                // Efficiently concatenate buffers
                const stdout = Buffer.concat(stdoutChunks).toString();
                const stderr = Buffer.concat(stderrChunks).toString();
                if (code === 0 && stdout.trim()) {
                    const cleanOutput = this.cleanOutput(stdout);
                    this.outputManager?.log('success', `Shell command completed (${duration}ms): ${cleanOutput.substring(0, progressStringLength)}...`);
                    resolve(cleanOutput);
                }
                else if (stderr) {
                    const errorMsg = `Command failed: ${stderr}`;
                    this.outputManager?.logError(`Shell command failed (${duration}ms): ${stderr}`);
                    reject(new Error(errorMsg));
                }
                else {
                    const errorMsg = `Command failed with exit code ${code}. No output received.`;
                    this.outputManager?.logError(`Shell command failed with code ${code} (${duration}ms)`);
                    reject(new Error(errorMsg));
                }
            });
            // Handle process errors
            child.on('error', (error) => {
                if (hasCompleted) {
                    return;
                }
                hasCompleted = true;
                clearTimeout(timeoutId);
                const enhancedError = new Error(`Failed to execute Claude CLI: ${error.message}. ` +
                    `Path: ${claudePath}. ` +
                    `Check if Claude CLI is installed and accessible.`);
                this.outputManager?.logError(`Shell command error: ${error.message}`, enhancedError);
                reject(enhancedError);
            });
        });
    }
    /**
     * WINDOWS COMPATIBLE: Properly escape strings for shell execution
     */
    escapeShellString(str) {
        if (isWindows) {
            // Windows CMD escaping - escape quotes and special characters
            return str.replace(/"/g, '""').replace(/[&<>|^]/g, '^$&');
        } else {
            // Unix shell escaping
            return str.replace(/'/g, "'\"'\"'");
        }
    }
    /**
     * Clean and normalize output
     */
    cleanOutput(output) {
        return output
            .replace(ansiColorRegex, '') // Remove ANSI color codes
            .replace(/\r\n/g, '\n') // Normalize line endings
            .replace(/\r/g, '\n') // Convert remaining \r to \n
            .trim();
    }
    /**
     * Execute command with result information
     */
    async executeCommandWithResult(prompt, options = {}) {
        const startTime = Date.now();
        const claudePath = this.claudePath ?? (isWindows ? 'claude.exe' : 'claude');
        const command = `${claudePath} --dangerously-skip-permissions --model sonnet --print`;
        try {
            const output = await this.executeCommand(prompt, options);
            return {
                success: true,
                output,
                duration: Date.now() - startTime,
                command,
            };
        }
        catch (error) {
            return {
                success: false,
                output: '',
                error: error instanceof Error ? error.message : String(error),
                duration: Date.now() - startTime,
                command,
            };
        }
    }
    /**
     * Test if Claude CLI is available with enhanced feedback
     */
    async testConnection() {
        try {
            this.outputManager?.log('info', 'Testing Claude CLI connection...');
            const result = await this.executeCommandWithResult('Say "Connection test successful"', {
                commandType: 'quick',
                useTTY: false, // Use simple subprocess for quick test
            });
            if (result.success) {
                this.outputManager?.log('success', `Claude CLI test passed (${result.duration}ms)`);
                return true;
            }
            else {
                this.outputManager?.logError('Claude CLI test failed', new Error(result.error ?? 'Unknown error'));
                return false;
            }
        }
        catch (error) {
            this.outputManager?.logError('Connection test exception', error instanceof Error ? error : new Error(String(error)));
            return false;
        }
    }
    /**
     * Get the detected Claude CLI path
     */
    getClaudePath() {
        return this.claudePath ?? (isWindows ? 'claude.exe' : 'claude');
    }
    /**
     * Validate Claude CLI installation
     */
    async validateInstallation() {
        const claudePath = this.getClaudePath();
        try {
            // Use direct subprocess call for version check to avoid recursive executeCommand
            const startTime = Date.now();
            return await new Promise(resolve => {
                const child = (0, child_process_1.spawn)(claudePath, ['--version'], {
                    stdio: ['pipe', 'pipe', 'pipe'],
                    env: this.getEnhancedEnvironment(),
                    timeout: 5000,
                    shell: isWindows, // Use shell on Windows
                });
                let output = '';
                let error = '';
                child.stdout.on('data', data => {
                    output += data.toString();
                });
                child.stderr.on('data', data => {
                    error += data.toString();
                });
                child.on('close', code => {
                    const duration = Date.now() - startTime;
                    if (code === 0 && output.trim()) {
                        this.outputManager?.log('success', `Claude CLI validated successfully in ${duration}ms`);
                        resolve({
                            valid: true,
                            version: output.trim(),
                            path: claudePath,
                        });
                    }
                    else {
                        resolve({
                            valid: false,
                            path: claudePath,
                            error: error || `Command failed with exit code ${code}`,
                        });
                    }
                });
                child.on('error', err => {
                    resolve({
                        valid: false,
                        path: claudePath,
                        error: `Failed to start Claude CLI: ${err.message}`,
                    });
                });
            });
        }
        catch (error) {
            return {
                valid: false,
                path: claudePath,
                error: error instanceof Error ? error.message : 'Unknown error',
            };
        }
    }
    /**
     * Execute an analysis command with VS Code terminal and streaming
     */
    async executeAnalysisCommand(prompt, onProgress) {
        return this.executeCommand(prompt, {
            commandType: 'analysis',
            useTTY: true,
            useStreamingOutput: true,
            enableProgressReporting: true,
            onProgress,
        });
    }
    /**
     * Execute an agent command with extended timeout
     */
    async executeAgentCommand(prompt, onProgress) {
        return this.executeCommand(prompt, {
            commandType: 'agent',
            useTTY: true,
            useStreamingOutput: true,
            enableProgressReporting: true,
            onProgress,
        });
    }
    /**
     * Execute an extended operation command with maximum timeout
     */
    async executeExtendedCommand(prompt, onProgress) {
        return this.executeCommand(prompt, {
            commandType: 'extended',
            useTTY: true,
            useStreamingOutput: true,
            enableProgressReporting: true,
            onProgress,
        });
    }
    /**
     * Get maximum retry attempts based on command type
     */
    getMaxRetries(commandType) {
        switch (commandType) {
            case 'quick':
                return 2;
            case 'analysis':
                return maxRetriesDefault;
            case 'agent':
            case 'extended':
                return 2; // Don't retry long operations aggressively
            default:
                return 2;
        }
    }
    /**
     * Check if error should not be retried
     */
    shouldNotRetry(errorMessage) {
        const noRetryPatterns = [
            /authentication/i,
            /unauthorized/i,
            /invalid.*credentials/i,
            /command.*not.*found/i,
            /permission.*denied/i,
            /quota.*exceeded/i,
            /rate.*limit.*exceeded/i,
            /prompt.*too.*large/i,
            /claude.*not.*found/i,
        ];
        return noRetryPatterns.some(pattern => pattern.test(errorMessage));
    }
    /**
     * Enhanced error handling for executeWithTerminal
     */
    async executeWithTerminalSafe(prompt, options = {}) {
        try {
            return await this.executeWithTerminal(prompt, options);
        }
        catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            // Handle specific terminal execution errors
            if (errorMessage.includes('ENOENT') || errorMessage.includes('command not found')) {
                throw new Error(`Claude CLI executable not found at path: ${this.claudePath}. Please install Claude CLI.`);
            }
            if (errorMessage.includes('EACCES') || errorMessage.includes('permission denied')) {
                throw new Error(`Permission denied executing Claude CLI. Please check file permissions for: ${this.claudePath}`);
            }
            if (errorMessage.includes('timed out')) {
                throw new Error(`Command timed out after ${options.timeout ?? defaultTimeoutMs}ms. Try increasing timeout or simplifying the request.`);
            }
            if (errorMessage.includes('ECONNREFUSED') || errorMessage.includes('network')) {
                throw new Error('Network connection failed. Please check your internet connection and try again.');
            }
            // Re-throw with enhanced context
            throw error;
        }
    }
    /**
     * Add delay utility method
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    /**
     * Enhanced connection test with detailed diagnostics
     */
    async testConnectionDetailed() {
        const diagnostics = {
            claudePathExists: false,
            claudeExecutable: false,
            networkConnectivity: false,
            authentication: false,
        };
        try {
            // Check if Claude path exists
            if (this.claudePath && (0, fs_1.existsSync)(this.claudePath)) {
                diagnostics.claudePathExists = true;
            }
            // Test basic command execution
            try {
                const versionResult = await this.validateInstallation();
                if (versionResult.valid) {
                    diagnostics.claudeExecutable = true;
                    diagnostics.version = versionResult.version;
                }
            }
            catch (error) {
                diagnostics.error = error instanceof Error ? error.message : String(error);
            }
            // Test network connectivity with a simple command
            try {
                await this.executeCommand('Test connection', { commandType: 'quick' });
                diagnostics.networkConnectivity = true;
                diagnostics.authentication = true;
                return { success: true, diagnostics };
            }
            catch (error) {
                const errorMessage = error instanceof Error ? error.message : String(error);
                diagnostics.error = errorMessage;
                if (errorMessage.includes('auth') || errorMessage.includes('unauthorized')) {
                    diagnostics.authentication = false;
                }
                else if (errorMessage.includes('network') || errorMessage.includes('connection')) {
                    diagnostics.networkConnectivity = false;
                }
                return { success: false, diagnostics };
            }
        }
        catch (error) {
            diagnostics.error = error instanceof Error ? error.message : String(error);
            return { success: false, diagnostics };
        }
    }
    /**
     * Get comprehensive health status
     */
    async getHealthStatus() {
        const errorSummary = this.errorHandler.getErrorSummary();
        const claudeErrors = errorSummary.byCategory[ErrorHandler_1.ErrorCategory.CLAUDE_CLI] || 0;
        // Test basic availability
        const testResult = await this.testConnectionDetailed();
        return {
            healthy: testResult.success,
            claudeCliAvailable: testResult.diagnostics.claudeExecutable,
            errorCount: claudeErrors,
            uptime: process.uptime() * uptimeMultiplier,
            performance: {
                averageResponseTime: 0, // Future enhancement: Track response times
                successRate: claudeErrors === 0
                    ? percentageBase
                    : Math.max(0, percentageBase - claudeErrors * errorPenalty),
            },
        };
    }
    /**
     * Cleanup method
     */
    dispose() {
        this.outputManager?.log('info', 'ClaudeCliManager disposed');
        this.errorHandler.dispose();
    }
}
exports.ClaudeCliManager = ClaudeCliManager;
//# sourceMappingURL=ClaudeCliManager.js.map