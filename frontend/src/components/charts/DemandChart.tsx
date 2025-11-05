// frontend/src/components/charts/DemandChart.tsx
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

interface DemandChartProps {
  data: { full_date: string; quantity: number }[];
}

// If no data is provided, use mock data
const mockData = [
  { full_date: '2025-01-01', quantity: 120.5 },
  { full_date: '2025-01-02', quantity: 98.3 },
  { full_date: '2025-01-03', quantity: 110.2 },
  { full_date: '2025-01-04', quantity: 130.7 },
  { full_date: '2025-01-05', quantity: 125.1 },
  { full_date: '2025-01-06', quantity: 140.5 },
  { full_date: '2025-01-07', quantity: 135.2 },
  { full_date: '2025-01-08', quantity: 150.8 },
  { full_date: '2025-01-09', quantity: 145.3 },
  { full_date: '2025-01-10', quantity: 160.9 },
];

export function DemandChart({ data }: DemandChartProps) {
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
          dataKey="quantity" 
          stroke="#8884d8" 
          strokeWidth={2}
          name="Demand Quantity" 
        />
      </LineChart>
    </ResponsiveContainer>
  );
}