# Deploy na Azure com Terraform

## Arquitetura na Azure

Para produção, o stack de monitoramento pode ser provisionado na Azure usando serviços gerenciados quando possível e containers para componentes open-source.

```
┌─────────────────────────────────────────────────┐
│              Azure Resource Group                │
│                                                  │
│  ┌────────────────┐   ┌──────────────────────┐  │
│  │ Azure Container│   │ Azure Container      │  │
│  │ Apps           │   │ Apps                 │  │
│  │ (Inference API)│   │ (Training Job)       │  │
│  └───────┬────────┘   └──────────┬───────────┘  │
│          │                       │               │
│          ▼                       ▼               │
│  ┌──────────────────────────────────────────┐   │
│  │     Azure Monitor / Managed Prometheus   │   │
│  │     (Azure Managed Grafana)              │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  ┌────────────────┐   ┌──────────────────────┐  │
│  │ Azure Database │   │ Azure Blob Storage   │  │
│  │ for PostgreSQL │   │ (MLflow artifacts)   │  │
│  │ (MLflow backend│   │                      │  │
│  └────────────────┘   └──────────────────────┘  │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │  Azure Container Apps (MLflow Server)      │ │
│  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

## Serviços Azure Utilizados

| Serviço | Papel | Justificativa |
|---|---|---|
| **Azure Managed Grafana** | Dashboards | Gerenciado, integração nativa com Azure Monitor |
| **Azure Monitor (Managed Prometheus)** | Métricas | Compatível com PromQL, sem overhead operacional |
| **Azure Container Apps** | Serviços (inferência, MLflow) | Serverless containers, escalabilidade automática |
| **Azure Database for PostgreSQL** | Backend do MLflow | Gerenciado, backup automático |
| **Azure Blob Storage** | Artefatos do MLflow | Durável, barato, integração com MLflow |
| **Azure Container Registry** | Imagens Docker | Registry privado próximo ao compute |

## Terraform — Visão Geral

O código Terraform em `infra/terraform/` provisiona:

1. Resource Group
2. Container Registry
3. Container Apps Environment
4. Managed Grafana workspace
5. Azure Monitor workspace (Managed Prometheus)
6. PostgreSQL Flexible Server
7. Storage Account (para artefatos MLflow)
8. Container Apps para MLflow e Inference API

### Variáveis Principais

```hcl
variable "location" {
  description = "Região Azure"
  default     = "eastus2"
}

variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  default     = "dev"
}

variable "project_name" {
  description = "Nome do projeto"
  default     = "mlmonitor"
}
```

### Aplicando

```bash
cd infra/terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

## Alternativa Agnóstica (Docker Compose)

Para cenários onde o aluno não tem acesso à Azure, toda a stack funciona localmente com Docker Compose. A transição para cloud envolve:

1. Substituir Prometheus local → Azure Monitor Managed Prometheus
2. Substituir Grafana local → Azure Managed Grafana
3. Substituir SQLite → Azure PostgreSQL
4. Substituir filesystem → Azure Blob Storage
5. Substituir Docker Compose → Azure Container Apps

O código Python permanece idêntico — apenas a configuração de endpoints muda via variáveis de ambiente.
