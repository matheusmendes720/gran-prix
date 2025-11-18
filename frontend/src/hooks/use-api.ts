/**
 * Custom SWR hooks for Nova Corrente API
 * Provides real-time data fetching with automatic revalidation
 */

import useSWR from 'swr';
import { api } from '@/lib/api-client';
import type {
  Item,
  KPI,
  Recommendation,
  DashboardSummary,
  AlertsResponse,
  ForecastResponse,
  RecommendationResponse,
  GeoSummaryResponse,
  ClimateFeatureResponse,
} from '@/lib/api-client';

const MAX_RETRY_COUNT = 3;

const shouldRetryOnError = (error: any) => {
  if (!error) {
    return false;
  }
  if (typeof navigator !== 'undefined' && !navigator.onLine) {
    return false;
  }
  if (error.status && error.status >= 400 && error.status < 500 && error.status !== 408) {
    return false;
  }
  return true;
};

const swrRetry = (
  error: any,
  _: string,
  __: any,
  revalidate: (opts?: { retryCount?: number }) => void,
  opts: { retryCount: number }
) => {
  if (!shouldRetryOnError(error)) {
    return;
  }
  if (opts.retryCount >= MAX_RETRY_COUNT) {
    return;
  }
  const delay = Math.min(30000, 1000 * 2 ** opts.retryCount);
  setTimeout(() => revalidate({ retryCount: opts.retryCount + 1 }), delay);
};

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

interface UseInventoryOptions {
  item_id: number;
  start_date?: string;
  end_date?: string;
}

interface UseRecommendationsOptions {
  familia?: string;
  stock_status?: string;
  limit?: number;
}

interface UseAlertsOptions {
  status?: string[];
  limit?: number;
}

// Dashboard summary hook
export function useDashboardSummary() {
  return useSWR<DashboardSummary>('/bff/dashboard/summary', () => api.getDashboardSummary(), {
    refreshInterval: 300000,
    revalidateOnFocus: false,
    shouldRetryOnError,
    onErrorRetry: swrRetry,
  });
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


// Recommendations hook
export function useRecommendations(options?: UseRecommendationsOptions) {
  const key = options ? ['/bff/recommendations', options] : '/bff/recommendations';

  return useSWR<RecommendationResponse>(
    key,
    () => api.getBffRecommendations(options),
    {
      refreshInterval: 60000,
      shouldRetryOnError,
      onErrorRetry: swrRetry,
    }
  );
}

// Alerts hook
export function useAlerts(options?: UseAlertsOptions) {
  const key = options ? ['/bff/alerts', options] : '/bff/alerts';

  return useSWR<AlertsResponse>(
    key,
    () => api.getBffAlerts(options),
    {
      refreshInterval: 30000,
      shouldRetryOnError,
      onErrorRetry: swrRetry,
    }
  );
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
      shouldRetryOnError,
      onErrorRetry: swrRetry,
    }
  );
}

// Forecasts hook (BFF)
export function useBffForecasts(params: { familia?: string; item_id?: string; site_id?: number; limit?: number } | null) {
  const key = params ? ['/bff/forecasts', params] : null;

  return useSWR<ForecastResponse>(
    key,
    () => (params ? api.getBffForecasts(params) : null),
    {
      revalidateOnFocus: false,
      dedupingInterval: 300000,
      shouldRetryOnError,
      onErrorRetry: swrRetry,
    }
  );
}

export function useGeoSummary() {
  return useSWR<GeoSummaryResponse>(
    '/bff/geo/summary',
    () => api.getGeoSummary(),
    {
      refreshInterval: 300000,
      revalidateOnFocus: false,
      shouldRetryOnError,
      onErrorRetry: swrRetry,
    }
  );
}

export function useClimateFeatures(params?: { start_date?: string; end_date?: string; limit?: number }) {
  const key = params ? ['/bff/features/climate', params] : '/bff/features/climate';

  return useSWR<ClimateFeatureResponse>(
    key,
    () => api.getClimateFeatures(params),
    {
      refreshInterval: 600000,
      revalidateOnFocus: false,
      shouldRetryOnError,
      onErrorRetry: swrRetry,
    }
  );
}

// Export types for convenience
export type {
  UseItemsOptions,
  UseKPIsOptions,
  UseInventoryOptions,
  UseRecommendationsOptions,
  UseAlertsOptions,
};
