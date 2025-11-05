// frontend/src/components/charts/InventoryChart.tsx
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface InventoryChartProps {
  data: { 
    full_date: string; 
    current_stock: number; 
    safety_stock: number; 
    reorder_point: number 
  }[];
}

// If no data is provided, use mock data
const mockData = [
  { full_date: '2025-01-01', current_stock: 500.0, safety_stock: 150.0, reorder_point: 200.0 },
  { full_date: '2025-01-02', current_stock: 450.0, safety_stock: 150.0, reorder_point: 200.0 },
  { full_date: '2025-01-03', current_stock: 400.0, safety_stock: 150.0, reorder_point: 200.0 },
  { full_date: '2025-01-04', current_stock: 350.0, safety_stock: 150.0, reorder_point: 200.0 },
  { full_date: '2025-01-05', current_stock: 300.0, safety_stock: 150.0, reorder_point: 200.0 },
  { full_date: '2025-01-06', current_stock: 250.0, safety_stock: 150.0, reorder_point: 200.0 },
  { full_date: '2025-01-07', current_stock: 200.0, safety_stock: 150.0, reorder_point: 200.0 },
  { full_date: '2025-01-08', current_stock: 180.0, safety_stock: 150.0, reorder_point: 200.0 },
  { full_date: '2025-01-09', current_stock: 160.0, safety_stock: 150.0, reorder_point: 200.0 },
  { full_date: '2025-01-10', current_stock: 140.0, safety_stock: 150.0, reorder_point: 200.0 },
];

export function InventoryChart({ data }: InventoryChartProps) {
  const chartData = data && data.length > 0 ? data : mockData;
  
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart
        data={chartData}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="full_date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line 
          type="monotone" 
          dataKey="current_stock" 
          stroke="#8884d8" 
          strokeWidth={2}
          name="Current Stock" 
        />
        <Line 
          type="monotone" 
          dataKey="safety_stock" 
          stroke="#82ca9d" 
          strokeWidth={2}
          name="Safety Stock" 
          strokeDasharray="3 3"
        />
        <Line 
          type="monotone" 
          dataKey="reorder_point" 
          stroke="#ff8042" 
          strokeWidth={2}
          name="Reorder Point" 
          strokeDasharray="3 3"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}