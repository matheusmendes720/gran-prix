'use client';

import { useState, useEffect } from 'react';
import { ForecastChart } from '@/components/charts/ForecastChart';
import { apiClient } from '@/lib/api';

interface Forecast {
  full_date: string;
  yhat: number;
  yhat_lower: number;
  yhat_upper: number;
  model_tag: string;
  horizon_days: number;
}

export default function ForecastsPage() {
  const [forecasts, setForecasts] = useState<Forecast[]>([]);
  const [loading, setLoading] = useState(true);
  const [itemId, setItemId] = useState<number | ''>('');
  const [siteId, setSiteId] = useState<number | ''>('');
  const [horizon, setHorizon] = useState<number | ''>(30);

  useEffect(() => {
    const fetchForecasts = async () => {
      try {
        const response = await apiClient.getForecasts({
          item_id: itemId ? Number(itemId) : undefined,
          site_id: siteId ? Number(siteId) : undefined,
          horizon: horizon ? Number(horizon) : undefined
        });
        setForecasts(response.data || []);
      } catch (error) {
        console.error('Error fetching forecasts:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchForecasts();
  }, [itemId, siteId, horizon]);

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="h-96 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Forecasts</h1>
      </div>

      {/* Filters */}
      <div className="mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Item ID</label>
          <input
            type="number"
            placeholder="All items"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            value={itemId}
            onChange={(e) => setItemId(e.target.value ? Number(e.target.value) : '')}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Site ID</label>
          <input
            type="number"
            placeholder="All sites"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            value={siteId}
            onChange={(e) => setSiteId(e.target.value ? Number(e.target.value) : '')}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Horizon (days)</label>
          <select
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            value={horizon}
            onChange={(e) => setHorizon(Number(e.target.value))}
          >
            <option value={7}>7 days</option>
            <option value={15}>15 days</option>
            <option value={30}>30 days</option>
            <option value={60}>60 days</option>
            <option value={90}>90 days</option>
          </select>
        </div>
      </div>

      {/* Forecast Chart */}
      <div className="bg-white p-4 shadow rounded-lg">
        <h2 className="text-lg font-medium mb-4">Forecast Chart</h2>
        <div className="h-96">
          <ForecastChart data={forecasts} />
        </div>
      </div>

      {/* Forecast Data Table */}
      <div className="mt-6 bg-white shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Forecast
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Lower Bound
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Upper Bound
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Model
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Horizon
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {forecasts.map((forecast, index) => (
              <tr key={index}>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {forecast.full_date}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {forecast.yhat.toFixed(2)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {forecast.yhat_lower.toFixed(2)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {forecast.yhat_upper.toFixed(2)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {forecast.model_tag}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {forecast.horizon_days} days
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}