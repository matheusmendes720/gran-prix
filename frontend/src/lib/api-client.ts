/**
 * Nova Corrente API Client
 * Type-safe client for Flask API v1 endpoints
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export interface ApiResponse<T> {
  status: 'success' | 'error';
  data: T;
  metadata?: {
    total_count?: number;
    page?: number;
    limit?: number;
  };
  error?: string;
}

export interface Item {
  item_id: number;
  sku: string;
  name: string;
  description?: string;
  family: string;
  category?: string;
  subcategory?: string;
  abc_class: 'A' | 'B' | 'C';
  criticality: number;
  unit_of_measure?: string;
  active: boolean;
  extra_attributes?: Record<string, any>;
  created_at: string;
  updated_at?: string;
}

export interface KPI {
  kpi_id: number;
  full_date: string;
  total_demand: number;
  stockout_rate: number;
  abc_a_share: number;
  delayed_orders_pct: number;
  forecast_mape: number;
  computed_at: string;
}

export interface DemandTimeseries {
  full_date: string;
  item_id: number;
  site_id: number;
  quantity: number;
  unit_cost?: number;
  total_cost?: number;
}

export interface InventoryTimeseries {
  full_date: string;
  item_id: number;
  site_id: number;
  stock_level: number;
  safety_stock?: number;
  reorder_point?: number;
}

export interface Forecast {
  forecast_id: number;
  item_id: number;
  site_id: number;
  forecast_date: string;
  horizon_days: number;
  model_name: string;
  predicted_demand: number;
  confidence_lower: number;
  confidence_upper: number;
  model_version?: string;
  created_at: string;
}

export interface Recommendation {
  recommendation_id: number;
  item_id: number;
  site_id?: number;
  recommendation_type: string;
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  description: string;
  suggested_action?: string;
  estimated_impact?: number;
  status: 'PENDING' | 'REVIEWED' | 'APPLIED' | 'REJECTED';
  created_at: string;
  reviewed_at?: string;
  reviewed_by?: string;
}

export interface Alert {
  alert_id: number;
  alert_type: string;
  severity: 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  item_id?: number;
  site_id?: number;
  message: string;
  details?: Record<string, any>;
  status: 'NEW' | 'ACKNOWLEDGED' | 'RESOLVED';
  created_at: string;
  acknowledged_at?: string;
  resolved_at?: string;
}

class NovaCorrenteAPI {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Unknown error' }));
        throw new Error(error.error || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  // Health check
  async health() {
    return this.request<{ status: string; database: string; timestamp: string; version: string }>(
      '/health'
    );
  }

  // Items API
  async getItems(params?: {
    limit?: number;
    offset?: number;
    family?: string;
    abc_class?: 'A' | 'B' | 'C';
  }) {
    const queryParams = new URLSearchParams();
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.offset) queryParams.append('offset', params.offset.toString());
    if (params?.family) queryParams.append('family', params.family);
    if (params?.abc_class) queryParams.append('abc_class', params.abc_class);

    return this.request<Item[]>(`/api/v1/items?${queryParams}`);
  }

  async getItem(itemId: number) {
    return this.request<Item>(`/api/v1/items/${itemId}`);
  }

  // KPIs API
  async getKPIs(params?: { start_date?: string; end_date?: string }) {
    const queryParams = new URLSearchParams();
    if (params?.start_date) queryParams.append('start_date', params.start_date);
    if (params?.end_date) queryParams.append('end_date', params.end_date);

    return this.request<KPI[]>(`/api/v1/analytics/kpis?${queryParams}`);
  }

  // Demand Timeseries API
  async getDemandTimeseries(params: {
    item_id: number;
    start_date?: string;
    end_date?: string;
  }) {
    const queryParams = new URLSearchParams({ item_id: params.item_id.toString() });
    if (params.start_date) queryParams.append('start_date', params.start_date);
    if (params.end_date) queryParams.append('end_date', params.end_date);

    return this.request<DemandTimeseries[]>(`/api/v1/demand/timeseries?${queryParams}`);
  }

  // Inventory Timeseries API
  async getInventoryTimeseries(params: {
    item_id: number;
    start_date?: string;
    end_date?: string;
  }) {
    const queryParams = new URLSearchParams({ item_id: params.item_id.toString() });
    if (params.start_date) queryParams.append('start_date', params.start_date);
    if (params.end_date) queryParams.append('end_date', params.end_date);

    return this.request<InventoryTimeseries[]>(`/api/v1/inventory/timeseries?${queryParams}`);
  }

  // Forecasts API
  async getForecasts(params: {
    item_id: number;
    site_id?: number;
    horizon_days?: number;
  }) {
    const queryParams = new URLSearchParams({ item_id: params.item_id.toString() });
    if (params.site_id) queryParams.append('site_id', params.site_id.toString());
    if (params.horizon_days) queryParams.append('horizon_days', params.horizon_days.toString());

    return this.request<Forecast[]>(`/api/v1/forecasts?${queryParams}`);
  }

  // Recommendations API
  async getRecommendations(params?: {
    status?: 'PENDING' | 'REVIEWED' | 'APPLIED' | 'REJECTED';
    priority?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    limit?: number;
  }) {
    const queryParams = new URLSearchParams();
    if (params?.status) queryParams.append('status', params.status);
    if (params?.priority) queryParams.append('priority', params.priority);
    if (params?.limit) queryParams.append('limit', params.limit.toString());

    return this.request<Recommendation[]>(`/api/v1/recommendations?${queryParams}`);
  }

  async updateRecommendation(recommendationId: number, status: string, reviewed_by?: string) {
    return this.request<Recommendation>(`/api/v1/recommendations/${recommendationId}`, {
      method: 'PATCH',
      body: JSON.stringify({ status, reviewed_by }),
    });
  }

  // Alerts API
  async getAlerts(params?: {
    status?: 'NEW' | 'ACKNOWLEDGED' | 'RESOLVED';
    severity?: 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
    limit?: number;
  }) {
    const queryParams = new URLSearchParams();
    if (params?.status) queryParams.append('status', params.status);
    if (params?.severity) queryParams.append('severity', params.severity);
    if (params?.limit) queryParams.append('limit', params.limit.toString());

    return this.request<Alert[]>(`/api/v1/alerts?${queryParams}`);
  }

  async updateAlert(alertId: number, status: string) {
    return this.request<Alert>(`/api/v1/alerts/${alertId}`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    });
  }

  // Feature Store API
  async getFeatures(params: {
    item_id: number;
    feature_date?: string;
  }) {
    const queryParams = new URLSearchParams({ item_id: params.item_id.toString() });
    if (params.feature_date) queryParams.append('feature_date', params.feature_date);

    return this.request<any[]>(`/api/v1/features?${queryParams}`);
  }
}

// Export singleton instance
export const api = new NovaCorrenteAPI();

// Export class for custom instances
export default NovaCorrenteAPI;
