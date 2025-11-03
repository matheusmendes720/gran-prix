/**
 * Shared forecast types
 */

export interface Forecast {
  item_id: string;
  forecast: number[];
  dates: string[];
  confidence_intervals?: {
    lower: number[];
    upper: number[];
  };
  metadata?: {
    model_type: string;
    training_date: string;
    data_points: number;
  };
}

export interface ForecastRequest {
  item_id: string;
  forecast_days?: number;
  model_type?: 'arima' | 'prophet' | 'lstm' | 'ensemble';
}

export interface ForecastMetrics {
  mape: number;
  rmse: number;
  mae: number;
  mase?: number;
}

