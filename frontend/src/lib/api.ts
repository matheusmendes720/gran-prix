// frontend/src/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

interface ApiClient {
  getKpis: (params?: { start_date?: string; end_date?: string }) => Promise<any>;
  getItems: (params?: { limit?: number; offset?: number; family?: string; abc_class?: string }) => Promise<any>;
  getItem: (itemId: number) => Promise<any>;
  getDemandTimeSeries: (params: { item_id: number; site_id: number; start_date?: string; end_date?: string }) => Promise<any>;
  getInventoryTimeSeries: (params: { item_id: number; site_id: number; start_date?: string }) => Promise<any>;
  getForecasts: (params: { item_id?: number; site_id?: number; horizon?: number; start_date?: string }) => Promise<any>;
  getFeatures: (params: { item_id?: number; start_date?: string; end_date?: string }) => Promise<any>;
  getRecommendations: (params?: { priority?: string; site_id?: number; limit?: number }) => Promise<any>;
  getAlerts: (params?: { level?: string; unread?: boolean; limit?: number }) => Promise<any>;
  acknowledgeRecommendation: (recId: number) => Promise<any>;
  markAlertRead: (alertId: number) => Promise<any>;
  login: (username: string, password: string) => Promise<any>;
}

class ApiClient implements ApiClient {
  private async request(endpoint: string, options: RequestInit = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getKpis(params?: { start_date?: string; end_date?: string }) {
    const queryParams = new URLSearchParams();
    if (params?.start_date) queryParams.append('start_date', params.start_date);
    if (params?.end_date) queryParams.append('end_date', params.end_date);

    return this.request(`/api/v1/analytics/kpis?${queryParams.toString()}`);
  }

  async getItems(params?: { limit?: number; offset?: number; family?: string; abc_class?: string }) {
    const queryParams = new URLSearchParams();
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params?.offset !== undefined) queryParams.append('offset', params.offset.toString());
    if (params?.family) queryParams.append('family', params.family);
    if (params?.abc_class) queryParams.append('abc_class', params.abc_class);

    return this.request(`/api/v1/items?${queryParams.toString()}`);
  }

  async getItem(itemId: number) {
    return this.request(`/api/v1/items/${itemId}`);
  }

  async getDemandTimeSeries(params: { item_id: number; site_id: number; start_date?: string; end_date?: string }) {
    const queryParams = new URLSearchParams();
    queryParams.append('item_id', params.item_id.toString());
    queryParams.append('site_id', params.site_id.toString());
    if (params.start_date) queryParams.append('start_date', params.start_date);
    if (params.end_date) queryParams.append('end_date', params.end_date);

    return this.request(`/api/v1/demand/timeseries?${queryParams.toString()}`);
  }

  async getInventoryTimeSeries(params: { item_id: number; site_id: number; start_date?: string }) {
    const queryParams = new URLSearchParams();
    queryParams.append('item_id', params.item_id.toString());
    queryParams.append('site_id', params.site_id.toString());
    if (params.start_date) queryParams.append('start_date', params.start_date);

    return this.request(`/api/v1/inventory/timeseries?${queryParams.toString()}`);
  }

  async getForecasts(params: { item_id?: number; site_id?: number; horizon?: number; start_date?: string }) {
    const queryParams = new URLSearchParams();
    if (params.item_id !== undefined) queryParams.append('item_id', params.item_id.toString());
    if (params.site_id !== undefined) queryParams.append('site_id', params.site_id.toString());
    if (params.horizon !== undefined) queryParams.append('horizon', params.horizon.toString());
    if (params.start_date) queryParams.append('start_date', params.start_date);

    return this.request(`/api/v1/forecasts?${queryParams.toString()}`);
  }

  async getFeatures(params: { item_id?: number; start_date?: string; end_date?: string }) {
    const queryParams = new URLSearchParams();
    if (params.item_id !== undefined) queryParams.append('item_id', params.item_id.toString());
    if (params.start_date) queryParams.append('start_date', params.start_date);
    if (params.end_date) queryParams.append('end_date', params.end_date);

    return this.request(`/api/v1/features?${queryParams.toString()}`);
  }

  async getRecommendations(params?: { priority?: string; site_id?: number; limit?: number }) {
    const queryParams = new URLSearchParams();
    if (params?.priority) queryParams.append('priority', params.priority);
    if (params?.site_id !== undefined) queryParams.append('site_id', params.site_id.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());

    return this.request(`/api/v1/recommendations?${queryParams.toString()}`);
  }

  async getAlerts(params?: { level?: string; unread?: boolean; limit?: number }) {
    const queryParams = new URLSearchParams();
    if (params?.level) queryParams.append('level', params.level);
    if (params?.unread !== undefined) queryParams.append('unread', params.unread.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());

    return this.request(`/api/v1/alerts?${queryParams.toString()}`);
  }

  async acknowledgeRecommendation(recId: number) {
    return this.request(`/api/v1/recommendations/${recId}/acknowledge`, {
      method: 'PATCH',
    });
  }

  async markAlertRead(alertId: number) {
    return this.request(`/api/v1/alerts/${alertId}/mark-read`, {
      method: 'PATCH',
    });
  }

  async login(username: string, password: string) {
    return this.request('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }
}

export const apiClient = new ApiClient();