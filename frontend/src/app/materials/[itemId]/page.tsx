'use client';

import { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { DemandChart } from '@/components/charts/DemandChart';
import { InventoryChart } from '@/components/charts/InventoryChart';
import { ForecastChart } from '@/components/charts/ForecastChart';
import { apiClient } from '@/lib/api';

interface ItemDetail {
  item_id: number;
  sku: string;
  name: string;
  family: string;
  abc_class: string;
  criticality: number;
  unit_measure: string;
}

export default function MaterialDetailPage({ params }: { params: { itemId: string } }) {
  const [item, setItem] = useState<ItemDetail | null>(null);
  const [demandData, setDemandData] = useState<any[]>([]);
  const [forecastData, setForecastData] = useState<any[]>([]);
  const [inventoryData, setInventoryData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchItemData = async () => {
      try {
        // Fetch item details
        const itemResponse = await apiClient.getItem(Number(params.itemId));
        setItem(itemResponse);
        
        // Fetch demand data for this item (last 90 days)
        const demandResponse = await apiClient.getDemandTimeSeries({
          item_id: Number(params.itemId),
          site_id: 1, // Using first site as default
          start_date: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
        });
        setDemandData(demandResponse.data || []);
        
        // Fetch forecast data for this item
        const forecastResponse = await apiClient.getForecasts({
          item_id: Number(params.itemId),
          site_id: 1, // Using first site as default
          horizon: 30
        });
        setForecastData(forecastResponse.data || []);
        
        // Fetch inventory data for this item
        const inventoryResponse = await apiClient.getInventoryTimeSeries({
          item_id: Number(params.itemId),
          site_id: 1, // Using first site as default
          start_date: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
        });
        setInventoryData(inventoryResponse.data || []);
      } catch (error) {
        console.error('Error fetching item data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchItemData();
  }, [params.itemId]);

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  if (!item) {
    return (
      <div className="p-6">
        <div className="text-red-500">Item not found</div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">{item.name} ({item.sku})</h1>
        <p className="text-gray-600">
          ABC: {item.abc_class} | Criticality: {item.criticality}/10 | Family: {item.family}
        </p>
      </div>

      <Tabs defaultValue="demand" className="mt-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="demand">Demand</TabsTrigger>
          <TabsTrigger value="inventory">Inventory</TabsTrigger>
          <TabsTrigger value="forecasts">Forecasts</TabsTrigger>
          <TabsTrigger value="features">Features</TabsTrigger>
        </TabsList>

        <TabsContent value="demand">
          <div className="mt-4 h-96">
            <DemandChart data={demandData} />
          </div>
        </TabsContent>

        <TabsContent value="inventory">
          <div className="mt-4 h-96">
            <InventoryChart data={inventoryData} />
          </div>
        </TabsContent>

        <TabsContent value="forecasts">
          <div className="mt-4 h-96">
            <ForecastChart data={forecastData} />
          </div>
        </TabsContent>

        <TabsContent value="features">
          <div className="mt-4 p-4 border rounded-md">
            <h3 className="font-medium mb-2">Feature JSON (Simplified View)</h3>
            <pre className="text-sm bg-gray-50 p-3 rounded overflow-x-auto">
              {JSON.stringify(demandData.slice(0, 5), null, 2)}
            </pre>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}