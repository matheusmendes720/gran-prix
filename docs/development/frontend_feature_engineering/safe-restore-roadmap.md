# Safe Restore Roadmap

## 1. Preparação
- **Fotografar o estado atual:** Salvar screenshots (já capturadas) para comparar com UI original.
- **Congelar trabalho em andamento:** Garantir que não há processos `npm run dev` ou `uvicorn` rodando que possam gerar arquivos temporários.
- **Branch de proteção:**
  ```bash
  git checkout -b rollback/legacy-ui-restore
  ```

## 2. Auditoria de Alterações
1. Listar arquivos alterados desde o último estado válido:
   ```bash
   git status
   git diff --stat main..HEAD
   ```
2. Consultar histórico focado em frontend:
   ```bash
   git log --oneline -- frontend/src/app frontend/src/components frontend/src/hooks
   ```
3. Identificar commit baseline (print antigo indica commit pré-storytelling). Registrar hash em `docs/development/frontend_feature_engineering/legacy-dashboard-restoration.md`.

## 3. Rollback Seletivo
### A. Restaurar UI Deep-Blue Original
```bash
# substituir arquivos principais pela versão do commit bom (HASH_BASELINE)
git checkout HASH_BASELINE -- \
  frontend/src/app/page.tsx \
  frontend/src/app/main/page.tsx \
  frontend/src/components/Dashboard.tsx \
  frontend/src/components/KpiCard.tsx \
  frontend/src/components/DemandChart.tsx
```

### B. Reverter Hooks/API (se necessário)
```bash
git checkout HASH_BASELINE -- frontend/src/hooks/use-api.ts frontend/src/lib/api-client.ts
```

### C. Limpar assets/storytelling (opcional)
```bash
git checkout HASH_BASELINE -- frontend/src/app/storytelling-dashboard/page.tsx
rm frontend/src/app/storytelling-dashboard/page.tsx # se não existir em baseline
```

## 4. Verificação
1. Instalar dependências compatíveis (caso novas libs tenham sido adicionadas):
   ```bash
   cd frontend
   npm install
   npm run lint
   npm run build
   npm run dev
   ```
2. Validar UI manualmente em `http://localhost:3000/` e comparar com screenshot legado.
3. Confirmar que componentes críticos (KPIs, tabela de materiais, charts) renderizam sem banners de fallback.

## 5. Consolidar Rollback
- Revisar diff:
  ```bash
  git status
  git diff
  ```
- Commitar alteração:
  ```bash
  git commit -am "chore: restore legacy deep-blue dashboard"
  ```
- Abrir merge request / pull request apontando motivos do rollback.

## 6. Contingência
- Se rollback quebrar build, aplicar reversão total:
  ```bash
  git reset --hard HASH_BASELINE
  ```
- Manter notas desta pasta como documentação do aprendizado; não apagar.
- Planejar reintrodução das features em branch separado (`feature/storytelling-v2`) com feature flags e fallbacks antes de mesclar novamente.
