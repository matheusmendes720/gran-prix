// frontend/src/components/charts/ForecastChart.tsx (with confidence intervals)
import React from 'react';
import {
  LineChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface ForecastChartProps {
  data: { full_date: string; yhat: number; yhat_lower: number; yhat_upper: number }[];
}

// If no data is provided, use mock data
const mockData = [
  { full_date: '2025-02-01', yhat: 105.2, yhat_lower: 92.1, yhat_upper: 118.3 },
  { full_date: '2025-02-02', yhat: 107.8, yhat_lower: 94.5, yhat_upper: 121.1 },
  { full_date: '2025-02-03', yhat: 102.5, yhat_lower: 89.2, yhat_upper: 115.8 },
  { full_date: '2025-02-04', yhat: 110.3, yhat_lower: 97.0, yhat_upper: 123.6 },
  { full_date: '2025-02-05', yhat: 115.7, yhat_lower: 102.4, yhat_upper: 129.0 },
  { full_date: '2025-02-06', yhat: 112.1, yhat_lower: 98.8, yhat_upper: 125.4 },
  { full_date: '2025-02-07', yhat: 118.6, yhat_lower: 105.3, yhat_upper: 131.9 },
  { full_date: '2025-02-08', yhat: 122.4, yhat_lower: 109.1, yhat_upper: 135.7 },
  { full_date: '2025-02-09', yhat: 125.8, yhat_lower: 112.5, yhat_upper: 139.1 },
  { full_date: '2025-02-10', yhat: 128.3, yhat_lower: 115.0, yhat_upper: 141.6 },
];

export function ForecastChart({ data }: ForecastChartProps) {
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
        <Area 
          type="monotone" 
          dataKey="yhat_upper" 
          fill="#8884d8" 
          fillOpacity={0.2} 
          stroke="none"
          name="Confidence Interval"
        />
        <Area 
          type="monotone" 
          dataKey="yhat_lower" 
          fill="#8884d8" 
          fillOpacity={0.2} 
          stroke="none"
        />
        <Line 
          type="monotone" 
          dataKey="yhat" 
          stroke="#8884d8" 
          strokeWidth={2} 
          name="Forecast"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}