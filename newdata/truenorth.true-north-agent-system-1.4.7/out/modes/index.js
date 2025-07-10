"use strict";
/**
 * Universal Development Modes System - Entry Point
 *
 * Exports all mode orchestrators and management classes
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ModeInfo = exports.EnhancementModeOrchestrator = exports.MaintenanceModeOrchestrator = exports.DeploymentModeOrchestrator = exports.ValidationModeOrchestrator = exports.CleanupModeOrchestrator = exports.CompletionModeOrchestrator = exports.BuildModeOrchestrator = exports.FoundationModeOrchestrator = exports.ModeManager = exports.ModeDetectionSystem = exports.BaseModeOrchestrator = exports.DevelopmentMode = void 0;
var BaseModeOrchestrator_1 = require("./BaseModeOrchestrator");
Object.defineProperty(exports, "DevelopmentMode", { enumerable: true, get: function () { return BaseModeOrchestrator_1.DevelopmentMode; } });
Object.defineProperty(exports, "BaseModeOrchestrator", { enumerable: true, get: function () { return BaseModeOrchestrator_1.BaseModeOrchestrator; } });
var ModeDetectionSystem_1 = require("./ModeDetectionSystem");
Object.defineProperty(exports, "ModeDetectionSystem", { enumerable: true, get: function () { return ModeDetectionSystem_1.ModeDetectionSystem; } });
var ModeManager_1 = require("./ModeManager");
Object.defineProperty(exports, "ModeManager", { enumerable: true, get: function () { return ModeManager_1.ModeManager; } });
// Mode Orchestrators
var FoundationModeOrchestrator_1 = require("./FoundationModeOrchestrator");
Object.defineProperty(exports, "FoundationModeOrchestrator", { enumerable: true, get: function () { return FoundationModeOrchestrator_1.FoundationModeOrchestrator; } });
var BuildModeOrchestrator_1 = require("./BuildModeOrchestrator");
Object.defineProperty(exports, "BuildModeOrchestrator", { enumerable: true, get: function () { return BuildModeOrchestrator_1.BuildModeOrchestrator; } });
var CompletionModeOrchestrator_1 = require("./CompletionModeOrchestrator");
Object.defineProperty(exports, "CompletionModeOrchestrator", { enumerable: true, get: function () { return CompletionModeOrchestrator_1.CompletionModeOrchestrator; } });
var CleanupModeOrchestrator_1 = require("./CleanupModeOrchestrator");
Object.defineProperty(exports, "CleanupModeOrchestrator", { enumerable: true, get: function () { return CleanupModeOrchestrator_1.CleanupModeOrchestrator; } });
var ValidationModeOrchestrator_1 = require("./ValidationModeOrchestrator");
Object.defineProperty(exports, "ValidationModeOrchestrator", { enumerable: true, get: function () { return ValidationModeOrchestrator_1.ValidationModeOrchestrator; } });
var DeploymentModeOrchestrator_1 = require("./DeploymentModeOrchestrator");
Object.defineProperty(exports, "DeploymentModeOrchestrator", { enumerable: true, get: function () { return DeploymentModeOrchestrator_1.DeploymentModeOrchestrator; } });
var MaintenanceModeOrchestrator_1 = require("./MaintenanceModeOrchestrator");
Object.defineProperty(exports, "MaintenanceModeOrchestrator", { enumerable: true, get: function () { return MaintenanceModeOrchestrator_1.MaintenanceModeOrchestrator; } });
var EnhancementModeOrchestrator_1 = require("./EnhancementModeOrchestrator");
Object.defineProperty(exports, "EnhancementModeOrchestrator", { enumerable: true, get: function () { return EnhancementModeOrchestrator_1.EnhancementModeOrchestrator; } });
const BaseModeOrchestrator_2 = require("./BaseModeOrchestrator");
// Mode Display Information
exports.ModeInfo = {
    [BaseModeOrchestrator_2.DevelopmentMode.FOUNDATION]: {
        icon: '🏗️',
        name: 'Foundation Mode',
        description: 'Get the basic development environment working from broken or new state',
        color: '#8B4513', // Brown
    },
    [BaseModeOrchestrator_2.DevelopmentMode.BUILD]: {
        icon: '🔧',
        name: 'Build Mode',
        description: 'Rapidly create new features and functionality from scratch',
        color: '#1E90FF', // Blue
    },
    [BaseModeOrchestrator_2.DevelopmentMode.COMPLETION]: {
        icon: '🏁',
        name: 'Completion Mode',
        description: 'Complete existing partial implementations - finish what was started',
        color: '#32CD32', // Green
    },
    [BaseModeOrchestrator_2.DevelopmentMode.CLEANUP]: {
        icon: '🧹',
        name: 'Cleanup Mode',
        description: 'Organize, optimize, and clean messy but functional code',
        color: '#FFD700', // Gold
    },
    [BaseModeOrchestrator_2.DevelopmentMode.VALIDATION]: {
        icon: '🧪',
        name: 'Validation Mode',
        description: 'Test and verify that everything works as expected',
        color: '#9932CC', // Purple
    },
    [BaseModeOrchestrator_2.DevelopmentMode.DEPLOYMENT]: {
        icon: '🚀',
        name: 'Deployment Mode',
        description: 'Get the application live in production successfully',
        color: '#FF4500', // Red-Orange
    },
    [BaseModeOrchestrator_2.DevelopmentMode.MAINTENANCE]: {
        icon: '🔄',
        name: 'Maintenance Mode',
        description: 'Keep production application running smoothly and address issues',
        color: '#708090', // Slate Gray
    },
    [BaseModeOrchestrator_2.DevelopmentMode.ENHANCEMENT]: {
        icon: '🎨',
        name: 'Enhancement Mode',
        description: 'Add new features and capabilities to existing working system',
        color: '#FF1493', // Deep Pink
    },
};
//# sourceMappingURL=index.js.map