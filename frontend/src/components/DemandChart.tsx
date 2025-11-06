/**
 * Demand Time Series Chart
 * Visualizes demand data with forecast overlay using Recharts
 */

'use client';

import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useDemandTimeseries, useForecasts } from '@/hooks/use-api';
import { format, subDays } from 'date-fns';

interface DemandChartProps {
  itemId: number;
  siteId?: number;
  days?: number;
}

export function DemandChart({ itemId, siteId, days = 90 }: DemandChartProps) {
  const today = new Date();
  const startDate = subDays(today, days);

  const { data: demandData, error: demandError, isLoading: demandLoading } = useDemandTimeseries({
    item_id: itemId,
    start_date: format(startDate, 'yyyy-MM-dd'),
    end_date: format(today, 'yyyy-MM-dd'),
  });

  const { data: forecastData, error: forecastError, isLoading: forecastLoading } = useForecasts(
    siteId ? { item_id: itemId, site_id: siteId } : { item_id: itemId }
  );

  if (demandError || forecastError) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">
          Erro ao carregar dados: {demandError?.message || forecastError?.message}
        </p>
      </div>
    );
  }

  if (demandLoading || forecastLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  // Combine demand and forecast data
  const demand = demandData?.data ?? [];
  const forecasts = forecastData?.data ?? [];

  // Create a map of dates to data points
  interface ChartDataPoint {
    date: string;
    fullDate: string;
    actualDemand: number;
    forecast?: number;
    lowerBound?: number;
    upperBound?: number;
  }

  const chartData: ChartDataPoint[] = demand.map((d) => ({
    date: format(new Date(d.full_date), 'dd/MM'),
    fullDate: d.full_date,
    actualDemand: d.quantity,
    forecast: forecasts.find((f) => f.forecast_date === d.full_date)?.predicted_demand,
    lowerBound: forecasts.find((f) => f.forecast_date === d.full_date)?.confidence_lower,
    upperBound: forecasts.find((f) => f.forecast_date === d.full_date)?.confidence_upper,
  }));

  const maxValue = Math.max(
    ...chartData.map((d) => Math.max(d.actualDemand, d.forecast || 0, d.upperBound || 0))
  );

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Série Temporal de Demanda (Últimos {days} dias)
      </h3>

      {chartData.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          Nenhum dado de demanda disponível para este item
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="date" 
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
            />
            <YAxis 
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
              domain={[0, maxValue * 1.1]}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'white', 
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                padding: '12px'
              }}
              labelStyle={{ fontWeight: 'bold', marginBottom: '8px' }}
            />
            <Legend 
              wrapperStyle={{ paddingTop: '20px' }}
              iconType="line"
            />
            
            {/* Confidence interval */}
            {chartData.some((d) => d.lowerBound !== undefined) && (
              <>
                <Line
                  type="monotone"
                  dataKey="lowerBound"
                  stroke="#93c5fd"
                  strokeWidth={1}
                  strokeDasharray="3 3"
                  dot={false}
                  name="Limite Inferior"
                  opacity={0.5}
                />
                <Line
                  type="monotone"
                  dataKey="upperBound"
                  stroke="#93c5fd"
                  strokeWidth={1}
                  strokeDasharray="3 3"
                  dot={false}
                  name="Limite Superior"
                  opacity={0.5}
                />
              </>
            )}
            
            {/* Actual demand */}
            <Line
              type="monotone"
              dataKey="actualDemand"
              stroke="#2563eb"
              strokeWidth={2}
              dot={{ r: 3 }}
              name="Demanda Real"
              activeDot={{ r: 5 }}
            />
            
            {/* Forecast */}
            {chartData.some((d) => d.forecast !== undefined) && (
              <Line
                type="monotone"
                dataKey="forecast"
                stroke="#f59e0b"
                strokeWidth={2}
                strokeDasharray="5 5"
                dot={{ r: 3 }}
                name="Previsão"
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      )}

      <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
        <div className="bg-gray-50 rounded p-3">
          <p className="text-gray-600 text-xs">Total de Registros</p>
          <p className="text-lg font-semibold text-gray-900">{chartData.length}</p>
        </div>
        <div className="bg-gray-50 rounded p-3">
          <p className="text-gray-600 text-xs">Demanda Média</p>
          <p className="text-lg font-semibold text-gray-900">
            {chartData.length > 0
              ? (chartData.reduce((sum, d) => sum + d.actualDemand, 0) / chartData.length).toFixed(1)
              : '–'}
          </p>
        </div>
        <div className="bg-gray-50 rounded p-3">
          <p className="text-gray-600 text-xs">Pico de Demanda</p>
          <p className="text-lg font-semibold text-gray-900">
            {chartData.length > 0 ? Math.max(...chartData.map((d) => d.actualDemand)).toFixed(0) : '–'}
          </p>
        </div>
        <div className="bg-gray-50 rounded p-3">
          <p className="text-gray-600 text-xs">Previsões Disponíveis</p>
          <p className="text-lg font-semibold text-gray-900">
            {chartData.filter((d) => d.forecast !== undefined).length}
          </p>
        </div>
      </div>
    </div>
  );
}

export default DemandChart;
