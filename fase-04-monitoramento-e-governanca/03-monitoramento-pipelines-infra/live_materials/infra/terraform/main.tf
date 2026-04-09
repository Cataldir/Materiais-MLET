# =============================================================================
# Resource Group
# =============================================================================

resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location

  tags = {
    project     = var.project_name
    environment = var.environment
    managed_by  = "terraform"
  }
}

# =============================================================================
# Log Analytics Workspace (required for Monitor and Container Apps)
# =============================================================================

resource "azurerm_log_analytics_workspace" "main" {
  name                = "log-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30

  tags = azurerm_resource_group.main.tags
}

# =============================================================================
# Azure Monitor Workspace (Managed Prometheus)
# =============================================================================

resource "azurerm_monitor_workspace" "prometheus" {
  name                = "mon-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  tags = azurerm_resource_group.main.tags
}

# =============================================================================
# Azure Managed Grafana
# =============================================================================

resource "azurerm_dashboard_grafana" "main" {
  name                              = "grafana-${var.project_name}-${var.environment}"
  location                          = azurerm_resource_group.main.location
  resource_group_name               = azurerm_resource_group.main.name
  grafana_major_version             = 10
  api_key_enabled                   = true
  deterministic_outbound_ip_enabled = false
  public_network_access_enabled     = true

  azure_monitor_workspace_integrations {
    resource_id = azurerm_monitor_workspace.prometheus.id
  }

  identity {
    type = "SystemAssigned"
  }

  tags = azurerm_resource_group.main.tags
}

# =============================================================================
# Azure Container Registry
# =============================================================================

resource "azurerm_container_registry" "main" {
  name                = "acr${var.project_name}${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Basic"
  admin_enabled       = true

  tags = azurerm_resource_group.main.tags
}

# =============================================================================
# Storage Account (MLflow artifact store)
# =============================================================================

resource "azurerm_storage_account" "mlflow" {
  name                     = "st${var.project_name}mlflow${var.environment}"
  location                 = azurerm_resource_group.main.location
  resource_group_name      = azurerm_resource_group.main.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"

  tags = azurerm_resource_group.main.tags
}

resource "azurerm_storage_container" "mlflow_artifacts" {
  name                  = "mlflow-artifacts"
  storage_account_id    = azurerm_storage_account.mlflow.id
  container_access_type = "private"
}

# =============================================================================
# PostgreSQL Flexible Server (MLflow backend)
# =============================================================================

resource "azurerm_postgresql_flexible_server" "mlflow" {
  name                          = "psql-${var.project_name}-${var.environment}"
  location                      = azurerm_resource_group.main.location
  resource_group_name           = azurerm_resource_group.main.name
  version                       = "16"
  administrator_login           = "mlflowadmin"
  administrator_password        = var.postgresql_admin_password
  storage_mb                    = 32768
  sku_name                      = "B_Standard_B1ms"
  backup_retention_days         = 7
  geo_redundant_backup_enabled  = false
  public_network_access_enabled = true

  tags = azurerm_resource_group.main.tags
}

resource "azurerm_postgresql_flexible_server_database" "mlflow" {
  name      = "mlflow"
  server_id = azurerm_postgresql_flexible_server.mlflow.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# =============================================================================
# Container Apps Environment
# =============================================================================

resource "azurerm_container_app_environment" "main" {
  name                       = "cae-${var.project_name}-${var.environment}"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  tags = azurerm_resource_group.main.tags
}

# =============================================================================
# Container App — MLflow Server
# =============================================================================

resource "azurerm_container_app" "mlflow" {
  name                         = "ca-mlflow-${var.environment}"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    container {
      name   = "mlflow"
      image  = "ghcr.io/mlflow/mlflow:v2.19.0"
      cpu    = 0.5
      memory = "1Gi"

      command = [
        "mlflow", "server",
        "--backend-store-uri", "postgresql://mlflowadmin:${var.postgresql_admin_password}@${azurerm_postgresql_flexible_server.mlflow.fqdn}:5432/mlflow",
        "--default-artifact-root", "wasbs://mlflow-artifacts@${azurerm_storage_account.mlflow.name}.blob.core.windows.net/",
        "--host", "0.0.0.0",
        "--port", "5000",
      ]

      env {
        name  = "AZURE_STORAGE_CONNECTION_STRING"
        value = azurerm_storage_account.mlflow.primary_connection_string
      }
    }

    min_replicas = 1
    max_replicas = 2
  }

  ingress {
    external_enabled = true
    target_port      = 5000
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  tags = azurerm_resource_group.main.tags
}

# =============================================================================
# Container App — Inference API
# =============================================================================

resource "azurerm_container_app" "inference" {
  name                         = "ca-inference-${var.environment}"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    container {
      name   = "inference"
      image  = "${azurerm_container_registry.main.login_server}/${var.project_name}-inference:latest"
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "MLFLOW_TRACKING_URI"
        value = "https://${azurerm_container_app.mlflow.ingress[0].fqdn}"
      }

      env {
        name  = "INFERENCE_HOST"
        value = "0.0.0.0"
      }

      env {
        name  = "INFERENCE_PORT"
        value = "8000"
      }
    }

    min_replicas = 1
    max_replicas = 5
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  tags = azurerm_resource_group.main.tags
}
