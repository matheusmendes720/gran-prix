# 🗺️ ROADMAP: ALINHAMENTO DO BANCO DE DADOS (LOCAL)
## Plano Executável - PostgreSQL Local sem Docker

**Versão:** 2.0  
**Data:** Novembro 2025  
**Status:** 📋 Instalação Local - Sem Docker  
**Tempo Total Estimado:** 2-3 dias

---

## 🎯 OBJETIVO

Resolver os **5 gaps críticos** identificados no diagnóstico e colocar o PostgreSQL 100% operacional localmente no Windows, **sem necessidade de Docker**.

---

## 📊 RESUMO EXECUTIVO

### Status Atual → Alvo (Instalação Local)

| Componente | Atual | Alvo | Esforço |
|------------|-------|------|---------|
| **PostgreSQL Local** | ❌ Não instalado | ✅ Serviço rodando | 30 min |
| **pgAdmin** | ❌ Não instalado | ✅ Interface gráfica | 15 min |
| **Database** | ❌ Não existe | ✅ Criado | 10 min |
| **Migrations** | ⚠️ Duplicadas | ✅ Limpas | 10 min |
| **Seed Data** | ❌ Vazio | ✅ Populado | 2h |
| **Partições** | ⚠️ 2 meses | ✅ Auto-create | 1h |
| **Backup** | ❌ Nenhum | ✅ Automático | 30 min |

**Total:** ~5h de trabalho efetivo

---

## 🔥 FASE 1: INSTALAÇÃO DO POSTGRESQL LOCAL (1h)

### STEP 1.1: Download e Instalação PostgreSQL (30min)

**Objetivo:** Instalar PostgreSQL 15 nativamente no Windows

#### Ações:

1. **Download do PostgreSQL**
   ```powershell
   # Abrir navegador e baixar:
   # https://www.postgresql.org/download/windows/
   # OU usar o instalador EDB:
   # https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
   
   # Versão recomendada: PostgreSQL 15.x (Windows x86-64)
   ```

2. **Executar Instalador**
   ```
   Configurações durante instalação:
   
   ✅ Installation Directory: C:\Program Files\PostgreSQL\15
   ✅ Data Directory: C:\Program Files\PostgreSQL\15\data
   ✅ Port: 5432 (padrão)
   ✅ Locale: Portuguese, Brazil (ou Default locale)
   
   ⚠️ IMPORTANTE - Definir senhas:
   - Superuser (postgres): strong_password
   - Database User (criar depois): nova_corrente
   
   ✅ Componentes para instalar:
   [x] PostgreSQL Server
   [x] pgAdmin 4
   [x] Stack Builder (opcional)
   [x] Command Line Tools
   ```

3. **Verificar Instalação**
   ```powershell
   # Adicionar ao PATH (se não foi automático)
   $env:Path += ";C:\Program Files\PostgreSQL\15\bin"
   
   # Testar versão
   psql --version
   # Esperado: psql (PostgreSQL) 15.x
   
   # Verificar serviço rodando
   Get-Service -Name postgresql*
   # Status deve ser: Running
   ```

4. **Testar Conexão**
   ```powershell
   # Conectar como superuser
   psql -U postgres -h localhost
   # Senha: strong_password
   
   # Dentro do psql:
   \l              # Listar databases
   \du             # Listar usuários
   \q              # Sair
   ```

**Critérios de Aceite:**
- ✅ `psql --version` retorna PostgreSQL 15.x
- ✅ Serviço `postgresql-x64-15` rodando
- ✅ Consegue conectar com `psql -U postgres`
- ✅ pgAdmin 4 instalado e acessível

---

### STEP 1.2: Criar Database e User (15min)

**Objetivo:** Configurar database e usuário do projeto

#### Ações:

1. **Conectar como superuser**
   ```powershell
   psql -U postgres -h localhost
   ```

2. **Criar usuário e database**
   ```sql
   -- Criar usuário do projeto
   CREATE USER nova_corrente WITH PASSWORD 'strong_password';
   
   -- Criar database
   CREATE DATABASE nova_corrente OWNER nova_corrente;
   
   -- Conceder privilégios
   GRANT ALL PRIVILEGES ON DATABASE nova_corrente TO nova_corrente;
   
   -- Conectar ao novo database
   \c nova_corrente
   
   -- Conceder permissões no schema public
   GRANT ALL ON SCHEMA public TO nova_corrente;
   
   -- Verificar
   \l
   \du
   ```

3. **Testar conexão com novo usuário**
   ```powershell
   # Sair do psql anterior
   \q
   
   # Conectar com usuário do projeto
   psql -U nova_corrente -h localhost -d nova_corrente
   # Senha: strong_password
   
   # Testar permissões
   CREATE TABLE test (id INT);
   DROP TABLE test;
   # Deve funcionar sem erro
   ```

**Critérios de Aceite:**
- ✅ Database `nova_corrente` criado
- ✅ User `nova_corrente` criado
- ✅ Consegue conectar: `psql -U nova_corrente -d nova_corrente`
- ✅ Pode criar/dropar tabelas

---

### STEP 1.3: Configurar Variáveis de Ambiente (10min)

**Objetivo:** Configurar acesso sem senha via arquivo .env

#### Ações:

1. **Criar/Atualizar arquivo .env**
   ```powershell
   # Navegar até o backend
   cd c:\Users\User\Desktop\work\gran_prix\gran_prix\backend
   
   # Criar/editar .env
   notepad .env
   ```

2. **Configuração do .env**
   ```ini
   # Database Configuration (PostgreSQL Local)
   DATABASE_URL=postgresql://nova_corrente:strong_password@localhost:5432/nova_corrente
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=nova_corrente
   DB_PASSWORD=strong_password
   DB_NAME=nova_corrente
   
   # Connection Pool
   DB_POOL_SIZE=10
   DB_MAX_OVERFLOW=20
   DB_POOL_TIMEOUT=30
   DB_POOL_RECYCLE=3600
   DB_ECHO=False
   
   # Application
   SECRET_KEY=change-this-in-production
   DEBUG=True
   
   # Features (ML disabled in deployment)
   EXTERNAL_APIS_ENABLED=false
   ENABLE_ML_PROCESSING=false
   
   # CORS
   CORS_ORIGINS=http://localhost:3000,http://localhost:3001
   ```

3. **Atualizar alembic.ini (opcional)**
   ```powershell
   # backend/alembic.ini - deixar sqlalchemy.url em branco
   # Será lido do .env via env.py
   notepad alembic.ini
   ```

**Critérios de Aceite:**
- ✅ Arquivo `.env` criado com credenciais corretas
- ✅ `DATABASE_URL` aponta para localhost
- ✅ Variáveis acessíveis pelo Python

---

## 🟡 FASE 2: APLICAR SCHEMA E MIGRATIONS (30min)

### STEP 2.1: Limpar Migrations Duplicadas (10min)

**Objetivo:** Resolver conflito de migrations

#### Ações:

1. **Verificar migrations existentes**
   ```powershell
   cd c:\Users\User\Desktop\work\gran_prix\gran_prix\backend
   dir alembic\versions
   # Saída:
   # 001_initial_schema.py (25.2KB) - REMOVER
   # 001_initial_postgres_schema.py (13.3KB) - MANTER
   ```

2. **Fazer backup da migration antiga**
   ```powershell
   Move-Item alembic\versions\001_initial_schema.py alembic\versions\001_initial_schema.py.backup
   ```

3. **Instalar dependências Python**
   ```powershell
   pip install alembic psycopg2-binary python-dotenv
   ```

4. **Aplicar migration limpa**
   ```powershell
   alembic upgrade head
   # Deve executar 001_initial_postgres_schema.py
   ```

5. **Verificar no banco**
   ```powershell
   psql -U nova_corrente -h localhost -d nova_corrente
   ```
   
   ```sql
   -- Verificar schemas
   \dn
   # Deve mostrar: core, analytics, support, staging
   
   -- Verificar tabelas core
   \dt core.*
   
   -- Verificar versão do Alembic
   SELECT * FROM alembic_version;
   ```

**Critérios de Aceite:**
- ✅ Apenas 1 migration ativa
- ✅ Schemas criados: core, analytics, support, staging
- ✅ Tabelas dimensões e fatos criados
- ✅ Partições iniciais criadas (2025_01, 2025_02)

---

## 🟢 FASE 3: SEED DATA & CALENDÁRIO (2h)

### STEP 3.1: Popular Calendário (45min)

**Objetivo:** Criar dimensão temporal para 10 anos

#### Ações:

1. **Criar diretório de scripts**
   ```powershell
   cd c:\Users\User\Desktop\work\gran_prix\gran_prix\backend
   New-Item -ItemType Directory -Force -Path scripts
   ```

2. **Criar script seed_calendar.py**
   ```powershell
   notepad scripts\seed_calendar.py
   ```

3. **Código do script** (copiar e colar):
   ```python
   import psycopg2
   import os
   from datetime import date, timedelta
   from dotenv import load_dotenv
   
   load_dotenv()
   
   def populate_calendar(start_year=2024, end_year=2034):
       conn = psycopg2.connect(
           host=os.getenv('DB_HOST', 'localhost'),
           port=int(os.getenv('DB_PORT', 5432)),
           user=os.getenv('DB_USER', 'nova_corrente'),
           password=os.getenv('DB_PASSWORD', 'strong_password'),
           database=os.getenv('DB_NAME', 'nova_corrente')
       )
       cur = conn.cursor()
       
       # Feriados brasileiros
       holidays = {
           '01-01': 'Ano Novo',
           '04-21': 'Tiradentes',
           '05-01': 'Dia do Trabalho',
           '09-07': 'Independência do Brasil',
           '10-12': 'Nossa Senhora Aparecida',
           '11-02': 'Finados',
           '11-15': 'Proclamação da República',
           '12-25': 'Natal'
       }
       
       start_date = date(start_year, 1, 1)
       end_date = date(end_year, 12, 31)
       current = start_date
       batch = []
       
       while current <= end_date:
           month_day = current.strftime('%m-%d')
           is_holiday = month_day in holidays
           holiday_name = holidays.get(month_day)
           is_weekend = current.weekday() >= 5
           quarter = (current.month - 1) // 3 + 1
           
           batch.append((
               current, current.year, current.month, quarter,
               current.weekday(), current.day, current.isocalendar()[1],
               is_weekend, is_holiday, holiday_name, current.year, quarter
           ))
           
           if len(batch) >= 1000:
               cur.executemany("""
                   INSERT INTO core.dim_calendar 
                   (full_date, year, month, quarter, weekday, day_of_month, 
                    week_of_year, is_weekend, is_holiday, holiday_name, 
                    fiscal_year, fiscal_quarter)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (full_date) DO NOTHING
               """, batch)
               conn.commit()
               print(f"✅ Inseridos {len(batch)} registros")
               batch = []
           
           current += timedelta(days=1)
       
       if batch:
           cur.executemany("""
               INSERT INTO core.dim_calendar 
               (full_date, year, month, quarter, weekday, day_of_month, 
                week_of_year, is_weekend, is_holiday, holiday_name, 
                fiscal_year, fiscal_quarter)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (full_date) DO NOTHING
           """, batch)
           conn.commit()
       
       cur.execute("SELECT COUNT(*) FROM core.dim_calendar")
       count = cur.fetchone()[0]
       print(f"✅ Total: {count} datas no calendário")
       
       cur.close()
       conn.close()
   
   if __name__ == "__main__":
       populate_calendar()
   ```

4. **Executar script**
   ```powershell
   python scripts\seed_calendar.py
   ```

5. **Verificar resultado**
   ```powershell
   psql -U nova_corrente -h localhost -d nova_corrente
   ```
   ```sql
   SELECT COUNT(*) FROM core.dim_calendar;
   -- Esperado: ~4018 linhas
   
   SELECT full_date, is_holiday, holiday_name
   FROM core.dim_calendar
   WHERE is_holiday = true
   LIMIT 10;
   ```

**Critérios de Aceite:**
- ✅ ~4018 datas inseridas (2024-2034)
- ✅ Feriados marcados corretamente
- ✅ Weekends identificados

---

### STEP 3.2: Seed Master Data (45min)

**Objetivo:** Popular dimensões com dados de teste

#### Ações:

1. **Criar script seed_master_data.py**
   ```powershell
   notepad scripts\seed_master_data.py
   ```

2. **Código do script**:
   ```python
   import psycopg2
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   def seed_master_data():
       conn = psycopg2.connect(
           host=os.getenv('DB_HOST'),
           port=int(os.getenv('DB_PORT')),
           user=os.getenv('DB_USER'),
           password=os.getenv('DB_PASSWORD'),
           database=os.getenv('DB_NAME')
       )
       cur = conn.cursor()
       
       # dim_item
       items = [
           ('MAT001', 'Cabo Rede Cat6 305m', 'Cabos', 'Redes', 'Infraestrutura', 'UN', 'A', 9),
           ('MAT002', 'Switch 24 Portas Gigabit', 'Switches', 'Ativos', 'Equipamentos', 'UN', 'A', 10),
           ('MAT003', 'Roteador WiFi 6', 'Roteadores', 'Ativos', 'Equipamentos', 'UN', 'B', 7),
           ('MAT004', 'Patch Cord Cat6 1.5m', 'Cabos', 'Redes', 'Infraestrutura', 'UN', 'C', 4),
           ('MAT005', 'Antena Setorial 5GHz', 'Antenas', 'RF', 'Equipamentos', 'UN', 'B', 8),
       ]
       
       for item in items:
           cur.execute("""
               INSERT INTO core.dim_item 
               (sku, name, family, category, subcategory, unit_measure, abc_class, criticality)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (sku) DO NOTHING
           """, item)
       
       # dim_site
       sites = [
           ('CD-SP-01', 'CD São Paulo - Guarulhos', 1, -23.4356, -46.4731, 'DISTRIBUTION_CENTER'),
           ('CD-RJ-01', 'CD Rio de Janeiro', 3, -22.9068, -43.1729, 'DISTRIBUTION_CENTER'),
           ('LJ-BA-01', 'Loja Salvador', 8, -12.9714, -38.5014, 'STORE'),
           ('LJ-MG-01', 'Loja Belo Horizonte', 2, -19.9167, -43.9345, 'STORE'),
       ]
       
       for site in sites:
           cur.execute("""
               INSERT INTO core.dim_site 
               (code, name, region_id, latitude, longitude, site_type)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT (code) DO NOTHING
           """, site)
       
       # dim_supplier
       suppliers = [
           ('FORN-001', 'Fornecedor Nacional A', 'DOMESTIC', 95.5, 7, 98.2),
           ('FORN-002', 'Importador China B', 'IMPORT', 78.3, 45, 85.7),
           ('FORN-003', 'Fornecedor Híbrido C', 'HYBRID', 88.9, 15, 92.1),
       ]
       
       for supplier in suppliers:
           cur.execute("""
               INSERT INTO core.dim_supplier 
               (code, name, supplier_type, reliability_score, avg_lead_time_days, on_time_delivery_rate)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT (code) DO NOTHING
           """, supplier)
       
       conn.commit()
       
       # Estatísticas
       cur.execute("SELECT COUNT(*) FROM core.dim_item")
       print(f"✅ Items: {cur.fetchone()[0]}")
       cur.execute("SELECT COUNT(*) FROM core.dim_site")
       print(f"✅ Sites: {cur.fetchone()[0]}")
       cur.execute("SELECT COUNT(*) FROM core.dim_supplier")
       print(f"✅ Suppliers: {cur.fetchone()[0]}")
       
       cur.close()
       conn.close()
   
   if __name__ == "__main__":
       seed_master_data()
   ```

3. **Executar**
   ```powershell
   python scripts\seed_master_data.py
   ```

**Critérios de Aceite:**
- ✅ 5 items, 4 sites, 3 suppliers inseridos

---

## 🔵 FASE 4: AUTO-PARTICIONAMENTO (1h)

### STEP 4.1: Criar Partições Automaticamente (45min)

**Objetivo:** Criar partições para próximos 24 meses

#### Ações:

1. **Criar script create_partitions.py**
   ```powershell
   notepad scripts\create_partitions.py
   ```

2. **Código do script**:
   ```python
   import psycopg2
   import os
   from datetime import date
   from dateutil.relativedelta import relativedelta
   from dotenv import load_dotenv
   
   load_dotenv()
   
   def create_monthly_partitions(months_ahead=24):
       conn = psycopg2.connect(
           host=os.getenv('DB_HOST'),
           port=int(os.getenv('DB_PORT')),
           user=os.getenv('DB_USER'),
           password=os.getenv('DB_PASSWORD'),
           database=os.getenv('DB_NAME')
       )
       cur = conn.cursor()
       
       tables = [
           'core.fact_demand_daily',
           'core.fact_inventory_daily',
           'core.fact_orders'
       ]
       
       current_date = date.today().replace(day=1)
       
       for i in range(months_ahead):
           partition_date = current_date + relativedelta(months=i)
           next_month = partition_date + relativedelta(months=1)
           
           year = partition_date.year
           month = partition_date.month
           start_date = partition_date.strftime('%Y-%m-%d')
           end_date = next_month.strftime('%Y-%m-%d')
           
           for table in tables:
               partition_name = f"{table}_{year}_{month:02d}"
               
               try:
                   cur.execute(f"""
                       CREATE TABLE IF NOT EXISTS {partition_name}
                       PARTITION OF {table}
                       FOR VALUES FROM ('{start_date}') TO ('{end_date}')
                   """)
                   print(f"✅ {partition_name}")
               except Exception as e:
                   print(f"⚠️  {partition_name}: {e}")
           
           conn.commit()
       
       cur.execute("""
           SELECT COUNT(*) FROM pg_tables 
           WHERE tablename LIKE 'fact_%_202%'
       """)
       count = cur.fetchone()[0]
       print(f"\n📊 Total: {count} partições criadas")
       
       cur.close()
       conn.close()
   
   if __name__ == "__main__":
       create_partitions(months_ahead=24)
   ```

3. **Instalar dependência**
   ```powershell
   pip install python-dateutil
   ```

4. **Executar**
   ```powershell
   python scripts\create_partitions.py
   ```

**Critérios de Aceite:**
- ✅ 72 partições criadas (3 tabelas × 24 meses)

---

## 🟣 FASE 5: BACKUP & MONITORING (1h)

### STEP 5.1: Backup com PowerShell (30min)

**Objetivo:** Criar rotina de backup

#### Ações:

1. **Criar diretório**
   ```powershell
   cd c:\Users\User\Desktop\work\gran_prix\gran_prix
   New-Item -ItemType Directory -Force -Path backups
   ```

2. **Criar script backup_database.ps1**
   ```powershell
   notepad backend\scripts\backup_database.ps1
   ```

3. **Código do script**:
   ```powershell
   $BACKUP_DIR = "c:\Users\User\Desktop\work\gran_prix\gran_prix\backups"
   $DATE = Get-Date -Format "yyyyMMdd_HHmmss"
   $BACKUP_FILE = "$BACKUP_DIR\backup_$DATE.sql"
   $PGPASSWORD = "strong_password"
   
   Write-Host "🔄 Iniciando backup..."
   
   $env:PGPASSWORD = $PGPASSWORD
   
   & "C:\Program Files\PostgreSQL\15\bin\pg_dump.exe" `
     -U nova_corrente -h localhost -d nova_corrente `
     -F c -f $BACKUP_FILE
   
   if ($?) {
       Write-Host "✅ Backup: $BACKUP_FILE"
       Compress-Archive -Path $BACKUP_FILE -DestinationPath "$BACKUP_FILE.zip"
       Remove-Item $BACKUP_FILE
   }
   
   Get-ChildItem $BACKUP_DIR -Filter "backup_*.zip" | `
     Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } | `
     Remove-Item -Force
   ```

4. **Executar**
   ```powershell
   .\backend\scripts\backup_database.ps1
   ```

---

### STEP 5.2: Monitoring com pg_stat_statements (15min)

**Objetivo:** Habilitar monitoramento

#### Ações:

1. **Habilitar extensão**
   ```powershell
   psql -U nova_corrente -h localhost -d nova_corrente
   ```
   ```sql
   CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
   ```

2. **Configurar postgresql.conf**
   ```powershell
   notepad "C:\Program Files\PostgreSQL\15\data\postgresql.conf"
   ```
   ```ini
   shared_preload_libraries = 'pg_stat_statements'
   pg_stat_statements.track = all
   ```

3. **Reiniciar serviço**
   ```powershell
   Restart-Service postgresql-x64-15
   ```

---

### STEP 5.3: Configurar pgAdmin 4 (15min)

**Objetivo:** Interface gráfica

#### Ações:

1. **Abrir pgAdmin 4**
   - Iniciar pelo Menu Iniciar: PostgreSQL 15 → pgAdmin 4

2. **Adicionar servidor**
   ```
   Servers → Register → Server
   
   General:
     Name: Nova Corrente Local
   
   Connection:
     Host: localhost
     Port: 5432
     Database: nova_corrente
     Username: nova_corrente
     Password: strong_password
     [x] Save password
   ```

3. **Explorar database**
   - Schemas → core, analytics, support
   - Tables → dim_*, fact_*
   - Query Tool → executar queries

---

## ✅ CHECKLIST FINAL

### Infraestrutura
- [ ] PostgreSQL 15 instalado
- [ ] Serviço postgresql-x64-15 rodando
- [ ] pgAdmin 4 configurado
- [ ] .env criado

### Database
- [ ] Database nova_corrente criado
- [ ] Migrations aplicadas
- [ ] Schemas criados
- [ ] Tabelas criadas

### Seed Data
- [ ] Calendário: ~4000 linhas
- [ ] Items: 5+
- [ ] Sites: 4+
- [ ] Suppliers: 3+

### Partições
- [ ] 72 partições criadas

### Backup & Monitoring
- [ ] Script backup funciona
- [ ] pg_stat_statements habilitado
- [ ] pgAdmin conectado

---

## 🎯 PRÓXIMO PASSO IMEDIATO

```powershell
# 1. Download PostgreSQL 15
# https://www.postgresql.org/download/windows/

# 2. Após instalação:
psql --version
Get-Service postgresql-x64-15

# 3. Criar database
psql -U postgres -h localhost
# Executar SQLs do STEP 1.2

# 4. Configurar projeto
cd c:\Users\User\Desktop\work\gran_prix\gran_prix\backend
notepad .env
pip install alembic psycopg2-binary python-dotenv python-dateutil
alembic upgrade head

# 5. Seeds
python scripts\seed_calendar.py
python scripts\seed_master_data.py
python scripts\create_partitions.py

# 6. Backup
.\scripts\backup_database.ps1
```

**Tempo:** 2-3 horas  
**Resultado:** PostgreSQL 100% local, sem Docker

---

**Versão:** 2.0 (Local)  
**Status:** ✅ Pronto para Execução
