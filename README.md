# AzureQueimadasINPE

Projeto de exemplo em Azure para coletar focos de queimadas (INPE) via HTTP Trigger (Azure Functions em Python), persistir em MySQL Flexible Server e automatizar infraestrutura + deploy com Terraform e GitHub Actions.

## Visão geral

- **Infra (Terraform)**: cria Resource Group, Storage Account da Function, App Service Plan (Linux), Function App (Python 3.11) e MySQL Flexible Server.
- **App (Azure Functions)**: rota HTTP `/api/coleta` baixa o CSV diário do INPE e insere os registros em uma tabela MySQL.
- **CI/CD (GitHub Actions)**:
  - PR: `terraform plan`
  - Push em `main`: `terraform apply` + build das dependências Python + deploy da Function

## Estrutura do repositório

- `.github/workflows/`
  - `ci-cd-infra-function.yml`: CI/CD (plan/apply + deploy function)
  - `ci-cd-infra-destroy.yml`: workflow manual para destruir infra
- `infra/`: Terraform (AzureRM)
- `function/`: código da Azure Function (Python)
  - `function_app.py`
  - `host.json`
  - `requirements.txt`
  - `sql/` (scripts auxiliares, se aplicável)
- `webapp/`: (se houver) artefatos/webapp futuros

## Pré-requisitos

- Azure CLI instalado (ou Cloud Shell)
- Terraform (local, se for executar manualmente)
- Uma assinatura Azure com permissões para criar:
  - App Service Plan / Function App
  - Storage Account
  - MySQL Flexible Server

## Configuração de secrets no GitHub

No repositório, configure em **Settings → Secrets and variables → Actions**:

- `AZURE_CREDENTIALS` (JSON do service principal) no formato aceito pelo `azure/login@v1`
- `MYSQL_ADMIN_PASSWORD` (senha do MySQL)

Opcional (recomendado para deploy mais determinístico):
- `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` (Publish Profile baixado no Portal da Function App)

## Como funciona a Function

### Endpoint
- URL: `https://<function_app>.azurewebsites.net/api/coleta`
- Auth Level: `FUNCTION` (precisa de key)

### Query params
- `data` (opcional) no formato `YYYY-MM-DD`
  - se não informado, usa “ontem” (UTC)

### Exemplo de chamada (curl)
1) Obter uma key (host key):
```bash
az functionapp keys list -g rg-monitor-queimadas -n func-queimadas-rm561575 -o jsonc
