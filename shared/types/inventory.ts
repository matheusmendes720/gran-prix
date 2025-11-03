/**
 * Shared inventory types
 */

export interface Inventory {
  item_id: string;
  current_stock: number;
  reorder_point: number;
  safety_stock: number;
  lead_time: number;
  days_to_rupture: number;
  alert_level: 'normal' | 'medium' | 'high' | 'critical';
}

export interface ReorderPointCalculation {
  average_demand: number;
  lead_time_demand: number;
  safety_stock: number;
  reorder_point: number;
  service_level: number;
}

