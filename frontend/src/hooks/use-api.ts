/**
 * Custom SWR hooks for Nova Corrente API
 * Provides real-time data fetching with automatic revalidation
 */

import useSWR from 'swr';
import { api } from '@/lib/api-client';
import type { Item, KPI, Forecast, Recommendation, Alert } from '@/lib/api-client';

interface UseItemsOptions {
  limit?: number;
  offset?: number;
  family?: string;
  abc_class?: 'A' | 'B' | 'C';
}

interface UseKPIsOptions {
  start_date?: string;
  end_date?: string;
}

interface UseDemandOptions {
  item_id: number;
  start_date?: string;
  end_date?: string;
}

interface UseInventoryOptions {
  item_id: number;
  start_date?: string;
  end_date?: string;
}

interface UseForecastsOptions {
  item_id: number;
  site_id?: number;
  horizon_days?: number;
}

interface UseRecommendationsOptions {
  status?: 'PENDING' | 'REVIEWED' | 'APPLIED' | 'REJECTED';
  priority?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  limit?: number;
}

interface UseAlertsOptions {
  status?: 'NEW' | 'ACKNOWLEDGED' | 'RESOLVED';
  severity?: 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  limit?: number;
}

// Health check hook
export function useHealth() {
  return useSWR('/health', () => api.health(), {
    refreshInterval: 30000, // Refresh every 30 seconds
  });
}

// Items hooks
export function useItems(options?: UseItemsOptions) {
  const key = options ? ['/api/v1/items', options] : '/api/v1/items';
  
  return useSWR(key, () => api.getItems(options), {
    revalidateOnFocus: false,
    dedupingInterval: 60000, // 1 minute
  });
}

export function useItem(itemId: number | null) {
  return useSWR(
    itemId ? `/api/v1/items/${itemId}` : null,
    () => (itemId ? api.getItem(itemId) : null),
    {
      revalidateOnFocus: false,
      dedupingInterval: 60000,
    }
  );
}

// KPIs hook
export function useKPIs(options?: UseKPIsOptions) {
  const key = options ? ['/api/v1/analytics/kpis', options] : '/api/v1/analytics/kpis';
  
  return useSWR(key, () => api.getKPIs(options), {
    refreshInterval: 300000, // Refresh every 5 minutes
    revalidateOnFocus: false,
  });
}

// Demand timeseries hook
export function useDemandTimeseries(options: UseDemandOptions | null) {
  const key = options ? ['/api/v1/demand/timeseries', options] : null;
  
  return useSWR(
    key,
    () => (options ? api.getDemandTimeseries(options) : null),
    {
      revalidateOnFocus: false,
      dedupingInterval: 60000,
    }
  );
}

// Inventory timeseries hook
export function useInventoryTimeseries(options: UseInventoryOptions | null) {
  const key = options ? ['/api/v1/inventory/timeseries', options] : null;
  
  return useSWR(
    key,
    () => (options ? api.getInventoryTimeseries(options) : null),
    {
      revalidateOnFocus: false,
      dedupingInterval: 60000,
    }
  );
}

// Forecasts hook
export function useForecasts(options: UseForecastsOptions | null) {
  const key = options ? ['/api/v1/forecasts', options] : null;
  
  return useSWR(
    key,
    () => (options ? api.getForecasts(options) : null),
    {
      revalidateOnFocus: false,
      dedupingInterval: 300000, // 5 minutes
    }
  );
}

// Recommendations hook
export function useRecommendations(options?: UseRecommendationsOptions) {
  const key = options ? ['/api/v1/recommendations', options] : '/api/v1/recommendations';
  
  return useSWR(key, () => api.getRecommendations(options), {
    refreshInterval: 60000, // Refresh every minute
  });
}

// Alerts hook
export function useAlerts(options?: UseAlertsOptions) {
  const key = options ? ['/api/v1/alerts', options] : '/api/v1/alerts';
  
  return useSWR(key, () => api.getAlerts(options), {
    refreshInterval: 30000, // Refresh every 30 seconds for alerts
  });
}

// Features hook
export function useFeatures(itemId: number | null, featureDate?: string) {
  const key = itemId ? ['/api/v1/features', { item_id: itemId, feature_date: featureDate }] : null;
  
  return useSWR(
    key,
    () => (itemId ? api.getFeatures({ item_id: itemId, feature_date: featureDate }) : null),
    {
      revalidateOnFocus: false,
      dedupingInterval: 300000,
    }
  );
}

// Export types for convenience
export type {
  UseItemsOptions,
  UseKPIsOptions,
  UseDemandOptions,
  UseInventoryOptions,
  UseForecastsOptions,
  UseRecommendationsOptions,
  UseAlertsOptions,
};
