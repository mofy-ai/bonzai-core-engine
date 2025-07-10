# ==================================================
# 🏗️ TrueNorth Infrastructure Variables
# ==================================================

variable "aws_region" {
  description = "AWS region for infrastructure deployment"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name (development, staging, production)"
  type        = string
  default     = "development"
  
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be one of: development, staging, production."
  }
}

# ==========================================
# Network Configuration
# ==========================================
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "private_subnets" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "public_subnets" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

# ==========================================
# Application Configuration
# ==========================================
variable "application_cpu" {
  description = "CPU units for the application container"
  type        = number
  default     = 512
}

variable "application_memory" {
  description = "Memory (MB) for the application container"
  type        = number
  default     = 1024
}

variable "application_replicas" {
  description = "Number of application replicas"
  type        = number
  default     = 2
}

variable "application_version" {
  description = "Version tag for the application Docker image"
  type        = string
  default     = "latest"
}

variable "docker_registry" {
  description = "Docker registry for application images"
  type        = string
  default     = "truenorth"
}

# ==========================================
# Auto Scaling Configuration
# ==========================================
variable "min_capacity" {
  description = "Minimum number of tasks"
  type        = number
  default     = 1
}

variable "max_capacity" {
  description = "Maximum number of tasks"
  type        = number
  default     = 10
}

# ==========================================
# Database Configuration
# ==========================================
variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Allocated storage for RDS instance (GB)"
  type        = number
  default     = 20
}

variable "db_max_allocated_storage" {
  description = "Maximum allocated storage for RDS instance (GB)"
  type        = number
  default     = 100
}

variable "postgresql_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "15.4"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "truenorth"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "truenorth"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
  
  validation {
    condition     = length(var.db_password) >= 12
    error_message = "Database password must be at least 12 characters long."
  }
  
  validation {
    condition     = can(regex("[A-Z]", var.db_password))
    error_message = "Database password must contain at least one uppercase letter."
  }
  
  validation {
    condition     = can(regex("[a-z]", var.db_password))
    error_message = "Database password must contain at least one lowercase letter."
  }
  
  validation {
    condition     = can(regex("[0-9]", var.db_password))
    error_message = "Database password must contain at least one number."
  }
  
  validation {
    condition     = can(regex("[^A-Za-z0-9]", var.db_password))
    error_message = "Database password must contain at least one special character."
  }
}

# ==========================================
# Cache Configuration
# ==========================================
variable "redis_node_type" {
  description = "ElastiCache Redis node type"
  type        = string
  default     = "cache.t3.micro"
}

# ==========================================
# Monitoring and Logging
# ==========================================
variable "log_retention_days" {
  description = "CloudWatch log retention period in days"
  type        = number
  default     = 7
}

variable "log_level" {
  description = "Application log level"
  type        = string
  default     = "info"
  
  validation {
    condition     = contains(["debug", "info", "warn", "error"], var.log_level)
    error_message = "Log level must be one of: debug, info, warn, error."
  }
}

# ==========================================
# Security Configuration
# ==========================================
variable "claude_api_key" {
  description = "Claude API key for the application"
  type        = string
  sensitive   = true
  
  validation {
    condition     = can(regex("^sk-ant-[a-zA-Z0-9\\-_]+$", var.claude_api_key))
    error_message = "Claude API key must start with 'sk-ant-' and contain only valid characters."
  }
  
  validation {
    condition     = length(var.claude_api_key) >= 20
    error_message = "Claude API key must be at least 20 characters long."
  }
}

# ==========================================
# Environment-specific Configurations
# ==========================================
variable "environment_configs" {
  description = "Environment-specific configuration overrides"
  type = map(object({
    application_cpu        = number
    application_memory     = number
    application_replicas   = number
    db_instance_class     = string
    redis_node_type       = string
    log_retention_days    = number
    min_capacity          = number
    max_capacity          = number
  }))
  
  default = {
    development = {
      application_cpu        = 256
      application_memory     = 512
      application_replicas   = 1
      db_instance_class     = "db.t3.micro"
      redis_node_type       = "cache.t3.micro"
      log_retention_days    = 3
      min_capacity          = 1
      max_capacity          = 3
    }
    
    staging = {
      application_cpu        = 512
      application_memory     = 1024
      application_replicas   = 2
      db_instance_class     = "db.t3.small"
      redis_node_type       = "cache.t3.small"
      log_retention_days    = 7
      min_capacity          = 1
      max_capacity          = 5
    }
    
    production = {
      application_cpu        = 1024
      application_memory     = 2048
      application_replicas   = 3
      db_instance_class     = "db.t3.medium"
      redis_node_type       = "cache.t3.medium"
      log_retention_days    = 30
      min_capacity          = 2
      max_capacity          = 20
    }
  }
}

# ==========================================
# Feature Flags
# ==========================================
variable "enable_monitoring" {
  description = "Enable monitoring stack (Prometheus, Grafana)"
  type        = bool
  default     = true
}

variable "enable_logging" {
  description = "Enable centralized logging (ELK stack)"
  type        = bool
  default     = true
}

variable "enable_backup" {
  description = "Enable automated backups"
  type        = bool
  default     = true
}

variable "enable_ssl" {
  description = "Enable SSL/TLS termination"
  type        = bool
  default     = true
}

variable "enable_waf" {
  description = "Enable Web Application Firewall"
  type        = bool
  default     = false
}

# ==========================================
# Cost Optimization
# ==========================================
variable "enable_spot_instances" {
  description = "Enable spot instances for cost optimization (non-production)"
  type        = bool
  default     = false
}

variable "enable_scheduled_scaling" {
  description = "Enable scheduled scaling for predictable workloads"
  type        = bool
  default     = false
}

# ==========================================
# Disaster Recovery
# ==========================================
variable "enable_multi_az" {
  description = "Enable multi-AZ deployment for high availability"
  type        = bool
  default     = false
}

variable "backup_retention_period" {
  description = "Database backup retention period (days)"
  type        = number
  default     = 7
}

variable "cross_region_backup" {
  description = "Enable cross-region backup replication"
  type        = bool
  default     = false
}

# ==========================================
# DNS and Domain Configuration
# ==========================================
variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = ""
}

variable "create_route53_records" {
  description = "Create Route53 DNS records"
  type        = bool
  default     = false
}

# ==========================================
# Compliance and Governance
# ==========================================
variable "enable_encryption_at_rest" {
  description = "Enable encryption at rest for all data stores"
  type        = bool
  default     = true
}

variable "enable_encryption_in_transit" {
  description = "Enable encryption in transit for all communications"
  type        = bool
  default     = true
}

variable "enable_audit_logging" {
  description = "Enable audit logging for compliance"
  type        = bool
  default     = true
}

variable "compliance_framework" {
  description = "Compliance framework to adhere to (SOC2, HIPAA, etc.)"
  type        = string
  default     = "SOC2"
}

# ==========================================
# Tags and Metadata
# ==========================================
variable "additional_tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "cost_center" {
  description = "Cost center for billing and accounting"
  type        = string
  default     = "Engineering"
}

variable "project_owner" {
  description = "Project owner for resource management"
  type        = string
  default     = "DevOps Team"
}

# ==========================================
# Notification Configuration
# ==========================================
variable "notification_email" {
  description = "Email address for infrastructure notifications"
  type        = string
  default     = "devops@truenorth.dev"
}

variable "slack_webhook_url" {
  description = "Slack webhook URL for notifications"
  type        = string
  default     = ""
  sensitive   = true
}

# ==========================================
# Resource Naming
# ==========================================
variable "resource_prefix" {
  description = "Prefix for resource names"
  type        = string
  default     = "truenorth"
}

variable "resource_suffix" {
  description = "Suffix for resource names"
  type        = string
  default     = ""
}