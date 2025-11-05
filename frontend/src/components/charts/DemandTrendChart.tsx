// frontend/src/components/charts/DemandTrendChart.tsx
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

// Mock data for the chart
const mockData = [
  { date: '2025-01-01', actual: 1200, forecast: 1150 },
  { date: '2025-01-02', actual: 1300, forecast: 1250 },
  { date: '2025-01-03', actual: 1100, forecast: 1180 },
  { date: '2025-01-04', actual: 1450, forecast: 1400 },
  { date: '2025-01-05', actual: 1600, forecast: 1550 },
  { date: '2025-01-06', actual: 1350, forecast: 1400 },
  { date: '2025-01-07', actual: 1200, forecast: 1250 },
  { date: '2025-01-08', actual: 1150, forecast: 1200 },
  { date: '2025-01-09', actual: 1400, forecast: 1350 },
  { date: '2025-01-10', actual: 1550, forecast: 1500 },
  { date: '2025-01-11', actual: 1700, forecast: 1650 },
  { date: '2025-01-12', actual: 1450, forecast: 1500 },
  { date: '2025-01-13', actual: 1300, forecast: 1350 },
  { date: '2025-01-14', actual: 1250, forecast: 1300 },
  { date: '2025-01-15', actual: 1500, forecast: 1450 },
  { date: '2025-01-16', actual: 1650, forecast: 1600 },
  { date: '2025-01-17', actual: 1800, forecast: 1750 },
  { date: '2025-01-18', actual: 1550, forecast: 1600 },
  { date: '2025-01-19', actual: 1400, forecast: 1450 },
  { date: '2025-01-20', actual: 1350, forecast: 1400 },
  { date: '2025-01-21', actual: 1600, forecast: 1550 },
  { date: '2025-01-22', actual: 1750, forecast: 1700 },
  { date: '2025-01-23', actual: 1900, forecast: 1850 },
  { date: '2025-01-24', actual: 1650, forecast: 1700 },
  { date: '2025-01-25', actual: 1500, forecast: 1550 },
  { date: '2025-01-26', actual: 1450, forecast: 1500 },
  { date: '2025-01-27', actual: 1700, forecast: 1650 },
  { date: '2025-01-28', actual: 1850, forecast: 1800 },
  { date: '2025-01-29', actual: 2000, forecast: 1950 },
  { date: '2025-01-30', actual: 1750, forecast: 1800 },
  { date: '2025-01-31', actual: 1600, forecast: 1650 },
];

export function DemandTrendChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart
        data={mockData}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="actual"
          stroke="#8884d8"
          activeDot={{ r: 8 }}
          name="Actual Demand"
        />
        <Line
          type="monotone"
          dataKey="forecast"
          stroke="#82ca9d"
          name="Forecast"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}