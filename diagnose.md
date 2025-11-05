# diagnose

### 3) Roteamento e Páginas

- App Router:
  - `src/app/main/page.tsx` permanece como shell principal com Sidebar/Header.
  - Criar páginas em `src/app/features/{temporal|climate|economic|5g|lead-time|sla|hierarchical|categorical|business}/page.tsx` consumindo `apiClient`.
  - Opcional: rotas para `clustering`, `models` e `prescriptive` fora de `Analytics` para deep-linking.

# Explicação do erro crítico

Pelo trecho, há um equívoco de arquitetura no App Router (Next.js 13+): você definiu `src/app/main/page.tsx` como “shell” (Sidebar/Header), mas em App Router o “shell” global deve ficar em `src/app/layout.tsx` (ou em um `layout.tsx` por segment). Um `page.tsx` é uma página de rota (`/main`), não um layout persistente.

## O que está errado

- **Shell no lugar errado**
  - `src/app/main/page.tsx` vira a rota `/main` e não envolve as outras páginas.
  - Sem `layout.tsx` no topo, cada página renderiza isolada; o Sidebar/Header não persistem entre rotas.

- **Estrutura de features sem layout comum**
  - Criar `src/app/features/{...}/page.tsx` sem um `layout.tsx` pai significa que cada feature renderiza sem o shell, ou com duplicação do shell em cada página.

- **Deep-linking “opcional” fora de Analytics**
  - Ao “espalhar” rotas como `clustering`, `models`, `prescriptive` fora do agrupamento, você pode quebrar a coerência de URL, breadcrumbs e layout compartilhado, além de introduzir 404 se os caminhos esperados não existirem.

- **Consumo do `apiClient`**
  - Se o `apiClient` for usado diretamente em Client Components quando deveria ser Server (ou vice-versa), podem ocorrer erros de hidratação, fetch duplicado e estado inconsistente.

## Sintomas que você verá

- **Layout não persistente**
  - Sidebar/Header somem ao navegar; re-montagem completa de página.
- **404/rotas quebradas**
  - Features em caminhos que não existem ou não correspondem ao esperado.
- **Erros/Hidratação**
  - Avisos do React/Next sobre hydration e “text content mismatch”.
- **SEO e Metadados inconsistentes**
  - `metadata` não aplicada de forma uniforme; títulos e OG tags variando indevidamente.
- **Navegação/UX ruins**
  - FOUC, flicker, perda de estado ao trocar de rota, pior tempo de transição.
- **Testes instáveis**
  - E2E e integração falhando por seletor/layout não persistente.

## Desdobramentos de não consertar

- **Impacto direto no usuário**
  - Páginas inacessíveis, links quebrados, experiência inconsistente.
- **Débito técnico alto**
  - Duplicação de UI por página, manutenção cara e frágil.
- **Perda de desempenho**
  - Re-renderizações completas e fetch redundante.
- **Problemas de SEO e analytics**
  - Metadados e estrutura de URL incorretos; perda de indexação e tracking.
- **Maior risco em produção**
  - Bugs intermitentes difíceis de reproduzir e corrigir.

# Como corrigir (objetivo)

- **Mover o shell para um layout**
  - Criar `src/app/layout.tsx` com Sidebar/Header e `children`.
  - Se quiser isolar, use um route group: `src/app/(main)/layout.tsx` e coloque features em `src/app/(main)/features/...`.

- **Organizar features sob um layout pai**
  - `src/app/(main)/features/{temporal|climate|...}/page.tsx`.
  - Opcional: `src/app/(main)/{clustering|models|prescriptive}/page.tsx` para deep-linking consistente sem perder o layout.

- **Padronizar `apiClient`**
  - Preferir Server Components para data fetching quando possível.
  - Se precisar de Client, envolva com provider/contexto e evite fetch duplicado.

- **Adicionar peças do App Router**
  - `loading.tsx`, `error.tsx` e `template.tsx` nos segmentos que precisarem UX melhor.
  - Definir `metadata` no layout para consistência SEO.

Exemplo minimalista de layout global:
```tsx
// src/app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>
        <Sidebar />
        <Header />
        <main>{children}</main>
      </body>
    </html>
  );
}
```

# Status

- Explicado o erro crítico (shell em `page.tsx` em vez de `layout.tsx`) e seus desdobramentos.
- Recomendadas ações curtas para corrigir estrutura de rotas e consumo do `apiClient`. Quer que eu revise a sua árvore `src/app/` atual e proponha um patch concreto?

---

### 4) Camada de Dados (API Client)

- Padronizar `apiClient` para utilizar caminhos relativos `/api/...` ao máximo, reduzindo dependência de `NEXT_PUBLIC_API_URL`.
- Adicionar adapters/DTOs quando necessário para mapear respostas do backend para estruturas usadas nos componentes (estabilidade contra mudanças de contrato).
- Estratégia de cache: manter TTL 30s, expor `clearCache()` e invalidar por ação do usuário quando aplicável.

# Explicação do erro crítico

O problema é a ausência de uma camada de dados padronizada e resiliente no `apiClient`. Três pontos-chave estão em risco:
- Dependência em `NEXT_PUBLIC_API_URL` em vez de usar caminhos relativos `/api/...`.
- Ausência de adapters/DTOs para estabilizar o contrato entre backend e UI.
- Estratégia de cache sem política clara de invalidação, TTL e limpeza.

Sem corrigir, você terá instabilidade entre ambientes, quebras por mudanças de contrato e bugs intermitentes por dados defasados.

## O que está errado

- **URL base exposta/instável**
  - Uso de `NEXT_PUBLIC_API_URL` em Client Components abre brecha para CORS, vazamento de origem e divergências entre dev/stage/prod.
  - Falta de proxy/rewrites e de uma rota `/api/...` interna (Next API Routes/edge/app routes) remove a oportunidade de centralizar headers, auth e retries.

- **Ausência de adapters/DTOs**
  - Componentes consomem respostas brutas do backend, acoplando a UI ao formato exato do payload.
  - Mudanças pequenas no backend (renomear campos, tipos opcionais) quebram diretamente a UI.

- **Cache ingovernável**
  - TTL indefinido ou mal aplicado causa dados obsoletos e “flicker” entre client/server.
  - Sem `clearCache()`/invalidadores, o usuário não consegue forçar refresh após ações (ex.: salvar, importar, treinar modelo).
  - Risco de “cache stampede” (picos de requisições) sem deduplicação.

## Sintomas que você verá

- **Inconsistência entre ambientes**
  - Em dev funciona (URL local), em prod falha (CORS, 404, headers ausentes).
- **Quebras silenciosas na UI**
  - Campos `undefined/null`, listas vazias, erros de render por alterações no backend.
- **Hidratação e duplicidade de fetch**
  - Mismatch de dados SSR/CSR, requisições em duplicidade no cliente.
- **Dados desatualizados**
  - Listas que não refletem ações recentes; usuário precisa recarregar a página.
- **Debug e testes frágeis**
  - Mocks difíceis, snapshots instáveis e E2E intermitentes.

## Desdobramentos de não consertar

- **Débito técnico acelerado**
  - Ajustes de contrato feitos “espalhados” em dezenas de componentes.
- **Risco operacional**
  - Incidentes em produção por CORS/timeout e dados obsoletos.
- **Segurança e compliance**
  - Exposição desnecessária de origens e tokens em client.
- **Custos de infraestrutura**
  - Mais tráfego por falta de cache efetivo e deduplicação.

# Como corrigir (objetivo)

- **Padronizar caminhos relativos**
  - Usar `/api/...` em toda a UI.
  - Implementar proxy em Next (App Router) via:
    - App Routes: `src/app/api/*/route.ts` como BFF para o backend.
    - Ou rewrites no `next.config.js` para encaminhar `/api` → backend.
  - Centralizar auth/headers/retries/timeouts no `apiClient`.

- **Introduzir adapters/DTOs**
  - Definir DTOs de entrada/saída no `apiClient`.
  - Mapear resposta do backend → modelo da UI em funções puras (`toUiModel`, `fromUiModel`).
  - Tipar (TS) e validar (Zod/Valibot) para detectar mudanças de contrato cedo.

- **Estratégia de cache coerente**
  - TTL padrão de 30s no `apiClient`.
  - Expor `clearCache()` e invalidadores por recurso/ação (ex.: `invalidate('forecasts')`).
  - Deduplicar requisições simultâneas (chave de cache por método+URL+params).
  - Em Server Components, usar `fetch` com `next: { revalidate: 30 }` (ou `no-store` quando necessário).
  - Em Client, alinhar com SWR/React Query: `staleTime: 30_000`, `refetchOnWindowFocus: false`, `mutation` invalidando chaves.

- **Política por tipo de endpoint**
  - GET idempotentes: cacheados 30s com dedupe.
  - POST/PUT/DELETE: `no-store`; invalidar chaves afetadas.
  - Endpoints críticos/tempo real: `no-store` + websockets/sse se aplicável.

- **Erros, observabilidade e testes**
  - Retries com jitter para 502/503/504.
  - Circuit breaker simples para hosts instáveis.
  - Logs/tracing no BFF (`/api`) para correlacionar falhas.
  - Mocks por camada (mocar `apiClient`, não o `fetch` cru) em testes.

## Boas práticas rápidas

- **Segurança**
  - Tokens só em server/BFF; nunca em `NEXT_PUBLIC_*`.
- **Tipos**
  - DTOs versionados (`v1`, `v2`) para migrações.
- **UX**
  - Expor métodos imperativos: `clearCache()`, `invalidate(keys)`, `prefetch(keys)`.
- **Performance**
  - Compactar/normalizar grandes coleções em adapters para reduzir uso de memória na UI.

# Status

- Erro crítico explicado: ausência de padronização do `apiClient`, de adapters/DTOs e de uma estratégia de cache/invalidação consistente.
- Sugerido um caminho de correção objetivo e prático.  
Quer que eu verifique seu `frontend/src` para propor um patch do `apiClient` com DTOs, cache 30s e `clearCache()`?

---