# Plano Detalhado para Desenvolvimento do Frontend

Documento expandido com instruções passo a passo, entregáveis por etapa e critérios de aceite para o time de frontend.

---

## 1. Configuração Inicial (Dia 1)


* **Pré-requisitos**

1. Confirmar Node.js ≥ 18.18 e npm ≥ 9 (`node -v`, `npm -v`).
2. Instalar PNPM (preferencial) `npm i -g pnpm@latest`.
3. Configurar `.nvmrc` com versão oficial do projeto.


**Bootstrap do projeto**

1. `pnpm create next-app frontend --ts --tailwind --eslint --app`.
2. Remover arquivos de boilerplate (ex.: `page.tsx`, `globals.css`).
3. Configurar `package.json` com scripts padrão:
   ```json
   {
     "scripts": {
       "dev": "next dev",
       "build": "next build",
       "start": "next start",
       "lint": "next lint"
     }
   }
   ```



**Estrutura de diretórios**

```
src/
├── app/
│   ├── layout.tsx            # Shell da aplicação (Header + Sidebar + Providers)
│   └── (routes)/             # Rotas agrupadas (main, itens, settings, auth)
├── components/
│   ├── ui/                   # UI atômica (botões, campos, badges)
│   ├── charts/               # Gráficos reutilizáveis
│   ├── tables/               # Tabelas e data-grids
│   └── layout/               # Header, Sidebar, Footer
├── hooks/                    # Hooks customizados
├── lib/                      # Clients, formatters, helpers
├── services/                 # Regras de negócio + chamadas API
├── store/                    # Estado global (Zustand)
├── styles/                   # Tailwind + tokens
└── types/                    # Tipos globais e DTOs
```



**Configurações de qualidade**

1. ESLint: adicionar presets `next`, `typescript`, `tailwindcss`, `vitest`.
2. Prettier: criar `.prettierrc` com largura 100 e aspas simples.
3. Husky + lint-staged: rejeitar commits sem lint e testes rápidos (`pnpm husky install`).



**Tema visual**

1. Definir tokens em `tailwind.config.ts` (cores, tipografia, spacing).
2. Criar `src/styles/tokens.css` com variáveis CSS para dark/light mode.
3. Documentar paleta oficial em Figma/Storybook (hex + contexto de uso).


---

## 2. Biblioteca de Componentes de UI (Dias 2-4)

1. **Governança de design system**

   - Criar guideline `docs/ui/base-components.md` com padrões de props, estados (hover/focus/disabled) e convenções de nomenclatura (`<Componente>`, `<Componente>Icon`, `<Componente>Skeleton`).
2. **Componentes fundamentais**

   - Botões (`Button`, `IconButton`, `ButtonGroup`) com variantes `primary`, `secondary`, `ghost`, `destructive`.
   - Inputs (`TextField`, `NumberField`, `Select`, `MultiSelect`, `DateRangePicker`).
   - Formatação (`Badge`, `Tag`, `StatusPill`).
   - Layout (`Card`, `MetricCard`, `SectionTitle`).
3. **Estados e acessibilidade**

   - Garantir foco visível (`outline` custom).
   - Suportar atalhos de teclado em botões críticos.
   - Implementar ARIA labels em inputs complexos.
4. **Storybook**

   - Configurar Storybook (`pnpm dlx storybook@latest init`) já nesta etapa.
   - Criar histórias com `Controls` para props principais e `Play function` para interações.
5. **Critérios de aceite**

   - Cobertura de testes unitários > 80% para componentes críticos.
   - Documentação de props em Storybook + design tokens referenciados.

---

## 3. Páginas e Fluxos Principais (Dias 5-9)

### 3.1 Dashboard Principal (`/main`)

1. Criar layout com `Sidebar`, `Topbar`, `KpiGrid`, `ForecastChart`, `AlertsList`.
2. Wireframe funcional com dados mockados (`src/mocks/dashboard.ts`).
3. Conectar API após seção 5 (React Query) utilizando `useDashboardData()`.
4. Widgets obrigatórios:
   - KPIs: MAPE, Rupturas, Estoque Médio, ROI (`KpiCard`).
   - Gráfico: previsão x realizado (interativo, range selecionável).
   - Alertas: lista com severidade, tempo restante, ação sugerida.
   - Filtros: período (7/30/90 dias), categoria de item, criticidade.

### 3.2 Itens (`/items`)

1. Usar `DataGrid` com paginação server-side.
2. Filtros: nome, SKU, categoria, status (em risco/OK), faixa de MAPE.
3. Ações inline: `Ver detalhes`, `Recalcular previsão`, `Criar alerta`.
4. Exportar CSV dos dados visíveis (`ExportButton`).

### 3.3 Detalhes do Item (`/items/[id]`)

1. Gráfico principal com comparativo (real x previsto) + intervalo de confiança.
2. Tabs: `Visão Geral`, `Fatores Externos`, `Alertas & Ações`, `Histórico`.
3. Cards explicativos com fatores críticos (clima, economia, manutenção).
4. Timeline de eventos relevantes (ex.: manutenção, troca de fornecedor).

### 3.4 Configurações (`/settings`)

1. Sessões: `Perfil`, `Notificações`, `Integrações`, `Preferências`.
2. Persistência via API (`PATCH /users/me`, `PUT /settings/notifications`).
3. Switch para dark mode com persistência em `localStorage` + API.

### 3.5 Autenticação (`/auth/login`, `/auth/reset`)

1. Form de login com validação Zod e mensagens contextualizadas.
2. Suporte a SSO (placeholder) e login tradicional.
3. Fluxo de recuperação de senha com feedback visual.

---

## 4. Gráficos e Visualizações (Dias 10-12)

1. **Seleção de biblioteca**

   - Adotar `Nivo` como padrão (com SSR e responsividade) + `Recharts` para curvas suaves.
2. **Implementação base**

   - Criar `ChartProvider` para temas (dark/light, paleta de cores).
   - Componentes: `TimeSeriesChart`, `StackedBarChart`, `DonutChart`, `HeatmapCalendar`.
3. **Interatividade avançada**

   - Hover sync entre múltiplos gráficos (`useSharedTooltip`).
   - Brush (seleção de período) com atualização de estado global.
   - Botão “Exportar” (PNG/CSV) utilizando `html-to-image` e conversão custom.
4. **Performance**

   - Lazy loading (`dynamic(() => import("..."), { ssr: false })`).
   - Suspense + skeletons para carregamento progressivo.
5. **Validação**

   - Dados mockados com diferentes volumes (pequeno, médio, grande).
   - Testes visuais via Storybook Chromatic.

---

## 5. Integração com API (Dias 13-15)

1. **Cliente HTTP**

   - Criar `src/lib/http.ts` com Axios e interceptores (auth, erros, retries).
   - Timeout padrão 10s, cancelamento com `AbortController`.
2. **Gerenciamento de dados**

   - React Query com `QueryClient` no `layout.tsx`.
   - Chaves padronizadas: `['dashboard', params]`, `['items', page, filters]`.
   - Mutations com `optimistic updates` onde aplicável.
3. **Tratamento de erros**

   - `ApiErrorBoundary` exibindo mensagens amigáveis.
   - Mapear códigos HTTP → mensagens (ex.: 401 → sessão expirada).
4. **Estados de carregamento**

   - Skeletons (`CardSkeleton`, `TableSkeleton`).
   - Fallback offline (React Query + IndexedDB opcional).
5. **Segurança**

   - Usar `NEXT_PUBLIC_API_URL` para baseURL (variáveis em `.env.local`).
   - Sanitizar dados antes de renderizar (ex.: `dangerouslySetInnerHTML` proibido).

---

## 6. Autenticação e Autorização (Dias 16-17)

1. **Fluxo de login**

   - Página `/auth/login` chama `POST /auth/login`.
   - Guardar `accessToken` em `HttpOnly cookie` (via API backend).
   - Guardar `refreshToken` apenas server-side (rota `/api/refresh`).
2. **Contexto de sessão**

   - Criar `AuthProvider` com Zustand/Context combinados.
   - Hook `useAuth()` com `isAuthenticated`, `user`, `roles`.
3. **Proteção de páginas**

   - Middleware `src/middleware.ts` redirecionando anônimos.
   - HOC `withAuthorization` para componentes com RBAC (`roles: ['admin']`).
4. **Renovação de tokens**

   - Interceptor Axios para `401` → chamar `/auth/refresh`.
   - Logout automático após falha dupla.
5. **Auditoria**

   - Registrar eventos críticos (login, logout, alteração de preferências) via `POST /audit/logs`.

---

## 7. Qualidade e Testes (Dias 18-20)

1. **Infraestrutura de testes**

   - Adicionar Vitest ou Jest com `jsdom`.
   - Configurar `@testing-library/react` + `@testing-library/user-event`.
   - Criar `vitest.config.ts` com alias `@/*`.
2. **Testes unitários**

   - Componentes de UI: snapshot + teste de interação.
   - Hooks: `renderHook` com cenários de sucesso/erro.
3. **Testes de integração**

   - Páginas chave com dados mockados (MSW).
   - Verificar fluxo completo (filtros → atualização de gráfico).
4. **Testes E2E**

   - Cypress com suite mínima: login, dashboard, detalhe do item.
   - Pipeline CI rodando E2E em modo headless (`cypress run`).
5. **Acessibilidade**

   - Executar `@axe-core/react` em desenvolvimento (`if (process.env.NODE_ENV !== 'production')`).
   - Validar contrastes com `axe` + Storybook addon.
6. **Critérios**

   - Cobertura global ≥ 70% (linhas), componentes críticos ≥ 85%.
   - Nenhum erro de acessibilidade nível crítico na release.

---

## 8. Otimização, Performance e Segurança (Dia 21)

1. **Performance**

   - Medir com Lighthouse (alvo: Performance ≥ 90).
   - Hidratação parcial (React Server Components + streaming).
   - Implementar `route prefetch` e `image optimization` (Next Image).
2. **Código**

   - `dynamic import` em componentes pesados (charts, tabelas).
   - Memoização (`useMemo`, `useCallback`) onde necessário.
3. **Segurança**

   - CSP via `next.config.js` (`contentSecurityPolicy` customizado).
   - Substituir `dangerouslySetInnerHTML` por sanitizadores.
   - Proteção contra CSRF (cookies HttpOnly + SameSite=strict).
4. **PWA**

   Instalar `next-pwa`, configurar manifest (`manifest.webmanifest`).

   Testar offline básico (dashboard cacheado).

---

## 9. Documentação e Observabilidade (Dia 22)

1. **Storybook completo**

   - Publicar em ambiente estático (Chromatic ou Vercel Preview).
   - Adicionar docs MDX com casos de uso e diretrizes.
2. **Guia de estilo**

   - `docs/ui/style-guide.md` descrevendo tipografia, cores, spacing, iconografia.
3. **Manual do desenvolvedor**

   - `docs/frontend/CONTRIBUTING.md` com fluxo de branches, scripts, testes.
4. **Observabilidade**

   - Integrar Sentry: `SENTRY_DSN` em `.env`, captura de erros/crashes.
   - LogRocket ou PostHog para replay de sessão.
   - Eventos custom (ex.: filtragem, exportações) via analytics.

---

## 10. Deploy, CI/CD e Monitoramento (Dias 23-24)

1. **Pipeline CI**

   - GitHub Actions com jobs: `lint`, `test`, `build`, `cypress`.
   - Cache de dependências PNPM.
2. **Deploy**

   - Staging em Vercel (preview por PR) ou AWS Amplify.
   - Produção com variáveis seguras (`NEXT_PUBLIC_API_URL`, `SENTRY_DSN`).
3. **Monitoramento em produção**

   - Dashboards Sentry (erros por release).
   - Health check em `/api/health` consumido pelo frontend (exibir banner se offline).
   - Configurar alerts Slack/Teams para falhas críticas.

---

## 11. Feedback Contínuo e Iterações (Dia 25+)

1. **Processo de feedback**

   - Reuniões quinzenais com stakeholders (produto, operações, dados).
   - Formulário in-app para coleta de sugestões.
2. **Backlog de melhorias**

   - Priorizar via RICE (Reach, Impact, Confidence, Effort).
   - Revisar métricas UX (tempo na página, cliques em alertas).
3. **Planejamento de releases**

   - Ciclos quinzenais com changelog publicado em `docs/releases/frontend.md`.

---

## 12. Refinamentos UX/UI e Experiência Assistida (Contínuo)

* **Estados de dados reais vs. mock**

  - Objetivo: eliminar dados estáticos diretamente nos componentes e garantir feedback adequado em todas as situações de API.
  - Tarefas
    - Mapear todos os componentes que usam mocks (`Dashboard`, `Analytics`, `Reports`, gráficos, mapas) e criar hooks `useDashboardData`, `useAnalyticsData`, etc. que encapsulam chamadas ao `apiClient` com React Query.
    - Definir e implementar estados `loading`, `empty`, `error`, `success` com mensagens e ícones orientativos (`EmptyState`, `ErrorState`, `RetryButton`).
    - Para fins de demos, criar `DemoDataProvider` opcional que injeta fixtures via Context, mantendo código de produção isolado.
  - Critérios de aceite
    - Nenhum componente consome arrays mockados diretamente; todo dado vem de hook ou provider configurável.
    - Para cada widget existe paridade visual entre loading (skeleton/shimmer), empty (mensagem clara + CTA) e error (toast + opção de retry).
* **Guia de hierarquia de informação e layout responsivo**

  - Objetivo: alinhar storytelling às métricas de negócio (MAPE, rupturas, ROI) com foco em clareza e prioridade visual.
  - Tarefas
    - Documentar hierarquia em `docs/ui/hierarchy-map.md` com diagramas de zonas (Above the Fold, Secondary Insights, Deep Dive).
    - Garantir breakpoints Tailwind (`sm`, `md`, `lg`, `xl`) com layouts ajustados em Dashboard, Itens e Analytics (testar 1280px, 1024px, 768px, 375px).
    - Ajustar componentes de KPI para suportar descrições curtas, meta/variação e tooltips com explicações de negócio.
  - Critérios de aceite
    - Em telas ≤ 768px: navegação via drawer, cards empilhados e mapas com carrossel.
    - KPIs exibem meta vs. valor atual e tooltip explica impacto no SLA/ROI.
* **Microinterações e feedback instantâneo**

  - Objetivo: reforçar perceção de performance e orientar o usuário durante ações críticas.
  - Tarefas
    - Implementar animações suaves usando `framer-motion` ou utilidades Tailwind para hover/focus/expansão.
    - Adicionar `Toast`/`Snackbar` consistentes para operações CRUD (favoritar relatório, regenerar, atualizar dados) integrados ao `ToastProvider`.
    - Criar `ActionProgressBar`/`InlineSpinner` para operações longas (geração de relatório, refresh de dashboards) com estimativa de tempo.
  - Critérios de aceite
    - Todas as ações com latência > 500ms exibem feedback visual.
    - Animações seguem curva `ease-out` ≤ 200ms e não prejudicam acessibilidade (usuário pode desabilitar via preferências).
* **Acessibilidade aprofundada e localização**

  - Objetivo: ir além do checklist mínimo e suportar diferentes perfis de operadores (ex.: alto contraste, teclado, traduções futuras).
  - Tarefas
    - Completar auditoria `axe` e gerar planilha de correção (roles ARIA, labels, heading structure, foco).
    - Inserir suporte a redução de movimento (`prefers-reduced-motion`) e contraste (`prefers-contrast`) nos tokens de tema.
    - Preparar `i18n` base: catálogo `pt-BR` + `en-US` com mensagens-chave (KPIs, alertas, botões) e hook `useLocaleContent`.
  - Critérios de aceite
    - Lighthouse Accessibility ≥ 95 em Desktop e Mobile.
    - Alternância de idioma atualiza títulos, tooltips e toasts sem recarregar a página.
* **QA de design e handoff contínuo**

  - Objetivo: sincronizar implementações com o design system vivo e manter consistência visual durante a migração para dados reais.
  - Tarefas
    - Configurar integração Storybook ↔ Figma (Design Token Sync ou Zeplin) e validar variáveis (`color`, `spacing`, `shadow`).
    - Criar checklist de QA visual por release (contraste, grids, typography) em `docs/ui/release-checklist.md`.
    - Rodar testes visuais automatizados (Chromatic) a cada PR que altera UI.
  - Critérios de aceite
    - Qualquer divergência > 2px ou cor fora da paleta oficial gera issue antes do merge.
    - Todas as páginas-chave possuem snapshot aceito no Chromatic.
* **Observabilidade da experiência**

  Objetivo: monitorar comportamento real dos usuários para validar hipóteses UX.

  Tarefas

  Registrar eventos essenciais (seleção de alertas, filtros aplicados, exportações, falhas de login) via analytics (PostHog/GA4) com nomenclatura padronizada.

  Configurar painéis de uso (funil de alerta → ação tomada, tempo médio até visualizar recomendação) e revisar quinzenalmente.

  Integrar LogRocket/Sentry para capturar sessão e reproduzir problemas de UI.


  Critérios de aceite

  - Eventos de analytics cobrem 100% dos fluxos críticos do roadmap.
  - Dashboard de UX é consultado nas cerimônias de feedback contínuo (seção 11).

---

## Técnicas Avançadas (Bônus)

1. **Visualização Geoespacial**

   - Adicionar mapa das torres (Mapbox ou Leaflet) com heatmap de SLA.
   - Clusters por região + tooltip com status de estoque.
2. **Dark Mode completo**

   - Toggle persistente (Context + localStorage).
   - Testar contraste mínimo WCAG 2.1 AA.
3. **Acessibilidade ampliada**

   - Navegação 100% teclado.
   - Suporte a leitores de tela (roles, aria-* completos).
4. **Internacionalização (i18n)**

   - Next i18n (pt-BR, en-US).
   - Arquitetura com `messages/pt.json`, `messages/en.json`.
5. **Plugins observabilidade**

   - Integração com `OpenTelemetry` para métricas custom.

---

## Entregáveis e Critérios de Aceite Gerais

- Definição de Done inclui: lint sem erros, testes da camada alterada, docs atualizados e deploy em ambiente de staging.
- Cada funcionalidade deve possuir história no Storybook (se UI) e teste automatizado.
- Integrações com backend devem tratar estados `loading`, `error`, `empty`.

---

## Próximos Passos Imediatos

1. Confirmar stack oficial (bibliotecas e padrões acima).
2. Criar backlog detalhado no Jira/Linear com tarefas por capítulo.
3. Iniciar sprint com foco na seção **1 – Configuração Inicial** e **2 – UI Core**.
4. Agendar design review com stakeholders para validar componentes base.

---

_Documento gerenciado pelo time Frontend Nova Corrente – atualizado Nov/2025._
