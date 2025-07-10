"use strict";
/**
 * Deployment Mode Orchestrator
 *
 * 🚀 DEPLOYMENT MODE: Prepare stable code for production deployment
 * Mission: Polish for production - ensure release-ready quality and deployment preparation
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.DeploymentModeOrchestrator = void 0;
const BaseModeOrchestrator_1 = require("./BaseModeOrchestrator");
class DeploymentModeOrchestrator extends BaseModeOrchestrator_1.BaseModeOrchestrator {
    getMode() {
        return BaseModeOrchestrator_1.DevelopmentMode.DEPLOYMENT;
    }
    getModeIcon() {
        return '🚀';
    }
    getModeDisplayName() {
        return 'Deployment Mode';
    }
    getGuardQuestions() {
        return [
            'Am I preparing for production deployment?',
            'Does this improve deployment readiness?',
            'Am I optimizing or adding features?',
            'Is this production prep or new development?',
            'Will this make the system more deployment-ready?',
        ];
    }
    getAllowedActions() {
        return [
            'Optimize build processes',
            'Configure production settings',
            'Set up deployment scripts',
            'Prepare release documentation',
            'Configure monitoring and logging',
            'Set up CI/CD pipelines',
            'Optimize performance for production',
            'Configure security settings',
            'Set up backup and recovery',
            'Prepare rollback procedures',
            'Configure load balancing',
            'Set up SSL certificates',
            'Optimize database for production',
            'Configure caching strategies',
            'Set up error tracking',
            'Prepare maintenance windows',
            'Configure environment variables',
            'Set up health checks',
        ];
    }
    getForbiddenActions() {
        return [
            'Adding new features',
            'Major architecture changes',
            'New integrations without testing',
            'Experimental implementations',
            'Breaking API changes',
            'Untested optimizations',
            'New dependencies without validation',
            'Major refactoring during deployment prep',
        ];
    }
    getSuccessCriteria() {
        return [
            {
                id: 'production_config_ready',
                description: 'Production configuration complete',
                completed: false,
                required: true,
            },
            {
                id: 'deployment_scripts_tested',
                description: 'Deployment scripts tested and validated',
                completed: false,
                required: true,
            },
            {
                id: 'security_hardened',
                description: 'Security settings configured for production',
                completed: false,
                required: true,
            },
            {
                id: 'monitoring_configured',
                description: 'Monitoring and alerting systems configured',
                completed: false,
                required: true,
            },
            {
                id: 'backup_strategy_implemented',
                description: 'Backup and recovery procedures in place',
                completed: false,
                required: true,
            },
            {
                id: 'performance_optimized',
                description: 'Performance optimized for production load',
                completed: false,
                required: false,
            },
            {
                id: 'rollback_tested',
                description: 'Rollback procedures tested and documented',
                completed: false,
                required: false,
            },
        ];
    }
    getRecommendedNextModes() {
        return [BaseModeOrchestrator_1.DevelopmentMode.MAINTENANCE];
    }
    createModeAgents() {
        return [
            {
                id: 'deployment_001',
                name: 'Production Configuration Agent',
                description: 'Configures production settings and environment variables',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'deployment_002',
                name: 'Deployment Script Agent',
                description: 'Creates and tests deployment automation scripts',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'deployment_003',
                name: 'Security Hardening Agent',
                description: 'Configures security settings for production deployment',
                mode: this.getMode(),
                status: 'pending',
                progress: 0,
                output: [],
                guardQuestions: this.getGuardQuestions(),
                allowedActions: this.getAllowedActions(),
                forbiddenActions: this.getForbiddenActions(),
            },
            {
                id: 'deployment_004',
                name: 'Monitoring & Alerting Agent',
                description: 'Sets up production monitoring and alerting systems',
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
exports.DeploymentModeOrchestrator = DeploymentModeOrchestrator;
//# sourceMappingURL=DeploymentModeOrchestrator.js.map