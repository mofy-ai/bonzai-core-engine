"use strict";
/**
 * Mode Detection System - Universal Development Modes
 *
 * Automatically detects current project state and recommends appropriate
 * development mode based on the Universal Development Modes framework.
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
exports.ModeDetectionSystem = void 0;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const BaseModeOrchestrator_1 = require("./BaseModeOrchestrator");
class ModeDetectionSystem {
    constructor() {
        this.workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? process.cwd();
    }
    /**
     * Perform comprehensive project assessment
     */
    assessProject() {
        const assessment = {
            canRunDevServer: this.checkDevServerStatus(),
            hasAllFeatures: this.checkFeatureCompleteness(),
            featuresPartiallyComplete: this.checkPartialFeatures(),
            codeIsClean: this.checkCodeQuality(),
            hasTestedThoroughly: this.checkTestCoverage(),
            isLiveInProduction: this.checkProductionStatus(),
            productionIsStable: this.checkProductionStability(),
            needsNewFeatures: this.checkFeatureRequests(),
        };
        return assessment;
    }
    /**
     * Get mode recommendation based on assessment
     */
    recommendMode() {
        const assessment = this.assessProject();
        const reasoning = [];
        // Follow the Universal Development Modes decision tree
        // 1. Can you run the development server successfully?
        if (!assessment.canRunDevServer) {
            return {
                recommendedMode: BaseModeOrchestrator_1.DevelopmentMode.FOUNDATION,
                confidence: 95,
                reasoning: [
                    'Development server cannot start successfully',
                    'Foundation mode is needed to fix basic infrastructure',
                    'Must establish working development environment first',
                ],
                assessment,
                alternativeModes: [],
            };
        }
        reasoning.push('✅ Development server can run');
        // 2. Do you have the features you need?
        if (!assessment.hasAllFeatures) {
            if (assessment.featuresPartiallyComplete) {
                return {
                    recommendedMode: BaseModeOrchestrator_1.DevelopmentMode.COMPLETION,
                    confidence: 90,
                    reasoning: [
                        ...reasoning,
                        'Features exist but are incomplete',
                        'Completion mode needed to finish partial implementations',
                        'Should complete existing work before building new features',
                    ],
                    assessment,
                    alternativeModes: [BaseModeOrchestrator_1.DevelopmentMode.BUILD],
                };
            }
            else {
                return {
                    recommendedMode: BaseModeOrchestrator_1.DevelopmentMode.BUILD,
                    confidence: 85,
                    reasoning: [
                        ...reasoning,
                        'Missing required features',
                        'Build mode needed for rapid feature development',
                        'Focus on creating new functionality',
                    ],
                    assessment,
                    alternativeModes: [BaseModeOrchestrator_1.DevelopmentMode.COMPLETION],
                };
            }
        }
        reasoning.push('✅ All required features exist');
        // 3. Is your code clean and organized?
        if (!assessment.codeIsClean) {
            return {
                recommendedMode: BaseModeOrchestrator_1.DevelopmentMode.CLEANUP,
                confidence: 80,
                reasoning: [
                    ...reasoning,
                    'Code is functional but disorganized',
                    'Cleanup mode needed to improve maintainability',
                    'Should clean code before testing or deployment',
                ],
                assessment,
                alternativeModes: [BaseModeOrchestrator_1.DevelopmentMode.VALIDATION],
            };
        }
        reasoning.push('✅ Code is clean and organized');
        // 4. Have you tested everything thoroughly?
        if (!assessment.hasTestedThoroughly) {
            return {
                recommendedMode: BaseModeOrchestrator_1.DevelopmentMode.VALIDATION,
                confidence: 85,
                reasoning: [
                    ...reasoning,
                    'Features exist but need thorough testing',
                    'Validation mode needed to verify functionality',
                    'Must test before deploying to production',
                ],
                assessment,
                alternativeModes: [BaseModeOrchestrator_1.DevelopmentMode.DEPLOYMENT],
            };
        }
        reasoning.push('✅ Everything has been tested');
        // 5. Is the application live in production?
        if (!assessment.isLiveInProduction) {
            return {
                recommendedMode: BaseModeOrchestrator_1.DevelopmentMode.DEPLOYMENT,
                confidence: 90,
                reasoning: [
                    ...reasoning,
                    'Application is ready but not yet deployed',
                    'Deployment mode needed to get live in production',
                    'All preparation work has been completed',
                ],
                assessment,
                alternativeModes: [],
            };
        }
        reasoning.push('✅ Application is live in production');
        // 6. Is the production system stable?
        if (!assessment.productionIsStable) {
            return {
                recommendedMode: BaseModeOrchestrator_1.DevelopmentMode.MAINTENANCE,
                confidence: 95,
                reasoning: [
                    ...reasoning,
                    'Production system has stability issues',
                    'Maintenance mode needed to fix production problems',
                    'Must stabilize before adding new features',
                ],
                assessment,
                alternativeModes: [],
            };
        }
        reasoning.push('✅ Production system is stable');
        // 7. Need new features or just maintaining?
        if (assessment.needsNewFeatures) {
            return {
                recommendedMode: BaseModeOrchestrator_1.DevelopmentMode.ENHANCEMENT,
                confidence: 75,
                reasoning: [
                    ...reasoning,
                    'Stable production system ready for new features',
                    'Enhancement mode for adding capabilities to working system',
                    'Can safely expand functionality',
                ],
                assessment,
                alternativeModes: [BaseModeOrchestrator_1.DevelopmentMode.MAINTENANCE],
            };
        }
        // Default to maintenance if everything is stable
        return {
            recommendedMode: BaseModeOrchestrator_1.DevelopmentMode.MAINTENANCE,
            confidence: 70,
            reasoning: [
                ...reasoning,
                'System is stable and functioning well',
                'Maintenance mode for ongoing care and monitoring',
                'Ready to enhance when new requirements arise',
            ],
            assessment,
            alternativeModes: [BaseModeOrchestrator_1.DevelopmentMode.ENHANCEMENT],
        };
    }
    /**
     * Check if development server can start
     */
    checkDevServerStatus() {
        try {
            // Check for common package.json scripts
            const packageJsonPath = path.join(this.workspaceRoot, 'package.json');
            if (fs.existsSync(packageJsonPath)) {
                const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
                const scripts = packageJson.scripts ?? {};
                // Check for dev scripts
                const hasDevScript = scripts.dev ?? scripts.start ?? scripts.serve;
                if (!hasDevScript) {
                    return false;
                }
                // Check for major compilation errors (TypeScript, ESLint, etc.)
                const hasCompilationErrors = this.checkCompilationErrors();
                return !hasCompilationErrors;
            }
            // Check for other project types (Python, etc.)
            return this.checkOtherProjectTypes();
        }
        catch {
            return false;
        }
    }
    /**
     * Check for TypeScript/compilation errors
     */
    checkCompilationErrors() {
        try {
            // Check for TypeScript config
            const tsconfigPath = path.join(this.workspaceRoot, 'tsconfig.json');
            if (fs.existsSync(tsconfigPath)) {
                // Could run tsc --noEmit to check for errors
                // For now, assume if tsconfig exists and we got here, it might work
                return false; // Assume no compilation errors for simplicity
            }
            return false;
        }
        catch {
            return true; // Assume errors if we can't check
        }
    }
    /**
     * Check for other project types (Python, etc.)
     */
    checkOtherProjectTypes() {
        // Check for Python projects
        const pythonFiles = ['manage.py', 'app.py', 'main.py', 'requirements.txt'];
        const hasPython = pythonFiles.some(file => fs.existsSync(path.join(this.workspaceRoot, file)));
        if (hasPython) {
            return true;
        }
        // Check for other frameworks
        const frameworkFiles = ['Cargo.toml', 'go.mod', 'composer.json'];
        return frameworkFiles.some(file => fs.existsSync(path.join(this.workspaceRoot, file)));
    }
    /**
     * Check if all required features exist
     */
    checkFeatureCompleteness() {
        // This is a heuristic - in a real implementation, this could:
        // - Check user stories/requirements tracking
        // - Analyze TODO comments
        // - Check if main user flows are implemented
        const todoCount = this.countTodoComments();
        const incompleteFeatures = this.countIncompleteFeatures();
        const todoCompleteThreshold = 10;
        const incompleteFeaturesThreshold = 3;
        // If lots of TODOs or incomplete features, assume features are missing
        return todoCount < todoCompleteThreshold && incompleteFeatures < incompleteFeaturesThreshold;
    }
    /**
     * Check if features are partially complete
     */
    checkPartialFeatures() {
        const todoCount = this.countTodoComments();
        this.countIncompleteFeatures(); // For future feature implementation
        const todoThreshold = 20;
        // If some TODOs but not too many, assume partial completion
        return todoCount > 0 && todoCount < todoThreshold;
    }
    /**
     * Check code quality and organization
     */
    checkCodeQuality() {
        try {
            // Check for linting errors
            const hasLintConfig = fs.existsSync(path.join(this.workspaceRoot, '.eslintrc.json')) ||
                fs.existsSync(path.join(this.workspaceRoot, '.eslintrc.js'));
            // Check for duplicate code patterns
            const duplicateCount = this.countDuplicateCode();
            // Check file organization
            const isWellOrganized = this.checkFileOrganization();
            const duplicateCodeThreshold = 5;
            return hasLintConfig && duplicateCount < duplicateCodeThreshold && isWellOrganized;
        }
        catch {
            return false;
        }
    }
    /**
     * Check test coverage and validation
     */
    checkTestCoverage() {
        try {
            // Check for test files
            const testDirs = ['test', 'tests', '__tests__', 'spec'];
            const hasTestDir = testDirs.some(dir => fs.existsSync(path.join(this.workspaceRoot, dir)));
            // Check for test configuration
            const testConfigs = ['jest.config.js', 'vitest.config.ts', 'playwright.config.ts'];
            const hasTestConfig = testConfigs.some(config => fs.existsSync(path.join(this.workspaceRoot, config)));
            return hasTestDir && hasTestConfig;
        }
        catch {
            return false;
        }
    }
    /**
     * Check if application is deployed to production
     */
    checkProductionStatus() {
        // Check for deployment configuration
        const deploymentFiles = [
            'Dockerfile',
            'docker-compose.yml',
            'vercel.json',
            'netlify.toml',
            '.github/workflows',
        ];
        const hasDeploymentConfig = deploymentFiles.some(file => fs.existsSync(path.join(this.workspaceRoot, file)));
        // This is a heuristic - in reality, you'd check actual deployment status
        return hasDeploymentConfig && this.checkForProductionEnv();
    }
    /**
     * Check production stability
     */
    checkProductionStability() {
        // Check for monitoring/error tracking
        // Check for monitoring/error tracking
        // Future implementation will check these indicators
        const monitoringTools = ['sentry', 'datadog', 'newrelic', 'bugsnag'];
        // This would normally check actual production metrics
        // For now, assume stable if monitoring is set up
        // Future: implement actual monitoring checks with monitoringTools
        void monitoringTools; // Prevent unused variable warning
        return true; // Simplified for demo
    }
    /**
     * Check if new features are needed
     */
    checkFeatureRequests() {
        // Check for feature request indicators
        const featureIndicators = this.countFeatureRequests();
        const roadmapExists = fs.existsSync(path.join(this.workspaceRoot, 'ROADMAP.md'));
        return featureIndicators > 0 || roadmapExists;
    }
    // Helper methods for heuristic analysis
    countTodoComments() {
        // Simple implementation - count TODO comments in source files
        try {
            const sourceFiles = this.findSourceFiles();
            let todoCount = 0;
            const maxFilesToCheck = 50;
            for (const file of sourceFiles.slice(0, maxFilesToCheck)) {
                // Limit for performance
                const content = fs.readFileSync(file, 'utf8');
                const matches = content.match(/TODO|FIXME|HACK|XXX/gi);
                todoCount += matches?.length ?? 0;
            }
            return todoCount;
        }
        catch {
            return 0;
        }
    }
    countIncompleteFeatures() {
        // Count incomplete feature indicators
        try {
            const sourceFiles = this.findSourceFiles();
            let incompleteCount = 0;
            const maxIncompleteFilesCheck = 30;
            for (const file of sourceFiles.slice(0, maxIncompleteFilesCheck)) {
                // Limit for performance
                const content = fs.readFileSync(file, 'utf8');
                const matches = content.match(/incomplete|partial|work.in.progress|wip/gi);
                incompleteCount += matches?.length ?? 0;
            }
            return incompleteCount;
        }
        catch {
            return 0;
        }
    }
    countDuplicateCode() {
        // Simplified duplicate detection
        return 2; // Placeholder
    }
    checkFileOrganization() {
        // Check if files are well organized in directories
        const srcExists = fs.existsSync(path.join(this.workspaceRoot, 'src'));
        const componentsExists = fs.existsSync(path.join(this.workspaceRoot, 'src/components')) ||
            fs.existsSync(path.join(this.workspaceRoot, 'components'));
        return srcExists && componentsExists;
    }
    checkForProductionEnv() {
        const envFiles = ['.env.production', '.env.prod'];
        return envFiles.some(file => fs.existsSync(path.join(this.workspaceRoot, file)));
    }
    countFeatureRequests() {
        // Check for feature request indicators in issues, docs, etc.
        const featureFiles = ['FEATURES.md', 'ROADMAP.md', 'BACKLOG.md'];
        let count = 0;
        for (const file of featureFiles) {
            if (fs.existsSync(path.join(this.workspaceRoot, file))) {
                const featuresPerFile = 3;
                count += featuresPerFile; // Assume multiple features per file
            }
        }
        return count;
    }
    findSourceFiles() {
        const files = [];
        const extensions = ['.ts', '.js', '.tsx', '.jsx', '.py', '.java', '.cpp', '.c'];
        const findFiles = (dir, depth = 0) => {
            const maxDepth = 3;
            if (depth > maxDepth) {
                return; // Limit depth for performance
            }
            try {
                const items = fs.readdirSync(dir);
                for (const item of items) {
                    if (item.startsWith('.') || item === 'node_modules') {
                        continue;
                    }
                    const fullPath = path.join(dir, item);
                    const stat = fs.statSync(fullPath);
                    if (stat.isDirectory()) {
                        findFiles(fullPath, depth + 1);
                    }
                    else if (extensions.some(ext => item.endsWith(ext))) {
                        files.push(fullPath);
                    }
                }
            }
            catch {
                // Ignore errors
            }
        };
        findFiles(this.workspaceRoot);
        return files;
    }
}
exports.ModeDetectionSystem = ModeDetectionSystem;
//# sourceMappingURL=ModeDetectionSystem.js.map