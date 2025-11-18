import React, { useState } from 'react';
import { Card } from './ui/card';
import { loadAlerts } from '../data/demoSnapshot';

interface AlertDrawerProps {
  alerts: any[];
}

export default function AlertDrawer({ alerts }: AlertDrawerProps) {
  const [filter, setFilter] = useState<'all' | 'critical' | 'warning' | 'info'>('all');
  
  const filteredAlerts = alerts.filter(alert => 
    filter === 'all' ? true : alert.severity === filter
  );
  
  return (
    <Card className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Alertas Inteligentes</h3>
        <div className="flex gap-2">
          {(['all', 'critical', 'warning', 'info'] as const).map((severity) => (
            <button
              key={severity}
              onClick={() => setFilter(severity as any)}
              className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors ${
                filter === severity
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {severity === 'all' ? 'Todos' : 
               severity === 'critical' ? 'Críticos' :
               severity === 'warning' ? 'Avisos' : 'Info'}
            </button>
          ))}
        </div>
      </div>
      
      <div className="space-y-3">
        {filteredAlerts.map((alert) => (
          <div
            key={alert.id}
            className={`p-4 rounded-lg border cursor-pointer transition-all hover:shadow-md ${
              alert.severity === 'critical' ? 'border-red-300 bg-red-50' :
              alert.severity === 'warning' ? 'border-yellow-300 bg-yellow-50' :
              'border-blue-300 bg-blue-50'
            }`}
          >
            <div className="flex justify-between items-start mb-2">
              <div className="flex items-center gap-2">
                <span className={`text-lg ${
                  alert.severity === 'critical' ? 'text-red-600' :
                  alert.severity === 'warning' ? 'text-yellow-600' :
                  'text-blue-600'
                }`}>
                  {alert.severity === 'critical' ? '🔴' :
                   alert.severity === 'warning' ? '🟡' : '🔵'}
                </span>
                <div>
                  <h4 className="font-semibold text-gray-900">{alert.title}</h4>
                  {alert.daysToStockout && (
                    <span className="ml-2 text-sm text-red-600 font-medium">
                      {alert.daysToStockout} dias até ruptura
                    </span>
                  )}
                </div>
              </div>
            </div>
            
            <p className="text-gray-700 text-sm mb-3">{alert.message}</p>
            
            <div className="mt-3 flex justify-between items-center">
              <div className="text-sm text-gray-600">
                <span className="font-medium">Recomendação:</span> {alert.recommendation}
              </div>
              <button className="px-3 py-1 bg-blue-600 text-white rounded text-xs font-medium hover:bg-blue-700">
                Executar Ação
              </button>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}