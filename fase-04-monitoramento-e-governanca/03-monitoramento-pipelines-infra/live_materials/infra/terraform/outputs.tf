output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "mlflow_url" {
  description = "MLflow Tracking Server URL"
  value       = "https://${azurerm_container_app.mlflow.ingress[0].fqdn}"
}

output "inference_url" {
  description = "Inference API URL"
  value       = "https://${azurerm_container_app.inference.ingress[0].fqdn}"
}

output "grafana_url" {
  description = "Azure Managed Grafana URL"
  value       = azurerm_dashboard_grafana.main.endpoint
}

output "container_registry_server" {
  description = "ACR login server"
  value       = azurerm_container_registry.main.login_server
}

output "postgresql_fqdn" {
  description = "PostgreSQL server FQDN"
  value       = azurerm_postgresql_flexible_server.mlflow.fqdn
}

output "storage_account_name" {
  description = "Storage account for MLflow artifacts"
  value       = azurerm_storage_account.mlflow.name
}
