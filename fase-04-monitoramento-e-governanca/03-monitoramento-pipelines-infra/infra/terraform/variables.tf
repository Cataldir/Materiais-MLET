variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}

variable "location" {
  description = "Azure region for all resources"
  type        = string
  default     = "eastus2"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "mlmonitor"
}

variable "admin_email" {
  description = "Email for Grafana admin and alert notifications"
  type        = string
  default     = "admin@example.com"
}

variable "postgresql_admin_password" {
  description = "Password for PostgreSQL admin user"
  type        = string
  sensitive   = true
}
