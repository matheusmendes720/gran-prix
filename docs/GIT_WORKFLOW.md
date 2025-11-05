# Git Workflow para o Projeto Nova Corrente

## Visão Geral

Este documento define o workflow de Git para o projeto Nova Corrente - uma plataforma de previsão de demanda e análise para a empresa de telecomunicações Nova Corrente. Este workflow visa garantir colaboração eficiente, rastreabilidade e qualidade do código.

## Estratégia de Branching: Git Flow Adaptado

O projeto utiliza uma variação do Git Flow, adaptado para as necessidades específicas da equipe:

```
main (produção estável)
├── develop (desenvolvimento ativo)
    ├── feature/nome-da-funcionalidade
    ├── bugfix/nome-do-bug
    └── release/v1.2.0
```

## Branches Principais

### `main`

- Representa o estado de produção
- Sempre estável
- Somente commits de releases
- Cada commit é uma release oficial

### `develop`

- Reflete o estado de desenvolvimento mais recente
- Integração de todas as features desenvolvidas
- Código testável mas não necessariamente estável

## Branches de Apoio

### `feature/*`

- Desenvolvimento de novas funcionalidades
- Originam-se de: `develop`
- Mergem-se em: `develop`
- Convenção de nomenclatura: `feature/descreva-sua-funcionalidade`

### `bugfix/*`

- Correções de bugs
- Originam-se de: `develop`
- Mergem-se em: `develop`
- Convenção de nomenclatura: `bugfix/descreva-o-bug`

### `release/*`

- Preparação de releases
- Originam-se de: `develop`
- Mergem-se em: `main` e `develop`
- Convenção de nomenclatura: `release/v1.2.0`

## Workflow de Desenvolvimento

### 1. Começando uma Nova Funcionalidade

```bash
# Atualize sua branch develop
git checkout develop
git pull origin develop

# Crie uma nova branch de feature
git checkout -b feature/nova-funcionalidade
```

### 2. Trabalhando na Funcionalidade

- Faça commits frequentes e atômicos
- Siga as convenções de commit
- Atualize regularmente com o develop: `git rebase develop`

### 3. Finalizando uma Funcionalidade

```bash
# Atualize sua branch
git checkout develop
git pull origin develop
git checkout feature/nova-funcionalidade
git rebase develop

# Teste sua funcionalidade
# Execute testes e linting

# Mergue para develop
git checkout develop
git merge feature/nova-funcionalidade --no-ff
git push origin develop

# Remova a branch
git branch -d feature/nova-funcionalidade
git push origin --delete feature/nova-funcionalidade
```

### 4. Criando uma Release

```bash
# Crie branch de release a partir de develop
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# Atualize números de versão, changelog, etc.
# Faça commits finais de ajustes

# Mergue para main
git checkout main
git pull origin main
git merge release/v1.2.0 --no-ff

# Crie tag de release
git tag -a v1.2.0 -m "Release v1.2.0"

# Mergue de volta para develop
git checkout develop
git merge release/v1.2.0 --no-ff

# Faça push das alterações e tag
git push origin main
git push origin develop
git push origin v1.2.0

# Remova branch de release
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

## Convenções de Commits

### Formato de Mensagem de Commit

```
<Tipo>(Escopo): Descrição curta

Corpo opcional com mais detalhes
- Pode usar listas
- Separado do cabeçalho por linha vazia

Rodapé opcional
Fixes #123
BREAKING CHANGE: descrição da quebra
```

### Tipos Válidos

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Atualizações de documentação
- `style`: Mudanças de estilo sem alterar lógica (formatting, missing semicolons, etc)
- `refactor`: Refatoração sem alterar funcionalidade/comportamento
- `perf`: Melhoria de performance
- `test`: Adição ou modificação de testes
- `chore`: Tarefas de manutenção, build, etc

### Escopo (Opcional)

- `frontend`: Alterações no frontend
- `backend`: Alterações no backend
- `api`: Alterações nas APIs
- `models`: Alterações nos modelos ML
- `data`: Alterações na pipeline de dados
- `docs`: Alterações na documentação

### Exemplos de Commits

```
feat(frontend): adicionar componente de dashboard geográfico
```

```
fix(backend): resolver erro de conexão com banco de dados
```

```
refactor(models): otimizar pipeline de treinamento LSTM

- Reduz tempo de treinamento em 30%
- Melhora estabilidade do modelo
- Adiciona logging detalhado
```

## Padrões de Codificação

### Commits Atômicos

- Faça commits pequenos e com propósitos bem definidos
- Cada commit deve representar uma alteração lógica completa
- Evite commits com múltiplas intenções

### Mensagens Claras

- Use imperativo no presente: "Add" não "Added" ou "Adds"
- Primeira linha deve ter no máximo 72 caracteres
- Se necessário, adicione corpo com mais detalhes

## Integração Contínua

### Hooks de Pre-commit

O projeto utiliza hooks de pre-commit para garantir qualidade de código:

```bash
# Instale os hooks
pip install pre-commit
pre-commit install

# Ou execute manualmente
pre-commit run --all-files
```

### Critérios para Merge

- Todos os testes devem passar
- Cobertura de testes não pode diminuir significativamente
- Pelo menos uma revisão aprovada
- Compatibilidade com o código existente

## Procedimentos de Emergência

### Hotfixes

Para correções urgentes em produção:

```bash
# Partindo de main
git checkout main
git pull origin main
git checkout -b hotfix/nome-do-hotfix

# Faça as correções e commit
# Teste imediatamente

# Mergue para main e develop
git checkout main
git merge hotfix/nome-do-hotfix --no-ff
git tag -a v1.0.1 -m "Hotfix v1.0.1"
git checkout develop
git merge hotfix/nome-do-hotfix --no-ff

# Faça push
git push origin main
git push origin develop
git push origin v1.0.1
```

## Ferramentas de Apoio

### Scripts de Workflow

O script `scripts/git-workflow.bat` fornece comandos auxiliares:

- `git-workflow.bat setup` - Configura branches iniciais
- `git-workflow.bat feature` - Cria branch de feature
- `git-workflow.bat bugfix` - Cria branch de bugfix
- `git-workflow.bat release` - Cria branch de release
- `git-workflow.bat merge-feature` - Merges feature para develop
- `git-workflow.bat merge-release` - Merges release para main

## Melhores Práticas

1. **Atualize Regularmente**

   - Mantenha sua branch develop atualizada
   - Rebase sua feature com develop regularmente
2. **Commits Significativos**

   - Evite commits "WIP" ou "Fix" genéricos
   - Cada commit deve ter uma razão clara
3. **Teste antes de Push**

   - Execute testes locais antes de fazer push
   - Verifique se o código está funcionando localmente
4. **Revisão de Código**

   - Sempre solicite revisão antes de fazer merge
   - Revise código de colegas ativamente
5. **Documentação**

   - Atualize documentação quando necessário
   - Comente código complexo adequadamente

## Padrões de Pull Request

### Título

- Siga o mesmo padrão de commits
- Seja claro e descritivo

### Descrição

- Descreva o problema resolvido
- Explique a solução implementada
- Liste impactos e mudanças relevantes
- Inclua capturas de tela se aplicável

### Labels

- Atribua labels apropriadas:
  - `feature`, `bug`, `enhancement`, `documentation`, etc.
  - `frontend`, `backend`, `ml-models`, etc.

## Recursos Adicionais

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)

# Git Workflow Completo para o Projeto Nova Corrente

## Sum├írio

1. [Introdu├º├úo e Vis├úo Geral](#introdu├º├úo-e-vis├úo-geral)
2. [Configura├º├úo Inicial do Ambiente](#configura├º├úo-inicial-do-ambiente)
3. [Estrat├®gia de Branching](#estrat├®gia-de-branching)
4. [Workflow de Desenvolvimento Completo](#workflow-de-desenvolvimento-completo)
5. [Conven├º├Áes de Commits](#conven├º├Áes-de-commits)
6. [Pull Requests e Code Review](#pull-requests-e-code-review)
7. [Procedimentos Avan├ºados](#procedimentos-avan├ºados)
8. [Solu├º├úo de Problemas e D├║vidas Comuns](#solu├º├úo-de-problemas-e-d├║vidas-comuns)
9. [Melhores Pr├íticas](#melhores-pr├íticas)
10. [Ferramentas de Apoio](#ferramentas-de-apoio)
11. [Integra├º├úo Cont├¡nua](#integra├º├úo-cont├¡nua)
12. [Recursos Adicionais](#recursos-adicionais)

## Introdu├º├úo e Vis├úo Geral

Este documento define o workflow de Git para o projeto Nova Corrente - uma plataforma de previs├úo de demanda e an├ílise para a empresa de telecomunica├º├Áes Nova Corrente. Este workflow visa garantir colabora├º├úo eficiente, rastreabilidade e qualidade do c├│digo em um ambiente de equipe colaborativa.

### O Que ├® Git?

Git ├® uma ferramenta de controle de vers├úo distribu├¡do que permite rastrear altera├º├Áes em arquivos e coordenar o trabalho entre m├║ltiplos desenvolvedores em projetos de desenvolvimento de software. Pense no Git como um sistema que registra instant├óneos do seu c├│digo ao longo do tempo, permitindo que voc├¬ volte a vers├Áes anteriores, compare altera├º├Áes e trabalhe em paralelo com outros desenvolvedores sem conflitos.

### Por Que Usar um Workflow Padronizado?

- **Consist├¬ncia**: Todos os membros da equipe seguem o mesmo padr├úo
- **Colabora├º├úo**: Facilita o trabalho em equipe e a integra├º├úo de c├│digo
- **Rastreabilidade**: Permite entender o hist├│rico de altera├º├Áes e decis├Áes
- **Qualidade**: Processo de revis├úo garante c├│digo de qualidade
- **Produtividade**: Fluxo de trabalho bem definido melhora a efici├¬ncia

## Configura├º├úo Inicial do Ambiente

### 1. Instala├º├úo do Git

Antes de come├ºar, certifique-se de ter o Git instalado em seu sistema:

```bash

# Verifique se o Git est├í instalado

git --version



# Se n├úo estiver instalado no Windows, baixe de: [https://git-scm.com/](https://git-scm.com/)

# Se n├úo estiver instalado no macOS, use: brew install git

# Se n├úo estiver instalado no Linux, use: sudo apt-get install git (Ubuntu/Debian) ou sudo yum install git (CentOS/RHEL)

```

### 2. Configura├º├úo B├ísica do Git

Configure seu nome e email globalmente (fa├ºa isso apenas uma vez):

```bash

git config --global user.name "Seu Nome Completo"

git config --global user.email "seu.email@empresa.com"

```

### 3. Configura├º├úo de Editor de Texto (Opcional)

Configure o editor de texto padr├úo para mensagens de commit:

```bash

# Para usar VS Code

git config --global core.editor "code --wait"



# Para usar Notepad++ no Windows

git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"

```

### 4. Configura├º├úo de CRLF (Carriage Return Line Feed)

No Windows, configure o Git para lidar corretamente com quebras de linha:

```bash

# Para converter CRLF para LF ao fazer commit, e LF para CRLF ao fazer checkout

git config --global core.autocrlf true



# Para n├úo converter (├║til para desenvolvedores que trabalham com m├║ltiplas plataformas)

git config --global core.autocrlf false

```

### 5. Clone do Reposit├│rio

Clone o reposit├│rio do projeto Nova Corrente:

```bash

git clone [https://github.com/nome-da-empresa/gran-prix.git](https://github.com/nome-da-empresa/gran-prix.git)

cd gran-prix

```

### 6. Instala├º├úo de Hooks de Pre-commit

Instale os hooks de pre-commit para garantir qualidade de c├│digo:

```bash

# Navegue at├® o diret├│rio do projeto

cd gran-prix



# Instale o pre-commit se ainda n├úo estiver instalado

pip install pre-commit



# Instale os hooks no reposit├│rio local

pre-commit install

```

## Estrat├®gia de Branching

### Git Flow Adaptado para o Projeto

O projeto utiliza uma varia├º├úo do Git Flow, adaptado para as necessidades espec├¡ficas da equipe:

```

main (produ├º├úo est├ível) - c├│digo em produ├º├úo

Ôö£ÔöÇÔöÇ develop (desenvolvimento ativo) - integra├º├úo de funcionalidades

    Ôö£ÔöÇÔöÇ feature/nome-da-funcionalidade - desenvolvimento de novas funcionalidades

    Ôö£ÔöÇÔöÇ bugfix/nome-do-bug - corre├º├Áes de bugs

    ÔööÔöÇÔöÇ release/v1.2.0 - prepara├º├úo de releases

```

### Branches Principais

#### `main`

- **Finalidade**: Representa o estado de produ├º├úo
- **Caracter├¡sticas**:

  - Sempre est├ível
  - Somente commits de releases
  - Cada commit ├® uma release oficial
  - **Protegida no GitHub**: Requer pull request e aprova├º├úo
  - Requer pelo menos uma revis├úo aprovada
  - Requer que todos os checks de integra├º├úo cont├¡nua passem

#### `develop`

- **Finalidade**: Reflete o estado de desenvolvimento mais recente
- **Caracter├¡sticas**:

  - Integra├º├úo de todas as features desenvolvidas
  - C├│digo test├ível mas n├úo necessariamente est├ível
  - **Protegida no GitHub**: Requer pull request e aprova├º├úo
  - Requer pelo menos uma revis├úo aprovada

### Branches de Apoio

#### `feature/*`

- **Finalidade**: Desenvolvimento de novas funcionalidades
- **Origem**: `develop`
- **Destino**: `develop`
- **Conven├º├úo de nomenclatura**: `feature/descreva-sua-funcionalidade`
- **Exemplos**:

  - `feature/adicionar-dashboard-geografico`
  - `feature/integrar-ia-prescritiva`
  - `feature/melhorar-calculo-estoque`

#### `bugfix/*`

- **Finalidade**: Corre├º├Áes de bugs
- **Origem**: `develop`
- **Destino**: `develop`
- **Conven├º├úo de nomenclatura**: `bugfix/descreva-o-bug`
- **Exemplos**:

  - `bugfix/corrigir-erro-previsao`
  - `bugfix/ajustar-calculo-reorder-point`
  - `bugfix/resolver-conexao-banco`

#### `release/*`

- **Finalidade**: Prepara├º├úo de releases
- **Origem**: `develop`
- **Destino**: `main` e `develop`
- **Conven├º├úo de nomenclatura**: `release/v1.2.0`
- **Exemplos**:

  - `release/v1.0.0`
  - `release/v2.1.1`
  - `release/v1.5.3`

#### `hotfix/*` (Emerg├¬ncia)

- **Finalidade**: Corre├º├Áes urgentes em produ├º├úo
- **Origem**: `main`
- **Destino**: `main` e `develop`
- **Conven├º├úo de nomenclatura**: `hotfix/versao-correcao`
- **Exemplos**:

  - `hotfix/v1.0.1-corrigir-bug-critico`
  - `hotfix/v2.1.2-resolver-problema-em-producao`

## Workflow de Desenvolvimento Completo

### 1. Prepara├º├úo para Trabalho

#### Atualiza├º├úo do Ambiente

Antes de come├ºar a trabalhar em uma nova tarefa:

```bash

# V├í para a branch develop e atualize com as ├║ltimas altera├º├Áes

git checkout develop

git pull origin develop



# Verifique o status do reposit├│rio

git status

```

### 2. Come├ºando uma Nova Funcionalidade

#### Passo 1: Atualize sua branch develop

```bash

# Atualize sua branch develop

git checkout develop

git pull origin develop

```

#### Passo 2: Crie uma nova branch de feature

```bash

# Crie uma nova branch de feature a partir de develop

git checkout -b feature/nome-da-funcionalidade

```

**Exemplo real**:

```bash

git checkout -b feature/adicionar-grafico-previsao-demanda

```

### 3. Trabalhando na Funcionalidade

#### Durante o Desenvolvimento

- Fa├ºa commits frequentes e at├┤micos (cada commit deve representar uma altera├º├úo l├│gica completa)
- Siga as conven├º├Áes de commit (ver se├º├úo espec├¡fica abaixo)
- Execute testes locais regularmente
- Atualize regularmente com o develop: `git rebase develop`

#### Exemplo de Workflow de Desenvolvimento

```bash

# Trabalhe na sua funcionalidade

# (fazer altera├º├Áes no c├│digo)



# Adicione os arquivos modificados

git add .



# Fa├ºa um commit com mensagem descritiva

git commit -m "feat(frontend): adicionar componente de gr├ífico de previs├úo"



# Continue trabalhando

# (fazer mais altera├º├Áes)



# Adicione mais altera├º├Áes (opcionalmente selecione arquivos espec├¡ficos)

git add src/components/ForecastChart.tsx



# Fa├ºa outro commit

git commit -m "docs: atualizar documenta├º├úo do componente ForecastChart"

```

### 4. Atualizando com as ├Ültimas Altera├º├Áes

#### Periodicamente, mantenha sua branch atualizada com develop:

```bash

# Atualize sua branch develop

git checkout develop

git pull origin develop



# Volte para sua branch de feature

git checkout feature/nome-da-funcionalidade



# Atualize sua feature com as ├║ltimas altera├º├Áes

git rebase develop

```

### 5. Finalizando a Funcionalidade

#### Passo 1: Teste localmente

```bash

# Execute testes

npm test  # ou python -m pytest, dependendo do projeto



# Execute linting

npm run lint  # ou o comando apropriado



# Execute formata├º├úo (se necess├írio)

npm run format  # ou black ., dependendo do projeto

```

#### Passo 2: Atualize novamente com develop

```bash

# Atualize sua branch develop

git checkout develop

git pull origin develop



# Volte para sua feature

git checkout feature/nome-da-funcionalidade



# Rebase com develop

git rebase develop



# Verifique se h├í conflitos e resolva se necess├írio

```

#### Passo 3: Envie sua branch para o GitHub

```bash

# Envie sua branch para o GitHub

git push -u origin feature/nome-da-funcionalidade

```

### 6. Criando um Pull Request

#### No GitHub:

1. Acesse o reposit├│rio no GitHub
2. Clique na aba "Pull requests"
3. Clique em "New pull request"
4. Selecione:

   - `base: develop`
   - `compare: feature/nome-da-funcionalidade`
5. Preencha o template do PR (ver se├º├úo de Pull Requests)
6. Clique em "Create pull request"

### 7. Processo de Code Review

#### Atribui├º├úo de Revisores

- Atribua revisores apropriados ao seu PR
- Normalmente, inclua pelo menos um mantenedor do projeto
- Pode incluir pessoas espec├¡ficas do dom├¡nio da funcionalidade

#### Respondendo a Feedbacks

Quando receber feedback:

1. Leia o feedback cuidadosamente
2. Agrade├ºa pelo feedback
3. Fa├ºa as altera├º├Áes solicitadas
4. Comunique suas altera├º├Áes
5. Responda aos coment├írios
6. Atualize sua branch no GitHub

```bash

# Ap├│s fazer altera├º├Áes

git add .

git commit -m "refactor: aplicar feedback de revis├úo"

git push origin feature/nome-da-funcionalidade

```

### 8. Mergando o Pull Request

#### Ap├│s Aprova├º├úo:

1. No GitHub, clique em "Merge pull request"
2. Confirme o merge
3. (Opcional) Clique em "Delete branch" para limpar

#### Atualize localmente:

```bash

# V├í para develop localmente

git checkout develop



# Puxe as ├║ltimas altera├º├Áes (seu merge estar├í inclu├¡do)

git pull origin develop



# Remova a branch local (j├í removida no GitHub)

git branch -d feature/nome-da-funcionalidade

```

## Conven├º├Áes de Commits

### Formato de Mensagem de Commit

```

<Tipo>(Escopo): Descri├º├úo curta



Corpo opcional com mais detalhes

- Pode usar listas

- Separado do cabe├ºalho por linha vazia



Rodap├® opcional

Fixes #123

BREAKING CHANGE: descri├º├úo da quebra

```

### Tipos V├ílidos

- `feat`: Nova funcionalidade
- `fix`: Corre├º├úo de bug
- `docs`: Atualiza├º├Áes de documenta├º├úo
- `style`: Mudan├ºas de estilo sem alterar l├│gica (formata├º├úo, espa├ºos em branco, etc.)
- `refactor`: Refatora├º├úo sem alterar funcionalidade/comportamento
- `perf`: Melhoria de performance
- `test`: Adi├º├úo ou modifica├º├úo de testes
- `chore`: Tarefas de manuten├º├úo, build, etc.

### Escopo (Opcional)

- `frontend`: Altera├º├Áes no frontend
- `backend`: Altera├º├Áes no backend
- `api`: Altera├º├Áes nas APIs
- `models`: Altera├º├Áes nos modelos ML
- `data`: Altera├º├Áes na pipeline de dados
- `docs`: Altera├º├Áes na documenta├º├úo
- `config`: Altera├º├Áes em arquivos de configura├º├úo
- `ci`: Altera├º├Áes na integra├º├úo cont├¡nua

### Exemplos de Commits Bem Formulados

```

feat(frontend): adicionar componente de dashboard geogr├ífico

```

```

fix(backend): resolver erro de conex├úo com banco de dados



Ocorria quando a conex├úo era perdida durante opera├º├Áes

longas de processamento de dados.

```

```

refactor(models): otimizar pipeline de treinamento LSTM



- Reduz tempo de treinamento em 30%

- Melhora estabilidade do modelo

- Adiciona logging detalhado para debug

```

```

test(backend): adicionar testes para valida├º├úo de previs├Áes



Adiciona casos de teste para valida├º├úo de outliers

e valores nulos nos dados de entrada.

```

```

docs: atualizar guia de contribui├º├úo para novos desenvolvedores



Adiciona se├º├úo detalhada sobre code review

e exemplos pr├íticos de commits.

```

### Padr├Áes Importantes

#### Commits At├┤micos

- Cada commit deve representar uma altera├º├úo l├│gica completa
- Um commit = um prop├│sito claro
- Evite commits com m├║ltiplas inten├º├Áes

#### Mensagens Claras

- Use imperativo no presente: "Add" n├úo "Added" ou "Adds"
- Primeira linha <= 72 caracteres
- Se necess├írio, adicione corpo com mais detalhes
- Use linguagem clara e descritiva

## Pull Requests e Code Review

### Template de Pull Request

Quando criar um Pull Request, siga este template:

```markdown

## Descri├º├úo



Descreva as altera├º├Áes feitas e por qu├¬.



## Tipos de altera├º├úo

- [ ] Bug fix (mudan├ºa que resolve um problema)

- [ ] Nova funcionalidade (mudan├ºa que adiciona funcionalidades)

- [ ] Breaking change (corre├º├úo ou funcionalidade que causaria problemas existentes)



## Checklist

- [ ] Meu c├│digo segue os padr├Áes deste projeto

- [ ] Eu revi meu pr├│prio c├│digo

- [ ] Comentei meu c├│digo, especialmente em ├íreas dif├¡ceis de entender

- [ ] Fiz altera├º├Áes correspondentes na documenta├º├úo

- [ ] Minhas altera├º├Áes n├úo geram novos alertas

- [ ] Testes de unidade novos ou existentes passaram

- [ ] Testes de integra├º├úo passaram (se aplic├ível)



## Testes

Descreva como voc├¬ testou as altera├º├Áes.



## Imagens (se aplic├ível)

Inclua capturas de tela ou GIFs demonstrando as altera├º├Áes.



Fixes # (n├║mero da issue, se houver)

```

### T├¡tulo do Pull Request

- Siga o mesmo padr├úo de commits
- Seja claro e descritivo
- Inclua o tipo e escopo se relevante

### Descri├º├úo do Pull Request

- Descreva o problema resolvido
- Explique a solu├º├úo implementada
- Liste impactos e mudan├ºas relevantes
- Inclua capturas de tela se aplic├ível
- Conecte issues relevantes (ex: "Fixes #123")

### Labels

- Atribua labels apropriadas:

  - `feature`, `bug`, `enhancement`, `documentation`, etc.
  - `frontend`, `backend`, `ml-models`, etc.
  - `needs review`, `ready for merge`, etc.

### Code Review - Processo Completo

#### Para Contribuidores (Respondendo a Revis├Áes)

1. **Leia todos os coment├írios** cuidadosamente
2. **Agrade├ºa pelo feedback** (mesmo que seja cr├¡tico)
3. **Fa├ºa as altera├º├Áes solicitadas**
4. **Comunique suas altera├º├Áes**: "Aplicado feedback de [usu├írio]"
5. **Responda aos coment├írios**: Use "Resolve conversation" quando aprovado
6. **Envie atualiza├º├Áes**: `git push origin sua-branch`

#### Para Revisores

1. **Revise o c├│digo objetivamente** - foque na funcionalidade e qualidade
2. **Seja construtivo** - explique por que algo precisa de altera├º├úo
3. **Sugira melhorias** em vez de apenas apontar problemas
4. **Verifique**: funcionalidade, seguran├ºa, performance, testes, documenta├º├úo
5. **Use coment├írios em linha** para pontos espec├¡ficos
6. **Aprove quando estiver tudo certo**!

#### Crit├®rios de Revis├úo

- **Funcionalidade**: O c├│digo faz o que deveria?
- **Qualidade**: Segue os padr├Áes e conven├º├Áes do projeto?
- **Seguran├ºa**: N├úo introduz vulnerabilidades?
- **Performance**: N├úo afeta negativamente o desempenho?
- **Testes**: Testes cobrem casos importantes?
- **Documenta├º├úo**: C├│digo est├í bem documentado?

## Procedimentos Avan├ºados

### 1. Criando uma Release

#### Passo a Passo:

```bash

# 1. Atualize develop

git checkout develop

git pull origin develop



# 2. Crie branch de release a partir de develop

git checkout -b release/v1.2.0



# 3. Atualize n├║meros de vers├úo, changelog, etc.

# (editar package.json, CHANGELOG.md, etc.)



# 4. Fa├ºa commits finais de ajustes

git add .

git commit -m "chore(release): preparar release v1.2.0"



# 5. Mergue para main

git checkout main

git pull origin main

git merge release/v1.2.0 --no-ff



# 6. Crie tag de release

git tag -a v1.2.0 -m "Release v1.2.0"



# 7. Mergue de volta para develop

git checkout develop

git merge release/v1.2.0 --no-ff



# 8. Fa├ºa push das altera├º├Áes e tag

git push origin main

git push origin develop

git push origin v1.2.0



# 9. Remova branch de release

git branch -d release/v1.2.0

git push origin --delete release/v1.2.0

```

### 2. Hotfixes (Corre├º├Áes Urgentes)

#### Para corre├º├Áes urgentes em produ├º├úo:

```bash

# 1. Partindo de main

git checkout main

git pull origin main



# 2. Crie uma branch de hotfix

git checkout -b hotfix/v1.0.1-resolver-problema-critico



# 3. Fa├ºa as corre├º├Áes e commit

git add .

git commit -m "fix: resolver problema cr├¡tico em produ├º├úo"



# 4. Teste imediatamente

npm test  # ou os testes apropriados



# 5. Mergue para main

git checkout main

git merge hotfix/v1.0.1-resolver-problema-critico --no-ff



# 6. Crie tag de hotfix

git tag -a v1.0.1 -m "Hotfix v1.0.1"



# 7. Mergue de volta para develop

git checkout develop

git merge hotfix/v1.0.1-resolver-problema-critico --no-ff



# 8. Fa├ºa push

git push origin main

git push origin develop

git push origin v1.0.1



# 9. Remova branch de hotfix

git branch -d hotfix/v1.0.1-resolver-problema-critico

git push origin --delete hotfix/v1.0.1-resolver-problema-critico

```

### 3. Rebase Interativo

Para reescrever o hist├│rico de commits:

```bash

# Reordenar, editar ou combinar os ├║ltimos 3 commits

git rebase -i HEAD~3

```

### 4. Cherry-pick

Para aplicar commits espec├¡ficos de outra branch:

```bash

# Aplicar um commit espec├¡fico

git cherry-pick <commit-hash>



# Aplicar v├írios commits

git cherry-pick <commit1> <commit2> <commit3>

```

## Solu├º├úo de Problemas e D├║vidas Comuns

### 1. Como atualizar minha branch com as ├║ltimas altera├º├Áes do develop?

```bash

# M├®todo 1: Rebase (recomendado para branches de feature)

git checkout develop

git pull origin develop

git checkout sua-branch

git rebase develop



# M├®todo 2: Merge (menos recomendado para evitar commits de merge)

git checkout sua-branch

git merge develop

```

### 2. Como resolver conflitos de merge/rebase?

#### Durante um rebase:

```bash

# Ap├│s git rebase, se houver conflitos:

# 1. Edite os arquivos conflitantes (marcados com <<<<<<<, =======, >>>>>>>)

# 2. Marque como resolvidos

git add arquivo_resolvido.py



# 3. Continue o rebase

git rebase --continue



# 4. Se precisar abortar

git rebase --abort

```

#### Durante um merge:

```bash

# Ap├│s git merge, se houver conflitos:

# 1. Edite os arquivos conflitantes

# 2. Marque como resolvidos

git add arquivo_resolvido.py



# 3. Complete o merge

git commit -m "Resolver conflitos de merge"



# 4. Se precisar abortar

git merge --abort

```

### 3. Como desfazer commits?

#### Desfazer o ├║ltimo commit, mantendo altera├º├Áes:

```bash

# Manter altera├º├Áes no staging

git reset --soft HEAD~1



# Desfazer commit e manter altera├º├Áes no working directory

git reset HEAD~1



# Desfazer commit e descartar altera├º├Áes

git reset --hard HEAD~1

```

#### Desfazer commits anteriores:

```bash

# Resetar para um commit espec├¡fico (perde commits ap├│s isso)

git reset --hard <commit-hash>



# Resetar mas manter altera├º├Áes

git reset <commit-hash>

```

### 4. Como renomear uma branch local e remota?

```bash

# Renomear branch local

git branch -m nome-antigo nome-novo



# Excluir branch antiga do remoto

git push origin --delete nome-antigo



# Fazer push da nova branch

git push origin -u nome-novo

```

### 5. Como remover commits de uma branch?

```bash

# Remover os ├║ltimos n commits

git reset --hard HEAD~n



# Remover commits espec├¡ficos usando rebase interativo

git rebase -i HEAD~n

# (marcar commits como 'drop' ou 'd')

```

### 6. Como trabalhar com m├║ltiplas funcionalidades?

- Crie branches separadas para cada funcionalidade
- Mantenha branches pequenas e focadas
- N├úo misture funcionalidades diferentes na mesma branch
- Complete uma funcionalidade por vez antes de passar para a pr├│xima

### 7. Como lidar com branches "abandonadas"?

```bash

# Listar branches remotas que n├úo existem mais localmente

git remote prune origin



# Excluir branches locais que j├í foram mergiadas e deletadas remotamente

git branch --merged | grep -v "\*\|main\|develop" | xargs -n 1 git branch -d

```

### 8. Como lidar com push rejeitado?

```bash

# Se o push for rejeitado por estar desatualizado

git pull --rebase origin sua-branch



# Se voc├¬ quiser for├ºar o push (cuidado!)

git push --force-with-lease origin sua-branch

```

### 9. Como verificar a diferen├ºa entre branches?

```bash

# Ver commits que est├úo em uma branch mas n├úo na outra

git log develop..feature/nome-da-funcionalidade



# Ver arquivos diferentes entre branches

git diff develop..feature/nome-da-funcionalidade



# Ver estat├¡sticas de diferen├ºas

git diff --stat develop..feature/nome-da-funcionalidade

```

### 10. Como restaurar um arquivo de um commit anterior?

```bash

# Restaurar um arquivo de um commit espec├¡fico

git checkout <commit-hash> -- caminho/do/arquivo



# Restaurar um arquivo para o estado em develop

git checkout develop -- caminho/do/arquivo

```

## Melhores Pr├íticas

### 1. Commits At├┤micos e Significativos

- Fa├ºa commits pequenos e com prop├│sitos bem definidos
- Cada commit deve representar uma altera├º├úo l├│gica completa
- Evite commits com m├║ltiplas inten├º├Áes
- Evite commits "WIP" ou "Fix" gen├®ricos
- Cada commit deve ter uma raz├úo clara

### 2. Mensagens de Commit Claras

- Use imperativo no presente: "Add" n├úo "Added" ou "Adds"
- Primeira linha deve ter no m├íximo 72 caracteres
- Se necess├írio, adicione corpo com mais detalhes
- Use linguagem clara e descritiva
- Inclua contexto quando necess├írio

### 3. Teste antes de Push

- Execute testes locais antes de fazer push
- Verifique se o c├│digo est├í funcionando localmente
- Execute linting e formata├º├úo
- Teste manualmente se aplic├ível

### 4. Atualiza├º├úo Regular de Branches

- Mantenha sua branch develop atualizada
- Rebase sua feature com develop regularmente
- Evite trabalhar com branches muito desatualizadas

### 5. Revis├úo de C├│digo Ativa

- Revise seu pr├│prio c├│digo antes de submeter
- Pe├ºa revis├úo de colegas
- Revise c├│digo de outros ativamente
- Agrade├ºa feedbacks construtivos
- Use o processo de revis├úo para aprendizado

### 6. Documenta├º├úo Apropriada

- Atualize documenta├º├úo quando necess├írio
- Comente c├│digo complexo adequadamente
- Escreva READMEs claros para novas funcionalidades
- Atualize CHANGELOG quando apropriado

### 7. Seguran├ºa e Qualidade

- N├úo comite credenciais ou senhas
- Use vari├íveis de ambiente para configura├º├Áes sens├¡veis
- Siga padr├Áes de seguran├ºa do projeto
- Use ferramentas de an├ílise est├ítica

## Ferramentas de Apoio

### Scripts de Workflow

O script `scripts/git-workflow.bat` fornece comandos auxiliares:

- `git-workflow.bat setup` - Configura branches iniciais
- `git-workflow.bat feature` - Cria branch de feature
- `git-workflow.bat bugfix` - Cria branch de bugfix
- `git-workflow.bat release` - Cria branch de release
- `git-workflow.bat merge-feature` - Merges feature para develop
- `git-workflow.bat merge-release` - Merges release para main

### GitHub CLI

Instale e use a CLI do GitHub para tarefas automatizadas:

```bash

# Instale GitHub CLI (no Windows: winget install GitHub.cli)

gh auth login



# Crie PR diretamente

gh pr create --title "feat: nova funcionalidade" --body "Descri├º├úo"



# Comentar em PR existente

gh pr comment 123 --body "Coment├írio sobre o PR"



# Checar status de CI

gh pr checks 123 --watch



# Fechar PR

gh pr close 123

```

### Extens├Áes de Navegador ├Üteis

- **Refined GitHub** - Melhora a interface do GitHub
- **Octotree** - Mostra estrutura de arquivos como ├írvore
- **GitHub File Icons** - ├ìcones para diferentes tipos de arquivos

### Atalhos de Teclado do GitHub

- `t` - Buscar arquivos
- `l` - Adicionar labels
- `a` - Atribuir revisores
- `/` - Buscar no reposit├│rio
- `Ctrl + Enter` - Submeter coment├írios

## Integra├º├úo Cont├¡nua

### Hooks de Pre-commit

O projeto utiliza hooks de pre-commit para garantir qualidade de c├│digo:

```bash

# Instale os hooks uma vez por projeto

pip install pre-commit

pre-commit install



# Execute manualmente se necess├írio

pre-commit run --all-files



# Execute para arquivos espec├¡ficos

pre-commit run --files arquivo1.py arquivo2.py

```

### Crit├®rios para Merge

- **Testes automatizados**: Todos os testes devem passar
- **Cobertura de testes**: N├úo pode diminuir significativamente
- **Revis├úo de c├│digo**: Pelo menos uma aprova├º├úo necess├íria
- **Status checks**: Todos os checks de CI devem estar verdes
- **Branch atualizada**: Deve estar atualizada com develop
- **Formato de c├│digo**: Deve seguir padr├Áes (auto-formatado pelo CI)

### Configura├º├úo de Integra├º├úo Cont├¡nua

O projeto pode usar GitHub Actions com configura├º├úo como:

```yaml

# .github/workflows/ci.yml

name: CI



on:

  pull_request:

    branches: [develop, main]

  push:

    branches: [develop, main]



jobs:

  test:

    runs-on: ubuntu-latest

    steps:

    - uses: actions/checkout@v3

    - name: Setup Python

      uses: actions/setup-python@v3

      with:

        python-version: '3.9'

    - name: Install dependencies

      run: |

        pip install -r requirements.txt

        pip install -r requirements-dev.txt

    - name: Run tests

      run: pytest

    - name: Run linting

      run: pylint src/

    - name: Run security scan

      run: bandit -r src/

```

## Recursos Adicionais

### Documenta├º├úo Oficial

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Documentation](https://docs.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

### Ferramentas de Aprendizado

- [Pro Git Book](https://git-scm.com/book/en/v2) - Livro completo e gratuito sobre Git
- [Learn Git Branching](https://learngitbranching.js.org/) - Jogo interativo para aprender Git
- [Git Immersion](http://gitimmersion.com/) - Tutorial completo para iniciantes
- [Oh Shit, Git!](https://ohshitgit.com/) - Guia para situa├º├Áes problem├íticas com Git

### Boas Pr├íticas Adicionais

- [Git Style Guide](https://github.com/agis/git-style-guide) - Guia completo de melhores pr├íticas
- [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) - Artigo original sobre Git Flow
- [GitHub Flow](https://guides.github.com/introduction/flow/) - Alternativa simplificada ao Git Flow

---

## Checklist de Contribui├º├úo

Antes de submeter um Pull Request, verifique:

- [ ] Segui as conven├º├Áes de commit
- [ ] Executei todos os testes locais
- [ ] Fiz linting e formata├º├úo
- [ ] Atualizei a documenta├º├úo (se necess├írio)
- [ ] Minha branch est├í atualizada com develop
- [ ] Coment├írios explicativos est├úo presentes
- [ ] Testei manualmente (se aplic├ível)
- [ ] Preenchi o template do PR
- [ ] Adicionei labels apropriados
- [ ] Solicitei revisores apropriados
- [ ] N├úo cometi informa├º├Áes sens├¡veis
- [ ] N├úo h├í conflitos com a branch base

Este workflow completo garante colabora├º├úo eficiente, c├│digo de qualidade e rastreabilidade completa no projeto Nova Corrente. Siga estas pr├íticas para contribuir de forma profissional e eficaz!
