'use client';

import React from 'react';
import type { DashboardSummary } from '@/lib/api-client';

interface KPICardProps {
  title: string;
  value: string;
  description: string;
  accent?: string;
  isLoading?: boolean;
}

const KPI_SKELETON = (
  <div className="bg-white rounded-lg shadow p-6 animate-pulse">
    <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
    <div className="h-8 bg-gray-200 rounded w-3/4 mb-2"></div>
    <div className="h-3 bg-gray-200 rounded w-1/3"></div>
  </div>
);

function KPICard({ title, value, description, accent, isLoading }: KPICardProps) {
  if (isLoading) {
    return KPI_SKELETON;
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow border border-transparent hover:border-brand-cyan/40">
      <h3 className="text-sm font-semibold text-brand-slate mb-2">{title}</h3>
      <p className="text-3xl font-bold text-gray-900">{value}</p>
      <p className="mt-2 text-xs text-brand-slate/80">{description}</p>
      {accent && (
        <p className="mt-3 text-xs font-semibold uppercase text-brand-cyan tracking-widest">
          {accent}
        </p>
      )}
    </div>
  );
}

interface KPIDashboardProps {
  summary?: DashboardSummary | null;
  isLoading?: boolean;
  isFallback?: boolean;
}

export function KPIDashboard({ summary, isLoading, isFallback }: KPIDashboardProps) {
  const totalSeries = summary?.series_total ?? 0;
  const seriesWithForecast = summary?.series_with_forecast ?? 0;
  const criticalSeries = summary?.critical_series ?? 0;

  const coveragePct =
    totalSeries > 0 ? ((seriesWithForecast / totalSeries) * 100).toFixed(1) : '0.0';

  const criticalShare =
    totalSeries > 0 ? ((criticalSeries / totalSeries) * 100).toFixed(1) : '0.0';

  const generatedAt = summary?.generated_at
    ? new Date(summary.generated_at)
    : undefined;

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-2">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Indicadores de Storytelling</h2>
          <p className="text-gray-600 mt-1">
            {generatedAt
              ? `Atualizado em ${generatedAt.toLocaleString('pt-BR')}`
              : 'Atualização pendente'}
          </p>
        </div>
        {isFallback && (
          <span className="text-xs font-semibold uppercase text-orange-500 bg-orange-500/10 px-3 py-1 rounded-full">
            Demo Mode
          </span>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title="Séries Monitoradas"
          value={totalSeries.toLocaleString('pt-BR')}
          description="Total de combinações item/site acompanhadas pela pipeline."
          isLoading={isLoading && !summary}
        />
        <KPICard
          title="Séries com Previsão"
          value={seriesWithForecast.toLocaleString('pt-BR')}
          description="Séries com modelos gerados no último ciclo."
          accent={`${coveragePct}% cobertura`}
          isLoading={isLoading && !summary}
        />
        <KPICard
          title="Séries Críticas"
          value={criticalSeries.toLocaleString('pt-BR')}
          description="Séries com risco de ruptura segundo prescrições."
          accent={`${criticalShare}% do total`}
          isLoading={isLoading && !summary}
        />
        <KPICard
          title="Latência do Snapshot"
          value={
            generatedAt
              ? `${Math.max(
                  0,
                  Math.round((Date.now() - generatedAt.getTime()) / (1000 * 60))
                )} min`
              : '—'
          }
          description="Tempo desde a última geração dos artefatos."
          isLoading={isLoading && !summary}
        />
      </div>
    </div>
  );
}

export default KPIDashboard;
