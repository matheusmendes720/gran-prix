# 🔄 GIT WORKFLOW - GUIA DE COLABORAÇÃO COMPLETO
## Nova Corrente - Pull Requests, Code Reviews & Branch Management

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Guia Completo Expandido

---

## 📋 ÍNDICE

1. [Adicionar Contribuidores no GitHub](#1-adicionar-contribuidores-no-github)
2. [Branch Naming Conventions](#2-branch-naming-conventions)
3. [Git Workflow - Pull Request Process](#3-git-workflow---pull-request-process)
4. [Code Review Guidelines](#4-code-review-guidelines)
5. [Branch Management Strategy](#5-branch-management-strategy)
6. [Merge Strategies](#6-merge-strategies)
7. [Troubleshooting](#7-troubleshooting)
8. [Comandos Essenciais](#8-comandos-essenciais)
9. [Best Practices](#9-best-practices)

---

## 1. ADICIONAR CONTRIBUIDORES NO GITHUB

### Opção 1: Adicionar como Colaborador (Simples)

#### Passo 1: Acessar Settings do Repositório
1. Acesse o repositório no GitHub: `https://github.com/YOUR_USERNAME/gran_prix`
2. Clique em **Settings** (Configurações) - ícone de engrenagem no topo
3. No menu lateral esquerdo, clique em **Collaborators** (Colaboradores)
4. Se não aparecer, você precisa ter permissões de admin no repositório

#### Passo 2: Adicionar Colaborador
1. Clique em **Add people** (Adicionar pessoas) - botão verde
2. Digite o username do GitHub ou email do colaborador
3. Selecione o nível de acesso:
   - **Read** - Apenas leitura (pode ver código, mas não pode fazer push)
   - **Write** - Pode fazer push direto (não recomendado para PR workflow)
   - **Maintain** - Pode gerenciar issues, pull requests, etc. (recomendado)
   - **Admin** - Acesso total (apenas para admins do projeto)

#### Passo 3: Colaborador Aceita Convite
1. O colaborador receberá um email de convite
2. Ele deve aceitar o convite clicando no link do email
3. Após aceitar, ele terá acesso ao repositório
4. Status mudará de "Pending" para "Active"

**Recomendação:** Use **Write** ou **Maintain** para colaboradores ativos que você confia

**Limitações:**
- Repositórios privados: Máximo 3 colaboradores no plano Free
- Repositórios públicos: Sem limite de colaboradores

---

### Opção 2: Fork & Pull Request (Recomendado para Code Review)

Este é o método recomendado para colaboração com code reviews obrigatórios:

#### Passo 1: Colaborador Faz Fork
1. Colaborador acessa o repositório no GitHub: `https://github.com/YOUR_USERNAME/gran_prix`
2. Clica em **Fork** (canto superior direito, próximo ao botão "Star")
3. Seleciona onde fazer fork (sua conta pessoal ou organização)
4. Aguarda fork ser criado (pode levar alguns segundos)
5. Isso cria uma cópia completa do repositório na conta do colaborador

**Vantagens do Fork:**
- ✅ Código do colaborador fica isolado
- ✅ Code reviews obrigatórios
- ✅ Não afeta repositório original
- ✅ Colaborador pode trabalhar sem restrições no fork

#### Passo 2: Colaborador Clona Fork
```bash
# Colaborador clona seu fork (não o repositório original!)
git clone https://github.com/COLLABORATOR_USERNAME/gran_prix.git
cd gran_prix

# Adiciona repositório original como upstream (para atualizar fork)
git remote add upstream https://github.com/YOUR_USERNAME/gran_prix.git

# Verifica remotes configurados
git remote -v
# Deve mostrar:
# origin    https://github.com/COLLABORATOR_USERNAME/gran_prix.git (fetch)
# origin    https://github.com/COLLABORATOR_USERNAME/gran_prix.git (push)
# upstream  https://github.com/YOUR_USERNAME/gran_prix.git (fetch)
# upstream  https://github.com/YOUR_USERNAME/gran_prix.git (push)
```

**Explicação dos Remotes:**
- **origin:** Fork do colaborador (onde ele faz push)
- **upstream:** Repositório original (para atualizar fork)

#### Passo 3: Colaborador Trabalha em Branch
```bash
# Atualiza fork com código mais recente do repositório original
git fetch upstream
git checkout master
git merge upstream/master
# Ou use rebase: git rebase upstream/master

# Cria nova branch para feature
git checkout -b feature/nome-da-feature
# Exemplos:
# git checkout -b feature/data-ingestion-pipeline
# git checkout -b fix/api-authentication-error
# git checkout -b docs/validation-guide-update
```

**Vantagens do Fork & PR:**
- ✅ Code reviews obrigatórios
- ✅ Melhor controle de qualidade
- ✅ Histórico limpo
- ✅ Não permite push direto (mais seguro)
- ✅ Colaborador pode trabalhar livremente no fork

**Desvantagens:**
- ⚠️ Fork pode ficar desatualizado (requer atualização manual)
- ⚠️ Mais passos para colaborador iniciante

---

### Opção 3: Organização GitHub (Para Times)

Para projetos maiores com múltiplos colaboradores, use uma GitHub Organization:

#### Passo 1: Criar Organization
1. GitHub → **+** (canto superior direito) → **New organization**
2. Escolha plano:
   - **Free:** Para times pequenos (público ou privado)
   - **Team:** $4/user/mês (recursos avançados)
   - **Enterprise:** Para empresas grandes
3. Configure:
   - **Organization name:** Ex: `nova-corrente-team`
   - **Email:** Email de contato
   - **Type:** Company ou Open source

#### Passo 2: Adicionar Membros
1. Organization → **People** → **Invite member**
2. Adicione membros por:
   - Username do GitHub
   - Email (se tiver conta GitHub associada)
3. Configure roles:
   - **Member** - Acesso padrão aos repositórios da organização
   - **Owner** - Acesso total (apenas para fundadores/admins)

#### Passo 3: Configurar Repository Permissions
1. Organization → **Settings** → **Repository permissions**
2. Configure níveis de acesso padrão:
   - **Read** - Apenas leitura
   - **Write** - Pode fazer push
   - **Admin** - Acesso total
3. Configure **Team permissions** (se usar teams):
   - Crie teams: `backend-team`, `frontend-team`, `data-team`
   - Atribua permissões por team

#### Passo 4: Transferir Repositório para Organization (Opcional)
1. Repositório → **Settings** → **Transfer ownership**
2. Selecione a organization
3. Confirme transferência

**Vantagens da Organization:**
- ✅ Gerenciamento centralizado de membros
- ✅ Melhor controle de permissões
- ✅ Teams e projetos organizados
- ✅ Billing centralizado
- ✅ Melhor para projetos grandes

**Quando Usar:**
- ✅ Times com 3+ pessoas
- ✅ Projetos com múltiplos repositórios
- ✅ Necessidade de controle granular de permissões

---

## 2. BRANCH NAMING CONVENTIONS

### Convenção Padrão

```
<tipo>/<nome-descritivo>
```

### Tipos de Branch

| Tipo | Prefixo | Descrição | Exemplo |
|------|---------|-----------|---------|
| **Feature** | `feature/` | Nova funcionalidade | `feature/data-ingestion-pipeline` |
| **Bugfix** | `fix/` | Correção de bug | `fix/api-authentication-error` |
| **Hotfix** | `hotfix/` | Correção urgente em produção | `hotfix/critical-security-patch` |
| **Refactor** | `refactor/` | Refatoração de código | `refactor/api-endpoints-structure` |
| **Documentation** | `docs/` | Documentação | `docs/api-documentation-update` |
| **Test** | `test/` | Testes | `test/integration-tests-backend` |
| **Chore** | `chore/` | Tarefas de manutenção | `chore/update-dependencies` |
| **Style** | `style/` | Mudanças de formatação | `style/format-code-with-black` |
| **Performance** | `perf/` | Melhorias de performance | `perf/optimize-database-queries` |
| **Security** | `security/` | Correções de segurança | `security/fix-sql-injection` |

### Convenção por Pessoa (Opcional)

Se quiser identificar quem criou a branch:

```
<tipo>/<pessoa>-<nome-descritivo>
```

**Exemplos:**
- `feature/matheus-data-pipeline`
- `fix/joao-api-error`
- `docs/maria-validation-guide`
- `refactor/pedro-api-structure`

**Nota:** GitHub mostra o autor do commit, então isso pode ser redundante. Mas pode ser útil para identificar quem está trabalhando em quê.

### Convenção por Cluster (4-Day Sprint)

Durante o sprint de 4 dias, use convenção por cluster:

```
sprint-4day/<cluster>/<dia>-<descricao>
```

**Exemplos:**
- `sprint-4day/data-cluster/day1-storage-ingestion`
- `sprint-4day/backend-cluster/day2-api-endpoints`
- `sprint-4day/frontend-cluster/day3-charts-interactions`
- `sprint-4day/deploy-cluster/day4-handover`

### Regras de Nomeação

1. **Use lowercase:** `feature/data-pipeline` ✅ (não `Feature/Data-Pipeline` ❌)
2. **Use hífens:** `feature/data-ingestion` ✅ (não `feature/data_ingestion` ❌)
3. **Seja descritivo:** `feature/data-ingestion-pipeline` ✅ (não `feature/new-thing` ❌)
4. **Mantenha curto:** Máximo 50 caracteres (ideal: 30-40)
5. **Sem espaços:** Use hífens ou underscores
6. **Sem caracteres especiais:** Apenas letras, números, hífens, underscores

### Exemplos Bons vs Ruins

**✅ Bons:**
- `feature/data-ingestion-pipeline`
- `fix/api-authentication-error`
- `docs/validation-guide-update`
- `refactor/api-endpoints-structure`

**❌ Ruins:**
- `new-feature` (sem tipo)
- `fix` (sem descrição)
- `Feature/Data-Pipeline` (uppercase, sem hífen)
- `feature/data_ingestion_pipeline` (underscores em vez de hífens)
- `feature/add-data-stuff` (muito vago)

---

## 3. GIT WORKFLOW - PULL REQUEST PROCESS

### Workflow Completo Visual

```
┌─────────────────────────────────────┐
│   MAIN REPOSITORY (master)         │
│   https://github.com/YOU/gran_prix │
└──────────────┬──────────────────────┘
               │
               │ 1. Fork
               ▼
┌─────────────────────────────────────┐
│   COLLABORATOR FORK                 │
│   https://github.com/COLLAB/gran_prix│
└──────────────┬──────────────────────┘
               │
               │ 2. Clone
               ▼
┌─────────────────────────────────────┐
│   COLLABORATOR LOCAL REPO           │
│   git clone ...                     │
└──────────────┬──────────────────────┘
               │
               │ 3. Create Branch
               ▼
┌─────────────────────────────────────┐
│   feature/data-pipeline (local)     │
│   git checkout -b feature/...       │
└──────────────┬──────────────────────┘
               │
               │ 4. Work & Commit
               ▼
┌─────────────────────────────────────┐
│   feature/data-pipeline (local)     │
│   git add . && git commit           │
└──────────────┬──────────────────────┘
               │
               │ 5. Push to Fork
               ▼
┌─────────────────────────────────────┐
│   feature/data-pipeline (fork)      │
│   git push origin feature/...       │
└──────────────┬──────────────────────┘
               │
               │ 6. Create PR
               ▼
┌─────────────────────────────────────┐
│   Pull Request (GitHub)             │
│   Base: master, Compare: feature/...│
└──────────────┬──────────────────────┘
               │
               │ 7. Code Review
               ▼
┌─────────────────────────────────────┐
│   Review & Feedback                 │
│   ✅ Approve / ❌ Request Changes   │
└──────────────┬──────────────────────┘
               │
               │ 8. Apply Feedback (if needed)
               ▼
┌─────────────────────────────────────┐
│   Updated PR                        │
│   git push origin feature/...       │
└──────────────┬──────────────────────┘
               │
               │ 9. Merge
               ▼
┌─────────────────────────────────────┐
│   master (updated)                  │
│   Squash & Merge / Merge Commit     │
└─────────────────────────────────────┘
```

---

### Passo a Passo Detalhado

#### Passo 1: Colaborador Atualiza Fork (Opcional mas Recomendado)

**Objetivo:** Garantir que fork está atualizado com código mais recente

```bash
# Busca mudanças do repositório original
git fetch upstream

# Atualiza branch master local com código mais recente
git checkout master
git merge upstream/master
# Ou use rebase para histórico mais limpo:
# git rebase upstream/master

# Push atualização para fork (opcional, mas recomendado)
git push origin master
```

**Por que fazer isso:**
- ✅ Evita conflitos futuros
- ✅ Garante que está trabalhando com código mais recente
- ✅ Facilita merge posterior

**Quando fazer:**
- ✅ Antes de criar nova branch
- ✅ Periodicamente durante desenvolvimento (se branch for longa)
- ✅ Antes de criar Pull Request

---

#### Passo 2: Colaborador Cria Branch

**Objetivo:** Isolar mudanças em branch separada

```bash
# Cria e muda para nova branch em um comando
git checkout -b feature/nome-da-feature

# Ou usando o novo comando do Git (2.23+)
git switch -c feature/nome-da-feature

# Exemplos:
# git checkout -b feature/data-ingestion-pipeline
# git checkout -b fix/api-authentication-error
# git checkout -b docs/validation-guide-update
# git checkout -b refactor/api-endpoints-structure
```

**Verificar branch criada:**
```bash
# Ver branch atual
git branch

# Ver todas branches (local + remote)
git branch -a
```

**Boas práticas:**
- ✅ Use naming convention (`feature/`, `fix/`, etc.)
- ✅ Seja descritivo no nome
- ✅ Crie branch a partir de master atualizado

---

#### Passo 3: Colaborador Trabalha e Commita

**Objetivo:** Fazer mudanças e commitá-las

```bash
# 1. Faz mudanças no código
# ... edita arquivos ...

# 2. Verifica mudanças
git status

# 3. Adiciona arquivos ao staging
git add .                    # Adiciona tudo
# ou
git add arquivo1.py arquivo2.py  # Adiciona arquivos específicos

# 4. Commit com mensagem descritiva
git commit -m "feat: add data ingestion pipeline

- Implement MinIO/S3 integration
- Add extractor scripts for external APIs
- Add validation logic for data quality
- Add error handling and logging

Closes #123"
```

**Formato de Commit Message (Conventional Commits):**

```
<tipo>(<escopo>): <descrição>

<corpo opcional>

<rodapé opcional>
```

**Tipos de Commit:**
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `style:` - Formatação (não afeta lógica)
- `refactor:` - Refatoração
- `test:` - Testes
- `chore:` - Tarefas de manutenção
- `perf:` - Performance
- `ci:` - CI/CD

**Exemplos:**
```bash
# Feature
git commit -m "feat(api): add data refresh endpoint"

# Bugfix
git commit -m "fix(auth): resolve JWT token expiration issue"

# Documentation
git commit -m "docs(validation): update validation guide"

# Multiple commits em branch
git commit -m "feat(data): add extractor scripts"
git commit -m "feat(data): add validation logic"
git commit -m "test(data): add unit tests for extractors"
```

**Boas práticas:**
- ✅ Commits pequenos e focados (uma mudança por commit)
- ✅ Mensagens descritivas
- ✅ Use conventional commits format
- ✅ Referencie issues (Closes #123)

---

#### Passo 4: Colaborador Faz Push para Fork

**Objetivo:** Enviar branch para fork no GitHub

```bash
# Push branch para fork (não para upstream!)
git push origin feature/nome-da-feature

# Se for a primeira vez, use -u para setar upstream tracking:
git push -u origin feature/nome-da-feature

# Após primeira vez, pode usar apenas:
git push
```

**Verificar push:**
```bash
# Ver branches remotas
git branch -r

# Ver status
git status
```

**Troubleshooting:**
- Se push falhar, verifique se está fazendo push para `origin` (fork), não `upstream`
- Se branch não existe remotamente, use `-u` na primeira vez
- Se conflitos, atualize branch primeiro: `git pull origin feature/nome-da-feature`

---

#### Passo 5: Colaborador Cria Pull Request no GitHub

**Objetivo:** Solicitar merge de mudanças para repositório original

**Passo a Passo:**

1. **Acessar Fork no GitHub:**
   - Acesse: `https://github.com/COLLABORATOR_USERNAME/gran_prix`
   - Você verá uma mensagem amarela: "feature/nome-da-feature had recent pushes"
   - Clique em **Compare & pull request**

2. **Ou Criar Manualmente:**
   - Clique em **Pull requests** (aba no topo)
   - Clique em **New pull request** (botão verde)

3. **Selecionar Branches:**
   - **Base repository:** `YOUR_USERNAME/gran_prix` (repositório original)
   - **Base:** `master` (branch de destino)
   - **Compare repository:** `COLLABORATOR_USERNAME/gran_prix` (fork)
   - **Compare:** `feature/nome-da-feature` (branch de origem)

4. **Preencher Template:**
   - **Título:** Descritivo (ex: "feat: Add data ingestion pipeline")
   - **Descrição:** Preencha template completo:
     - Tipo de mudança
     - Checklist
     - Screenshots (se aplicável)
     - Issues relacionadas
     - Notas adicionais

5. **Configurar PR:**
   - **Reviewers:** Marque reviewers (opcional)
   - **Assignees:** Atribua a si mesmo ou outros (opcional)
   - **Labels:** Adicione labels (feature, bugfix, etc.)
   - **Projects:** Associe a projeto (se aplicável)
   - **Milestone:** Associe a milestone (se aplicável)

6. **Criar PR:**
   - Clique em **Create pull request** (botão verde)
   - PR será criada e aparecerá na lista de PRs

**Template de PR Description:**

```markdown
## 📋 Descrição
Breve descrição do que foi implementado/corrigido.

## 🔢 Tipo de Mudança
- [ ] 🐛 Bugfix
- [ ] ✨ Feature
- [ ] 📝 Documentação
- [ ] 🔧 Refactor

## ✅ Checklist
- [ ] Código testado localmente
- [ ] Testes passando
- [ ] Documentação atualizada
- [ ] Sem breaking changes

## 🔗 Issues Relacionadas
Closes #123
Fixes #456
```

---

#### Passo 6: Code Review (Agora)

Veja seção [Code Review Guidelines](#4-code-review-guidelines)

**Processo:**
1. Maintainer revisa código
2. Adiciona comentários inline ou gerais
3. Aprova ou solicita mudanças
4. Colaborador aplica feedback
5. PR atualiza automaticamente
6. Re-review se necessário

---

#### Passo 7: Merge Pull Request

**Após aprovação, maintainer faz merge:**

**Opção 1: Squash and Merge (Recomendado para Features)**

**Quando usar:**
- Features simples
- Múltiplos commits pequenos
- Histórico limpo desejado

**Como fazer:**
1. GitHub PR → **Squash and merge** (dropdown)
2. Edita mensagem de commit (se necessário)
3. Clique em **Confirm squash and merge**

**Resultado:**
```
Antes:
master: [commit 1] [commit 2] [commit 3] [commit 4] [commit 5]

Depois:
master: [single squashed commit with all changes]
```

**Vantagens:**
- ✅ Histórico limpo
- ✅ Um commit por feature
- ✅ Fácil de reverter

**Desvantagens:**
- ❌ Perde histórico detalhado de commits individuais

---

**Opção 2: Merge Commit (Recomendado para Branches Complexas)**

**Quando usar:**
- Branches com muitos commits significativos
- Preservar histórico detalhado
- Features complexas

**Como fazer:**
1. GitHub PR → **Create a merge commit** (dropdown)
2. Clique em **Confirm merge**

**Resultado:**
```
Antes:
master: [commit 1] [commit 2]
feature: [commit A] [commit B] [commit C]

Depois:
master: [commit 1] [commit 2] [merge commit] [commit A] [commit B] [commit C]
```

**Vantagens:**
- ✅ Preserva histórico completo
- ✅ Fácil de ver todas mudanças
- ✅ Merge commit documenta quando foi merged

**Desvantagens:**
- ❌ Histórico mais "poluído" com merge commits

---

**Opção 3: Rebase and Merge (Recomendado para Histórico Linear)**

**Quando usar:**
- Histórico linear é importante
- Branches pequenas
- Sem necessidade de merge commit

**Como fazer:**
1. GitHub PR → **Rebase and merge** (dropdown)
2. Clique em **Confirm rebase and merge**

**Resultado:**
```
Antes:
master: [commit 1] [commit 2]
feature: [commit A] [commit B]

Depois:
master: [commit 1] [commit 2] [commit A] [commit B]
```

**Vantagens:**
- ✅ Histórico linear limpo
- ✅ Sem merge commits
- ✅ Fácil de seguir

**Desvantagens:**
- ⚠️ Rebase pode ser complicado se branch já foi compartilhada
- ⚠️ Rewrites history (muda commit hashes)

**⚠️ Atenção:** Rebase não deve ser usado se:
- Branch já foi compartilhada com outros
- Commits foram referenciados em outros lugares
- Histórico precisa ser preservado exatamente como foi

---

**Recomendação Geral:**
- **Features simples:** Squash and merge
- **Features complexas:** Merge commit
- **Histórico linear crítico:** Rebase and merge (com cuidado)

---

#### Passo 8: Após Merge

**Colaborador atualiza fork:**

```bash
# Atualiza master local com código merged
git checkout master
git fetch upstream
git merge upstream/master

# Push para fork
git push origin master

# Deleta branch local (opcional, mas recomendado)
git branch -d feature/nome-da-feature

# Deleta branch remota no fork (opcional)
git push origin --delete feature/nome-da-feature
```

**GitHub deleta branch automaticamente:**
- Após merge, GitHub oferece opção de deletar branch
- Marque checkbox "Delete branch" se quiser

---

## 4. CODE REVIEW GUIDELINES

### Checklist de Code Review

#### Para o Reviewer (Você - Maintainer)

**Funcionalidade:**
- [ ] Código funciona como esperado?
- [ ] Atende aos requisitos da issue/PR?
- [ ] Casos edge tratados?
- [ ] Error handling adequado?

**Código Limpo:**
- [ ] Código segue padrões do projeto?
- [ ] Naming conventions seguidas?
- [ ] Formatação consistente?
- [ ] Sem código duplicado (DRY principle)?
- [ ] Código legível e bem documentado?

**Testes:**
- [ ] Testes incluídos?
- [ ] Testes passando?
- [ ] Cobertura adequada?
- [ ] Testes significativos (não apenas "testa que funciona")?

**Documentação:**
- [ ] README atualizado (se necessário)?
- [ ] Docstrings/comentários adicionados?
- [ ] Changelog atualizado?
- [ ] Breaking changes documentados?

**ML Ops Constraint (Se aplicável):**
- [ ] Sem dependências ML em código de deployment?
- [ ] Sem endpoints ML (inference, training)?
- [ ] Sem imports ML em código de deployment?
- [ ] Validação executada e passando?

**Performance:**
- [ ] Sem performance regressions?
- [ ] Queries otimizadas (se aplicável)?
- [ ] Caching usado quando apropriado?

**Segurança:**
- [ ] Sem vulnerabilidades introduzidas?
- [ ] Dados sensíveis protegidos?
- [ ] Autenticação/autorização correta?
- [ ] Input validation adequada?

---

#### Para o Autor (Colaborador)

**Antes de Criar PR:**
- [ ] Código testado localmente?
- [ ] Todos os testes passando?
- [ ] Documentação atualizada?
- [ ] Commits descritivos?
- [ ] PR description completa?
- [ ] Sem merge conflicts?
- [ ] Branch atualizada com master?

**Após Review:**
- [ ] Feedback aplicado?
- [ ] Testes ainda passando após mudanças?
- [ ] Re-request review se necessário?

---

### Tipos de Comentários

#### ✅ Aprovação
```
Looks good to me! ✅
Ready to merge! 🚀
Great work! Just a few minor suggestions below.
```

#### ❌ Solicitar Mudanças
```
Please fix the following:
- [ ] Issue 1: [descrição]
- [ ] Issue 2: [descrição]
- [ ] Issue 3: [descrição]

Once fixed, I'll approve!
```

#### 💬 Comentário Geral
```
Nice work! Consider:
- Option 1: [descrição]
- Option 2: [descrição]

This would make the code more [benefício].
```

#### 🐛 Bug Identificado
```
Found a bug here:
[descrição do bug]

Suggested fix:
[descrição da solução]
```

#### 💡 Sugestão de Melhoria
```
Consider improving:
[descrição]

This would make the code:
- [benefício 1]
- [benefício 2]
```

#### 📝 Comentário Inline
```
// Sugestão de código inline
// Antes:
old_code();

// Depois:
new_code();
```

---

### Processo de Review

#### Passo 1: Review Automático (CI/CD)

**GitHub Actions roda automaticamente:**
- ✅ Validação ML Ops constraint
- ✅ Testes automatizados
- ✅ Code quality checks
- ✅ Linting
- ✅ Build verification

**Verificar status:**
- PR mostra status checks no topo
- ✅ Verde = passou
- ❌ Vermelho = falhou
- ⏳ Amarelo = rodando

**Não aprovar PR se:**
- ❌ Status checks falhando
- ❌ Build falhando
- ❌ Testes falhando

---

#### Passo 2: Review Manual

**1. Review de Código:**
- Clique em **Files changed** no PR
- Adicione comentários inline:
  - Clique em linha de código
  - Digite comentário
  - Clique em **Add single comment** ou **Start a review**

- **Comentário único:**
  - Comentário isolado
  - Não precisa de aprovação final

- **Review completo:**
  - Múltiplos comentários
  - Ao final, escolha:
    - ✅ **Comment** - Apenas comentário
    - ✅ **Approve** - Aprova PR
    - ❌ **Request changes** - Solicita mudanças

**2. Comentários Gerais:**
- Use seção de comentários no final da PR
- Para feedback geral, não específico de código

**3. Sugestões de Código:**
- GitHub permite sugerir mudanças direto no PR
- Colaborador pode aceitar sugestão com um clique
- Facilita muito o processo

**4. Aprovação:**
- **No mínimo 1 aprovação** antes de merge (configurável)
- Para mudanças críticas, **2+ aprovações** recomendadas
- Você pode configurar isso em Branch Protection Rules

---

#### Passo 3: Resolver Feedback

**Colaborador:**
1. Faz mudanças baseadas no feedback
2. Commita e push para mesma branch:
   ```bash
   git add .
   git commit -m "fix: address review feedback"
   git push origin feature/nome-da-feature
   ```
3. PR atualiza automaticamente
4. Re-request review se necessário:
   - Clique em **Re-request review** no PR
   - Ou mencione reviewer: `@username`

**Reviewer:**
1. Recebe notificação de atualização
2. Revisa mudanças
3. Aprova ou solicita mais mudanças

---

## 5. BRANCH MANAGEMENT STRATEGY

### Estratégia Recomendada

```
master (production-ready)
  │
  ├── develop (integration branch - opcional)
  │     │
  │     ├── feature/data-pipeline (Matheus)
  │     ├── feature/api-endpoints (João)
  │     ├── fix/auth-bug (Maria)
  │     └── docs/validation-guide (Pedro)
  │
  └── hotfix/critical-patch (urgente)
```

### Estratégia 1: Branch por Pessoa (Simples)

**Quando usar:** Projetos pequenos, times pequenos (2-3 pessoas)

```
master
  ├── feature/matheus-data-pipeline
  ├── feature/joao-api-endpoints
  ├── feature/maria-frontend-dashboard
  └── fix/pedro-auth-bug
```

**Vantagens:**
- ✅ Simples de gerenciar
- ✅ Fácil identificar quem trabalha em quê
- ✅ Menos conflitos

**Desvantagens:**
- ❌ Não escala bem para times grandes
- ❌ Pode ter nomes duplicados

---

### Estratégia 2: Branch por Feature + Pessoa (Recomendado)

**Quando usar:** Times médios/grandes, features complexas

```
master
  ├── feature/data-pipeline
  │     ├── feature/data-pipeline-matheus-extraction
  │     ├── feature/data-pipeline-joao-transformation
  │     └── feature/data-pipeline-maria-validation
  ├── feature/api-endpoints
  │     ├── feature/api-endpoints-joao-items
  │     └── feature/api-endpoints-pedro-forecasts
  └── fix/auth-bug
        └── fix/auth-bug-maria
```

**Workflow:**
1. Criar branch da feature no repositório principal (ou fork)
2. Cada pessoa cria sub-branch da feature
3. PRs individuais para branch da feature
4. Após todos PRs aprovados, merge feature para master

**Vantagens:**
- ✅ Organização por feature
- ✅ Colaboração em mesma feature
- ✅ Histórico limpo por feature

---

### Estratégia 3: Branch por Cluster (4-Day Sprint)

**Quando usar:** Durante o sprint de 4 dias

```
master
  ├── sprint-4day/data-cluster
  │     ├── sprint-4day/data-cluster-day1
  │     ├── sprint-4day/data-cluster-day2
  │     └── sprint-4day/data-cluster-day3
  ├── sprint-4day/backend-cluster
  │     ├── sprint-4day/backend-cluster-day1
  │     └── sprint-4day/backend-cluster-day2
  ├── sprint-4day/frontend-cluster
  │     └── sprint-4day/frontend-cluster-day1
  └── sprint-4day/deploy-cluster
        └── sprint-4day/deploy-cluster-day1
```

**Workflow:**
1. Cada cluster cria branch principal
2. Daily branches para entregas diárias
3. PRs diários para branch do cluster
4. Merge cluster para master no final do sprint

---

### Branch Protection Rules

**Configure no GitHub para proteger master:**

1. **Acessar Settings:**
   - GitHub → Repositório → **Settings**
   - Menu lateral → **Branches**

2. **Adicionar Rule:**
   - Clique em **Add rule**
   - Em **Branch name pattern**, digite: `master`

3. **Configurar Regras:**

   **Required pull request reviews before merging:**
   - ✅ **Require pull request reviews before merging**
   - ✅ **Required approvals:** 1 (ou mais, conforme necessário)
   - ✅ **Dismiss stale reviews when new commits are pushed**
   - ✅ **Require review from Code Owners** (se configurado)
   - ✅ **Restrict who can dismiss pull request reviews** (opcional)

   **Require status checks to pass before merging:**
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
   - ✅ **Status checks:** Selecione workflows:
     - `validate-deployment`
     - `pre-deploy-validation`
     - Outros checks relevantes

   **Restrict who can push to matching branches:**
   - ✅ (Opcional) Permitir apenas certos usuários/teams

   **Include administrators:**
   - ✅ (Opcional) Aplicar regras também para admins

4. **Salvar:**
   - Clique em **Create** para salvar regras

**Resultado:**
- ✅ Ninguém pode fazer push direto para master
- ✅ PRs obrigatórias antes de merge
- ✅ Code reviews obrigatórios
- ✅ Status checks devem passar
- ✅ Branches devem estar atualizadas

---

### Como Gerenciar Branches de Cada Pessoa

#### Cenário 1: Cada Pessoa Trabalha em Feature Separada

```bash
# Matheus trabalha em data pipeline
git checkout -b feature/matheus-data-pipeline

# João trabalha em API endpoints
git checkout -b feature/joao-api-endpoints

# Maria trabalha em bug fix
git checkout -b fix/maria-auth-bug
```

**Vantagens:**
- ✅ Isolamento de mudanças
- ✅ Menos conflitos
- ✅ Merge independente

**Gerenciamento:**
- Cada pessoa trabalha independentemente
- PRs separados para cada feature
- Merge independente após aprovação

---

#### Cenário 2: Múltiplas Pessoas na Mesma Feature

**Opção A: Sub-branches da Feature**

```bash
# Branch principal da feature (no repositório ou fork)
feature/data-pipeline

# Sub-branches por pessoa
feature/data-pipeline-matheus-extraction
feature/data-pipeline-joao-transformation
feature/data-pipeline-maria-validation
```

**Workflow:**
1. Criar branch principal da feature
2. Cada pessoa cria sub-branch da feature principal
3. Trabalha isoladamente na sub-branch
4. Faz PR para branch da feature (não para master)
5. Após todos PRs da feature aprovados, merge feature para master

**Exemplo:**
```bash
# Pessoa 1 cria feature principal
git checkout -b feature/data-pipeline
git push origin feature/data-pipeline

# Pessoa 2 cria sub-branch
git checkout feature/data-pipeline
git checkout -b feature/data-pipeline-matheus-extraction
# Trabalha e faz PR para feature/data-pipeline

# Pessoa 3 cria sub-branch
git checkout feature/data-pipeline
git checkout -b feature/data-pipeline-joao-transformation
# Trabalha e faz PR para feature/data-pipeline

# Após todos PRs mergeados em feature/data-pipeline:
# PR final: feature/data-pipeline → master
```

**Vantagens:**
- ✅ Colaboração em mesma feature
- ✅ Isolamento de mudanças por pessoa
- ✅ Histórico limpo por feature

---

**Opção B: Commits Sequenciais na Mesma Branch**

```bash
# Todos trabalham na mesma branch
feature/data-pipeline

# Pessoa 1: Commits iniciais
git commit -m "feat: add extraction logic"

# Pessoa 2: Puxa branch, adiciona commits
git pull origin feature/data-pipeline
git commit -m "feat: add transformation logic"

# Pessoa 3: Puxa branch, adiciona commits
git pull origin feature/data-pipeline
git commit -m "feat: add validation logic"
```

**Vantagens:**
- ✅ Simples
- ✅ Trabalho sequencial

**Desvantagens:**
- ❌ Mais conflitos
- ❌ Dependência entre pessoas
- ❌ Difícil rastrear quem fez o quê

**Recomendação:** Use Opção A (sub-branches) para evitar conflitos

---

### Comandos Úteis para Gerenciar Branches

#### Ver Todas as Branches

```bash
# Branches locais
git branch

# Branches remotas
git branch -r

# Todas (local + remote)
git branch -a

# Branches por pessoa (se usar naming convention)
git branch | grep matheus
git branch -r | grep joao
```

#### Ver Branches Merged

```bash
# Ver branches merged em master
git branch --merged master

# Ver branches não merged
git branch --no-merged master
```

#### Limpar Branches Antigas

```bash
# Deletar branches merged localmente
git branch --merged | grep -v master | xargs git branch -d

# Deletar branches merged remotamente
git push origin --delete nome-da-branch

# Deletar múltiplas branches
git branch --merged | grep -v master | xargs -n 1 git branch -d
```

#### Ver Histórico de Branches

```bash
# Histórico visual de todas branches
git log --oneline --graph --all --decorate

# Histórico de branch específica
git log --oneline --graph feature/nome-da-branch

# Ver quem trabalha em quê (último commit de cada branch)
git for-each-ref --format='%(refname:short) %(authorname) %(subject)' refs/heads/
```

---

## 6. MERGE STRATEGIES

### Squash and Merge (Recomendado para Features)

**Quando usar:**
- Features simples
- Múltiplos commits pequenos
- Histórico limpo desejado

**Como fazer:**
1. GitHub PR → Dropdown "Merge pull request"
2. Selecione **Squash and merge**
3. Edita mensagem de commit (se necessário)
4. Clique em **Confirm squash and merge**

**Resultado:**
```
Antes:
master:     [commit 1] [commit 2] [commit 3]
feature:    [commit A] [commit B] [commit C] [commit D] [commit E]

Depois:
master:     [commit 1] [commit 2] [commit 3] [squashed commit with all A-E changes]
```

**Vantagens:**
- ✅ Histórico limpo
- ✅ Um commit por feature
- ✅ Fácil de reverter (um commit)
- ✅ Mensagem de commit pode ser editada

**Desvantagens:**
- ❌ Perde histórico detalhado de commits individuais
- ❌ Não preserva autoria de commits individuais

---

### Merge Commit (Recomendado para Branches Complexas)

**Quando usar:**
- Branches com muitos commits significativos
- Preservar histórico detalhado
- Features complexas

**Como fazer:**
1. GitHub PR → Dropdown "Merge pull request"
2. Selecione **Create a merge commit**
3. Clique em **Confirm merge**

**Resultado:**
```
Antes:
master:     [commit 1] [commit 2]
feature:    [commit A] [commit B] [commit C]

Depois:
master:     [commit 1] [commit 2] [merge commit] [commit A] [commit B] [commit C]
```

**Vantagens:**
- ✅ Preserva histórico completo
- ✅ Fácil de ver todas mudanças
- ✅ Merge commit documenta quando foi merged
- ✅ Preserva autoria de commits individuais

**Desvantagens:**
- ❌ Histórico mais "poluído" com merge commits
- ❌ Mais difícil de seguir linearmente

---

### Rebase and Merge (Recomendado para Histórico Linear)

**Quando usar:**
- Histórico linear é importante
- Branches pequenas
- Sem necessidade de merge commit

**Como fazer:**
1. GitHub PR → Dropdown "Merge pull request"
2. Selecione **Rebase and merge**
3. Clique em **Confirm rebase and merge**

**Resultado:**
```
Antes:
master:     [commit 1] [commit 2]
feature:    [commit A] [commit B]

Depois:
master:     [commit 1] [commit 2] [commit A] [commit B]
```

**Vantagens:**
- ✅ Histórico linear limpo
- ✅ Sem merge commits
- ✅ Fácil de seguir
- ✅ Commits aparecem como se fossem feitos diretamente em master

**Desvantagens:**
- ⚠️ Rebase rewrites history (muda commit hashes)
- ⚠️ Pode ser complicado se branch foi compartilhada
- ⚠️ Não funciona bem se branch já foi mergeada em outros lugares

**⚠️ Atenção:** Rebase não deve ser usado se:
- Branch já foi compartilhada com outros
- Commits foram referenciados em outros lugares
- Histórico precisa ser preservado exatamente como foi
- Branch tem múltiplos colaboradores

---

### Recomendação Geral

**Para a maioria dos casos:**
- **Features simples:** ✅ Squash and merge
- **Features complexas:** ✅ Merge commit
- **Histórico linear crítico:** ✅ Rebase and merge (com cuidado)

**Para este projeto (Nova Corrente):**
- **Features:** ✅ Squash and merge (histórico limpo)
- **Hotfixes:** ✅ Merge commit (preservar histórico)
- **Documentação:** ✅ Squash and merge (simples)

---

## 7. TROUBLESHOOTING

### Problema: Merge Conflicts

**Sintoma:** GitHub mostra "This branch has conflicts that must be resolved"

#### Solução 1: Resolver no GitHub (Simples)

1. GitHub PR mostra conflitos
2. Clique em **Resolve conflicts** (botão)
3. GitHub abre editor online
4. Edita arquivos conflitantes:
   - Remove marcadores: `<<<<<<<`, `=======`, `>>>>>>>`
   - Mantém código correto
   - Remove código incorreto
5. Marca arquivo como resolvido: **Mark as resolved**
6. Repete para todos arquivos conflitantes
7. Clique em **Commit merge**

**Vantagens:**
- ✅ Não precisa de Git local
- ✅ Interface visual
- ✅ Fácil para iniciantes

**Desvantagens:**
- ❌ Não pode testar localmente antes de resolver
- ❌ Editor online limitado

---

#### Solução 2: Resolver Localmente (Avançado)

```bash
# Colaborador atualiza branch
git fetch upstream
git checkout feature/nome-da-feature
git merge upstream/master

# Git mostra conflitos
# Auto-merging arquivo.py
# CONFLICT (content): Merge conflict in arquivo.py

# Abre arquivo conflitante no editor
# Você verá:
<<<<<<< HEAD
seu código
=======
código do master
>>>>>>> upstream/master

# Edita arquivo:
# - Remove marcadores <<<<<<<, =======, >>>>>>>
# - Mantém código correto
# - Remove código incorreto

# Adiciona arquivo resolvido
git add arquivo.py

# Continua merge
git commit -m "resolve: merge conflicts with master"

# Push para fork
git push origin feature/nome-da-feature
```

**Vantagens:**
- ✅ Pode testar localmente antes
- ✅ Usa seu editor favorito
- ✅ Mais controle

**Desvantagens:**
- ❌ Requer Git local
- ❌ Mais complexo para iniciantes

---

### Problema: Branch Desatualizada

**Sintoma:** GitHub mostra "This branch is X commits behind master"

#### Solução: Atualizar Branch

```bash
# Colaborador atualiza branch
git fetch upstream
git checkout feature/nome-da-feature

# Opção 1: Merge (preserva histórico)
git merge upstream/master

# Opção 2: Rebase (histórico linear)
git rebase upstream/master

# Se houver conflitos, resolve e continua:
# Para merge:
git add .
git commit

# Para rebase:
git add .
git rebase --continue

# Push (force se usar rebase)
git push origin feature/nome-da-feature
# Se usar rebase, precisa force:
git push origin feature/nome-da-feature --force-with-lease
```

**⚠️ Atenção:** Force push só se necessário (após rebase). Use `--force-with-lease` para segurança.

---

### Problema: Commit Errado na Branch

**Sintoma:** Fez commit errado ou esqueceu de adicionar algo

#### Solução 1: Desfazer Último Commit (Mantém Mudanças)

```bash
# Desfaz commit mas mantém mudanças
git reset --soft HEAD~1

# Agora pode:
# - Editar arquivos
# - Adicionar mais arquivos: git add .
# - Fazer novo commit: git commit -m "mensagem corrigida"
```

#### Solução 2: Desfazer Commit e Mudanças

```bash
# Desfaz commit e todas mudanças (⚠️ cuidado!)
git reset --hard HEAD~1

# Mudanças são perdidas permanentemente!
```

#### Solução 3: Amendar Último Commit

```bash
# Adiciona mudanças ao último commit
git add arquivo-esquecido.py
git commit --amend -m "mensagem atualizada"

# Push force (se já foi pushado)
git push origin feature/nome-da-feature --force-with-lease
```

---

### Problema: Múltiplas Pessoas na Mesma Branch

**Sintoma:** Conflitos constantes, código sendo sobrescrito

**Solução:** Cada pessoa cria sub-branch

```bash
# Branch principal da feature
feature/data-pipeline

# Pessoa 1 cria sub-branch
git checkout feature/data-pipeline
git checkout -b feature/data-pipeline-pessoa1

# Pessoa 2 cria sub-branch
git checkout feature/data-pipeline
git checkout -b feature/data-pipeline-pessoa2

# Trabalham separadamente, fazem PRs separados
```

**Vantagens:**
- ✅ Isolamento de mudanças
- ✅ Menos conflitos
- ✅ PRs independentes

---

### Problema: PR Não Atualiza Após Push

**Sintoma:** Fez push mas PR não mostra mudanças

**Solução:**
1. Verifica se push foi para branch correta:
   ```bash
   git branch  # Ver branch atual
   git push origin feature/nome-da-feature  # Push para branch correta
   ```

2. Verifica se PR está apontando para branch correta:
   - GitHub PR → Ver branch de origem
   - Deve ser `feature/nome-da-feature`

3. Atualiza página do PR (refresh)

4. Se ainda não aparecer, verifica se há conflitos:
   - GitHub PR mostra status
   - Resolve conflitos se houver

---

## 8. COMANDOS ESSENCIAIS

### Para Colaboradores

#### Setup Inicial
```bash
# Clone fork
git clone https://github.com/SEU_USERNAME/gran_prix.git
cd gran_prix

# Configurar upstream
git remote add upstream https://github.com/YOUR_USERNAME/gran_prix.git

# Verificar remotes
git remote -v
```

#### Atualizar Fork
```bash
# Buscar mudanças
git fetch upstream

# Atualizar master
git checkout master
git merge upstream/master
git push origin master
```

#### Criar e Trabalhar em Branch
```bash
# Criar branch
git checkout -b feature/nome-da-feature

# Trabalhar e commitar
git add .
git commit -m "feat: descrição"

# Push para fork
git push origin feature/nome-da-feature
```

#### Atualizar Branch com Master
```bash
# Atualizar master
git fetch upstream
git checkout master
git merge upstream/master

# Atualizar branch
git checkout feature/nome-da-feature
git merge master
# ou
git rebase master
```

---

### Para Você (Maintainer)

#### Ver Branches de Colaboradores
```bash
# Ver todas branches remotas
git fetch origin
git branch -r

# Ver branches por pessoa
git branch -r | grep matheus
git branch -r | grep joao
```

#### Merge de PR Localmente (Se necessário)
```bash
# Atualizar master
git checkout master
git pull upstream master

# Merge branch de colaborador
git merge origin/feature/nome-da-feature

# Push
git push upstream master
```

#### Limpar Branches Antigas
```bash
# Ver branches merged
git branch --merged master

# Deletar branches merged
git branch --merged master | grep -v master | xargs git branch -d

# Deletar branches remotas merged
git push origin --delete nome-da-branch
```

---

## 9. BEST PRACTICES

### Para Colaboradores

1. **Sempre atualize fork antes de criar branch:**
   ```bash
   git fetch upstream
   git checkout master
   git merge upstream/master
   ```

2. **Use branches pequenas e focadas:**
   - Uma feature por branch
   - Commits pequenos e frequentes

3. **Commits descritivos:**
   - Use conventional commits
   - Referencie issues
   - Seja específico

4. **Atualize branch periodicamente:**
   - Se branch for longa, atualize com master periodicamente
   - Evita conflitos grandes

5. **Teste localmente antes de PR:**
   - Rode testes
   - Teste funcionalidade
   - Verifica linting

6. **Preencha PR description completamente:**
   - Use template
   - Seja descritivo
   - Adicione screenshots se aplicável

7. **Responda a feedback rapidamente:**
   - Aplica feedback
   - Comunica quando aplicado
   - Re-request review se necessário

---

### Para Você (Maintainer)

1. **Configure branch protection:**
   - Require PR reviews
   - Require status checks
   - Require branches up to date

2. **Review PRs rapidamente:**
   - Dentro de 24-48h
   - Seja claro no feedback
   - Seja respeitoso

3. **Use templates:**
   - PR template
   - Issue templates
   - Facilita trabalho de colaboradores

4. **Documente processo:**
   - Como fazer fork
   - Como criar PR
   - O que esperar no review

5. **Celebre contribuições:**
   - Agradeça colaboradores
   - Reconheça bom trabalho
   - Crie ambiente positivo

---

## 📋 CHECKLISTS RÁPIDAS

### Checklist para Colaborador (Criar PR)

- [ ] Fork do repositório criado
- [ ] Fork atualizado com upstream/master
- [ ] Branch criada seguindo naming convention
- [ ] Código implementado e testado
- [ ] Testes passando localmente
- [ ] Documentação atualizada
- [ ] Commits descritivos (conventional commits)
- [ ] Push para fork realizado
- [ ] PR criada com descrição completa
- [ ] Template de PR preenchido
- [ ] Screenshots adicionados (se aplicável)
- [ ] Issues relacionadas referenciadas

---

### Checklist para Maintainer (Review PR)

- [ ] CI/CD passando (status checks)
- [ ] Código revisado (funcionalidade, padrões, qualidade)
- [ ] Testes incluídos e passando
- [ ] Documentação atualizada
- [ ] Sem breaking changes (ou documentados)
- [ ] ML Ops constraint validada (se aplicável)
- [ ] Performance adequada
- [ ] Segurança verificada
- [ ] Aprovado ou feedback dado
- [ ] Merge realizado após aprovação
- [ ] Branch deletada após merge (opcional)

---

## 🔗 REFERÊNCIAS

### Documentação GitHub
- [Collaborating with pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)
- [Managing branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository)
- [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [Fork a repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

### Git Workflows
- [Git Branching Strategies](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [Conventional Commits](https://www.conventionalcommits.org/)

### Templates
- Pull Request Template: `.github/pull_request_template.md`
- Issue Templates: `.github/ISSUE_TEMPLATE/`

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Guia Completo Expandido de Colaboração

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

