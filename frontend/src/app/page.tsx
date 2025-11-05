'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { KPICard } from '@/components/KPICard';
import { DemandTrendChart } from '@/components/charts/DemandTrendChart';
import { AlertList } from '@/components/AlertList';
import { apiClient } from '@/lib/api';

export default function DashboardPage() {
  const [kpis, setKpis] = useState<any>(null);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch KPIs for the last 30 days
        const kpiResponse = await apiClient.getKpis({
          start_date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          end_date: new Date().toISOString().split('T')[0]
        });
        
        setKpis(kpiResponse.data[0] || {});
        
        // Fetch critical alerts
        const alertsResponse = await apiClient.getAlerts({
          level: 'CRITICAL',
          limit: 5
        });
        
        setAlerts(alertsResponse.data || []);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="p-6">Loading dashboard...</div>;
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="text-sm text-gray-500">
          Last updated: {new Date().toLocaleString()}
        </div>
      </div>
      
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard 
          title="Stockout Rate"
          value={kpis.stockout_rate ? (kpis.stockout_rate * 100).toFixed(2) + '%' : '0.00%'}
          change={-0.5}
          format="percentage"
        />
        <KPICard 
          title="Forecast MAPE"
          value={kpis.forecast_mape ? (kpis.forecast_mape * 100).toFixed(2) + '%' : '0.00%'}
          change={1.2}
          format="percentage"
        />
        <KPICard 
          title="Delayed Orders"
          value={kpis.delayed_orders_pct ? (kpis.delayed_orders_pct * 100).toFixed(2) + '%' : '0.00%'}
          change={-0.8}
          format="percentage"
        />
        <KPICard 
          title="ABC A-Share"
          value={kpis.abc_a_share ? (kpis.abc_a_share * 100).toFixed(2) + '%' : '0.00%'}
          change={0.3}
          format="percentage"
        />
      </div>
      
      {/* Demand Trend Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Demand Trend (Last 30 Days)</CardTitle>
          <CardDescription>Actual vs Forecast demand over time</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <DemandTrendChart />
          </div>
        </CardContent>
      </Card>
      
      {/* Alerts & Recommendations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Top Alerts</CardTitle>
            <CardDescription>Critical system alerts</CardDescription>
          </CardHeader>
          <CardContent>
            <AlertList alerts={alerts} />
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Critical Recommendations</CardTitle>
            <CardDescription>Immediate actions required</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                <p className="font-medium">Reorder 500 units of ITEM-00123</p>
                <p className="text-sm text-gray-600">Stock below safety level</p>
              </div>
              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                <p className="font-medium">Expedite order TEL-789</p>
                <p className="text-sm text-gray-600">Delivery delayed by 5 days</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}