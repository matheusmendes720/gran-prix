'use client';

import React, { useState } from 'react';
import EconomicFeaturesChart from '../../../components/charts/EconomicFeaturesChart';
import Card from '../../../components/Card';

export default function EconomicFeaturesPage() {
  const [startDate, setStartDate] = useState<string>(
    new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  );
  const [endDate, setEndDate] = useState<string>(
    new Date().toISOString().split('T')[0]
  );
  const [selectedMaterial, setSelectedMaterial] = useState<number | undefined>();

  return (
    <div className="w-full space-y-6 p-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-brand-lightest-slate">Features Econômicas</h1>
          <p className="text-sm text-brand-slate mt-1">
            Indicadores econômicos do BACEN e seus impactos na demanda
          </p>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <div className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-brand-slate mb-2">Data Inicial</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-full px-3 py-2 bg-brand-light-navy border border-brand-light-navy/50 rounded-lg text-brand-lightest-slate focus:outline-none focus:border-brand-cyan"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-brand-slate mb-2">Data Final</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="w-full px-3 py-2 bg-brand-light-navy border border-brand-light-navy/50 rounded-lg text-brand-lightest-slate focus:outline-none focus:border-brand-cyan"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-brand-slate mb-2">Material (Opcional)</label>
              <input
                type="number"
                value={selectedMaterial || ''}
                onChange={(e) => setSelectedMaterial(e.target.value ? parseInt(e.target.value) : undefined)}
                placeholder="ID do Material"
                className="w-full px-3 py-2 bg-brand-light-navy border border-brand-light-navy/50 rounded-lg text-brand-lightest-slate focus:outline-none focus:border-brand-cyan"
              />
            </div>
          </div>
        </div>
      </Card>

      {/* Story Card */}
      <Card>
        <div className="p-4">
          <h3 className="text-lg font-bold text-brand-lightest-slate mb-2">💰 Sobre Features Econômicas</h3>
          <p className="text-sm text-brand-slate mb-3">
            Indicadores econômicos do BACEN (IPCA, câmbio USD/BRL, PIB, SELIC) afetam diretamente a demanda de materiais 
            e custos operacionais. Monitoramos inflação, desvalorização cambial, crescimento econômico e taxa de juros 
            para antecipar impactos na demanda e nos custos.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            <div className="p-3 bg-brand-light-navy/50 rounded-lg">
              <h4 className="text-sm font-semibold text-brand-lightest-slate mb-1">📊 Indicadores BACEN</h4>
              <p className="text-xs text-brand-slate">
                IPCA (inflação), câmbio, PIB e SELIC atualizados diariamente
              </p>
            </div>
            <div className="p-3 bg-brand-light-navy/50 rounded-lg">
              <h4 className="text-sm font-semibold text-brand-lightest-slate mb-1">📈 Impactos na Demanda</h4>
              <p className="text-xs text-brand-slate">
                Análise de como fatores econômicos influenciam a demanda de materiais
              </p>
            </div>
          </div>
        </div>
      </Card>

      {/* Charts */}
      <EconomicFeaturesChart materialId={selectedMaterial} startDate={startDate} endDate={endDate} />
    </div>
  );
}

