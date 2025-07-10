"use strict";
/**
 * Enhancement Mode Orchestrator
 *
 * 🚀 ENHANCEMENT MODE: Explore new technologies and proof-of-concepts
 * Mission: Explore without breaking - enhance existing features with new capabilities
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.EnhancementModeOrchestrator = void 0;
const BaseModeOrchestrator_1 = require("./BaseModeOrchestrator");
class EnhancementModeOrchestrator extends BaseModeOrchestrator_1.BaseModeOrchestrator {
    getMode() {
        return BaseModeOrchestrator_1.DevelopmentMode.ENHANCEMENT;
    }
    getModeIcon() {
        return '✨';
    }
    getModeDisplayName() {
        return 'Enhancement Mode';
    }
    getGuardQuestions() {
        return [
            'Am I improving existing functionality?',
            'Does this enhance without breaking current features?',
            'Am I building new or improving existing?',
            'Is this enhancement or replacement?',
            'Will this add value to current users?',
        ];
    }
    getAllowedActions() {
        return [
            'Enhance existing features',
            'Improve user experience',
            'Add optional new capabilities',
            'Optimize performance',
            'Improve accessibility',
            'Add integrations that extend functionality',
            'Enhance error handling',
            'Improve data visualization',
            'Add export/import capabilities',
            'Enhance search functionality',
            'Improve mobile responsiveness',
            'Add keyboard shortcuts',
            'Enhance notifications',
            'Improve caching strategies',
            'Add analytics and insights',
            'Enhance security measures',
            'Improve API responses',
            'Add batch operations',
        ];
    }
    getForbiddenActions() {
        return [
            'Breaking existing APIs',
            'Removing existing functionality',
            'Major architecture overhauls',
            'Changing core business logic',
            'Experimental features in production',
            'Unproven technologies in core systems',
            'Changes that affect existing user workflows',
            'Database schema breaking changes',
        ];
    }
    getSuccessCriteria() {
        return [
            {
                id: 'features_enhanced',
                description: 'Existing features successfully enhanced',
                completed: false,
                required: true,
            },
            {
                id: 'backwards_compatible',
                description: 'All enhancements are backwards compatible',
                completed: false,
                required: true,
            },
            {
                id: 'user_experience_improved',
                description: 'User experience measurably improved',
                completed: false,
                required: true,
            },
            {
                id: 'performance_maintained',
                description: 'Performance maintained or improved',
                completed: false,
                required: true,
            },
            {
                id: 'existing_tests_pass',
                description: 'All existing tests continue to pass',
                completed: false,
                required: true,
            },
            {
                id: 'new_features_tested',
                description: 'New enhancements have comprehensive tests',
                completed: false,
                required: false,
            },
            {
                id: 'documentation_updated',
                description: 'Documentation updated for new enhancements',
                completed: false,
                required: false,
            },
            {
                id: 'user_feedback_positive',
                description: 'User feedback on enhancements is positive',
                completed: false,
                required: false,
            },
        ];
    }
    getRecommendedNextModes() {
        return [BaseModeOrchestrator_1.DevelopmentMode.VALIDATION, BaseModeOrchestrator_1.DevelopmentMode.MAINTENANCE];
    }
    createModeAgents() {
        return [
            {
                id: 'enhancement_001',
                name: 'UX Enhancement Agent',
                description: 'Improves user experience and interface design',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'enhancement_002',
                name: 'Performance Enhancement Agent',
                description: 'Optimizes system performance and responsiveness',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'enhancement_003',
                name: 'Feature Extension Agent',
                description: 'Extends existing features with new capabilities',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'enhancement_004',
                name: 'Integration Enhancement Agent',
                description: 'Improves and adds new system integrations',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'enhancement_005',
                name: 'Security Enhancement Agent',
                description: 'Enhances security features and protections',
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
}
exports.EnhancementModeOrchestrator = EnhancementModeOrchestrator;
//# sourceMappingURL=EnhancementModeOrchestrator.js.map