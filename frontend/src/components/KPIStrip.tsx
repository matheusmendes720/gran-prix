import React from 'react';
import { Card } from './ui/card';

interface KPIStripProps {
  kpis: Array<{
    id: string;
    label: string;
    value: number;
    unit: string;
    delta: number;
    deltaType: 'increase' | 'decrease';
    target?: number;
    status?: 'success' | 'warning' | 'critical';
  }>;
}

export default function KPIStrip({ kpis }: KPIStripProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {kpis.map((kpi) => (
        <Card key={kpi.id} className="p-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600">{kpi.label}</h3>
            <span className={`text-xs px-2 py-1 rounded-full ${
              kpi.status === 'success' ? 'bg-green-100 text-green-800' :
              kpi.status === 'warning' ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800'
            }`}>
              {kpi.status === 'success' ? '✅' :
               kpi.status === 'warning' ? '⚠️' : '🔴'}
            </span>
          </div>          
          <div className="flex items-baseline">
            <span className="text-2xl font-bold text-gray-900">
              {kpi.value}{kpi.unit}
            </span>
            <span className={`ml-2 text-sm font-medium ${
              kpi.deltaType === 'increase' ? 'text-green-600' : 'text-red-600'
            }`}>
              {kpi.deltaType === 'increase' ? '↑' : '↓'} {Math.abs(kpi.delta)}%
            </span>
          </div>          
          {kpi.target && (
            <div className="mt-2">
              <div className="flex justify-between text-xs text-gray-500">
                <span>Meta: {kpi.target}{kpi.unit}</span>
                <span>{Math.round((kpi.value / kpi.target) * 100)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                <div 
                  className={`h-1.5 rounded-full ${
                    kpi.value >= kpi.target ? 'bg-green-500' : 'bg-yellow-500'
                  }`}
                  style={{ width: `${Math.min(100, (kpi.value / kpi.target) * 100)}%` }}
                />
              </div>
            </div>
          )}
        </Card>
      ))}
    </div>
  );
}