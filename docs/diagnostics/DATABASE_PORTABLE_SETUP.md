# 🗺️ SETUP POSTGRESQL PORTÁVEL (SEM INSTALAÇÃO)
## Usar PostgreSQL sem instalar no Windows

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** 📋 PostgreSQL Portable - Zero Instalação

---

## 🎯 OPÇÃO 1: POSTGRESQL PORTABLE (RECOMENDADO)

### Download e Configuração (15min)

#### STEP 1: Download PostgreSQL Portable

```powershell
# 1. Criar diretório para portable
cd c:\Users\User\Desktop\work\gran_prix\gran_prix
New-Item -ItemType Directory -Force -Path portable_db

# 2. Download PostgreSQL Portable
# Opção A: PostgreSQL Binaries (oficial)
# https://www.enterprisedb.com/download-postgresql-binaries

# Opção B: PostgreSQL Portable (community)
# https://github.com/garethflowers/postgresql-portable
# OU
# https://sourceforge.net/projects/postgresqlportable/
```

#### STEP 2: Extrair e Configurar

```powershell
# Assumindo que baixou o ZIP para Downloads
cd c:\Users\User\Desktop\work\gran_prix\gran_prix\portable_db

# Extrair (ajuste o caminho do ZIP)
Expand-Archive -Path "$env:USERPROFILE\Downloads\postgresql-*.zip" -DestinationPath .

# Estrutura esperada:
# portable_db/
#   ├── pgsql/
#   │   ├── bin/
#   │   ├── lib/
#   │   └── share/
#   └── data/  (será criado)
```

#### STEP 3: Inicializar Database Cluster

```powershell
cd portable_db\pgsql\bin

# Inicializar cluster de dados
.\initdb.exe -D ..\..\data -U postgres -W -E UTF8 --locale="Portuguese_Brazil"
# Quando pedir senha: strong_password

# Verificar criação
dir ..\..\data
# Deve mostrar: postgresql.conf, pg_hba.conf, base/, etc.
```

#### STEP 4: Configurar postgresql.conf

```powershell
# Editar configuração
notepad ..\..\data\postgresql.conf
```

```ini
# Adicionar/modificar estas linhas:
port = 5432
max_connections = 100
shared_buffers = 128MB
listen_addresses = 'localhost'

# Para pg_stat_statements
shared_preload_libraries = 'pg_stat_statements'
```

#### STEP 5: Configurar Autenticação (pg_hba.conf)

```powershell
notepad ..\..\data\pg_hba.conf
```

```conf
# Modificar linha local para md5:
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
```

#### STEP 6: Iniciar PostgreSQL Server

```powershell
# Iniciar servidor manualmente
.\pg_ctl.exe -D ..\..\data -l ..\..\data\logfile start

# Verificar status
.\pg_ctl.exe -D ..\..\data status

# Deve mostrar:
# pg_ctl: server is running (PID: XXXX)
```

#### STEP 7: Criar Database e User

```powershell
# Conectar como postgres
.\psql.exe -U postgres -h localhost
# Senha: strong_password
```

```sql
-- Criar usuário
CREATE USER nova_corrente WITH PASSWORD 'strong_password';

-- Criar database
CREATE DATABASE nova_corrente OWNER nova_corrente;

-- Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE nova_corrente TO nova_corrente;

-- Verificar
\l
\q
```

#### STEP 8: Atualizar .env do Projeto

```powershell
cd c:\Users\User\Desktop\work\gran_prix\gran_prix\backend
notepad .env
```

```ini
# Database (PostgreSQL Portable)
DATABASE_URL=postgresql://nova_corrente:strong_password@localhost:5432/nova_corrente
DB_HOST=localhost
DB_PORT=5432
DB_USER=nova_corrente
DB_PASSWORD=strong_password
DB_NAME=nova_corrente
```

#### STEP 9: Scripts de Controle (Start/Stop)

**Criar: `portable_db/start_postgres.ps1`**
```powershell
$PGSQL_BIN = "$PSScriptRoot\pgsql\bin"
$PGSQL_DATA = "$PSScriptRoot\data"

Write-Host "🚀 Iniciando PostgreSQL Portable..."

& "$PGSQL_BIN\pg_ctl.exe" -D $PGSQL_DATA -l "$PGSQL_DATA\logfile" start

if ($?) {
    Write-Host "✅ PostgreSQL rodando na porta 5432"
    Write-Host "📊 Conectar: psql -U nova_corrente -h localhost -d nova_corrente"
} else {
    Write-Host "❌ Erro ao iniciar PostgreSQL"
}
```

**Criar: `portable_db/stop_postgres.ps1`**
```powershell
$PGSQL_BIN = "$PSScriptRoot\pgsql\bin"
$PGSQL_DATA = "$PSScriptRoot\data"

Write-Host "🛑 Parando PostgreSQL Portable..."

& "$PGSQL_BIN\pg_ctl.exe" -D $PGSQL_DATA stop

Write-Host "✅ PostgreSQL parado"
```

**Criar: `portable_db/status_postgres.ps1`**
```powershell
$PGSQL_BIN = "$PSScriptRoot\pgsql\bin"
$PGSQL_DATA = "$PSScriptRoot\data"

& "$PGSQL_BIN\pg_ctl.exe" -D $PGSQL_DATA status
```

#### STEP 10: Usar no Projeto

```powershell
# 1. Iniciar PostgreSQL
cd c:\Users\User\Desktop\work\gran_prix\gran_prix\portable_db
.\start_postgres.ps1

# 2. Aplicar migrations
cd ..\backend
alembic upgrade head

# 3. Executar seeds
python scripts\seed_calendar.py
python scripts\seed_master_data.py
python scripts\create_partitions.py

# 4. Parar quando terminar
cd ..\portable_db
.\stop_postgres.ps1
```

---

## 🎯 OPÇÃO 2: NEON.TECH (CLOUD GRÁTIS)

### PostgreSQL Cloud Serverless (0min setup)

#### STEP 1: Criar Conta Gratuita

```
1. Acessar: https://neon.tech
2. Criar conta (GitHub, Google ou Email)
3. Tier Gratuito:
   - 0.5 GB storage
   - Serverless (paga só quando usa)
   - PostgreSQL 15+
```

#### STEP 2: Criar Database

```
1. Dashboard → Create Project
2. Project Name: nova-corrente
3. PostgreSQL Version: 15
4. Region: AWS US East (mais próximo do Brasil)
5. Criar
```

#### STEP 3: Obter Connection String

```
Dashboard → Connection Details:

Host: ep-xxx.us-east-2.aws.neon.tech
Database: neondb
User: nova_corrente_user
Password: (copiar)
Port: 5432

Connection String:
postgresql://nova_corrente_user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

#### STEP 4: Atualizar .env

```ini
# Neon.tech Cloud Database
DATABASE_URL=postgresql://nova_corrente_user:PASSWORD@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
DB_HOST=ep-xxx.us-east-2.aws.neon.tech
DB_PORT=5432
DB_USER=nova_corrente_user
DB_PASSWORD=password_gerado
DB_NAME=neondb
```

#### STEP 5: Aplicar Schema

```powershell
cd backend
alembic upgrade head
python scripts\seed_calendar.py
python scripts\seed_master_data.py
```

**✅ Vantagens Neon:**
- Zero configuração local
- Backup automático
- Alta disponibilidade
- SSL incluso
- Dashboard web

---

## 🎯 OPÇÃO 3: SUPABASE (CLOUD GRÁTIS)

### PostgreSQL Cloud com Interface Visual

#### Setup Rápido

```
1. https://supabase.com
2. Start your project (grátis)
3. Project Settings → Database
4. Connection String:
   postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres
```

**✅ Vantagens Supabase:**
- 500 MB grátis
- SQL Editor visual
- Backup automático
- API REST automática

---

## 🎯 OPÇÃO 4: ELEPHANTSQL (CLOUD GRÁTIS)

### PostgreSQL Cloud Tradicional

```
1. https://www.elephantsql.com
2. Plano Tiny Turtle (grátis)
   - 20 MB storage
   - 5 conexões simultâneas
3. Connection String fornecida
```

---

## ⚖️ COMPARAÇÃO DAS OPÇÕES

| Opção | Vantagem | Desvantagem | Recomendado Para |
|-------|----------|-------------|------------------|
| **PostgreSQL Portable** | ✅ 100% local<br>✅ Offline<br>✅ Sem limites | ⚠️ Precisa baixar (~50MB)<br>⚠️ Manual start/stop | Desenvolvimento local |
| **Neon.tech** | ✅ Zero setup<br>✅ Serverless<br>✅ 0.5 GB grátis | ⚠️ Precisa internet<br>⚠️ Latência cloud | Prototipagem rápida |
| **Supabase** | ✅ Interface visual<br>✅ API REST<br>✅ 500 MB grátis | ⚠️ Precisa internet | Fullstack com frontend |
| **ElephantSQL** | ✅ Fácil setup<br>✅ Estável | ⚠️ Apenas 20 MB grátis | Testes pequenos |

---

## 🚀 RECOMENDAÇÃO FINAL

### Para seu caso (Nova Corrente):

**🥇 OPÇÃO 1: PostgreSQL Portable**
- ✅ Funciona 100% offline
- ✅ Sem necessidade de internet
- ✅ Performance máxima (local)
- ✅ Controle total
- ✅ Pode ser copiado para qualquer pasta
- ✅ Não modifica registro do Windows

**Passos Imediatos:**
```powershell
# 1. Download PostgreSQL Binaries
# https://www.enterprisedb.com/download-postgresql-binaries
# Escolher: PostgreSQL 15.x Windows x64 binaries

# 2. Extrair para portable_db/
cd c:\Users\User\Desktop\work\gran_prix\gran_prix
New-Item -ItemType Directory -Force -Path portable_db

# 3. Seguir STEP 2-10 acima
```

---

## 📝 TROUBLESHOOTING

### Problema: pg_ctl não encontrado

```powershell
# Adicionar ao PATH temporariamente
$env:Path += ";c:\Users\User\Desktop\work\gran_prix\gran_prix\portable_db\pgsql\bin"

# Testar
pg_ctl --version
```

### Problema: Porta 5432 em uso

```powershell
# Verificar quem está usando
netstat -ano | findstr :5432

# Mudar porta no postgresql.conf
notepad portable_db\data\postgresql.conf
# port = 5433

# Atualizar .env
DB_PORT=5433
```

### Problema: Senha incorreta

```powershell
# Editar pg_hba.conf para trust temporário
notepad portable_db\data\pg_hba.conf
# Mudar md5 → trust

# Reiniciar
cd portable_db\pgsql\bin
.\pg_ctl.exe -D ..\..\data restart

# Conectar sem senha e resetar
.\psql.exe -U postgres -h localhost
ALTER USER postgres PASSWORD 'nova_senha';

# Reverter pg_hba.conf para md5
```

---

**Status:** ✅ Pronto para usar PostgreSQL sem instalação!
