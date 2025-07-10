"use strict";
/**
 * Completion Mode Orchestrator
 *
 * 🏁 COMPLETION MODE: Complete existing partial implementations - finish what was started
 * Mission: Polish and complete existing features without adding new scope
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
exports.CompletionModeOrchestrator = void 0;
const BaseModeOrchestrator_1 = require("./BaseModeOrchestrator");
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const vscode = __importStar(require("vscode"));
class CompletionModeOrchestrator extends BaseModeOrchestrator_1.BaseModeOrchestrator {
    getMode() {
        return BaseModeOrchestrator_1.DevelopmentMode.COMPLETION;
    }
    getModeIcon() {
        return '🏁';
    }
    getModeDisplayName() {
        return 'Completion Mode';
    }
    getGuardQuestions() {
        return [
            'Am I completing existing work or adding new scope?',
            'Does this finish something already started?',
            'Is this enhancement or completion?',
            'Am I polishing what exists or creating something new?',
            'Will this make existing features feel complete?',
        ];
    }
    getAllowedActions() {
        return [
            'Add missing functionality to existing features',
            'Implement remaining user stories',
            'Complete partial user flows',
            'Fill in missing edge cases',
            'Connect loose ends between features',
            'Improve user experience of existing features',
            'Add proper error handling to existing code',
            'Complete incomplete forms/interfaces',
            'Finish partial API implementations',
            'Complete partial third-party integrations',
            'Finish incomplete data flows',
            'Complete authentication/authorization flows',
            'Finish partial database implementations',
            'Polish existing functionality',
            'Complete missing validations',
            'Finish incomplete business logic',
        ];
    }
    getForbiddenActions() {
        return [
            'Adding completely new features',
            'Building new components/modules',
            'Starting new integrations',
            'Major architecture changes',
            'New user stories/requirements',
            'Creating new pages/screens',
            'Adding new API endpoints (unless needed to complete existing)',
            'New database tables (unless needed to complete existing)',
            'Expanding scope beyond current features',
            'Feature requests from users',
            'New third-party integrations',
        ];
    }
    getSuccessCriteria() {
        return [
            {
                id: 'features_feel_complete',
                description: 'All existing features feel complete',
                completed: false,
                required: true,
            },
            {
                id: 'no_missing_functionality',
                description: 'No obvious missing functionality in current features',
                completed: false,
                required: true,
            },
            {
                id: 'complete_user_flows',
                description: 'User flows are complete end-to-end',
                completed: false,
                required: true,
            },
            {
                id: 'edge_cases_handled',
                description: 'Existing features handle edge cases properly',
                completed: false,
                required: true,
            },
            {
                id: 'features_polished',
                description: 'Features feel polished and finished',
                completed: false,
                required: true,
            },
            {
                id: 'no_incomplete_implementations',
                description: 'No partial or incomplete implementations remaining',
                completed: false,
                required: true,
            },
        ];
    }
    getRecommendedNextModes() {
        return [BaseModeOrchestrator_1.DevelopmentMode.CLEANUP, BaseModeOrchestrator_1.DevelopmentMode.VALIDATION];
    }
    createModeAgents() {
        return [
            {
                id: 'completion_001',
                name: 'Feature Gap Analyzer',
                description: 'Identify missing functionality and incomplete implementations in existing features',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_002',
                name: 'User Flow Completer',
                description: 'Complete partial user flows and ensure end-to-end functionality',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_003',
                name: 'Edge Case Handler',
                description: 'Identify and implement handling for edge cases in existing features',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_004',
                name: 'Error Handler',
                description: 'Add proper error handling and validation to existing features',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_005',
                name: 'API Completer',
                description: 'Complete partial API implementations and missing endpoints',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_006',
                name: 'UI/UX Polisher',
                description: 'Polish user interfaces and improve user experience of existing features',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_007',
                name: 'Integration Finisher',
                description: 'Complete partial third-party integrations and data flows',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_008',
                name: 'Authentication Completer',
                description: 'Complete authentication and authorization flows',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_009',
                name: 'Data Flow Completer',
                description: 'Complete incomplete data flows and database implementations',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_010',
                name: 'Validation Implementer',
                description: 'Add missing input validation and data validation to existing features',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_011',
                name: 'Business Logic Completer',
                description: 'Complete partial business logic implementations',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_012',
                name: 'Feature Connector',
                description: 'Connect loose ends between features and ensure integration',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_013',
                name: 'Form Completer',
                description: 'Complete incomplete forms and user input interfaces',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_014',
                name: 'Feature Polish Agent',
                description: 'Polish existing features to feel complete and professional',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'completion_015',
                name: 'Completion Validator',
                description: 'Validate that all features are complete and ready for next phase',
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
        // Completion mode requires existing features that need completion
        try {
            const hasPartialFeatures = this.checkForPartialFeatures();
            return hasPartialFeatures;
        }
        catch {
            return true; // Allow entry if we can't validate
        }
    }
    checkForPartialFeatures() {
        // Check for indicators of partial implementations
        try {
            // Look for TODO comments in the source code
            const todoCount = this.countTodoComments();
            // Look for incomplete function patterns
            const incompletePatterns = this.findIncompletePatterns();
            // Check for empty implementations or stub functions
            const hasStubs = this.findStubImplementations();
            // Return true if any indicators of partial work are found
            return todoCount > 0 || incompletePatterns > 0 || hasStubs;
        }
        catch {
            // If analysis fails, assume partial features exist (safe default)
            return true;
        }
    }
    countTodoComments() {
        try {
            // Get workspace root
            const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
            if (!workspaceFolder) {
                return 0;
            }
            let todoCount = 0;
            // Search for TODO comments in source files
            const srcPath = path.join(workspaceFolder.uri.fsPath, 'src');
            if (fs.existsSync(srcPath)) {
                const files = this.getAllSourceFiles(srcPath);
                for (const file of files) {
                    const content = fs.readFileSync(file, 'utf8');
                    const matches = content.match(/(?:TODO|FIXME|HACK|XXX|BUG)[\s:]/gi);
                    todoCount += matches?.length ?? 0;
                }
            }
            return todoCount;
        }
        catch {
            return 0;
        }
    }
    findIncompletePatterns() {
        try {
            const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
            if (!workspaceFolder) {
                return 0;
            }
            let incompleteCount = 0;
            const srcPath = path.join(workspaceFolder.uri.fsPath, 'src');
            if (fs.existsSync(srcPath)) {
                const files = this.getAllSourceFiles(srcPath);
                for (const file of files) {
                    const content = fs.readFileSync(file, 'utf8');
                    // Look for incomplete patterns
                    const patterns = [
                        /throw new Error\(['"]Not implemented['"]\)/gi,
                        /return\s+null;\s*\/\/\s*TODO/gi,
                        /\/\*\s*TODO:.*\*\//gi,
                        /function\s+\w+\([^)]*\)\s*{\s*\/\/\s*TODO/gi,
                        /=>\s*{\s*\/\/\s*TODO/gi,
                    ];
                    for (const pattern of patterns) {
                        const matches = content.match(pattern);
                        incompleteCount += matches?.length ?? 0;
                    }
                }
            }
            return incompleteCount;
        }
        catch {
            return 0;
        }
    }
    findStubImplementations() {
        try {
            const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
            if (!workspaceFolder) {
                return false;
            }
            const srcPath = path.join(workspaceFolder.uri.fsPath, 'src');
            if (fs.existsSync(srcPath)) {
                const files = this.getAllSourceFiles(srcPath);
                for (const file of files) {
                    const content = fs.readFileSync(file, 'utf8');
                    // Look for stub patterns
                    if (content.includes('// Simplified for now') ||
                        content.includes('// Placeholder') ||
                        content.includes('// TODO:') ||
                        content.match(/return\s+true;\s*\/\/\s*Simplified/gi)) {
                        return true;
                    }
                }
            }
            return false;
        }
        catch {
            return false;
        }
    }
    getAllSourceFiles(dirPath) {
        const files = [];
        try {
            const items = fs.readdirSync(dirPath);
            for (const item of items) {
                const fullPath = path.join(dirPath, item);
                const stat = fs.statSync(fullPath);
                if (stat.isDirectory() && !item.startsWith('.')) {
                    // Recursively search subdirectories
                    files.push(...this.getAllSourceFiles(fullPath));
                }
                else if (stat.isFile() && (item.endsWith('.ts') || item.endsWith('.js'))) {
                    files.push(fullPath);
                }
            }
        }
        catch {
            // If we can't read the directory, return empty array
        }
        return files;
    }
}
exports.CompletionModeOrchestrator = CompletionModeOrchestrator;
//# sourceMappingURL=CompletionModeOrchestrator.js.map