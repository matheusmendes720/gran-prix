# 🚀 Início Rápido - Gran Prix Repository

## ⚡ Setup Rápido (3 Passos)

### 1️⃣ Instalar Git LFS

```bash
# Windows (Chocolatey)
choco install git-lfs

# macOS
brew install git-lfs

# Linux
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
```

**Depois, inicializar:**
```bash
git lfs install
```

### 2️⃣ Clonar o Repositório

```bash
git clone https://github.com/matheusmendes720/gran-prix.git
cd gran-prix
```

### 3️⃣ Baixar Arquivos Grandes (LFS)

```bash
git lfs pull
```

## 📖 Guia Completo

Para instruções detalhadas, consulte:
**[Guia Completo PT-BR](docs/development/GUIA_COMPLETO_CLONAR_REPOSITORIO_GIT_LFS_PT_BR.md)**

## ✅ Verificar se Funcionou

```bash
# Verificar arquivos LFS
git lfs ls-files

# Ver status do repositório
git status
```

## ❗ Problemas?

Se os arquivos CSV aparecerem como ponteiros (pequenos), execute:

```bash
git lfs fetch --all
git lfs checkout
```

---

**Repositório:** https://github.com/matheusmendes720/gran-prix  
**Guia Completo:** [docs/development/GUIA_COMPLETO_CLONAR_REPOSITORIO_GIT_LFS_PT_BR.md](docs/development/GUIA_COMPLETO_CLONAR_REPOSITORIO_GIT_LFS_PT_BR.md)
