"use strict";
/**
 * Build Mode Orchestrator
 *
 * 🔧 BUILD MODE: Rapidly create new features and functionality from scratch
 * Mission: Build new features quickly without worrying about polish or perfection
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.BuildModeOrchestrator = void 0;
const BaseModeOrchestrator_1 = require("./BaseModeOrchestrator");
class BuildModeOrchestrator extends BaseModeOrchestrator_1.BaseModeOrchestrator {
    getMode() {
        return BaseModeOrchestrator_1.DevelopmentMode.BUILD;
    }
    getModeIcon() {
        return '🔧';
    }
    getModeDisplayName() {
        return 'Build Mode';
    }
    getGuardQuestions() {
        return [
            'Am I creating something new?',
            'Is this building toward a new feature?',
            'Am I polishing existing work instead of building?',
            'Does this expand functionality rather than perfect it?',
            'Is this rapid prototyping or careful refinement?',
        ];
    }
    getAllowedActions() {
        return [
            'Create new components/modules',
            'Build new API endpoints',
            'Implement new user interfaces',
            'Add new database tables/models',
            'Create new services/utilities',
            'Build basic feature structure',
            'Create minimal viable implementations',
            'Use placeholder data/content',
            'Focus on getting features working',
            'Quick and dirty solutions acceptable',
            'Add third-party libraries',
            'Implement external API connections',
            'Set up new services',
            'Configure new tools',
            'Rapid prototyping',
            'Create proof-of-concept implementations',
        ];
    }
    getForbiddenActions() {
        return [
            "Perfecting existing features (that's Completion Mode)",
            "Code cleanup/refactoring (that's Cleanup Mode)",
            "Extensive testing (that's Validation Mode)",
            'Production optimizations',
            'Fixing old bugs (unless blocking new features)',
            'Polishing user interfaces',
            'Performance optimization',
            'Code organization',
            'Documentation writing',
            'Error handling improvements',
            'Security hardening',
            'Accessibility improvements',
        ];
    }
    getSuccessCriteria() {
        return [
            {
                id: 'new_features_exist',
                description: 'New features exist and are accessible',
                completed: false,
                required: true,
            },
            {
                id: 'basic_functionality_works',
                description: 'Basic functionality works (even if rough)',
                completed: false,
                required: true,
            },
            {
                id: 'core_user_flows',
                description: 'Core user flows are possible',
                completed: false,
                required: true,
            },
            {
                id: 'system_integration',
                description: 'New features integrate with existing system',
                completed: false,
                required: true,
            },
            {
                id: 'ready_for_completion',
                description: 'Ready for completion/polish phase',
                completed: false,
                required: true,
            },
        ];
    }
    getRecommendedNextModes() {
        return [BaseModeOrchestrator_1.DevelopmentMode.COMPLETION, BaseModeOrchestrator_1.DevelopmentMode.CLEANUP];
    }
    createModeAgents() {
        return [
            {
                id: 'build_001',
                name: 'Feature Architect',
                description: 'Design and plan the structure of new features to be built',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_002',
                name: 'Component Creator',
                description: 'Build new UI components and interface elements rapidly',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_003',
                name: 'API Builder',
                description: 'Create new API endpoints and backend services',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_004',
                name: 'Database Designer',
                description: 'Design and implement new database tables and models',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_005',
                name: 'Integration Specialist',
                description: 'Connect new features with existing system and third-party services',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_006',
                name: 'User Flow Creator',
                description: 'Build basic user flows and navigation between new features',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_007',
                name: 'State Manager',
                description: 'Implement state management for new features',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_008',
                name: 'Service Creator',
                description: 'Build utility services and helper functions for new features',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_009',
                name: 'Prototype Assembler',
                description: 'Assemble built components into working prototypes',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_010',
                name: 'Feature Validator',
                description: 'Validate that new features work basically and are ready for completion',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_011',
                name: 'Rapid Prototyper',
                description: 'Create quick prototypes and proof-of-concept implementations',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_012',
                name: 'Feature Connector',
                description: 'Connect new features to make them accessible to users',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_013',
                name: 'Library Integrator',
                description: 'Add and configure third-party libraries needed for new features',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_014',
                name: 'External API Connector',
                description: 'Implement connections to external APIs and services',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'build_015',
                name: 'Build Completion Inspector',
                description: 'Inspect built features and prepare transition to completion mode',
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
        // Build mode requires a working development environment
        try {
            // Check if we can run dev server (Foundation mode success criteria)
            const hasWorkingEnv = this.checkDevEnvironment();
            return hasWorkingEnv;
        }
        catch {
            return false;
        }
    }
    checkDevEnvironment() {
        // This would check if development server can start
        // For now, assume it's working if we got to this mode
        return true;
    }
}
exports.BuildModeOrchestrator = BuildModeOrchestrator;
//# sourceMappingURL=BuildModeOrchestrator.js.map