# Anamnese 

#Frontend — Estado Atual, Especificações Técnicas e Roadmap

## Sumário Executivo

- Stack: Next.js (App Router) + TypeScript + Tailwind CSS + Recharts + MSW/Jest.
- Ponto central: `src/app/main/page.tsx` com navegação interna (Dashboard, Relatórios, Análises, Configurações).
- Integração: `src/lib/api.ts` com cache simples (30s) e mensagens claras quando o backend está indisponível.
- Backend alvo: FastAPI na porta 5000 (rewrites em `next.config.js`), porém README ainda refere Flask (desalinhado).
- Estado atual: UI das 5 abas planejadas presente (Geográfico, Fórmulas, Clustering, Modelos, Prescritivo). Múltiplas telas usam dados mockados no client; integração real com API é parcial.

---

## Requisitos do Cliente (consolidados das docs/README)

- Visualização em 5 abas (Geográfico, Fórmulas, Clustering, Modelos, Prescritivo).
- KPIs e alertas em “quase” tempo real com atualização periódica.
- Clustering de falhas de equipamentos e performance de torres, com estatísticas e visualizações.
- Comparação de modelos (ARIMA/Prophet/LSTM/Ensemble), curvas de perda, importância de features e resíduos.
- Recomendações prescritivas com prioridade, impacto, economia estimada e mapeamento regional.
- Roadmap: exportação, theme toggle, acessibilidade, integração com DB, streaming em tempo real, dashboards customizados, PWA.

---

## Estado de Implementação

- Abas de Analytics: presentes via `src/components/Analytics.tsx` (tabs: Geográfico, Fórmulas, Clustering, Modelos, Prescritivo).
- Dashboard: KPIs, status operacional, previsão (mock), tabela de alertas com drilldown para Análises, toasts, auto-refresh simulado.
- Prescritivo: `PrescriptiveRecommendationsEnhanced` busca `/api/prescriptive/recommendations` (fallback local se falhar) e exibe totais/alta prioridade.
- API Client: `src/lib/api.ts` expõe endpoints de `/api/v1/features/*`, `/api/*` (kpis, alerts, clustering, models, prescriptive) e `/health`; tem cache (30s) e tratamento de indisponibilidade.
- Configuração: `next.config.js` define `NEXT_PUBLIC_API_URL` (default `http://localhost:5000`) e rewrites `/api/:path*` → `${API_URL}/api/v1/:path*`.
- Testes: Jest + JSDOM + MSW com handlers cobrindo diversos endpoints.
- UX/UI: Tema escuro com Tailwind; componentes e animações prontos; Sidebar lista atalhos para rotas ML.

---

## Lacunas Identificadas

- *Dados mockados no client (Dashboard/Analytics) em vez de consumir API real.*
- Inconsistência nas chamadas: uso misto de caminhos absolutos (`baseURL + '/api/...'`) e relativos. Nem todas as chamadas se beneficiam do `rewrite`.
- Sidebar referencia páginas em `/features/*` que não existem no App Router.
- README desatualizado (fala em Flask `api_standalone.py`), divergindo do backend FastAPI.
- Gemini/IA: componente existe (`GeminiAnalysis`), mas integração real e configuração de API key estão ausentes.
- Test coverage: infra existe, mas faltam testes de smoke para páginas principais.

---

## Especificações Técnicas (alvo)

### 1) Integração com Backend (FastAPI)

- Padrão de URL: utilizar caminhos relativos começando por `/api` sempre que o endpoint mapeia para `/api/v1/*`, aproveitando `rewrites` de `next.config.js` e evitando CORS.
- Para endpoints fora de `/api/v1/*` (ex.: `/health`, endpoints legados `/api/kpis` etc.):
  - Preferir caminhos relativos e adicionar rewrites correspondentes; ou
  - Centralizar `API_BASE_URL` via `NEXT_PUBLIC_API_URL` e documentar `.env.local`.

### 2) Configuração e Ambiente

- `.env.local` (frontend):
  - `NEXT_PUBLIC_API_URL=http://localhost:5000`
- `next.config.js`:
  - Manter rewrite `/api/:path*` → `${NEXT_PUBLIC_API_URL}/api/v1/:path*`.
  - Avaliar adicionar rewrites para endpoints não-v1 (ex.: `/kpis`, `/alerts`) caso migrem para `/api` relativo.

### 3) Roteamento e Páginas

- App Router:
  - `src/app/main/page.tsx` permanece como shell principal com Sidebar/Header.
  - Criar páginas em `src/app/features/{temporal|climate|economic|5g|lead-time|sla|hierarchical|categorical|business}/page.tsx` consumindo `apiClient`.
  - Opcional: rotas para `clustering`, `models` e `prescriptive` fora de `Analytics` para deep-linking.

### 4) Camada de Dados (API Client)

- Padronizar `apiClient` para utilizar caminhos relativos `/api/...` ao máximo, reduzindo dependência de `NEXT_PUBLIC_API_URL`.
- Adicionar adapters/DTOs quando necessário para mapear respostas do backend para estruturas usadas nos componentes (estabilidade contra mudanças de contrato).
- Estratégia de cache: manter TTL 30s, expor `clearCache()` e invalidar por ação do usuário quando aplicável.

### 5) Substituição de Mocks

- Dashboard: migrar KPIs/alerts/forecast para chamadas reais (`getKpis`, `getAlerts`, `get30DayForecast`).
- Analytics/Geográfico: substituir `mockStateData` por dados reais (combinação de endpoints de features). Enquanto a API não tiver um endpoint agregado, implementar composições no client com loading states.
- MSW: manter handlers para testes; não usar em runtime.

### 6) Testes

- Smoke tests para `Dashboard`, `Analytics (cada aba)`, `PrescriptiveRecommendationsEnhanced` com MSW.
- Testes de contrato mínimos (tipos essenciais) e de erros (backend off, 4xx/5xx) no `apiClient`.

### 7) Performance & Observabilidade

- Lazy-loading de componentes pesados (clustering/modelos) se necessário.
- Medição de TTFB/LCP via Web Vitals e logs simples no console em dev.
- Caching de requisições idempotentes (já existe) e memoização em componentes.

### 8) Acessibilidade e UX

- Theme toggle (classe na raiz + persistência em `localStorage`).
- Export (CSV/PNG) para tabelas e gráficos principais.
- Foco visível, labels ARIA em componentes interativos, contrastes checados.
- Loading skeletons em dashboards e abas com chamadas remotas.

---

## Plano de Ação (Backlog Priorizado)

### Alta Prioridade (Impacto alto, Esforço baixo-médio)

- Padronizar `apiClient` para usar caminhos relativos `/api/*` quando aplicável; ajustar `next.config.js` se necessário.
- Atualizar README para FastAPI: comandos de start (`python backend/run_server.py`), links de docs (`/docs`), e `.env.local` do frontend.
- Implementar `.env.local.example` e instruções.
- Migrar Dashboard (KPIs/alerts/forecast) para dados reais via `apiClient` com loading/skeletons e toasts de erro.
- Criar páginas em `/features/*` consumindo `/api/v1/features/*` com tabelas simples e paginação básica.

### Média Prioridade (Impacto alto, Esforço médio)

- Remover `mockStateData` gradualmente: introduzir camada de agregação de features para o mapa geográfico.
- Unificar endpoints “não-v1” do `api.ts` para caminhos relativos e/ou adicionar rewrites específicos.
- Adicionar smoke tests com MSW para páginas principais e `apiClient` (erros e sucesso).
- Implementar Theme toggle e Export básico (CSV para tabelas, PNG para charts principais).

### Baixa Prioridade (Impacto médio, Esforço variável)

- Otimizações de performance (lazy-loading, split de bundle em abas pesadas).
- Métricas de Web Vitals e logging leve.
- Acessibilidade (varredura de contrastes, ARIA, navegação por teclado) e skeletons adicionais.
- Páginas deep-link separadas para Clustering/Modelos/Prescritivo com SEO básico.

---

## Critérios de Aceite (DoD) por Entrega

- Padronização de API: todas as chamadas que mapeiam para `/api/v1/*` usam caminhos relativos e passam pelo rewrite.
- Dashboard integrado: KPIs/alerts/forecast renderizam de dados reais, com loading e fallback de erro.
- Páginas `/features/*`: cada página lista dados com paginação, estados de loading/erro e tipagem estrita.
- README e `.env.local.example` atualizados e testados em Windows.
- Testes: smoke tests passam no CI; MSW cobre endpoints essenciais; cobertura mínima nas páginas principais.
- UX: Theme toggle persistente, Export funcional nos principais componentes.

---

## Riscos e Mitigações

- Divergência contrato API ↔ UI: introduzir adapters/DTOs e testes de contrato mínimos.
- CORS/ambiente: priorizar rewrites e caminhos relativos; documentar `.env.local`.
- Debt de mocks: migração gradual com feature flags/switches de dados e MSW apenas em testes.

---

## Instruções de Execução (Dev)

- Backend: `cd backend && pip install -r requirements.txt && python run_server.py` (Docs: `http://127.0.0.1:5000/docs`).
- Frontend: `cd frontend && npm install && npm run dev` (Acesse `http://localhost:3000`).
- Ambiente: crie `frontend/.env.local` com `NEXT_PUBLIC_API_URL=http://localhost:5000` se não usar só rewrites.

---

## Anexos

- Arquivos relevantes: `frontend/src/lib/api.ts`, `frontend/next.config.js`, `frontend/src/app/main/page.tsx`, `frontend/src/components/Analytics.tsx`, `frontend/src/components/PrescriptiveRecommendationsEnhanced.tsx`, `frontend/mocks/*`.
- Documentos: `docs/misc/NEXT_ENHANCEMENTS.md`, `README.md` (desatualizado para backend).
