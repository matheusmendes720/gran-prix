# Demo Snapshot Mode

## Objetivo
Fornecer modo "snapshot" para apresentações comerciais, exibindo banner global quando dados mock estão ativos.

## Implementação
- `frontend/src/app/page.tsx` (storytelling) e `frontend/src/app/main/page.tsx` (legacy) exibem banner destacando seções em modo snapshot vs. live.
- `frontend/src/components/Dashboard.tsx` usa constantes `FALLBACK_ALERTS`, `FALLBACK_SERIES` quando BFF falha.
- `frontend/src/lib/analytics.ts` registra eventos `demo_toggle` e `material_select`.

## Lacunas
- Banner global depende de estado do storytelling page; na página legacy, fallback é silencioso (apenas alerta âmbar no DemandChart).
- Não há botão explícito para alternar demo vs. live na home legacy.
- Faltam testes garantindo que snapshot cobre todas as seções (KPIs, alertas, recomendações).

## Rollback Strategy
- Reverter `frontend/src/app/main/page.tsx` para versão pré-banner.
- Remover sinais de snapshot do Dashboard restaurando arrays mock originais.
- Desabilitar tracking de analytics (evitar eventos órfãos).

## Melhorias Futuras
- Criar serviço central (`useDataMode`) para expor `isSnapshot` a toda aplicação.
- Persistir escolha do usuário em `localStorage`.
- Documentar dataset snapshot oficial com versão e checksum.
