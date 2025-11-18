'use client';

import { useEffect, useMemo, useState } from 'react';
import { KPIDashboard } from '@/components/KPIDashboard';
import { MaterialsTable } from '@/components/MaterialsTable';
import { DemandChart, type ScenarioUpdatePayload } from '@/components/DemandChart';
import GeoHeatmap from '@/components/GeoHeatmap';
import PrescriptiveRecommendations from '@/components/PrescriptiveRecommendations';
import { useAlerts, useDashboardSummary } from '@/hooks/use-api';
import type { BffAlertItem, DashboardSummary } from '@/lib/api-client';
import type { Alert } from '@/types';
import { AlertLevel } from '@/types';
import { useOnlineStatus } from '@/hooks/use-online-status';
import { trackEvent } from '@/lib/analytics';

const DEMO_SUMMARY: DashboardSummary = {
  series_total: 2731,
  series_with_forecast: 15,
  critical_series: 13,
  generated_at: new Date().toISOString(),
};

const DEMO_ALERTS: Alert[] = [
  {
    item: 'Transceptor 5G',
    itemCode: 'itemTRANSCEPTOR_5G_site12',
    currentStock: 22,
    reorderPoint: 50,
    daysUntilStockout: 2,
    level: AlertLevel.CRITICAL,
    recommendation: 'Reposição imediata de 30 unidades no fornecedor principal.',
    stateId: 'RJ',
  },
  {
    item: 'Conector Óptico SC/APC',
    itemCode: 'itemABRASIVOS_BATERIA_9V_site22',
    currentStock: 0,
    reorderPoint: 7,
    daysUntilStockout: 0,
    level: AlertLevel.CRITICAL,
    recommendation: 'Emitir pedido emergencial para recompor estoque mínimo.',
    stateId: 'SP',
  },
  {
    item: 'Bateria de Lítio 48V',
    itemCode: 'itemBATERIA_LITIO_48V_site81',
    currentStock: 12,
    reorderPoint: 30,
    daysUntilStockout: 4,
    level: AlertLevel.WARNING,
    recommendation: 'Planejar transferência interna de 10 unidades do centro MG.',
    stateId: 'MG',
  },
];

const mapBffAlertToUi = (alert: BffAlertItem, scenario?: ScenarioUpdatePayload | null): Alert => {
  const level =
    alert.stock_status?.toLowerCase() === 'critical'
      ? AlertLevel.CRITICAL
      : alert.stock_status?.toLowerCase() === 'warning'
      ? AlertLevel.WARNING
      : AlertLevel.NORMAL;

  const stateId =
    alert.region ??
    (alert.site_id !== null && alert.site_id !== undefined
      ? `Site ${alert.site_id}`
      : alert.deposito ?? 'N/A');

  const suggestedGap = Math.max(
    0,
    Math.round((alert.reorder_point ?? 0) - (alert.current_stock ?? 0))
  );

  const scenarioMultiplier = scenario ? scenario.combinedMultiplier : 1;
  const currentStock = Math.round(alert.current_stock ?? 0);
  const baseReorderPoint = Math.round(alert.reorder_point ?? 0);
  const adjustedReorderPoint =
    scenario && alert.reorder_point != null
      ? Math.max(0, Math.round((alert.reorder_point ?? 0) * scenarioMultiplier))
      : undefined;
  const scenarioSuggestedOrder =
    adjustedReorderPoint !== undefined ? Math.max(0, adjustedReorderPoint - currentStock) : undefined;
  const scenarioMessage =
    scenario && (scenario.demandShift !== 0 || scenario.leadTimeDelta !== 0)
      ? `Cenário simulado (${scenario.demandShift >= 0 ? '+' : ''}${scenario.demandShift}% demanda, ${
          scenario.leadTimeDelta >= 0 ? '+' : ''
        }${scenario.leadTimeDelta} dia(s) lead time)${
          adjustedReorderPoint !== undefined
            ? ` sugere PP ${adjustedReorderPoint} e repor ${scenarioSuggestedOrder ?? 0} un.`
            : ''
        }`
      : undefined;

  const recommendation = `
Estoque atual de ${Math.round(alert.current_stock ?? 0)} vs PP ${
    Math.round(alert.reorder_point ?? 0)
  }. Recomenda-se repor ${suggestedGap} unidades e revisar lead time de ${
    alert.lead_time ?? 0
  } dias.`
    .trim()
    .replace(/\s+/g, ' ');

  return {
    item: alert.item_id ?? alert.series_key,
    itemCode: alert.series_key,
    currentStock: Math.round(alert.current_stock ?? 0),
    reorderPoint: Math.round(alert.reorder_point ?? 0),
    daysUntilStockout: Math.round(alert.days_to_rupture ?? 0),
    level,
    recommendation,
    stateId,
    scenarioMessage,
    scenarioSuggestedOrder,
    scenarioAdjustedReorderPoint: adjustedReorderPoint ?? baseReorderPoint,
  };
};

const getSeverityColor = (level: AlertLevel) => {
  switch (level) {
    case AlertLevel.CRITICAL:
      return 'bg-red-100 border-red-300 text-red-800';
    case AlertLevel.WARNING:
      return 'bg-yellow-100 border-yellow-300 text-yellow-800';
    default:
      return 'bg-blue-100 border-blue-300 text-blue-800';
  }
};

export default function StorytellingDashboardPage() {
  const [selectedSeries, setSelectedSeries] = useState<{
    series_key: string;
    item_id: string;
    familia?: string | null;
  } | null>(null);
  const [demoMode, setDemoMode] = useState(false);
  const [scenarioMetrics, setScenarioMetrics] = useState<ScenarioUpdatePayload | null>(null);
  const isOnline = useOnlineStatus();

  const {
    data: summaryData,
    error: summaryError,
    isLoading: summaryLoading,
  } = useDashboardSummary();
  const {
    data: alertsResponse,
    error: alertsError,
    isLoading: alertsLoading,
  } = useAlerts({ status: ['critical', 'warning'], limit: 8 });
  const shouldUseDemoSummary = demoMode || (!!summaryError && !summaryData);
  const summary = shouldUseDemoSummary ? DEMO_SUMMARY : summaryData ?? null;

  const shouldUseDemoAlerts = demoMode || !!alertsError;
  const mappedAlerts = useMemo(() => {
    if (shouldUseDemoAlerts) {
      return DEMO_ALERTS;
    }

    const items = alertsResponse?.items ?? [];
    return items.map((item) => mapBffAlertToUi(item, scenarioMetrics)).slice(0, 5);
  }, [shouldUseDemoAlerts, alertsResponse?.items, scenarioMetrics]);

  const summaryGeneratedAt = summary?.generated_at ? new Date(summary.generated_at) : null;

  const sectionStates = [
    { id: 'summary', label: 'KPIs', isDemo: shouldUseDemoSummary },
    { id: 'alerts', label: 'Alertas', isDemo: shouldUseDemoAlerts },
    { id: 'recs', label: 'Recomendações', isDemo: demoMode },
    { id: 'geo', label: 'Mapa Geo', isDemo: demoMode },
  ] as const;

  const demoSections = sectionStates.filter((section) => section.isDemo);
  const liveSections = sectionStates.filter((section) => !section.isDemo);

  useEffect(() => {
    if (!selectedSeries) {
      setScenarioMetrics(null);
    }
  }, [selectedSeries]);

  return (
    <div className="min-h-screen bg-gray-50 p-6 space-y-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Nova Corrente Analytics</h1>
          <p className="text-gray-600 mt-1">
            Dashboard de Previsão e Prescrição Alimentado pela Storytelling Pipeline
          </p>
        </div>
        <div className="flex items-center gap-3">
          {summaryGeneratedAt && !demoMode && (
            <span className="text-sm text-gray-500">
              Snapshot: {summaryGeneratedAt.toLocaleString('pt-BR')}
            </span>
          )}
          <button
            type="button"
            onClick={() =>
              setDemoMode((prev) => {
                const next = !prev;
                trackEvent('dashboard:demo_toggle', { active: next });
                return next;
              })
            }
            className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
              demoMode
                ? 'bg-brand-cyan text-brand-navy border border-brand-cyan'
                : 'bg-white text-brand-slate border border-brand-light-slate hover:border-brand-cyan/60'
            }`}
          >
            {demoMode ? 'Modo Demo Ativo' : 'Ativar Modo Demo'}
          </button>
        </div>
      </div>

      {!isOnline && (
        <div className="rounded-lg border border-yellow-300 bg-yellow-50 text-yellow-800 text-sm px-4 py-2">
          Conexão offline detectada. Exibindo dados a partir do último snapshot disponível.
        </div>
      )}

      {(demoMode || demoSections.length > 0) && (
        <div className="rounded-lg border border-brand-cyan/30 bg-brand-cyan/10 text-brand-navy text-sm px-4 py-3 flex flex-col gap-1 md:flex-row md:items-center md:justify-between">
          <div className="font-medium">
            {demoMode
              ? 'Exibindo instantâneo de demonstração.'
              : 'Dados em modo snapshot devido a indisponibilidade momentânea.'}
          </div>
          <div className="text-xs md:text-sm space-x-2">
            <span>
              <span className="font-semibold">Snapshot:</span>{' '}
              {demoSections.length > 0 ? demoSections.map((d) => d.label).join(', ') : '—'}
            </span>
            <span className="hidden md:inline-block text-brand-slate/70">|</span>
            <span className="font-semibold text-brand-slate">
              Ao vivo: {liveSections.length > 0 ? liveSections.map((d) => d.label).join(', ') : '—'}
            </span>
          </div>
        </div>
      )}

      {/* KPI Dashboard */}
      <KPIDashboard
        summary={summary}
        isLoading={summaryLoading && !summary}
        isFallback={shouldUseDemoSummary}
      />

      {selectedSeries && (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h2 className="text-xl font-bold text-gray-900">{selectedSeries.item_id}</h2>
              <p className="text-gray-600">Série: {selectedSeries.series_key}</p>
            </div>
            <button
              onClick={() => {
                if (selectedSeries) {
                  trackEvent('materials:close_details', { seriesKey: selectedSeries.series_key });
                }
                setSelectedSeries(null);
                setScenarioMetrics(null);
              }}
              className="text-gray-400 hover:text-gray-600"
              aria-label="Fechar detalhes do item selecionado"
            >
              ✕
            </button>
          </div>

          <DemandChart
            seriesKey={selectedSeries.series_key}
            familia={selectedSeries.familia ?? undefined}
            days={90}
            onScenarioUpdate={setScenarioMetrics}
          />
        </div>
      )}

      <MaterialsTable
        onSelectItem={(item) => {
          setScenarioMetrics(null);
          setSelectedSeries({
            series_key: item.series_key,
            item_id: item.item_id,
            familia: item.familia ?? undefined,
          });
          trackEvent('materials:select', {
            seriesKey: item.series_key,
            itemId: item.item_id,
          });
        }}
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-gray-900">Alertas Prescritivos</h2>
              <p className="text-gray-600 text-sm mt-1">
                Prioridade calculada via storytelling_prescriptions.parquet
              </p>
              {scenarioMetrics && (
                <p className="text-xs text-brand-cyan mt-2">
                  Cenário atual:{' '}
                  {`${scenarioMetrics.demandShift >= 0 ? '+' : ''}${scenarioMetrics.demandShift}% demanda`} •{' '}
                  {`${scenarioMetrics.leadTimeDelta >= 0 ? '+' : ''}${scenarioMetrics.leadTimeDelta} dia(s) lead time`} •{' '}
                  Buffer: {Math.round(scenarioMetrics.adjustedSafetyStock)} (
                  {scenarioMetrics.safetyStockDelta >= 0 ? '+' : ''}
                  {Math.round(scenarioMetrics.safetyStockDelta)} vs. base)
                </p>
              )}
            </div>
            {shouldUseDemoAlerts && (
              <span className="text-xs font-semibold uppercase text-orange-500 bg-orange-500/10 px-3 py-1 rounded-full">
                Snapshot
              </span>
            )}
            {alertsLoading && !shouldUseDemoAlerts && (
              <span className="text-xs text-gray-500">Atualizando…</span>
            )}
          </div>
          <div className="p-6">
            {mappedAlerts.length === 0 ? (
              <p className="text-gray-500 text-center py-6">
                Nenhum alerta crítico encontrado no snapshot atual.
              </p>
            ) : (
              <div className="space-y-3">
                {mappedAlerts.map((alert) => (
                  <div key={alert.itemCode} className={`p-4 rounded-lg border ${getSeverityColor(alert.level)}`}>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-xs font-semibold uppercase">{alert.level}</span>
                      <span className="text-xs opacity-70">{alert.stateId}</span>
                    </div>
                    <p className="font-semibold text-sm text-gray-900">{alert.item}</p>
                    <p className="text-xs text-gray-600 mt-1">
                      Estoque {alert.currentStock} • PP {alert.reorderPoint} •{' '}
                      {alert.daysUntilStockout > 0 ? `${alert.daysUntilStockout} dias até ruptura` : 'Ruptura iminente'}
                    </p>
                    <p className="text-sm text-gray-700 mt-2 leading-relaxed">{alert.recommendation}</p>
                    {alert.scenarioMessage && (
                      <p className="text-xs text-brand-cyan mt-2 border-t border-brand-cyan/30 pt-2">
                        {alert.scenarioMessage}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="relative">
          {demoMode && (
            <span className="absolute right-4 top-4 text-xs font-semibold uppercase text-orange-500 bg-orange-500/10 px-3 py-1 rounded-full z-10">
              Snapshot
            </span>
          )}
          <PrescriptiveRecommendations scenarioMetrics={scenarioMetrics} />
        </div>
      </div>

      <div className="space-y-2">
        {demoMode && (
          <div className="flex items-center justify-end">
            <span className="text-xs font-semibold uppercase text-orange-500 bg-orange-500/10 px-3 py-1 rounded-full">
              Snapshot
            </span>
          </div>
        )}
        <GeoHeatmap />
      </div>
    </div>
  );
}


