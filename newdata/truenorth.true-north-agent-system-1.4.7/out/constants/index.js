"use strict";
/**
 * Application-wide constants to eliminate magic numbers
 * Centralized location for all numeric and string constants used throughout the application
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.OPTIMIZATION = exports.VALIDATION = exports.API = exports.MATH = exports.fileSystem = exports.ENERGY = exports.resourceLimits = exports.NETWORK = exports.SCORING = exports.monitoringIntervals = exports.dataProcessing = exports.efficiencyRatings = exports.performanceThresholds = exports.timeConstants = void 0;
// Time constants
exports.timeConstants = {
    MILLISECONDS_IN_SECOND: 1000,
    SECONDS_IN_MINUTE: 60,
    MINUTES_IN_HOUR: 60,
    HOURS_IN_DAY: 24,
    DAYS_IN_WEEK: 7,
    WEEKS_IN_MONTH: 4,
    MONTHS_IN_YEAR: 12,
    DAYS_IN_MONTH: 30,
    MAX_PARALLEL_AGENTS: 3,
    COMPLETE_PERCENTAGE: 100,
    CLAUDE_TIMEOUT_MS: 5400000, // 90 minutes for complex operations (extended for long-running agents)
    CLAUDE_AUTH_TIMEOUT_MS: 30000, // 30 seconds for auth checks
    CLAUDE_TEST_TIMEOUT_MS: 90000, // 90 seconds for test commands
    CLAUDE_QUICK_TIMEOUT_MS: 10000, // 10 seconds for version checks
    CLAUDE_ANALYSIS_TIMEOUT_MS: 1800000, // 30 minutes for project analysis
    CLAUDE_AGENT_TIMEOUT_MS: 5400000, // 90 minutes for agent operations
    CLAUDE_EXTENDED_TIMEOUT_MS: 7200000, // 120 minutes for extremely long operations
    CLAUDE_RETRY_DELAY_MS: 2000, // 2 seconds between retries (base delay)
    CLAUDE_MAX_RETRIES: 3, // Maximum retry attempts
    CLAUDE_EXPONENTIAL_BACKOFF_BASE: 2, // Base multiplier for exponential backoff
};
// Performance thresholds
exports.performanceThresholds = {
    CPU_HIGH_USAGE_PERCENT: 85,
    CPU_MODERATE_USAGE_PERCENT: 70,
    CPU_LOW_USAGE_PERCENT: 50,
    CPU_CRITICAL_USAGE_PERCENT: 95,
    CPU_OPTIMIZATION_THRESHOLD: 90,
    MEMORY_HIGH_USAGE_PERCENT: 85,
    MEMORY_MODERATE_USAGE_PERCENT: 70,
    MEMORY_LOW_USAGE_PERCENT: 50,
    MEMORY_CRITICAL_USAGE_PERCENT: 95,
    MEMORY_OPTIMIZATION_THRESHOLD: 80,
    STORAGE_HIGH_USAGE_PERCENT: 85,
    STORAGE_MODERATE_USAGE_PERCENT: 70,
    STORAGE_LOW_USAGE_PERCENT: 50,
    NETWORK_LATENCY_THRESHOLD_MS: 100,
    NETWORK_BANDWIDTH_THRESHOLD_MBPS: 10,
};
// Efficiency ratings
exports.efficiencyRatings = {
    EXCELLENT_THRESHOLD: 90,
    GOOD_THRESHOLD: 80,
    MODERATE_THRESHOLD: 70,
    POOR_THRESHOLD: 60,
    CRITICAL_THRESHOLD: 50,
};
// Data processing constants
const kbSize = 1024;
exports.dataProcessing = {
    BYTES_IN_KB: kbSize,
    BYTES_IN_MB: kbSize * kbSize,
    BYTES_IN_GB: kbSize * kbSize * kbSize,
    MEGABYTES_IN_GB: kbSize,
    KILOBYTES_IN_MB: kbSize,
    DEFAULT_BATCH_SIZE: 100,
    MAX_BATCH_SIZE: 1000,
    MIN_BATCH_SIZE: 10,
    DEFAULT_TIMEOUT_MS: 5000,
    LONG_TIMEOUT_MS: 10000,
    SHORT_TIMEOUT_MS: 1000,
};
// Monitoring intervals
exports.monitoringIntervals = {
    FAST_POLLING_MS: 1000,
    NORMAL_POLLING_MS: 5000,
    SLOW_POLLING_MS: 10000,
    VERY_SLOW_POLLING_MS: 30000,
    HEARTBEAT_INTERVAL_MS: 30000,
    CLEANUP_INTERVAL_MS: 60000,
    METRICS_COLLECTION_INTERVAL_SECONDS: 30,
    CONTINUOUS_MONITORING_INTERVAL_SECONDS: 60,
};
// Scoring and rating constants
exports.SCORING = {
    MIN_SCORE: 0,
    MAX_SCORE: 100,
    AVERAGE_SCORE: 50,
    HIGH_PRIORITY_THRESHOLD: 80,
    MEDIUM_PRIORITY_THRESHOLD: 60,
    LOW_PRIORITY_THRESHOLD: 40,
    PERCENTAGE_MULTIPLIER: 100,
    DECIMAL_PRECISION: 2,
    ROUNDING_PRECISION: 1,
};
// Network and connectivity
exports.NETWORK = {
    DEFAULT_PORT: 3000,
    WEBSOCKET_PORT: 8080,
    SECURE_PORT: 443,
    HTTP_PORT: 80,
    CONNECTION_TIMEOUT_MS: 5000,
    REQUEST_TIMEOUT_MS: 10000,
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY_MS: 1000,
    MAX_CONNECTIONS: 100,
    MIN_CONNECTIONS: 1,
};
// Resource limits
exports.resourceLimits = {
    MAX_MEMORY_USAGE_MB: 500,
    MAX_CPU_CORES: 8,
    MAX_PROCESS_COUNT: 50,
    MAX_FILE_SIZE_MB: 100,
    MIN_FREE_MEMORY_MB: 100,
    MIN_FREE_STORAGE_GB: 1,
    CACHE_SIZE_LIMIT_MB: 50,
    LOG_FILE_SIZE_LIMIT_MB: 10,
};
// Energy and sustainability
exports.ENERGY = {
    CARBON_INTENSITY_THRESHOLD: 400, // g CO2/kWh
    RENEWABLE_ENERGY_TARGET_PERCENT: 80,
    ENERGY_EFFICIENCY_TARGET_PERCENT: 85,
    POWER_SAVING_THRESHOLD_PERCENT: 20,
    LOW_POWER_MODE_THRESHOLD_PERCENT: 15,
    CRITICAL_POWER_THRESHOLD_PERCENT: 10,
    OPTIMIZATION_IMPACT_THRESHOLD_PERCENT: 5,
    MINIMUM_SAVINGS_THRESHOLD_PERCENT: 1,
};
// File system constants
exports.fileSystem = {
    MAX_FILE_NAME_LENGTH: 255,
    MAX_PATH_LENGTH: 4096,
    DEFAULT_PERMISSION: 644,
    EXECUTABLE_PERMISSION: 755,
    TEMP_FILE_CLEANUP_HOURS: 24,
    LOG_ROTATION_DAYS: 7,
    BACKUP_RETENTION_DAYS: 30,
};
// Mathematical constants
exports.MATH = {
    PERCENTAGE_BASE: 100,
    DECIMAL_BASE: 10,
    BINARY_BASE: 2,
    HEX_BASE: 16,
    FLOAT_PRECISION: 6,
    CURRENCY_PRECISION: 2,
    ZERO: 0,
    ONE: 1,
    NEGATIVE_ONE: -1,
    TWO: 2,
    THREE: 3,
    FOUR: 4,
    FIVE: 5,
    TEN: 10,
    FIFTEEN: 15,
    TWENTY: 20,
    THIRTY: 30,
    FORTY: 40,
    FIFTY: 50,
    ONE_HUNDRED: 100,
    FIVE_HUNDRED: 500,
    ONE_THOUSAND: 1000,
    NEGATIVE_FIVE_HUNDRED: -500,
    NEGATIVE_ONE_THOUSAND: -1000,
    NEGATIVE_TEN_THOUSAND: -10000,
};
// API and response constants
exports.API = {
    DEFAULT_PAGE_SIZE: 20,
    MAX_PAGE_SIZE: 100,
    MIN_PAGE_SIZE: 1,
    SUCCESS_STATUS: 200,
    CREATED_STATUS: 201,
    BAD_REQUEST_STATUS: 400,
    UNAUTHORIZED_STATUS: 401,
    NOT_FOUND_STATUS: 404,
    SERVER_ERROR_STATUS: 500,
    RATE_LIMIT_PER_MINUTE: 60,
    RATE_LIMIT_PER_HOUR: 1000,
};
// Validation constants
exports.VALIDATION = {
    MIN_PASSWORD_LENGTH: 8,
    MAX_PASSWORD_LENGTH: 128,
    MIN_USERNAME_LENGTH: 3,
    MAX_USERNAME_LENGTH: 30,
    EMAIL_MAX_LENGTH: 254,
    PHONE_MIN_LENGTH: 10,
    PHONE_MAX_LENGTH: 15,
    MIN_AGE: 13,
    MAX_AGE: 120,
};
// Optimization constants
exports.OPTIMIZATION = {
    MEMORY_CLEANUP_THRESHOLD_PERCENT: 80,
    CACHE_EVICTION_THRESHOLD_PERCENT: 90,
    COMPRESSION_RATIO_TARGET: 0.7,
    PERFORMANCE_DEGRADATION_THRESHOLD: 0.3,
    RESPONSE_TIME_THRESHOLD_MS: 500,
    THROUGHPUT_THRESHOLD_OPS_PER_SEC: 1000,
    AUTO_SCALING_CPU_THRESHOLD: 75,
    AUTO_SCALING_MEMORY_THRESHOLD: 80,
    AUTO_SCALING_COOLDOWN_MINUTES: 5,
};
//# sourceMappingURL=index.js.map