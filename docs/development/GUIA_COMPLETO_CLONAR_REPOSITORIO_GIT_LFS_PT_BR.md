# 📚 Guia Completo: Clonar e Trabalhar com o Repositório Gran Prix (Git LFS)

**Projeto:** Nova Corrente - Demand Forecasting & Analytics System  
**Repositório:** `https://github.com/matheusmendes720/gran-prix.git`  
**Data:** Novembro 2025  
**Versão:** 1.0.0

---

## 🎯 Visão Geral

Este repositório utiliza **Git Large File Storage (LFS)** para gerenciar arquivos grandes (principalmente arquivos CSV de dados de ML). Todos os arquivos CSV são armazenados no Git LFS, permitindo que o repositório seja clonado e atualizado normalmente, mesmo com arquivos de centenas de megabytes.

**Importante:** É **OBRIGATÓRIO** instalar o Git LFS antes de clonar o repositório, caso contrário os arquivos grandes não serão baixados corretamente.

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação do Git LFS](#instalação-do-git-lfs)
3. [Clonar o Repositório](#clonar-o-repositório)
4. [Trabalhar com o Repositório](#trabalhar-com-o-repositório)
5. [Solução de Problemas](#solução-de-problemas)
6. [Comandos Úteis](#comandos-úteis)
7. [FAQ](#faq)

---

## 🔧 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- ✅ **Git** (versão 2.13.0 ou superior)
- ✅ **Git LFS** (versão 2.0.0 ou superior)
- ✅ **Python** 3.9+ (para desenvolvimento)
- ✅ **Node.js** 18+ (para o frontend)
- ✅ Acesso ao repositório GitHub

### Verificar Instalações

```bash
# Verificar versão do Git
git --version

# Verificar versão do Git LFS
git lfs version

# Verificar versão do Python
python --version

# Verificar versão do Node.js
node --version
```

---

## 📥 Instalação do Git LFS

### Windows

#### Opção 1: Usando o Instalador Oficial (Recomendado)

1. Baixe o instalador em: https://git-lfs.github.com/
2. Execute o instalador `git-lfs-windows-amd64.exe`
3. Siga o assistente de instalação
4. Reinicie o terminal/PowerShell

#### Opção 2: Usando Chocolatey

```powershell
# Instalar Chocolatey (se não tiver)
# Execute no PowerShell como Administrador:
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar Git LFS
choco install git-lfs
```

#### Opção 3: Usando Scoop

```powershell
scoop install git-lfs
```

### macOS

```bash
# Usando Homebrew (recomendado)
brew install git-lfs

# Ou usando MacPorts
sudo port install git-lfs
```

### Linux (Ubuntu/Debian)

```bash
# Adicionar o repositório do GitHub
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash

# Instalar Git LFS
sudo apt-get install git-lfs
```

### Linux (CentOS/RHEL/Fedora)

```bash
# Adicionar o repositório do GitHub
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | sudo bash

# Instalar Git LFS (CentOS/RHEL)
sudo yum install git-lfs

# Ou (Fedora)
sudo dnf install git-lfs
```

---

## 🚀 Clonar o Repositório

### Passo 1: Instalar Git LFS Globalmente

Após instalar o Git LFS, você precisa inicializá-lo uma vez no seu sistema:

```bash
git lfs install
```

**Nota:** Este comando só precisa ser executado uma vez por usuário do sistema. Ele configura hooks do Git LFS globalmente.

### Passo 2: Clonar o Repositório

```bash
# Clonar o repositório completo
git clone https://github.com/matheusmendes720/gran-prix.git

# Navegar para o diretório
cd gran-prix
```

### Passo 3: Verificar se os Arquivos LFS Foram Baixados

Após clonar, verifique se os arquivos grandes foram baixados corretamente:

```bash
# Verificar arquivos rastreados pelo LFS
git lfs ls-files

# Verificar status dos arquivos LFS
git lfs fetch --all
git lfs checkout
```

Você deve ver uma lista de arquivos CSV. Se aparecer apenas ponteiros (pointers), execute:

```bash
git lfs pull
```

---

## 💻 Trabalhar com o Repositório

### Atualizar o Repositório (Pull)

Quando você ou outros membros da equipe fizerem push de alterações:

```bash
# Atualizar o repositório (baixa alterações normais e LFS)
git pull origin master

# Se os arquivos LFS não foram baixados automaticamente:
git lfs pull
```

### Fazer Alterações e Commits

O Git LFS funciona automaticamente. Você só precisa fazer commits normalmente:

```bash
# Adicionar arquivos (incluindo CSVs grandes)
git add .

# Fazer commit
git commit -m "feat: adicionar novo dataset"

# Fazer push
git push origin master
```

**Importante:** O Git LFS automaticamente detecta arquivos CSV e os trata como arquivos LFS baseado no `.gitattributes`.

### Adicionar Novos Arquivos CSV Grandes

Se você adicionar novos arquivos CSV grandes, eles serão automaticamente rastreados pelo LFS:

```bash
# Adicionar arquivo CSV (será automaticamente tratado como LFS)
git add data/novo_dataset.csv

# Verificar se está sendo rastreado pelo LFS
git lfs ls-files

# Fazer commit normalmente
git commit -m "feat: adicionar novo dataset CSV"
git push origin master
```

---

## 🔍 Verificar Status e Informações

### Verificar Arquivos Rastreados pelo LFS

```bash
# Listar todos os arquivos LFS no repositório
git lfs ls-files

# Ver informações detalhadas
git lfs ls-files --long

# Ver apenas arquivos em um diretório específico
git lfs ls-files data/processed/
```

### Verificar Status do LFS

```bash
# Ver informações de uso do LFS
git lfs env

# Ver informações de armazenamento
git lfs version
```

### Verificar Qual Arquivo é LFS ou Normal

```bash
# Verificar se um arquivo específico é LFS
git lfs ls-files | grep "nome_do_arquivo.csv"

# Ver o conteúdo do ponteiro LFS (não faça isso para arquivos grandes!)
cat .git/lfs/objects/[hash]/[hash]  # Caminho do objeto LFS
```

---

## 🛠️ Solução de Problemas

### Problema 1: Arquivos CSV Aparecem como Ponteiros (Pointers)

**Sintoma:** Arquivos CSV têm apenas algumas linhas e começam com `version https://git-lfs.github.com/spec/v1`

**Solução:**

```bash
# Forçar download de todos os arquivos LFS
git lfs fetch --all
git lfs checkout

# Ou fazer pull completo
git lfs pull
```

### Problema 2: Erro "git: 'lfs' is not a git command"

**Sintoma:** Git não reconhece o comando `git lfs`

**Solução:**

1. Verifique se o Git LFS está instalado:
   ```bash
   git lfs version
   ```

2. Se não estiver instalado, instale seguindo a seção [Instalação do Git LFS](#instalação-do-git-lfs)

3. Reinicie o terminal/PowerShell após instalar

### Problema 3: Erro ao Fazer Push - "File is too large"

**Sintoma:** GitHub rejeita arquivos grandes mesmo após configurar LFS

**Solução:**

1. Verifique se o `.gitattributes` está correto:
   ```bash
   cat .gitattributes
   ```
   Deve conter: `*.csv filter=lfs diff=lfs merge=lfs -text`

2. Migre o arquivo para LFS manualmente:
   ```bash
   git lfs track "arquivo.csv"
   git add .gitattributes arquivo.csv
   git commit -m "chore: migrar arquivo.csv para LFS"
   ```

3. Se o arquivo já foi commitado sem LFS, você precisará reescrever o histórico (consulte a seção avançada)

### Problema 4: Clone Demora Muito

**Sintoma:** O clone do repositório demora muito tempo

**Solução:**

Isso é normal! O repositório tem muitos arquivos grandes. O Git LFS baixa os arquivos em segundo plano. Você pode:

1. Clonar apenas o histórico Git primeiro (sem arquivos LFS):
   ```bash
   GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/matheusmendes720/gran-prix.git
   cd gran-prix
   git lfs pull
   ```

2. Ou apenas esperar - o download dos arquivos LFS acontece automaticamente

### Problema 5: Erro "LFS object not found"

**Sintoma:** Arquivo LFS não encontrado ao fazer checkout

**Solução:**

```bash
# Limpar cache do LFS
git lfs prune

# Forçar fetch de todos os objetos
git lfs fetch --all

# Fazer checkout novamente
git lfs checkout
```

---

## 📝 Comandos Úteis

### Comandos Básicos do Git LFS

```bash
# Instalar Git LFS (uma vez por sistema)
git lfs install

# Rastrear um tipo de arquivo específico
git lfs track "*.csv"

# Ver arquivos rastreados
git lfs ls-files

# Baixar todos os arquivos LFS
git lfs pull

# Fazer fetch de todos os objetos LFS
git lfs fetch --all

# Fazer checkout dos arquivos LFS
git lfs checkout

# Ver informações de ambiente
git lfs env

# Limpar objetos LFS não referenciados
git lfs prune

# Verificar integridade dos arquivos LFS
git lfs fsck
```

### Comandos de Workflow Comum

```bash
# Workflow completo: Atualizar repositório
git pull origin master
git lfs pull

# Workflow completo: Adicionar e commitar arquivos
git add .
git commit -m "mensagem"
git push origin master

# Verificar antes de fazer push
git status
git lfs ls-files

# Ver histórico de um arquivo LFS
git log --all -- "caminho/arquivo.csv"
```

---

## ❓ FAQ (Perguntas Frequentes)

### P: Preciso instalar Git LFS toda vez que clonar o repositório?

**R:** Não. O Git LFS precisa ser instalado apenas uma vez no seu sistema. Depois disso, execute `git lfs install` uma vez para configurar os hooks globalmente.

### P: Posso trabalhar sem baixar todos os arquivos LFS?

**R:** Sim! Você pode clonar o repositório sem baixar os arquivos LFS usando `GIT_LFS_SKIP_SMUDGE=1`. Os arquivos aparecerão como ponteiros pequenos. Você pode baixá-los depois com `git lfs pull`.

### P: O que acontece se eu modificar um arquivo CSV grande?

**R:** O Git LFS funciona automaticamente. Quando você modificar e commitar um arquivo CSV, o Git LFS automaticamente detecta a mudança e armazena a nova versão no LFS.

### P: Posso usar o repositório sem Git LFS instalado?

**R:** Tecnicamente sim, mas você não conseguirá baixar os arquivos grandes. Eles aparecerão apenas como ponteiros (arquivos pequenos com metadados). Para trabalhar adequadamente, instale o Git LFS.

### P: O Git LFS afeta o tamanho do repositório local?

**R:** Sim. Os arquivos LFS são baixados e armazenados localmente, então o repositório pode ocupar bastante espaço em disco. Use `git lfs prune` para limpar objetos antigos não referenciados.

### P: Como faço para remover um arquivo do LFS?

**R:** Para parar de rastrear um tipo de arquivo no LFS:
```bash
git lfs untrack "*.csv"
git add .gitattributes
git commit -m "chore: parar de rastrear CSVs no LFS"
```

### P: Posso ver o histórico de um arquivo LFS?

**R:** Sim! O Git mantém o histórico normalmente:
```bash
git log --all -- "caminho/arquivo.csv"
git show HEAD:caminho/arquivo.csv
```

### P: O Git LFS é gratuito no GitHub?

**R:** Sim, o GitHub oferece 1 GB de armazenamento LFS gratuito e 1 GB de largura de banda por mês. Para projetos maiores, há planos pagos.

---

## 🎓 Recursos Adicionais

### Documentação Oficial

- **Git LFS:** https://git-lfs.github.com/
- **Git LFS GitHub:** https://github.com/git-lfs/git-lfs
- **Documentação Git LFS:** https://github.com/git-lfs/git-lfs/tree/main/docs

### Tutoriais e Guias

- **Getting Started with Git LFS:** https://git-lfs.github.com/
- **Git LFS Tutorial:** https://www.atlassian.com/git/tutorials/git-lfs

### Suporte

Se você encontrar problemas que não foram resolvidos neste guia:

1. Verifique a seção [Solução de Problemas](#solução-de-problemas)
2. Consulte a documentação oficial do Git LFS
3. Abra uma issue no repositório do projeto
4. Contate o time de desenvolvimento

---

## ✅ Checklist de Verificação

Antes de começar a trabalhar, certifique-se de:

- [ ] Git instalado (versão 2.13.0+)
- [ ] Git LFS instalado (versão 2.0.0+)
- [ ] `git lfs install` executado
- [ ] Repositório clonado com sucesso
- [ ] Arquivos LFS baixados (`git lfs ls-files` mostra arquivos)
- [ ] Python 3.9+ instalado
- [ ] Node.js 18+ instalado
- [ ] Dependências instaladas (`pip install -r backend/requirements.txt` e `npm install` no frontend)

---

## 📞 Contato e Suporte

**Repositório:** https://github.com/matheusmendes720/gran-prix  
**Issues:** https://github.com/matheusmendes720/gran-prix/issues

---

**Última Atualização:** Novembro 2025  
**Versão do Guia:** 1.0.0  
**Mantido por:** Time de Desenvolvimento Nova Corrente

---

## 🎉 Pronto para Começar!

Agora você está pronto para clonar e trabalhar com o repositório completo! Se tiver dúvidas, consulte este guia ou entre em contato com o time.

**Boa codificação! 🚀**
