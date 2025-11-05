# ❌ MIGRAÇÃO MySQL → PostgreSQL - CANCELADA
## Status: DEPRECATED - Arquitetura Alterada

**Versão:** 2.0 (Novembro 2025)  
**Status:** 🚫 **CANCELADO** - Não aplicável ao escopo atual  
**Motivo:** Sistema atual usa SQLite, não MySQL

---

## 🔴 AVISO CRÍTICO

Este documento de migração MySQL → PostgreSQL está **CANCELADO** pelos seguintes motivos:

### 1️⃣ Sistema Atual Não Usa MySQL
```python
# backend/app/config.py (REALIDADE ATUAL)
DATABASE_URL = "sqlite:///./data/nova_corrente.db"  # ✅ SQLite em uso

# backend/config/database_config.py (NÃO UTILIZADO)
# Configurações MySQL existem mas NÃO estão integradas
MYSQL_URI = "mysql+pymysql://..."  # ❌ Nunca foi usado
```

### 2️⃣ Nova Arquitetura: Data Lakehouse (Sem RDBMS Tradicional)
Segundo o [Roadmap de Engenharia de Dados](./DATA_ENGINEERING_ROADMAP_PT_BR.md), a arquitetura alvo é:

```
❌ NÃO FAZER: MySQL → PostgreSQL (abordagem tradicional)

✅ FAZER: SQLite → MinIO/S3 + Delta Lake (arquitetura moderna)

┌─────────────────────────────────────────────┐
│  ARQUITETURA ALVO (Data Lakehouse)         │
├─────────────────────────────────────────────┤
│                                             │
│  Storage: MinIO/S3 (objeto storage)        │
│  Format:  Delta Lake (ACID + versionamento)│
│  Layers:  Bronze → Silver → Gold           │
│  Transform: dbt (SQL)                       │
│  Orchestration: Airflow (DAGs)             │
│                                             │
│  PostgreSQL: APENAS para metadata/catalog   │
│  (Airflow metadata, MLflow tracking)        │
│                                             │
└─────────────────────────────────────────────┘
```

### 3️⃣ PostgreSQL Tem Papel Diferente
No novo escopo, PostgreSQL será usado **SOMENTE** para:
- ✅ Airflow metadata database
- ✅ MLflow tracking backend
- ✅ Great Expectations validation store
- ❌ **NÃO** para dados de negócio (estes vão para Delta Lake)

---

## ✅ PLANO CORRETO: SQLite → Delta Lake

### Migração Real Necessária

#### Atual (SQLite - Inadequado)
```python
# backend/app/config.py
DATABASE_URL = "sqlite:///./data/nova_corrente.db"

# Problemas:
# ❌ Sem suporte adequado a concorrência
# ❌ Não escala para múltiplos workers
# ❌ Sem ACID robusto
# ❌ Lock de arquivo inteiro
```

#### Alvo (Delta Lake - Escalável)
```python
# Dados de negócio → Delta Lake (MinIO/S3)
from delta import DeltaTable
import pyspark

# Bronze Layer (raw data)
df.write \
  .format("delta") \
  .mode("overwrite") \
  .partitionBy("year", "month", "day") \
  .save("s3a://bronze/materials/")

# Silver Layer (cleaned via dbt)
# dbt models transformam Bronze → Silver

# Gold Layer (star schema via dbt)
# Analytics-ready dimensional model
```

---

## 📋 DOCUMENTO SUBSTITUTO

Este documento é substituído por:

### 1. [DATA_STORAGE_DIAGNOSTIC_DEEP_DIVE.md](./DATA_STORAGE_DIAGNOSTIC_DEEP_DIVE.md)
**Seção:** TASK 1.1 (Setup MinIO) + TASK 1.2 (Implementar Delta Lake)  
**Conteúdo:**
- Provisionamento MinIO via Docker Compose
- Migração CSV → Parquet → Delta Lake
- Configuração PySpark + Delta Lake
- Scripts de migração completos

### 2. [DATA_ENGINEERING_ROADMAP_PT_BR.md](./DATA_ENGINEERING_ROADMAP_PT_BR.md)
**Seção:** Fase 0 (Foundation)  
**Conteúdo:**
- Arquitetura Medallion (Bronze/Silver/Gold)
- Stack tecnológico completo
- Plano de implementação em sprints

### 3. PostgreSQL - Uso Limitado
PostgreSQL será configurado **SOMENTE** para:

```yaml
# docker-compose.yml (ATUALIZAR)
services:
  # PostgreSQL para serviços de infraestrutura
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: nova_corrente_metadata
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  # Airflow usa PostgreSQL
  airflow-webserver:
    environment:
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow123@postgres/nova_corrente_metadata
  
  # MLflow usa PostgreSQL
  mlflow-server:
    environment:
      BACKEND_STORE_URI: postgresql://airflow:airflow123@postgres/mlflow
      ARTIFACT_ROOT: s3://mlflow-artifacts/

volumes:
  postgres_data:
```

---

## 🎯 AÇÕES CORRETAS (Em vez deste documento)

### ✅ Sprint 1: Setup MinIO + Delta Lake
Executar [TASK 1.1](./DATA_STORAGE_DIAGNOSTIC_DEEP_DIVE.md#task-11-setup-minio-dia-1-2--urgente) e [TASK 1.2](./DATA_STORAGE_DIAGNOSTIC_DEEP_DIVE.md#task-12-implementar-delta-lake-dia-3-7--urgente)

### ✅ Sprint 2: Configurar PostgreSQL (Metadata Only)
```bash
# 1. Provisionar PostgreSQL (Docker Compose)
docker-compose up -d postgres

# 2. Criar databases separados
psql -h localhost -U airflow -d postgres -c "CREATE DATABASE airflow_metadata;"
psql -h localhost -U airflow -d postgres -c "CREATE DATABASE mlflow_tracking;"
psql -h localhost -U airflow -d postgres -c "CREATE DATABASE great_expectations;"

# 3. Executar migrations
airflow db init  # Cria schema Airflow
mlflow db upgrade  # Cria schema MLflow

# 4. NÃO migrar dados de negócio para PostgreSQL
# Dados vão para Delta Lake (MinIO/S3)
```

### ✅ Sprint 3: Depreciar SQLite
```python
# backend/app/config.py (ATUALIZAR)
# ANTES:
DATABASE_URL = "sqlite:///./data/nova_corrente.db"  # ❌ DEPRECAR

# DEPOIS:
# PostgreSQL APENAS para metadata de aplicação (se necessário)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://app:app123@postgres/app_metadata"  # Metadata app
)

# Dados de negócio → Delta Lake (não RDBMS)
# Acessados via Spark/dbt, não SQLAlchemy
```

---

## 📊 COMPARAÇÃO: Abordagem Antiga vs. Nova

| Aspecto | ❌ Antiga (Este Doc) | ✅ Nova (Roadmap) |
|---------|---------------------|-------------------|
| **Storage** | PostgreSQL RDBMS | MinIO/S3 + Delta Lake |
| **Formato** | Tabelas relacionais | Parquet + Delta (ACID) |
| **Escalabilidade** | Vertical (CPU/RAM) | Horizontal (object storage) |
| **Custos** | Alto (instância dedicada) | Baixo (commodity storage) |
| **ACID** | PostgreSQL nativo | Delta Lake |
| **Versionamento** | Backup/restore | Time travel nativo |
| **Analytics** | Queries SQL diretas | dbt + Spark SQL |
| **Particionamento** | Limitado | Nativo (year/month/day) |
| **Compressão** | Limitada | 70% (Parquet + Snappy) |
| **Transformação** | Stored procedures | dbt (versionado) |

---

## 🗑️ CONTEÚDO DEPRECADO

<details>
<summary>⚠️ Conteúdo original (manter para referência histórica)</summary>

- **Objetivo**: migrar do MySQL para PostgreSQL com zero perda de dados, mínimo downtime e controle total via `SQLAlchemy` + `Alembic`.
- **Escopo**: modelo de dados (DDL), migração de dados, adequações na aplicação, testes, CI/CD, deploy e rollback.
- **Fases**:
  - **F0 – Descoberta**: inventário completo do MySQL (schemas, tabelas, FKs, índices, volumes, rotinas, grants).
  - **F1 – Design**: DDL do PostgreSQL (tipos, constraints, índices, sequences, FKs, particionamento quando aplicável).
  - **F2 – Migração**: escolha de estratégia (bulk cutover ou incremental), scripts automatizados e validações pós-carga.
  - **F3 – App/ORM**: `SQLAlchemy` models, Alembic, refactors de queries específicas de MySQL.
  - **F4 – Testes/Perf**: integridade, checksums, regressão de queries e benchmarks.
  - **F5 – Deploy/Cutover**: execução controlada (migrations-first + canary/blue-green) e rollback testado.
- **Priorização imediata**: (A) inventário + mapeamento tipos + DDL exemplo; (B) script automatizado para 1 tabela; (C) plano de cutover + validações.

---

## 2) Plano técnico detalhado por fase (comandos e exemplos)

### Fase 0 — Descoberta e inventário

- **Artefatos necessários**
  - Credenciais MySQL (host, porta, usuário, senha, database).
  - Tamanho total do banco e por tabela; crescimento histórico.
  - Dependências de aplicação (quais serviços escrevem/leem diretamente).
- **Comandos (MySQL INFORMATION_SCHEMA)**
  - Colunas e tipos:
    ```sql
    SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT,
           COLUMN_KEY, EXTRA, COLLATION_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'YOUR_DB'
    ORDER BY TABLE_NAME, ORDINAL_POSITION;
    ```
  - Chaves e FKs:
    ```sql
    SELECT CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA='YOUR_DB' AND REFERENCED_TABLE_NAME IS NOT NULL;
    ```
  - Índices:
    ```sql
    SELECT TABLE_NAME, INDEX_NAME, NON_UNIQUE, COLUMN_NAME, SEQ_IN_INDEX
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA='YOUR_DB'
    ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;
    ```
  - Tamanhos e linhas (estimativas):
    ```sql
    SELECT TABLE_NAME, ENGINE, TABLE_ROWS, DATA_LENGTH, INDEX_LENGTH
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA='YOUR_DB'
    ORDER BY DATA_LENGTH DESC;
    ```
  - Rotinas/Views/Triggers:
    ```sql
    SELECT ROUTINE_TYPE, ROUTINE_NAME FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_SCHEMA='YOUR_DB';
    SHOW FULL TABLES WHERE TABLE_TYPE = 'VIEW';
    SHOW TRIGGERS FROM YOUR_DB;
    ```
  - Slow queries (opcional): habilitar `slow_query_log` e usar `mysqldumpslow` ou `pt-query-digest`.
- **Saída esperada**: CSV/JSON com inventário completo (guardar em `docs/migration/mysql_inventory/`).

### Fase 1 — Design do schema PostgreSQL

- **Mapeamento de tipos (MySQL → PostgreSQL)**
  - `TINYINT(1)` → `BOOLEAN` (flags)
  - `TINYINT/SMALLINT/INT` unsigned → `INTEGER`/`BIGINT` + `CHECK (col >= 0)` (ou `BIGINT` para evitar overflow)
  - `INT AUTO_INCREMENT` → `GENERATED ALWAYS AS IDENTITY`
  - `VARCHAR(n)` → `VARCHAR(n)` (revisar collation; usar `UTF8`)
  - `TEXT` → `TEXT`
  - `DATETIME`/`TIMESTAMP` → `TIMESTAMP [WITH] TIME ZONE` (preferir `WITH` se há fusos)
  - `ENUM` → `CREATE TYPE ... AS ENUM` ou `VARCHAR` + `CHECK`
  - `JSON` → `JSONB` (com índices GIN quando necessário)
  - `DOUBLE`/`FLOAT` → `DOUBLE PRECISION`/`REAL`
  - `DECIMAL(p,s)` → `NUMERIC(p,s)`
- **DDL exemplo (PostgreSQL)**
  ```sql
  CREATE TABLE public.material (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code         VARCHAR(64) NOT NULL UNIQUE,
    family       VARCHAR(64) NOT NULL,
    supplier     VARCHAR(128),
    created_at   TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at   TIMESTAMP WITH TIME ZONE DEFAULT now()
  );

  CREATE TABLE public.series (
    material_id  BIGINT NOT NULL REFERENCES public.material(id) ON DELETE CASCADE,
    ts_date      DATE NOT NULL,
    demand      NUMERIC(18,4),
    stock       NUMERIC(18,4),
    lead_time   INTEGER,
    features    JSONB,
    PRIMARY KEY (material_id, ts_date)
  );

  CREATE INDEX series_ts_date_idx ON public.series(ts_date);
  CREATE INDEX series_features_gin ON public.series USING GIN (features);
  ```
- **Particionamento (quando útil)**
  - Por data (range) em tabelas de séries temporais grandes:
    ```sql
    CREATE TABLE public.series (
      material_id BIGINT NOT NULL,
      ts_date DATE NOT NULL,
      ...,
      PRIMARY KEY (material_id, ts_date)
    ) PARTITION BY RANGE (ts_date);
    ```

### Fase 2 — Estratégia de migração

- **Opção A: Bulk cutover (downtime curto)**
  - Pausar gravações, exportar, importar, validar, apontar app para Postgres, liberar gravações.
- **Opção B: Incremental (quase zero downtime)**
  - Replicação lógica (Debezium → Kafka → sink Postgres) ou `pgloader` com `--with data only` + delta final.
- **Ferramentas e scripts**
  - `pgloader`:
    ```bash
    pgloader mysql://USER:PASS@MYSQL_HOST/YOUR_DB \
            postgresql://PGUSER:PGPASS@PG_HOST/YOUR_DB \
            --with "workers = 8, concurrency = 4" \
            --with "prefetch rows = 10000" \
            --with data only
    ```
  - `mysqldump` → `psql`:
    ```bash
    mysqldump -h MYSQL_HOST -u USER -p --routines --no-tablespaces --default-character-set=utf8mb4 YOUR_DB > dump.sql
    psql postgresql://PGUSER:PGPASS@PG_HOST/YOUR_DB -f dump.sql
    ```
  - ETL incremental (Python) para tabelas críticas e reconciliação.
- **Validações pós-carga**
  - Contagens por tabela, checksums por chunks, amostras linha a linha.
  - Regressão de queries-chaves e latência P95.

### Fase 3 — Aplicação/ORM

- **`SQLAlchemy` + `Alembic`**
  - Adicionar modelos ORM e criar `alembic/` com `env.py` e `versions/0001_initial.py`.
  - `DATABASE_URL` de produção: `postgresql+psycopg://USER:PASS@HOST:5432/DB`.
- **Refactors MySQL→Postgres**
  - `INSERT ... ON DUPLICATE KEY` → `INSERT ... ON CONFLICT (col) DO UPDATE ...`
  - Diferenças em `GROUP BY`, collation e `LIKE` vs `ILIKE`.
  - Full-text search: `MATCH ... AGAINST` → `to_tsvector`/`ts_rank`.

### Fase 4 — Testes e performance

- **Integridade**: FKs válidas, contagens, checksums.
- **Performance**: `EXPLAIN ANALYZE`, índices sugeridos, `pgbench`.
- **Manutenção**: `VACUUM (ANALYZE)`, `REINDEX` quando necessário.

### Fase 5 — Deploy e cutover

- **Pré-cutover**: snapshot/backup MySQL, congelar writes (se Bulk), aquecer Postgres, rodar migrations.
- **Cutover**: executar migração, validar (contagens, checksums), apontar app, monitorar.
- **Rollback**: critérios de gatilho e script de retorno para MySQL (se necessário) ou reexecução de versão anterior.

---

## 3) Exemplos de scripts e comandos (prontos para adaptação)

- `scripts/mysql_inventory.sql` (coleta inventário; ver consultas Fase 0).
- `scripts/generate_pg_ddl.py` (protótipo):
  ```python
  # Lê inventário JSON do MySQL e gera DDL Postgres com mapping tipos
  # Uso: python scripts/generate_pg_ddl.py --inventory docs/migration/mysql_inventory/schema.json --out ddl/postgres_schema.sql
  ```
- `scripts/migrate_table_pgloader.sh`:
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  SRC="mysql://$MYSQL_USER:$MYSQL_PASS@$MYSQL_HOST/$MYSQL_DB"
  DST="postgresql://$PG_USER:$PG_PASS@$PG_HOST/$PG_DB"
  TABLE="$1" # ex.: material
  pgloader <<EOF
  LOAD DATABASE
      FROM $SRC
      INTO $DST
  WITH include drop, create no tables, materialize view no tables,
       workers = 8, concurrency = 4, prefetch rows = 10000
  CAST type datetime to timestamp with time zone drop default using zero-dates-to-null,
       type json to jsonb using identity
  ALTER SCHEMA 'YOUR_DB' RENAME TO 'public'
  SET work_mem to '256MB', maintenance_work_mem to '512MB'
  EXCLUDING TABLE NAMES MATCHING 'tmp_.*'
  INCLUDING ONLY TABLE NAMES MATCHING "$TABLE"
  BEFORE LOAD DO
      $$ ALTER TABLE IF EXISTS public.$TABLE DISABLE TRIGGER ALL; $$,
  AFTER LOAD DO
      $$ ALTER TABLE IF EXISTS public.$TABLE ENABLE TRIGGER ALL; $$;
  EOF
  ```
- `scripts/verify_migration.py` (amostra):
  ```python
  # Compara counts e checksums por chunks entre MySQL e Postgres para uma tabela
  # Uso: python scripts/verify_migration.py --table material --chunk-size 100000
  ```
- Alembic inicial:
  ```bash
  alembic init alembic
  alembic revision -m "initial schema" --autogenerate
  alembic upgrade head
  ```
- CI (ex.: `.github/workflows/migrate.yml`):
  ```yaml
  # job: spin Postgres, run alembic upgrade, run verify tests
  ```

---

## 4) Checklist de aceitação

- Alembic aplicado em staging, `alembic current` = `head`.
- Contagens por tabela iguais (± tolerância justificada) e checksums por amostra/chunks batem.
- Testes de integração da aplicação OK com Postgres.
- Queries críticas com performance aceitável (P95 dentro da meta) e índices ajustados.
- Plano de cutover/rollback testado (dry run) e documentação assinada.
- Observabilidade ativa (métricas/logs/alertas por 72h pós-cutover).

---

## 5) Prioridade imediata (A/B/C)

- **A — Inventário + mapeamento + DDL**
  - Rodar `scripts/mysql_inventory.sql` e salvar inventário.
  - Gerar DDL-alvo inicial com `generate_pg_ddl.py` (ou manualmente para 2-3 tabelas críticas).
- **B — Script de conversão (tabela exemplo)**
  - Rodar `migrate_table_pgloader.sh material` e validar contagens/checksums.
- **C — Plano de cutover + validações**
  - Definir janela/downtime alvo; ensaiar em staging.
  - Documentar passos e critérios de rollback.

---

## 6) Informações faltantes (coletar automaticamente)

- Acesso MySQL (HOST, PORT, USER, PASS, DB) e volume de dados por tabela.
- Tabelas e relações críticas para a aplicação.
- Lista de queries críticas para benchmark.

Comandos de coleta: ver consultas de Fase 0; salvar CSV/JSON em `docs/migration/mysql_inventory/`.

---

## 7) Adaptação ao projeto atual

- O backend hoje usa `DATABASE_URL` e ainda não está integrado a MySQL; a migração focará em padronizar `PostgreSQL` como alvo final.
- Introduzir `SQLAlchemy` + `Alembic` no app e mover `DATABASE_URL` para Postgres via `.env` e `docker-compose`.
- Criar `alembic/versions/0001_initial.py` com as tabelas mínimas (materials, series, forecasts, pipeline_runs, feature_snapshots).

---

## 8) Comandos prontos (placeholders para parametrizar)

```bash
# Variáveis
export MYSQL_HOST=... MYSQL_DB=... MYSQL_USER=... MYSQL_PASS=...
export PG_HOST=... PG_DB=... PG_USER=... PG_PASS=...

# Inventário
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASS -e "SOURCE scripts/mysql_inventory.sql" > docs/migration/mysql_inventory/inventory_$(date +%F).txt

# Geração DDL (exemplo)
python scripts/generate_pg_ddl.py --inventory docs/migration/mysql_inventory/schema.json --out ddl/postgres_schema.sql

# Criação schema no Postgres
psql postgresql://$PG_USER:$PG_PASS@$PG_HOST/$PG_DB -f ddl/postgres_schema.sql

# Migração de 1 tabela (material)
bash scripts/migrate_table_pgloader.sh material

# Verificação
python scripts/verify_migration.py --table material --chunk-size 100000

# Alembic
alembic upgrade head
```

---

</details>

---

## 📚 REFERÊNCIAS ATUALIZADAS

### Documentos de Diagnóstico Válidos:
1. **[DATA_ENGINEERING_ROADMAP_PT_BR.md](./DATA_ENGINEERING_ROADMAP_PT_BR.md)**
   - Arquitetura completa Data Lakehouse
   - Sprint 1-4 com tasks detalhadas
   - Stack tecnológico: MinIO, Delta Lake, dbt, Airflow

2. **[DATA_STORAGE_DIAGNOSTIC_DEEP_DIVE.md](./DATA_STORAGE_DIAGNOSTIC_DEEP_DIVE.md)**
   - Inventário técnico atual (SQLite, CSV)
   - Gaps críticos identificados
   - Plano de ação com código completo

3. **[COMPREHENSIVE_DATA_ENGINEERING_DIAGNOSTIC_PT_BR.md](./COMPREHENSIVE_DATA_ENGINEERING_DIAGNOSTIC_PT_BR.md)**
   - Diagnóstico completo (85% gap)
   - Análise top-down e bottom-up
   - Riscos e mitigações

4. **[GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md](./clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)**
   - Política de ML Ops fora do deployment
   - Arquitetura de deployment leve
   - Precomputed results only

### Código Real Existente:
```
backend/
├── app/config.py                    # ✅ DATABASE_URL atual (SQLite)
├── config/database_config.py        # ❌ MySQL config (não usado)
├── data/
│   ├── Nova_Corrente_ML_Ready_DB.sql  # Schema PostgreSQL (referência)
│   └── collectors/                  # Extractors ETL
├── pipelines/
│   ├── orchestrator_service.py      # ⚠️ Scheduler básico (deprecar)
│   ├── anatel_5g_etl.py            # ✅ Refatorar para Bronze layer
│   ├── climate_etl.py              # ✅ Refatorar para Bronze layer
│   └── economic_etl.py             # ✅ Refatorar para Bronze layer

data/
├── processed/                       # ✅ Migrar para MinIO/Bronze
│   └── unified_dataset_with_factors.csv  # 27MB
├── raw/                            # ✅ Migrar para MinIO/Bronze
│   ├── anatel_5g/
│   ├── weather/
│   └── economic/
└── training/                       # ✅ Migrar para MinIO/Silver
    ├── unknown_train.csv
    └── unknown_test.csv
```

---

## ✅ PRÓXIMOS PASSOS IMEDIATOS

### 1. Abandonar Migração MySQL → PostgreSQL
- ❌ Não implementar nenhum script deste documento
- ❌ Não criar infra MySQL
- ❌ Não migrar para PostgreSQL como storage principal

### 2. Seguir Roadmap Data Lakehouse
- ✅ **TASK 1.1:** Setup MinIO (Dia 1-2)
- ✅ **TASK 1.2:** Implementar Delta Lake (Dia 3-7)
- ✅ **TASK 1.3:** Setup dbt (Dia 8-12)
- ✅ **TASK 1.4:** Setup Airflow (Dia 8-12)

### 3. PostgreSQL Apenas para Metadata
- ✅ Provisionar PostgreSQL para Airflow metadata
- ✅ Provisionar PostgreSQL para MLflow tracking
- ✅ **NÃO** usar PostgreSQL para dados de negócio

---

**Documento atualizado:** Novembro 2025  
**Versão:** 2.0  
**Status:** 🚫 **CANCELADO** - Substituído por arquitetura Data Lakehouse  
**Ação Imediata:** Seguir [DATA_STORAGE_DIAGNOSTIC_DEEP_DIVE.md](./DATA_STORAGE_DIAGNOSTIC_DEEP_DIVE.md)

**IMPORTANTE:** Este documento foi mantido apenas para **referência histórica**. A decisão arquitetural foi revisada e o sistema seguirá a abordagem moderna de Data Lakehouse (MinIO + Delta Lake) ao invés de RDBMS tradicional (MySQL/PostgreSQL).
