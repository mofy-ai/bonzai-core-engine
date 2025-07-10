"use strict";
/**
 * Clean Config Manager - MVP Implementation
 * Focuses on core configuration without over-engineering
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
exports.ConfigManager = void 0;
const vscode = __importStar(require("vscode"));
const constants_1 = require("../constants");
// Configuration constants
const defaultMaxAgents = 5;
const defaultTimeoutMs = 120000;
class ConfigManager {
    constructor(context) {
        this.context = context;
        this.config = new Map();
        this.loadDefaultConfig();
    }
    loadDefaultConfig() {
        this.config.set('claudeCommand', 'claude');
        this.config.set('dashboardPort', constants_1.NETWORK.WEBSOCKET_PORT);
        this.config.set('maxAgents', defaultMaxAgents);
        this.config.set('timeout', defaultTimeoutMs);
    }
    getConfig(key) {
        // First check VSCode workspace settings
        const workspaceConfig = vscode.workspace.getConfiguration('truenorth');
        const workspaceValue = workspaceConfig.get(key);
        if (workspaceValue !== undefined) {
            return workspaceValue;
        }
        // Fall back to internal config
        return this.config.get(key);
    }
    async setConfig(key, value) {
        this.config.set(key, value);
        // Also save to workspace settings
        const workspaceConfig = vscode.workspace.getConfiguration('truenorth');
        await workspaceConfig.update(key, value, vscode.ConfigurationTarget.Workspace);
    }
    getAllConfig() {
        const result = {};
        for (const [key] of Array.from(this.config.entries())) {
            result[key] = this.getConfig(key);
        }
        return result;
    }
    /**
     * Get workspace folder path
     */
    getWorkspacePath() {
        return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    }
    /**
     * Dispose resources
     */
    dispose() {
        this.config.clear();
    }
}
exports.ConfigManager = ConfigManager;
//# sourceMappingURL=ConfigManager.js.map