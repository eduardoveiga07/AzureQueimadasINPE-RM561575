# Checkpoint 02 - Cloud Computing & IoT
## Eduardo Veiga | RM561575

### Descrição
Pipeline de dados de queimadas do INPE utilizando Azure Databricks, MySQL Flexible Server e GitHub Actions com Terraform.

### Arquitetura
```
CSV (INPE) → Volume Databricks (Bronze) → Delta Table Silver → MySQL Gold
```

### Estrutura do Repositório
- **infra/**: Scripts Terraform para provisionamento do MySQL Flexible Server
- **databricks/**: Notebooks PySpark (Bronze → Silver → Gold)
- **.github/workflows/**: GitHub Actions para execução automática do Terraform

### Configuração das Secrets no GitHub
| Secret | Descrição |
|--------|-----------|
| `AZURE_CREDENTIALS` | JSON com credenciais do Service Principal Azure |
| `MYSQL_ADMIN_PASSWORD` | Senha do administrador do MySQL |

### Como Executar
1. Configure as secrets no repositório GitHub
2. Execute o workflow `provision-mysql-queimadas` em **Actions** > **Run workflow**
3. Após o MySQL ser criado, configure os notebooks no Databricks com o host gerado
4. Crie o Job no Databricks com trigger de **File Arrival** apontando para `/Volumes/inpe/bronze/arquivo/`
5. Faça upload dos CSVs mensais do INPE para disparar o pipeline automaticamente

### Fontes de Dados
- [INPE - Focos de Queimadas (CSV Mensal)](https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/mensal/Brasil/)
