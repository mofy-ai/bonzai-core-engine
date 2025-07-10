"use strict";
/**
 * Cleanup Mode Orchestrator
 *
 * 🧹 CLEANUP MODE: Organize, optimize, and clean messy but functional code
 * Mission: Improve code quality without changing functionality
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.CleanupModeOrchestrator = void 0;
const BaseModeOrchestrator_1 = require("./BaseModeOrchestrator");
class CleanupModeOrchestrator extends BaseModeOrchestrator_1.BaseModeOrchestrator {
    getMode() {
        return BaseModeOrchestrator_1.DevelopmentMode.CLEANUP;
    }
    getModeIcon() {
        return '🧹';
    }
    getModeDisplayName() {
        return 'Cleanup Mode';
    }
    getGuardQuestions() {
        return [
            'Am I cleaning existing code or adding new functionality?',
            'Does this improve code quality without changing behavior?',
            'Am I organizing or expanding?',
            'Will this make the code more maintainable without new features?',
            'Is this refactoring existing code or building new code?',
        ];
    }
    getAllowedActions() {
        return [
            'Remove duplicate code/components',
            'Consolidate similar functionality',
            'Organize file/folder structure',
            'Standardize naming conventions',
            'Extract reusable utilities',
            'Fix linting errors',
            'Improve code formatting',
            'Add proper TypeScript types',
            'Improve error handling',
            'Add proper logging',
            'Remove unused imports/dependencies',
            'Optimize database queries',
            'Improve performance bottlenecks',
            'Reduce bundle sizes',
            'Memory leak fixes',
            'Code documentation improvements',
            'Extract constants and configuration',
            'Improve code readability',
            'Standardize code patterns',
        ];
    }
    getForbiddenActions() {
        return [
            'Adding new features',
            'Changing functionality behavior',
            'Major architecture rewrites',
            'New integrations',
            'Feature enhancements',
            'New components/modules',
            'New API endpoints',
            'New user interfaces',
            'Expanding scope',
            'Adding new dependencies (unless for cleanup)',
            'New business logic',
            'Feature requests',
        ];
    }
    getSuccessCriteria() {
        return [
            {
                id: 'no_duplicate_code',
                description: 'No duplicate code/components',
                completed: false,
                required: true,
            },
            {
                id: 'consistent_patterns',
                description: 'Consistent code patterns throughout',
                completed: false,
                required: true,
            },
            {
                id: 'clean_organization',
                description: 'Clean file/folder organization',
                completed: false,
                required: true,
            },
            {
                id: 'no_linting_errors',
                description: 'All linting errors resolved',
                completed: false,
                required: true,
            },
            {
                id: 'good_readability',
                description: 'Good code readability and maintainability',
                completed: false,
                required: true,
            },
            {
                id: 'performance_optimized',
                description: 'Performance improvements implemented',
                completed: false,
                required: false,
            },
        ];
    }
    getRecommendedNextModes() {
        return [BaseModeOrchestrator_1.DevelopmentMode.VALIDATION, BaseModeOrchestrator_1.DevelopmentMode.ENHANCEMENT];
    }
    createModeAgents() {
        return [
            {
                id: 'cleanup_001',
                name: 'Duplicate Code Eliminator',
                description: 'Find and remove duplicate code and components throughout the codebase',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'cleanup_002',
                name: 'File Organizer',
                description: 'Organize file and folder structure for better maintainability',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'cleanup_003',
                name: 'Linting Error Resolver',
                description: 'Fix all linting errors and improve code formatting',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'cleanup_004',
                name: 'TypeScript Type Enforcer',
                description: 'Add proper TypeScript types and improve type safety',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'cleanup_005',
                name: 'Unused Code Remover',
                description: 'Remove unused imports, dependencies, and dead code',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'cleanup_006',
                name: 'Pattern Standardizer',
                description: 'Standardize code patterns and naming conventions',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'cleanup_007',
                name: 'Utility Extractor',
                description: 'Extract reusable utilities and common functionality',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'cleanup_008',
                name: 'Performance Optimizer',
                description: 'Optimize performance bottlenecks and reduce bundle sizes',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'cleanup_009',
                name: 'Error Handling Improver',
                description: 'Improve error handling and logging throughout the application',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'cleanup_010',
                name: 'Code Documentation Enhancer',
                description: 'Improve code documentation and comments for maintainability',
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
        // Cleanup mode requires functional but messy code
        return true; // Can always clean up code
    }
}
exports.CleanupModeOrchestrator = CleanupModeOrchestrator;
//# sourceMappingURL=CleanupModeOrchestrator.js.map