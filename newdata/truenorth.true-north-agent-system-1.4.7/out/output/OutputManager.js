"use strict";
/**
 * OutputManager - Handles VS Code output panel for TrueNorth
 * Provides centralized logging and Claude CLI response display
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
exports.OutputManager = void 0;
const vscode = __importStar(require("vscode"));
// Constants for output formatting
const outputConstants = {
    maxHistorySize: 100,
    separatorLength: 80,
};
class OutputManager {
    constructor() {
        this.commandHistory = [];
        this.maxHistorySize = outputConstants.maxHistorySize;
        this.outputChannel = vscode.window.createOutputChannel('TrueNorth');
    }
    /**
     * Show the output panel
     */
    show(preserveFocus = false) {
        this.outputChannel.show(preserveFocus);
    }
    /**
     * Clear the output panel
     */
    clear() {
        this.outputChannel.clear();
        this.log('info', 'Output cleared');
    }
    /**
     * Log a message to the output panel
     */
    log(type, message, source) {
        const timestamp = new Date();
        const timeStr = timestamp.toLocaleTimeString();
        const sourceStr = source ? `[${source}]` : '[TrueNorth]';
        let prefix = '';
        switch (type) {
            case 'success':
                prefix = '✅ SUCCESS';
                break;
            case 'warning':
                prefix = '⚠️  WARNING';
                break;
            case 'error':
                prefix = '❌ ERROR';
                break;
            case 'command':
                prefix = '🤖 COMMAND';
                break;
            case 'response':
                prefix = '💬 RESPONSE';
                break;
            default:
                prefix = 'ℹ️  INFO';
        }
        const formattedMessage = `[${timeStr}] ${sourceStr} ${prefix}: ${message}`;
        this.outputChannel.appendLine(formattedMessage);
        // Auto-show on errors and commands
        if (type === 'error' || type === 'command') {
            this.show(true);
        }
    }
    /**
     * Log a Claude CLI command execution
     */
    logCommand(command, args) {
        const fullCommand = `${command} ${args.join(' ')}`;
        this.commandHistory.unshift(fullCommand);
        // Keep history size manageable
        if (this.commandHistory.length > this.maxHistorySize) {
            this.commandHistory = this.commandHistory.slice(0, this.maxHistorySize);
        }
        this.log('command', `Executing: ${fullCommand}`);
    }
    /**
     * Log a Claude CLI response
     */
    logResponse(response, duration) {
        const durationStr = duration ? ` (${duration}ms)` : '';
        this.log('response', `Claude response received${durationStr}`);
        // Add separator for readability
        this.outputChannel.appendLine(''.padEnd(outputConstants.separatorLength, '-'));
        this.outputChannel.appendLine(response);
        this.outputChannel.appendLine(''.padEnd(outputConstants.separatorLength, '-'));
    }
    /**
     * Log an error with optional error object
     */
    logError(message, error) {
        this.log('error', message);
        if (error) {
            this.outputChannel.appendLine(`Error details: ${error.message}`);
            if (error.stack) {
                this.outputChannel.appendLine(`Stack trace: ${error.stack}`);
            }
        }
    }
    /**
     * Log command progress/status
     */
    logProgress(message) {
        this.log('info', `Progress: ${message}`);
    }
    /**
     * Get command history
     */
    getCommandHistory() {
        return [...this.commandHistory];
    }
    /**
     * Log a structured agent update
     */
    logAgentUpdate(agentName, status, message) {
        const statusEmoji = status === 'running'
            ? '🔄'
            : status === 'completed'
                ? '✅'
                : status === 'failed'
                    ? '❌'
                    : '⏸️';
        const fullMessage = `Agent ${agentName} ${statusEmoji} ${status.toUpperCase()}${message ? `: ${message}` : ''}`;
        this.log('info', fullMessage, 'Agent');
    }
    /**
     * Create a section separator in the output
     */
    logSeparator(title) {
        this.outputChannel.appendLine('');
        if (title) {
            const separator = `=== ${title} ===`;
            this.outputChannel.appendLine(separator.padEnd(outputConstants.separatorLength, '='));
        }
        else {
            this.outputChannel.appendLine(''.padEnd(outputConstants.separatorLength, '='));
        }
        this.outputChannel.appendLine('');
    }
    /**
     * Dispose resources
     */
    dispose() {
        this.outputChannel.dispose();
    }
}
exports.OutputManager = OutputManager;
//# sourceMappingURL=OutputManager.js.map