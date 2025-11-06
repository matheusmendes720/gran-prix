'use client';

import { useState } from 'react';
import { KPIDashboard } from '@/components/KPIDashboard';
import { MaterialsTable } from '@/components/MaterialsTable';
import { DemandChart } from '@/components/DemandChart';
import { useAlerts, useRecommendations } from '@/hooks/use-api';
import type { Item, Alert, Recommendation } from '@/lib/api-client';

export default function DashboardPage() {
  const [selectedItem, setSelectedItem] = useState<Item | null>(null);
  
  const { data: alertsData } = useAlerts({ status: 'NEW', limit: 5 });
  const { data: recsData } = useRecommendations({ status: 'PENDING', priority: 'CRITICAL', limit: 5 });
  
  const alerts = alertsData?.data ?? [];
  const recommendations = recsData?.data ?? [];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL': return 'bg-red-100 border-red-300 text-red-800';
      case 'ERROR': return 'bg-orange-100 border-orange-300 text-orange-800';
      case 'WARNING': return 'bg-yellow-100 border-yellow-300 text-yellow-800';
      default: return 'bg-blue-100 border-blue-300 text-blue-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'CRITICAL': return 'bg-red-100 border-red-300 text-red-800';
      case 'HIGH': return 'bg-orange-100 border-orange-300 text-orange-800';
      case 'MEDIUM': return 'bg-yellow-100 border-yellow-300 text-yellow-800';
      default: return 'bg-green-100 border-green-300 text-green-800';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Nova Corrente Analytics</h1>
          <p className="text-gray-600 mt-1">Dashboard de Previsão de Demanda</p>
        </div>
        <div className="text-sm text-gray-500">
          Atualizado: {new Date().toLocaleString('pt-BR')}
        </div>
      </div>
      
      {/* KPI Dashboard */}
      <KPIDashboard />
      
      {/* Selected Item Details */}
      {selectedItem && (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h2 className="text-xl font-bold text-gray-900">
                {selectedItem.name || selectedItem.sku}
              </h2>
              <p className="text-gray-600">SKU: {selectedItem.sku} | Família: {selectedItem.family}</p>
            </div>
            <button
              onClick={() => setSelectedItem(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
          
          <DemandChart itemId={selectedItem.item_id} days={90} />
        </div>
      )}
      
      {/* Materials Table */}
      <MaterialsTable onSelectItem={setSelectedItem} />
      
      {/* Alerts & Recommendations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Alerts */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Alertas Recentes</h2>
            <p className="text-gray-600 text-sm mt-1">Novos alertas do sistema</p>
          </div>
          <div className="p-6">
            {alerts.length === 0 ? (
              <p className="text-gray-500 text-center py-6">Nenhum alerta novo</p>
            ) : (
              <div className="space-y-3">
                {alerts.map((alert: Alert) => (
                  <div
                    key={alert.alert_id}
                    className={`p-4 rounded-lg border ${getSeverityColor(alert.severity)}`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-xs font-semibold uppercase">{alert.severity}</span>
                      <span className="text-xs opacity-75">
                        {new Date(alert.created_at).toLocaleDateString('pt-BR')}
                      </span>
                    </div>
                    <p className="font-medium">{alert.message}</p>
                    {alert.alert_type && (
                      <p className="text-xs mt-1 opacity-75">Tipo: {alert.alert_type}</p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        
        {/* Recommendations */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Recomendações Críticas</h2>
            <p className="text-gray-600 text-sm mt-1">Ações pendentes de alta prioridade</p>
          </div>
          <div className="p-6">
            {recommendations.length === 0 ? (
              <p className="text-gray-500 text-center py-6">Nenhuma recomendação pendente</p>
            ) : (
              <div className="space-y-3">
                {recommendations.map((rec: Recommendation) => (
                  <div
                    key={rec.recommendation_id}
                    className={`p-4 rounded-lg border ${getPriorityColor(rec.priority)}`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-xs font-semibold uppercase">{rec.priority}</span>
                      <span className="text-xs opacity-75">
                        {new Date(rec.created_at).toLocaleDateString('pt-BR')}
                      </span>
                    </div>
                    <p className="font-medium">{rec.description}</p>
                    {rec.suggested_action && (
                      <p className="text-sm mt-2 opacity-90">→ {rec.suggested_action}</p>
                    )}
                    {rec.estimated_impact && (
                      <p className="text-xs mt-1 opacity-75">
                        Impacto estimado: {rec.estimated_impact.toLocaleString('pt-BR')}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}