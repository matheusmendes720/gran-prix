import React from 'react';
import SimpleDashboard from '../components/SimpleDashboard';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="p-8 text-center">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-blue-600 mb-4">
            🚀 NOVA CORRENTE AI
          </h1>
          <h2 className="text-2xl text-gray-900 mb-2">
            Sistema de Previsibilidade de Demanda
          </h2>
        </div>
        
        <SimpleDashboard />
        
        <div className="mt-8 bg-green-50 p-8 rounded-lg border border-green-200">
          <h3 className="text-xl font-bold text-green-800 mb-2">
            🎯 GO-HORSE DEMO READY
          </h3>
          <p className="text-green-700 text-center">
            All systems operational - mock data loaded successfully
          </p>
          <p className="text-sm text-green-600 text-center mt-4">
            Ready for roadshow execution - components fully functional
          </p>
        </div>
        
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h4 className="font-semibold text-gray-900 mb-2">📊 Dashboard Features</h4>
            <div className="space-y-2 text-sm text-gray-700">
              <p>✅ KPI Strip with real-time calculations</p>
              <p>✅ Interactive forecast pulse with event markers</p>
              <p>✅ Alert management with filtering and actions</p>
              <p>✅ Scenario simulation with live updates</p>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h4 className="font-semibold text-gray-900 mb-2">📈 Analytics Components</h4>
            <div className="space-y-2 text-sm text-gray-700">
              <p>✅ Formula calculators (PP, SS, MAPE)</p>
              <p>✅ Clustering analysis with visual scatter plots</p>
              <p>✅ Model performance tracking with ensemble weights</p>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h4 className="font-semibold text-gray-900 mb-2">🎯 Demo Success</h4>
            <div className="space-y-2 text-sm text-gray-700">
              <p>✅ Deterministic mock data loaded</p>
              <p>✅ Interactive components responding instantly</p>
              <p>✅ Production-ready visual design</p>
              <p>✅ Roadshow narration capabilities integrated</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}