/**
 * KPI Cards Component
 * Displays key performance indicators from analytics.kpis_daily
 */

'use client';

import React from 'react';
import { useKPIs } from '@/hooks/use-api';
import { format, subDays } from 'date-fns';

interface KPICardProps {
  title: string;
  value: string | number;
  trend?: number;
  unit?: string;
  description?: string;
  isLoading?: boolean;
}

function KPICard({ title, value, trend, unit, description, isLoading }: KPICardProps) {
  const trendColor = trend && trend > 0 ? 'text-green-600' : trend && trend < 0 ? 'text-red-600' : 'text-gray-500';
  const trendIcon = trend && trend > 0 ? '↑' : trend && trend < 0 ? '↓' : '–';

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
        <div className="h-8 bg-gray-200 rounded w-3/4 mb-2"></div>
        <div className="h-3 bg-gray-200 rounded w-1/3"></div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
      <h3 className="text-sm font-medium text-gray-600 mb-2">{title}</h3>
      <div className="flex items-baseline">
        <p className="text-3xl font-bold text-gray-900">
          {typeof value === 'number' ? value.toLocaleString('pt-BR', { maximumFractionDigits: 2 }) : value}
        </p>
        {unit && <span className="ml-2 text-sm text-gray-500">{unit}</span>}
      </div>
      {trend !== undefined && (
        <div className={`flex items-center mt-2 text-sm ${trendColor}`}>
          <span className="mr-1">{trendIcon}</span>
          <span>{Math.abs(trend).toFixed(1)}%</span>
          <span className="ml-1 text-gray-500">vs. anterior</span>
        </div>
      )}
      {description && (
        <p className="mt-2 text-xs text-gray-500">{description}</p>
      )}
    </div>
  );
}

export function KPIDashboard() {
  const today = new Date();
  const thirtyDaysAgo = subDays(today, 30);
  
  const { data, error, isLoading } = useKPIs({
    start_date: format(thirtyDaysAgo, 'yyyy-MM-dd'),
    end_date: format(today, 'yyyy-MM-dd'),
  });

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">Erro ao carregar KPIs: {error.message}</p>
      </div>
    );
  }

  // Get latest KPI data
  const latestKPI = data?.data?.[0];
  const previousKPI = data?.data?.[1];

  // Calculate trends
  const calculateTrend = (current?: number, previous?: number) => {
    if (!current || !previous || previous === 0) return undefined;
    return ((current - previous) / previous) * 100;
  };

  const demandTrend = calculateTrend(latestKPI?.total_demand, previousKPI?.total_demand);
  const stockoutTrend = calculateTrend(latestKPI?.stockout_rate, previousKPI?.stockout_rate);
  const mapeTrend = calculateTrend(latestKPI?.forecast_mape, previousKPI?.forecast_mape);
  const delayedTrend = calculateTrend(latestKPI?.delayed_orders_pct, previousKPI?.delayed_orders_pct);

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Indicadores de Performance</h2>
        <p className="text-gray-600 mt-1">
          Última atualização: {latestKPI ? format(new Date(latestKPI.full_date), 'dd/MM/yyyy') : '–'}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title="Demanda Total"
          value={latestKPI?.total_demand ?? 0}
          trend={demandTrend}
          unit="unidades"
          description="Volume total de demanda"
          isLoading={isLoading}
        />

        <KPICard
          title="Taxa de Ruptura"
          value={latestKPI?.stockout_rate ?? 0}
          trend={stockoutTrend}
          unit="%"
          description="Percentual de itens em falta"
          isLoading={isLoading}
        />

        <KPICard
          title="MAPE Forecast"
          value={latestKPI?.forecast_mape ?? 0}
          trend={mapeTrend}
          unit="%"
          description="Erro médio de previsão"
          isLoading={isLoading}
        />

        <KPICard
          title="Pedidos Atrasados"
          value={latestKPI?.delayed_orders_pct ?? 0}
          trend={delayedTrend}
          unit="%"
          description="Pedidos com atraso"
          isLoading={isLoading}
        />

        <KPICard
          title="Share Classe A"
          value={latestKPI?.abc_a_share ?? 0}
          unit="%"
          description="Participação itens classe A"
          isLoading={isLoading}
        />

        <KPICard
          title="Total de Registros"
          value={data?.metadata?.total_count ?? 0}
          description="Dias com dados disponíveis"
          isLoading={isLoading}
        />
      </div>

      {data && data.data && data.data.length > 0 && (
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            ✓ Sistema operando normalmente com {data.data.length} dias de dados KPI disponíveis
          </p>
        </div>
      )}
    </div>
  );
}

export default KPIDashboard;
