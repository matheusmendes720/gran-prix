import React from 'react';
import { Card } from './ui/card';

export default function ForecastPulse() {
  return (
    <Card className="p-6">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Demand Forecast Pulse</h3>
        <div className="text-sm text-gray-600">
          Projeção vs. Ponto de Pedido
        </div>
      </div>
      
      <div className="h-64 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <div className="text-3xl font-bold text-indigo-600 mb-2">DUAL-AXIS CHART</div>
          <div className="text-sm text-gray-600">
            Historical + Forecast with Confidence Band
          </div>
          <div className="mt-4 p-3 bg-white rounded border border-blue-200">
            <div className="grid grid-cols-2 gap-4 text-xs">
              <div>
                <div className="font-semibold text-blue-600">HISTÓRICO</div>
                <div className="text-gray-600">60 dias reais</div>
              </div>
              <div>
                <div className="font-semibold text-green-600">PREVISÃO</div>
                <div className="text-gray-600">30 dias projetados</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-4 flex flex-wrap gap-2">
        <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
          🛠️ Manutenção
        </span>
        <span className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-xs font-medium">
          🎭 Carnaval 2025
        </span>
        <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-medium">
          ⚠️ Alerta Clima
        </span>
      </div>
      
      <div className="mt-4 grid grid-cols-3 gap-4">
        <div className="text-center p-3 bg-gray-50 rounded">
          <div className="text-2xl font-bold text-gray-900">340</div>
          <div className="text-sm text-gray-600">Demanda Média</div>
        </div>
        <div className="text-center p-3 bg-yellow-50 rounded">
          <div className="text-2xl font-bold text-yellow-600">92.7%</div>
          <div className="text-sm text-gray-600">Precisão</div>
        </div>
        <div className="text-center p-3 bg-green-50 rounded">
          <div className="text-2xl font-bold text-green-600">-60%</div>
          <div className="text-sm text-gray-600">Redução Rupturas</div>
        </div>
      </div>
    </Card>
  );
}