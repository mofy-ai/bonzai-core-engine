"use strict";
/**
 * Validation Mode Orchestrator
 *
 * 🧪 VALIDATION MODE: Test and verify that everything works as expected
 * Mission: Thoroughly test and validate all functionality before deployment
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ValidationModeOrchestrator = void 0;
const BaseModeOrchestrator_1 = require("./BaseModeOrchestrator");
class ValidationModeOrchestrator extends BaseModeOrchestrator_1.BaseModeOrchestrator {
    getMode() {
        return BaseModeOrchestrator_1.DevelopmentMode.VALIDATION;
    }
    getModeIcon() {
        return '🧪';
    }
    getModeDisplayName() {
        return 'Validation Mode';
    }
    getGuardQuestions() {
        return [
            'Am I testing/fixing existing functionality?',
            'Does this verify or improve existing features?',
            'Am I adding scope or validating scope?',
            'Is this testing what exists or building something new?',
            'Will this ensure quality without expanding features?',
        ];
    }
    getAllowedActions() {
        return [
            'Manual testing of all features',
            'Write automated tests',
            'Test edge cases',
            'Cross-browser/device testing',
            'Performance testing',
            'Verify user flows work end-to-end',
            'Check error handling',
            'Validate data integrity',
            'Confirm security measures',
            'Test integrations',
            'Fix discovered bugs',
            'Address usability issues',
            'Resolve compatibility problems',
            'Fix edge case failures',
        ];
    }
    getForbiddenActions() {
        return [
            'Adding new features',
            'Major code refactoring',
            'New integrations',
            'Architecture changes',
            'Feature enhancements',
            'Building new components',
            'Creating new functionality',
        ];
    }
    getSuccessCriteria() {
        return [
            {
                id: 'all_features_tested',
                description: 'All features tested and working',
                completed: false,
                required: true,
            },
            {
                id: 'edge_cases_handled',
                description: 'Edge cases handled properly',
                completed: false,
                required: true,
            },
            {
                id: 'no_critical_bugs',
                description: 'No critical bugs',
                completed: false,
                required: true,
            },
            {
                id: 'acceptable_performance',
                description: 'Performance is acceptable',
                completed: false,
                required: true,
            },
            {
                id: 'security_addressed',
                description: 'Security vulnerabilities addressed',
                completed: false,
                required: true,
            },
            {
                id: 'ready_for_production',
                description: 'Ready for production',
                completed: false,
                required: true,
            },
        ];
    }
    getRecommendedNextModes() {
        return [BaseModeOrchestrator_1.DevelopmentMode.DEPLOYMENT];
    }
    createModeAgents() {
        return [
            {
                id: 'validation_001',
                name: 'Feature Tester',
                description: 'Test all features thoroughly and document findings',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'validation_002',
                name: 'Edge Case Validator',
                description: 'Test edge cases and error conditions',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'validation_003',
                name: 'Bug Hunter',
                description: 'Find and fix bugs discovered during testing',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'validation_004',
                name: 'Performance Validator',
                description: 'Test and validate application performance',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'validation_005',
                name: 'Security Validator',
                description: 'Test security measures and address vulnerabilities',
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
exports.ValidationModeOrchestrator = ValidationModeOrchestrator;
//# sourceMappingURL=ValidationModeOrchestrator.js.map