/**
 * Demand Time Series Chart
 * Visualizes demand data with forecast overlay using Recharts
 */

'use client';

import React, { useEffect, useMemo, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import Card from './Card';
import { useBffForecasts } from '@/hooks/use-api';
import { trackEvent } from '@/lib/analytics';

interface DemandChartProps {
  seriesKey: string;
  familia?: string;
  days?: number;
  onScenarioUpdate?: (payload: ScenarioUpdatePayload) => void;
  initialScenario?: {
    demandShift?: number;
    leadTimeDelta?: number;
  };
  /**
   * @deprecated Legacy prop retained for backward compatibility with older pages.
   */
  data?: unknown;
}

const SNAPSHOT_POINTS = Array.from({ length: 90 }, (_, index) => {
  const base = 60 + Math.sin(index / 6) * 18;
  const noise = Math.sin(index / 3) * 6;
  const actual = Math.max(20, base + noise);
  const forecast = actual * (0.95 + (Math.sin(index / 8) + 1) * 0.025);
  const date = new Date();
  date.setDate(date.getDate() - (89 - index));
  return {
    ds: date.toISOString().split('T')[0],
    actual_qty: Number(actual.toFixed(1)),
    forecast_qty: Number(forecast.toFixed(1)),
    lower: Number((forecast * 0.88).toFixed(1)),
    upper: Number((forecast * 1.12).toFixed(1)),
  } as const;
});

export const BASE_LEAD_TIME_DAYS = 7;
export const LEAD_TIME_SENSITIVITY = 0.03;

export interface ScenarioUpdatePayload {
  demandShift: number;
  leadTimeDelta: number;
  demandMultiplier: number;
  leadTimeMultiplier: number;
  combinedMultiplier: number;
  scenarioAvgForecast: number;
  baselineAvgDemand: number;
  baselineSafetyStock: number;
  adjustedSafetyStock: number;
  safetyStockDelta: number;
  peakDemand: number;
  forecastCount: number;
}

export function DemandChart({ seriesKey, familia, days = 90, onScenarioUpdate, initialScenario }: DemandChartProps) {
  const [demandShift, setDemandShift] = useState(initialScenario?.demandShift ?? 0);
  const [leadTimeDelta, setLeadTimeDelta] = useState(initialScenario?.leadTimeDelta ?? 0);
  const { data, error, isLoading } = useBffForecasts({
    familia,
    limit: 200,
  });

  const rawPoints = data?.series.find((series) => series.series_key === seriesKey)?.points ?? [];
  const usingFallback = Boolean(error) || rawPoints.length === 0;

  const effectivePoints = useMemo(() => {
    if (usingFallback) {
      return SNAPSHOT_POINTS.slice(-days);
    }
    return rawPoints.slice(-days);
  }, [rawPoints, usingFallback, days]);

  interface ChartDataPoint {
    date: string;
    ds: string;
    actualDemand?: number;
    forecast?: number;
    scenarioForecast?: number;
    lowerBound?: number;
    upperBound?: number;
  }

  const demandMultiplier = 1 + demandShift / 100;
  const leadTimeMultiplier = 1 + leadTimeDelta * LEAD_TIME_SENSITIVITY;

  const chartData: ChartDataPoint[] = useMemo(() => {
    return effectivePoints.map((point) => {
      const sourceDate = typeof point.ds === 'string' ? new Date(point.ds) : new Date(point.ds ?? Date.now());
      const baselineForecast = point.forecast_qty ?? undefined;
      const scenarioForecast =
        baselineForecast !== undefined
          ? Math.max(baselineForecast * demandMultiplier * leadTimeMultiplier, 0)
          : undefined;

      return {
        date: sourceDate.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' }),
        ds:
          typeof point.ds === 'string'
            ? point.ds
            : point.ds instanceof Date
            ? point.ds.toISOString()
            : sourceDate.toISOString(),
        actualDemand: point.actual_qty ?? undefined,
        forecast: baselineForecast,
        scenarioForecast,
        lowerBound: point.lower ?? undefined,
        upperBound: point.upper ?? undefined,
      };
    });
  }, [effectivePoints, demandMultiplier, leadTimeMultiplier]);

  const maxValue = useMemo(
    () =>
      Math.max(
        ...chartData.map((d) =>
          Math.max(
            d.actualDemand ?? 0,
            d.forecast ?? 0,
            d.scenarioForecast ?? 0,
            d.upperBound ?? 0,
            0
          )
        )
      ),
    [chartData]
  );

  const baselineAvgDemand = useMemo(() => {
    const actuals = chartData.map((d) => d.actualDemand).filter((value) => value !== undefined);
    if (actuals.length === 0) return 0;
    return actuals.reduce((sum, value) => sum + (value ?? 0), 0) / actuals.length;
  }, [chartData]);

  const scenarioAvgForecast = useMemo(() => {
    const scenarioValues = chartData.map((d) => d.scenarioForecast).filter((value) => value !== undefined);
    if (scenarioValues.length === 0) return 0;
    return scenarioValues.reduce((sum, value) => sum + (value ?? 0), 0) / scenarioValues.length;
  }, [chartData]);

  const baselineSafetyStock = Math.max(baselineAvgDemand * BASE_LEAD_TIME_DAYS, 0);
  const adjustedSafetyStock = Math.max(baselineAvgDemand * (BASE_LEAD_TIME_DAYS + leadTimeDelta), 0);
  const safetyStockDelta = adjustedSafetyStock - baselineSafetyStock;
  const peakDemand = useMemo(() => {
    if (chartData.length === 0) return 0;
    return Math.max(...chartData.map((d) => d.actualDemand ?? 0));
  }, [chartData]);
  const forecastCount = useMemo(() => chartData.filter((d) => d.forecast !== undefined).length, [chartData]);

  useEffect(() => {
    if (!onScenarioUpdate || chartData.length === 0) {
      return;
    }

    onScenarioUpdate({
      demandShift,
      leadTimeDelta,
      demandMultiplier,
      leadTimeMultiplier,
      combinedMultiplier: demandMultiplier * leadTimeMultiplier,
      scenarioAvgForecast,
      baselineAvgDemand,
      baselineSafetyStock,
      adjustedSafetyStock,
      safetyStockDelta,
      peakDemand,
      forecastCount,
    });
  }, [
    onScenarioUpdate,
    chartData.length,
    demandShift,
    leadTimeDelta,
    demandMultiplier,
    leadTimeMultiplier,
    scenarioAvgForecast,
    baselineAvgDemand,
    baselineSafetyStock,
    adjustedSafetyStock,
    safetyStockDelta,
    peakDemand,
    forecastCount,
  ]);

  const hasData = chartData.length > 0;

  return (
    <Card className="bg-gradient-to-br from-brand-deep-blue/70 via-brand-navy/80 to-brand-deep-blue/60 border border-brand-light-navy shadow-2xl shadow-brand-deep-blue/40">
      <div className="flex flex-col gap-4">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h3 className="text-lg font-semibold text-brand-lightest-slate">Simulador de Cenários Storytelling</h3>
            <p className="text-sm text-brand-slate">
              Ajuste demanda e lead time para avaliar impacto em PP, estoque de segurança e recomendações.
            </p>
          </div>
          <div className="text-xs text-brand-slate/80">
            Lead time base: {BASE_LEAD_TIME_DAYS} dia{BASE_LEAD_TIME_DAYS === 1 ? '' : 's'} • Sensibilidade:{' '}
            {Math.round(LEAD_TIME_SENSITIVITY * 100)}% por dia
          </div>
        </div>

        {usingFallback && (
          <div className="rounded-lg border border-amber-500/40 bg-amber-500/10 px-4 py-3 text-sm text-amber-200 shadow-inner">
            <p>
              Modo snapshot ativo. Dados demonstrativos carregados localmente porque a API de previsão não respondeu.
            </p>
            {error && <p className="mt-1 text-amber-100/80 text-xs">Detalhes: {error.message}</p>}
          </div>
        )}

        <div className="grid gap-4 md:grid-cols-2" role="group" aria-label="Controles de cenário simulados">
          <div>
            <label htmlFor="demand-shift" className="block text-xs font-semibold text-brand-slate mb-2">
              Variação de demanda ({demandShift >= 0 ? '+' : ''}
              {demandShift}%)
            </label>
            <input
              id="demand-shift"
              type="range"
              min={-30}
              max={50}
              step={5}
              value={demandShift}
              onChange={(event) => {
                const value = Number(event.target.value);
                setDemandShift(value);
                trackEvent('scenario:demand_shift', { seriesKey, value });
              }}
              className="w-full accent-brand-cyan"
              aria-valuemin={-30}
              aria-valuemax={50}
              aria-valuenow={demandShift}
              aria-valuetext={`${demandShift}%`}
            />
            <p className="text-xs text-brand-slate mt-1">Explore quedas (-30%) ou aumentos (+50%) de demanda.</p>
          </div>

          <div>
            <label htmlFor="leadtime-shift" className="block text-xs font-semibold text-brand-slate mb-2">
              Ajuste de lead time ({leadTimeDelta >= 0 ? '+' : ''}
              {leadTimeDelta} dia{Math.abs(leadTimeDelta) === 1 ? '' : 's'})
            </label>
            <input
              id="leadtime-shift"
              type="range"
              min={-5}
              max={10}
              step={1}
              value={leadTimeDelta}
              onChange={(event) => {
                const value = Number(event.target.value);
                setLeadTimeDelta(value);
                trackEvent('scenario:leadtime_shift', { seriesKey, value });
              }}
              className="w-full accent-amber-400"
              aria-valuemin={-5}
              aria-valuemax={10}
              aria-valuenow={leadTimeDelta}
              aria-valuetext={`${leadTimeDelta} dias`}
            />
            <p className="text-xs text-brand-slate mt-1">
              Adiciona {Math.round(LEAD_TIME_SENSITIVITY * 100)}% de demanda estimada para cada dia extra de lead time.
            </p>
          </div>
        </div>

        <div className="bg-brand-navy/40 rounded-2xl border border-brand-light-navy/40 p-4">
          {isLoading && !hasData ? (
            <div className="h-72 flex items-center justify-center text-brand-slate">Carregando série…</div>
          ) : hasData ? (
            <ResponsiveContainer width="100%" height={360}>
              <LineChart data={chartData} margin={{ top: 5, right: 30, left: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2a44" />
                <XAxis dataKey="date" stroke="#94a3b8" style={{ fontSize: '12px' }} aria-hidden="true" />
                <YAxis
                  stroke="#94a3b8"
                  style={{ fontSize: '12px' }}
                  domain={[0, maxValue ? maxValue * 1.2 : 10]}
                  aria-hidden="true"
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    border: '1px solid #1e293b',
                    borderRadius: '8px',
                    color: '#e2e8f0',
                    padding: '12px',
                  }}
                  labelStyle={{ fontWeight: 'bold', marginBottom: '8px', color: '#38bdf8' }}
                />
                <Legend wrapperStyle={{ paddingTop: 20, color: '#e2e8f0' }} iconType="line" />

                {chartData.some((d) => d.lowerBound !== undefined) && (
                  <>
                    <Line
                      type="monotone"
                      dataKey="lowerBound"
                      stroke="#38bdf8"
                      strokeWidth={1}
                      strokeDasharray="3 3"
                      dot={false}
                      name="Limite Inferior"
                      opacity={0.3}
                    />
                    <Line
                      type="monotone"
                      dataKey="upperBound"
                      stroke="#38bdf8"
                      strokeWidth={1}
                      strokeDasharray="3 3"
                      dot={false}
                      name="Limite Superior"
                      opacity={0.3}
                    />
                  </>
                )}

                <Line
                  type="monotone"
                  dataKey="actualDemand"
                  stroke="#38bdf8"
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                  name="Demanda Real"
                  activeDot={{ r: 5 }}
                />

                {chartData.some((d) => d.forecast !== undefined) && (
                  <Line
                    type="monotone"
                    dataKey="forecast"
                    stroke="#facc15"
                    strokeWidth={2}
                    strokeDasharray="6 4"
                    dot={{ r: 3 }}
                    name="Previsão"
                  />
                )}
                {chartData.some((d) => d.scenarioForecast !== undefined) && (
                  <Line
                    type="monotone"
                    dataKey="scenarioForecast"
                    stroke="#a855f7"
                    strokeWidth={2}
                    strokeDasharray="4 4"
                    dot={false}
                    name="Cenário Simulado"
                  />
                )}
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-72 flex items-center justify-center text-brand-slate">Nenhum dado disponível para esta série.</div>
          )}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div className="bg-brand-navy/50 rounded-lg border border-brand-light-navy/40 p-3">
            <p className="text-brand-slate text-xs">Total de Registros</p>
            <p className="text-lg font-semibold text-brand-lightest-slate" aria-label={`Total de ${chartData.length} registros`}>
              {chartData.length}
            </p>
          </div>
          <div className="bg-brand-navy/50 rounded-lg border border-brand-light-navy/40 p-3">
            <p className="text-brand-slate text-xs">Demanda Média</p>
            <p className="text-lg font-semibold text-brand-lightest-slate" aria-label={`Demanda média de ${baselineAvgDemand.toFixed(1)}`}>
              {chartData.length > 0 ? baselineAvgDemand.toFixed(1) : '–'}
            </p>
          </div>
          <div className="bg-brand-navy/50 rounded-lg border border-brand-light-navy/40 p-3">
            <p className="text-brand-slate text-xs">Pico de Demanda</p>
            <p className="text-lg font-semibold text-brand-lightest-slate" aria-label={`Pico de demanda de ${chartData.length > 0 ? peakDemand.toFixed(0) : 'não disponível'}`}>
              {chartData.length > 0 ? peakDemand.toFixed(0) : '–'}
            </p>
          </div>
          <div className="bg-brand-navy/50 rounded-lg border border-brand-light-navy/40 p-3">
            <p className="text-brand-slate text-xs">Previsões Disponíveis</p>
            <p className="text-lg font-semibold text-brand-lightest-slate" aria-label={`${forecastCount} previsões disponíveis`}>
              {forecastCount}
            </p>
          </div>
          <div className="bg-purple-900/30 rounded-lg border border-purple-500/20 p-3 md:col-span-1 col-span-2">
            <p className="text-purple-200 text-xs font-semibold">Cenário Simulado</p>
            <p className="text-lg font-semibold text-purple-100">
              {scenarioAvgForecast > 0 ? scenarioAvgForecast.toFixed(1) : '–'}
            </p>
            <p className="text-xs text-purple-200/70">Média prevista após ajustes</p>
          </div>
        </div>

        <div className="bg-brand-navy/60 border border-brand-light-navy/50 text-brand-lightest-slate rounded-xl p-4 text-sm leading-relaxed">
          <p>
            Estoque de segurança recomendado: <strong>{Math.round(adjustedSafetyStock)}</strong> unidades ({
              safetyStockDelta >= 0 ? '+' : ''
            }
            {Math.round(safetyStockDelta)} vs. base de {Math.round(baselineSafetyStock)}).{' '}
            {leadTimeDelta > 0
              ? `Atrasos de ${leadTimeDelta} dia${leadTimeDelta === 1 ? '' : 's'} exigem antecipar pedidos para evitar ruptura.`
              : leadTimeDelta < 0
              ? `Antecipar em ${Math.abs(leadTimeDelta)} dia${Math.abs(leadTimeDelta) === 1 ? '' : 's'} libera capital sem comprometer o atendimento.`
              : 'Lead time inalterado mantém o buffer alinhado ao histórico.'}{' '}
            Ajuste de demanda aplicado: <strong>{demandShift}%</strong>.
          </p>
        </div>
      </div>
    </Card>
  );
}

export default DemandChart;
