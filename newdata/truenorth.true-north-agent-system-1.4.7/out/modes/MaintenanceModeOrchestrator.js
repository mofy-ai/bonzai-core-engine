"use strict";
/**
 * Maintenance Mode Orchestrator
 *
 * 🔧 MAINTENANCE MODE: Maintain and improve existing stable codebase
 * Mission: Keep it running smoothly - ongoing maintenance, monitoring, and incremental improvements
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.MaintenanceModeOrchestrator = void 0;
const BaseModeOrchestrator_1 = require("./BaseModeOrchestrator");
class MaintenanceModeOrchestrator extends BaseModeOrchestrator_1.BaseModeOrchestrator {
    getMode() {
        return BaseModeOrchestrator_1.DevelopmentMode.MAINTENANCE;
    }
    getModeIcon() {
        return '🔧';
    }
    getModeDisplayName() {
        return 'Maintenance Mode';
    }
    getGuardQuestions() {
        return [
            'Am I maintaining existing functionality?',
            'Does this keep the system running smoothly?',
            'Am I fixing or expanding?',
            'Is this maintenance or development?',
            'Will this preserve current stability?',
        ];
    }
    getAllowedActions() {
        return [
            'Fix bugs and issues',
            'Update dependencies',
            'Improve performance',
            'Optimize existing code',
            'Refactor for maintainability',
            'Update documentation',
            'Monitor system health',
            'Apply security patches',
            'Database maintenance',
            'Server maintenance',
            'Log analysis and cleanup',
            'Backup verification',
            'System monitoring improvements',
            'Error handling improvements',
            'Code quality improvements',
            'Technical debt reduction',
            'Infrastructure updates',
            'Configuration tuning',
        ];
    }
    getForbiddenActions() {
        return [
            'Adding major new features',
            'Changing core architecture',
            'Breaking existing APIs',
            'Removing existing functionality',
            'Major UI/UX overhauls',
            'Experimental implementations',
            'Unproven technologies',
            'Major database schema changes',
        ];
    }
    getSuccessCriteria() {
        return [
            {
                id: 'system_stable',
                description: 'System running stably with minimal issues',
                completed: false,
                required: true,
            },
            {
                id: 'dependencies_current',
                description: 'Dependencies up to date and secure',
                completed: false,
                required: true,
            },
            {
                id: 'monitoring_healthy',
                description: 'Monitoring systems showing healthy metrics',
                completed: false,
                required: true,
            },
            {
                id: 'backups_verified',
                description: 'Backup systems verified and working',
                completed: false,
                required: true,
            },
            {
                id: 'security_patches_applied',
                description: 'All security patches applied',
                completed: false,
                required: true,
            },
            {
                id: 'performance_optimized',
                description: 'Performance within acceptable ranges',
                completed: false,
                required: false,
            },
            {
                id: 'documentation_current',
                description: 'Documentation updated and accurate',
                completed: false,
                required: false,
            },
            {
                id: 'technical_debt_reduced',
                description: 'Technical debt reduced systematically',
                completed: false,
                required: false,
            },
        ];
    }
    getRecommendedNextModes() {
        return [BaseModeOrchestrator_1.DevelopmentMode.ENHANCEMENT, BaseModeOrchestrator_1.DevelopmentMode.CLEANUP];
    }
    createModeAgents() {
        return [
            {
                id: 'maintenance_001',
                name: 'Bug Fix Agent',
                description: 'Identifies and fixes bugs in existing functionality',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'maintenance_002',
                name: 'Dependency Management Agent',
                description: 'Manages and updates project dependencies safely',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'maintenance_003',
                name: 'Performance Monitoring Agent',
                description: 'Monitors and improves system performance',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'maintenance_004',
                name: 'Security Maintenance Agent',
                description: 'Applies security patches and monitors for vulnerabilities',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'maintenance_005',
                name: 'Infrastructure Maintenance Agent',
                description: 'Maintains and monitors system infrastructure',
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
exports.MaintenanceModeOrchestrator = MaintenanceModeOrchestrator;
//# sourceMappingURL=MaintenanceModeOrchestrator.js.map