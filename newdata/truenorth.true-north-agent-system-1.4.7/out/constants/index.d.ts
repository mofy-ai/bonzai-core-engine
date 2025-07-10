/**
 * Application-wide constants to eliminate magic numbers
 * Centralized location for all numeric and string constants used throughout the application
 */
export declare const timeConstants: {
    readonly MILLISECONDS_IN_SECOND: 1000;
    readonly SECONDS_IN_MINUTE: 60;
    readonly MINUTES_IN_HOUR: 60;
    readonly HOURS_IN_DAY: 24;
    readonly DAYS_IN_WEEK: 7;
    readonly WEEKS_IN_MONTH: 4;
    readonly MONTHS_IN_YEAR: 12;
    readonly DAYS_IN_MONTH: 30;
    readonly MAX_PARALLEL_AGENTS: 3;
    readonly COMPLETE_PERCENTAGE: 100;
    readonly CLAUDE_TIMEOUT_MS: 5400000;
    readonly CLAUDE_AUTH_TIMEOUT_MS: 30000;
    readonly CLAUDE_TEST_TIMEOUT_MS: 90000;
    readonly CLAUDE_QUICK_TIMEOUT_MS: 10000;
    readonly CLAUDE_ANALYSIS_TIMEOUT_MS: 1800000;
    readonly CLAUDE_AGENT_TIMEOUT_MS: 5400000;
    readonly CLAUDE_EXTENDED_TIMEOUT_MS: 7200000;
    readonly CLAUDE_RETRY_DELAY_MS: 2000;
    readonly CLAUDE_MAX_RETRIES: 3;
    readonly CLAUDE_EXPONENTIAL_BACKOFF_BASE: 2;
};
export declare const performanceThresholds: {
    readonly CPU_HIGH_USAGE_PERCENT: 85;
    readonly CPU_MODERATE_USAGE_PERCENT: 70;
    readonly CPU_LOW_USAGE_PERCENT: 50;
    readonly CPU_CRITICAL_USAGE_PERCENT: 95;
    readonly CPU_OPTIMIZATION_THRESHOLD: 90;
    readonly MEMORY_HIGH_USAGE_PERCENT: 85;
    readonly MEMORY_MODERATE_USAGE_PERCENT: 70;
    readonly MEMORY_LOW_USAGE_PERCENT: 50;
    readonly MEMORY_CRITICAL_USAGE_PERCENT: 95;
    readonly MEMORY_OPTIMIZATION_THRESHOLD: 80;
    readonly STORAGE_HIGH_USAGE_PERCENT: 85;
    readonly STORAGE_MODERATE_USAGE_PERCENT: 70;
    readonly STORAGE_LOW_USAGE_PERCENT: 50;
    readonly NETWORK_LATENCY_THRESHOLD_MS: 100;
    readonly NETWORK_BANDWIDTH_THRESHOLD_MBPS: 10;
};
export declare const efficiencyRatings: {
    readonly EXCELLENT_THRESHOLD: 90;
    readonly GOOD_THRESHOLD: 80;
    readonly MODERATE_THRESHOLD: 70;
    readonly POOR_THRESHOLD: 60;
    readonly CRITICAL_THRESHOLD: 50;
};
export declare const dataProcessing: {
    readonly BYTES_IN_KB: 1024;
    readonly BYTES_IN_MB: number;
    readonly BYTES_IN_GB: number;
    readonly MEGABYTES_IN_GB: 1024;
    readonly KILOBYTES_IN_MB: 1024;
    readonly DEFAULT_BATCH_SIZE: 100;
    readonly MAX_BATCH_SIZE: 1000;
    readonly MIN_BATCH_SIZE: 10;
    readonly DEFAULT_TIMEOUT_MS: 5000;
    readonly LONG_TIMEOUT_MS: 10000;
    readonly SHORT_TIMEOUT_MS: 1000;
};
export declare const monitoringIntervals: {
    readonly FAST_POLLING_MS: 1000;
    readonly NORMAL_POLLING_MS: 5000;
    readonly SLOW_POLLING_MS: 10000;
    readonly VERY_SLOW_POLLING_MS: 30000;
    readonly HEARTBEAT_INTERVAL_MS: 30000;
    readonly CLEANUP_INTERVAL_MS: 60000;
    readonly METRICS_COLLECTION_INTERVAL_SECONDS: 30;
    readonly CONTINUOUS_MONITORING_INTERVAL_SECONDS: 60;
};
export declare const SCORING: {
    readonly MIN_SCORE: 0;
    readonly MAX_SCORE: 100;
    readonly AVERAGE_SCORE: 50;
    readonly HIGH_PRIORITY_THRESHOLD: 80;
    readonly MEDIUM_PRIORITY_THRESHOLD: 60;
    readonly LOW_PRIORITY_THRESHOLD: 40;
    readonly PERCENTAGE_MULTIPLIER: 100;
    readonly DECIMAL_PRECISION: 2;
    readonly ROUNDING_PRECISION: 1;
};
export declare const NETWORK: {
    readonly DEFAULT_PORT: 3000;
    readonly WEBSOCKET_PORT: 8080;
    readonly SECURE_PORT: 443;
    readonly HTTP_PORT: 80;
    readonly CONNECTION_TIMEOUT_MS: 5000;
    readonly REQUEST_TIMEOUT_MS: 10000;
    readonly RETRY_ATTEMPTS: 3;
    readonly RETRY_DELAY_MS: 1000;
    readonly MAX_CONNECTIONS: 100;
    readonly MIN_CONNECTIONS: 1;
};
export declare const resourceLimits: {
    readonly MAX_MEMORY_USAGE_MB: 500;
    readonly MAX_CPU_CORES: 8;
    readonly MAX_PROCESS_COUNT: 50;
    readonly MAX_FILE_SIZE_MB: 100;
    readonly MIN_FREE_MEMORY_MB: 100;
    readonly MIN_FREE_STORAGE_GB: 1;
    readonly CACHE_SIZE_LIMIT_MB: 50;
    readonly LOG_FILE_SIZE_LIMIT_MB: 10;
};
export declare const ENERGY: {
    readonly CARBON_INTENSITY_THRESHOLD: 400;
    readonly RENEWABLE_ENERGY_TARGET_PERCENT: 80;
    readonly ENERGY_EFFICIENCY_TARGET_PERCENT: 85;
    readonly POWER_SAVING_THRESHOLD_PERCENT: 20;
    readonly LOW_POWER_MODE_THRESHOLD_PERCENT: 15;
    readonly CRITICAL_POWER_THRESHOLD_PERCENT: 10;
    readonly OPTIMIZATION_IMPACT_THRESHOLD_PERCENT: 5;
    readonly MINIMUM_SAVINGS_THRESHOLD_PERCENT: 1;
};
export declare const fileSystem: {
    readonly MAX_FILE_NAME_LENGTH: 255;
    readonly MAX_PATH_LENGTH: 4096;
    readonly DEFAULT_PERMISSION: 644;
    readonly EXECUTABLE_PERMISSION: 755;
    readonly TEMP_FILE_CLEANUP_HOURS: 24;
    readonly LOG_ROTATION_DAYS: 7;
    readonly BACKUP_RETENTION_DAYS: 30;
};
export declare const MATH: {
    readonly PERCENTAGE_BASE: 100;
    readonly DECIMAL_BASE: 10;
    readonly BINARY_BASE: 2;
    readonly HEX_BASE: 16;
    readonly FLOAT_PRECISION: 6;
    readonly CURRENCY_PRECISION: 2;
    readonly ZERO: 0;
    readonly ONE: 1;
    readonly NEGATIVE_ONE: -1;
    readonly TWO: 2;
    readonly THREE: 3;
    readonly FOUR: 4;
    readonly FIVE: 5;
    readonly TEN: 10;
    readonly FIFTEEN: 15;
    readonly TWENTY: 20;
    readonly THIRTY: 30;
    readonly FORTY: 40;
    readonly FIFTY: 50;
    readonly ONE_HUNDRED: 100;
    readonly FIVE_HUNDRED: 500;
    readonly ONE_THOUSAND: 1000;
    readonly NEGATIVE_FIVE_HUNDRED: -500;
    readonly NEGATIVE_ONE_THOUSAND: -1000;
    readonly NEGATIVE_TEN_THOUSAND: -10000;
};
export declare const API: {
    readonly DEFAULT_PAGE_SIZE: 20;
    readonly MAX_PAGE_SIZE: 100;
    readonly MIN_PAGE_SIZE: 1;
    readonly SUCCESS_STATUS: 200;
    readonly CREATED_STATUS: 201;
    readonly BAD_REQUEST_STATUS: 400;
    readonly UNAUTHORIZED_STATUS: 401;
    readonly NOT_FOUND_STATUS: 404;
    readonly SERVER_ERROR_STATUS: 500;
    readonly RATE_LIMIT_PER_MINUTE: 60;
    readonly RATE_LIMIT_PER_HOUR: 1000;
};
export declare const VALIDATION: {
    readonly MIN_PASSWORD_LENGTH: 8;
    readonly MAX_PASSWORD_LENGTH: 128;
    readonly MIN_USERNAME_LENGTH: 3;
    readonly MAX_USERNAME_LENGTH: 30;
    readonly EMAIL_MAX_LENGTH: 254;
    readonly PHONE_MIN_LENGTH: 10;
    readonly PHONE_MAX_LENGTH: 15;
    readonly MIN_AGE: 13;
    readonly MAX_AGE: 120;
};
export declare const OPTIMIZATION: {
    readonly MEMORY_CLEANUP_THRESHOLD_PERCENT: 80;
    readonly CACHE_EVICTION_THRESHOLD_PERCENT: 90;
    readonly COMPRESSION_RATIO_TARGET: 0.7;
    readonly PERFORMANCE_DEGRADATION_THRESHOLD: 0.3;
    readonly RESPONSE_TIME_THRESHOLD_MS: 500;
    readonly THROUGHPUT_THRESHOLD_OPS_PER_SEC: 1000;
    readonly AUTO_SCALING_CPU_THRESHOLD: 75;
    readonly AUTO_SCALING_MEMORY_THRESHOLD: 80;
    readonly AUTO_SCALING_COOLDOWN_MINUTES: 5;
};
//# sourceMappingURL=index.d.ts.map