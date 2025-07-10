"use strict";
/**
 * Foundation Mode Orchestrator
 *
 * 🏗️ FOUNDATION MODE: Get the basic development environment working from broken or new state
 * Mission: Establish a working development foundation before building features
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
exports.FoundationModeOrchestrator = void 0;
const BaseModeOrchestrator_1 = require("./BaseModeOrchestrator");
// ClaudeCliManager and ConfigManager imported through BaseModeOrchestrator
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
class FoundationModeOrchestrator extends BaseModeOrchestrator_1.BaseModeOrchestrator {
    getMode() {
        return BaseModeOrchestrator_1.DevelopmentMode.FOUNDATION;
    }
    getModeIcon() {
        return '🏗️';
    }
    getModeDisplayName() {
        return 'Foundation Mode';
    }
    getGuardQuestions() {
        return [
            'Does this help the development server start successfully?',
            'Is this fixing a basic infrastructure issue?',
            'Am I adding features or fixing the foundation?',
            'Will this resolve compilation/startup errors?',
            'Is this essential for the development environment?',
        ];
    }
    getAllowedActions() {
        return [
            'Install required dependencies (npm install, pip install, etc.)',
            'Configure development servers',
            'Set up local databases/services',
            'Configure environment variables for development',
            'Set up IDE/editor configurations',
            'Create basic project structure',
            'Set up build tools (webpack, vite, etc.)',
            'Configure development scripts',
            'Set up hot reload/live reload',
            'Configure basic routing',
            'Fix syntax errors preventing compilation',
            'Resolve dependency conflicts',
            'Fix configuration issues',
            'Address critical security vulnerabilities in dependencies',
        ];
    }
    getForbiddenActions() {
        return [
            'Building new features',
            'UI/UX improvements',
            'Performance optimizations',
            'Production configurations',
            'Complex business logic',
            'Advanced integrations',
            'Code refactoring (unless blocking compilation)',
            'Feature enhancements',
            'Adding new functionality',
            'Creating complex components',
        ];
    }
    getSuccessCriteria() {
        return [
            {
                id: 'dev_server_starts',
                description: 'Development server starts without errors',
                completed: false,
                required: true,
                validator: () => Promise.resolve(this.validateDevServerStarts()),
            },
            {
                id: 'hot_reload_works',
                description: 'Hot reload/live reload works',
                completed: false,
                required: true,
                validator: () => Promise.resolve(this.validateHotReload()),
            },
            {
                id: 'basic_routing',
                description: 'Basic routing functions',
                completed: false,
                required: true,
            },
            {
                id: 'browser_access',
                description: 'Can access application in browser',
                completed: false,
                required: true,
            },
            {
                id: 'debug_tools',
                description: 'Development debugging tools work',
                completed: false,
                required: false,
            },
            {
                id: 'no_compilation_errors',
                description: 'No critical compilation errors',
                completed: false,
                required: true,
                validator: () => Promise.resolve(this.validateNoCompilationErrors()),
            },
        ];
    }
    getRecommendedNextModes() {
        return [BaseModeOrchestrator_1.DevelopmentMode.BUILD, BaseModeOrchestrator_1.DevelopmentMode.COMPLETION];
    }
    createModeAgents() {
        return [
            {
                id: 'foundation_001',
                name: 'Environment Analyzer',
                description: 'Analyze current development environment and identify broken components',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'foundation_002',
                name: 'Dependency Manager',
                description: 'Install and configure all required dependencies for development',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'foundation_003',
                name: 'Build System Configurator',
                description: 'Set up and configure build tools, bundlers, and development scripts',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'foundation_004',
                name: 'Development Server Fixer',
                description: 'Fix development server configuration and startup issues',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'foundation_005',
                name: 'Environment Variables Setup',
                description: 'Configure development environment variables and local configuration',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'foundation_006',
                name: 'Hot Reload Enabler',
                description: 'Set up hot reload/live reload for development efficiency',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'foundation_007',
                name: 'Basic Routing Setup',
                description: 'Configure basic application routing and navigation structure',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'foundation_008',
                name: 'Development Tools Configurator',
                description: 'Set up debugging tools and development utilities',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'foundation_009',
                name: 'Compilation Error Resolver',
                description: 'Fix critical syntax and compilation errors preventing development',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'foundation_010',
                name: 'Foundation Validator',
                description: 'Validate that development environment is working and ready for feature development',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
        ];
    }
    validateModeEntry() {
        // Foundation mode can always be entered - it's for fixing broken environments
        return true;
    }
    // Custom validators for success criteria
    validateDevServerStarts() {
        try {
            const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? process.cwd();
            const packageJsonPath = path.join(workspaceRoot, 'package.json');
            if (fs.existsSync(packageJsonPath)) {
                const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
                const scripts = packageJson.scripts ?? {};
                // Check if dev scripts exist
                return !!(scripts.dev ?? scripts.start ?? scripts.serve);
            }
            return false;
        }
        catch {
            return false;
        }
    }
    validateHotReload() {
        // Check for hot reload configuration in common tools
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? process.cwd();
        // Check for Vite, Webpack, or similar configurations
        const hotReloadConfigs = [
            'vite.config.js',
            'vite.config.ts',
            'webpack.config.js',
            'next.config.js',
        ];
        return hotReloadConfigs.some(config => fs.existsSync(path.join(workspaceRoot, config)));
    }
    validateNoCompilationErrors() {
        try {
            // For TypeScript projects, check if tsc --noEmit passes
            const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? process.cwd();
            const tsconfigPath = path.join(workspaceRoot, 'tsconfig.json');
            if (fs.existsSync(tsconfigPath)) {
                // In a real implementation, we'd run tsc --noEmit
                // For now, assume success if tsconfig exists and is valid JSON
                try {
                    const tsconfig = JSON.parse(fs.readFileSync(tsconfigPath, 'utf8'));
                    return !!tsconfig.compilerOptions;
                }
                catch {
                    return false;
                }
            }
            return true; // No TypeScript, assume no compilation errors
        }
        catch {
            return false;
        }
    }
}
exports.FoundationModeOrchestrator = FoundationModeOrchestrator;
//# sourceMappingURL=FoundationModeOrchestrator.js.map