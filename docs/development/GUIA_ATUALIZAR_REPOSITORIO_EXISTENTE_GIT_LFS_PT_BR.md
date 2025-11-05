# 🔄 Guia: Atualizar Repositório Existente para Git LFS

**Projeto:** Nova Corrente - Demand Forecasting & Analytics System  
**Para:** Membros da equipe que já têm o repositório clonado  
**Data:** Novembro 2025  
**Versão:** 1.0.0

---

## 🎯 Visão Geral

Este guia é para membros da equipe que **já têm o repositório `gran-prix` clonado** e precisam atualizar para trabalhar com **Git LFS** (Large File Storage).

O repositório agora utiliza Git LFS para gerenciar arquivos CSV grandes. Você precisa seguir estes passos para atualizar seu repositório local.

---

## ⚠️ Importante

- ✅ Este guia é **apenas para quem já tem o repositório clonado**
- ✅ Se você ainda não clonou, use o [Guia Completo de Clonagem](GUIA_COMPLETO_CLONAR_REPOSITORIO_GIT_LFS_PT_BR.md)
- ✅ Faça backup das suas alterações locais antes de começar
- ✅ Certifique-se de ter commitado ou feito stash de todas as mudanças

---

## 📋 Pré-requisitos

Antes de começar, verifique se você tem:

- ✅ Git instalado (versão 2.13.0 ou superior)
- ✅ Acesso ao repositório remoto
- ✅ Todas as suas alterações locais commitadas ou em stash

### Verificar Versões

```bash
# Verificar versão do Git
git --version

# Verificar se já tem Git LFS instalado
git lfs version
```

---

## 🚀 Passo a Passo para Atualizar

### Passo 1: Fazer Backup das Alterações Locais

**⚠️ IMPORTANTE:** Antes de atualizar, salve suas alterações:

```bash
# Navegar para o diretório do projeto
cd gran-prix

# Verificar status atual
git status

# Se houver alterações não commitadas, fazer commit ou stash
# Opção 1: Fazer commit das alterações
git add .
git commit -m "chore: backup antes de atualizar para Git LFS"

# OU Opção 2: Fazer stash (guardar temporariamente)
git stash save "backup antes de atualizar para Git LFS"
```

### Passo 2: Instalar Git LFS

Se você ainda não tem Git LFS instalado:

#### Windows

```powershell
# Opção 1: Chocolatey
choco install git-lfs

# Opção 2: Download direto
# Baixe de: https://git-lfs.github.com/
```

#### macOS

```bash
brew install git-lfs
```

#### Linux (Ubuntu/Debian)

```bash
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
```

### Passo 3: Inicializar Git LFS

```bash
# Inicializar Git LFS (apenas uma vez por sistema)
git lfs install
```

### Passo 4: Buscar Todas as Alterações do Remoto

```bash
# Buscar todas as branches e atualizações do remoto
git fetch origin

# Verificar quais branches foram atualizadas
git branch -r
```

### Passo 5: Atualizar a Branch Master

```bash
# Certificar-se de estar na branch master
git checkout master

# Fazer pull das atualizações (isso vai baixar o histórico atualizado)
git pull origin master
```

### Passo 6: Baixar Arquivos LFS

Após atualizar o repositório, você precisa baixar os arquivos grandes do LFS:

```bash
# Baixar todos os arquivos LFS
git lfs pull

# OU fazer fetch e checkout separadamente
git lfs fetch --all
git lfs checkout
```

### Passo 7: Verificar se Funcionou

```bash
# Verificar se os arquivos LFS foram baixados
git lfs ls-files

# Deve mostrar uma lista de arquivos CSV
# Se estiver vazio ou mostrar apenas alguns arquivos, execute novamente:
git lfs pull
```

### Passo 8: Restaurar Suas Alterações (se usou stash)

Se você usou `git stash` no Passo 1:

```bash
# Ver lista de stashes
git stash list

# Restaurar o último stash
git stash pop

# OU restaurar um stash específico
git stash apply stash@{0}
```

---

## 🔧 Solução de Problemas

### Problema 1: Erro "Your branch and 'origin/master' have diverged"

**Sintoma:** Git avisa que sua branch local divergiu da remota

**Solução:**

```bash
# Ver quantos commits você tem localmente que não estão no remoto
git log origin/master..master

# Se você não tem commits importantes locais, pode fazer reset:
git fetch origin
git reset --hard origin/master

# OU se tem commits importantes, faça merge:
git pull origin master --no-rebase
```

### Problema 2: Arquivos CSV ainda aparecem como pequenos (ponteiros)

**Sintoma:** Os arquivos CSV têm apenas algumas linhas de texto

**Solução:**

```bash
# Forçar download de todos os arquivos LFS
git lfs fetch --all
git lfs checkout

# Verificar novamente
git lfs ls-files
```

### Problema 3: Erro "git: 'lfs' is not a git command"

**Sintoma:** Comando `git lfs` não funciona

**Solução:**

1. Instale o Git LFS seguindo o **Passo 2** acima
2. Reinicie o terminal/PowerShell
3. Execute `git lfs install` novamente

### Problema 4: Conflitos ao Fazer Pull

**Sintoma:** Git mostra conflitos ao tentar fazer pull

**Solução:**

```bash
# Ver quais arquivos estão em conflito
git status

# Resolver conflitos manualmente ou usar uma estratégia:
# Opção 1: Aceitar versão do remoto
git checkout --theirs arquivo_com_conflito.csv

# Opção 2: Aceitar versão local
git checkout --ours arquivo_com_conflito.csv

# Depois de resolver conflitos:
git add arquivo_com_conflito.csv
git commit -m "merge: resolver conflitos"
```

### Problema 5: Não Consigo Fazer Pull - "Permission denied"

**Sintoma:** Erro de permissão ao acessar o repositório

**Solução:**

1. Verifique suas credenciais do GitHub:
   ```bash
   git config --global user.name "Seu Nome"
   git config --global user.email "seu.email@example.com"
   ```

2. Se usar HTTPS, você pode precisar atualizar seu token de acesso pessoal do GitHub

3. Ou configure SSH:
   ```bash
   # Verificar se tem chave SSH
   ls -al ~/.ssh
   
   # Se não tiver, gerar uma nova
   ssh-keygen -t ed25519 -C "seu.email@example.com"
   ```

---

## 📝 Comandos Resumidos (Copy & Paste)

Para facilitar, aqui está uma sequência completa de comandos que você pode executar:

```bash
# 1. Ir para o diretório do projeto
cd gran-prix

# 2. Salvar alterações locais (escolha uma opção)
git add . && git commit -m "backup antes de atualizar"
# OU
git stash save "backup antes de atualizar"

# 3. Instalar Git LFS (se necessário - veja instruções acima)
# Windows: choco install git-lfs
# macOS: brew install git-lfs
# Linux: sudo apt-get install git-lfs

# 4. Inicializar Git LFS
git lfs install

# 5. Buscar atualizações
git fetch origin

# 6. Atualizar branch master
git checkout master
git pull origin master

# 7. Baixar arquivos LFS
git lfs pull

# 8. Verificar se funcionou
git lfs ls-files

# 9. Restaurar alterações (se usou stash)
git stash pop
```

---

## ✅ Checklist de Verificação

Após seguir os passos, verifique:

- [ ] Git LFS instalado (`git lfs version` funciona)
- [ ] `git lfs install` executado
- [ ] Repositório atualizado (`git pull` concluído)
- [ ] Arquivos LFS baixados (`git lfs ls-files` mostra arquivos)
- [ ] Alterações locais restauradas (se aplicável)
- [ ] Projeto funciona normalmente

---

## 🎯 Próximos Passos

Após atualizar com sucesso:

1. **Testar o projeto:** Certifique-se de que tudo funciona
2. **Trabalhar normalmente:** Agora você pode trabalhar normalmente - o Git LFS funciona automaticamente
3. **Fazer push de alterações:** Quando fizer push de arquivos CSV, eles serão automaticamente tratados pelo LFS

### Trabalhar com o Repositório (Após Atualização)

```bash
# Atualizar repositório (incluindo arquivos LFS)
git pull origin master
git lfs pull

# Adicionar e commitar arquivos (LFS funciona automaticamente)
git add .
git commit -m "feat: nova funcionalidade"
git push origin master
```

---

## 📚 Recursos Adicionais

- **[Guia Completo de Clonagem](GUIA_COMPLETO_CLONAR_REPOSITORIO_GIT_LFS_PT_BR.md)** - Para novos membros da equipe
- **[Início Rápido](../README_INICIO_RAPIDO_PT_BR.md)** - Setup rápido em 3 passos

---

## 🆘 Precisa de Ajuda?

Se você encontrar problemas:

1. ✅ Revise a seção [Solução de Problemas](#solução-de-problemas)
2. ✅ Consulte o [Guia Completo](GUIA_COMPLETO_CLONAR_REPOSITORIO_GIT_LFS_PT_BR.md)
3. ✅ Entre em contato com o time de desenvolvimento
4. ✅ Abra uma issue no repositório

---

**Última Atualização:** Novembro 2025  
**Versão do Guia:** 1.0.0  
**Mantido por:** Time de Desenvolvimento Nova Corrente

---

## 🎉 Pronto!

Agora seu repositório está atualizado e pronto para trabalhar com Git LFS! 🚀
