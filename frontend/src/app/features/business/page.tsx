'use client';

import React, { useState } from 'react';
import BusinessMetricsChart from '../../../components/charts/BusinessMetricsChart';
import Card from '../../../components/Card';

export default function BusinessFeaturesPage() {
  const [selectedMaterial, setSelectedMaterial] = useState<number | undefined>();

  return (
    <div className="w-full space-y-6 p-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-brand-lightest-slate">Features de Negócio</h1>
          <p className="text-sm text-brand-slate mt-1">
            Features específicas da Nova Corrente B2B
          </p>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <div className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
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
          <h3 className="text-lg font-bold text-brand-lightest-slate mb-2">🏢 Sobre Features de Negócio</h3>
          <p className="text-sm text-brand-slate mb-3">
            Features específicas da operação B2B da Nova Corrente, incluindo top 5 famílias, analytics por tier 
            e contexto de materiais. Essas features capturam aspectos únicos da operação B2B da empresa.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
            <div className="p-3 bg-brand-light-navy/50 rounded-lg">
              <h4 className="text-sm font-semibold text-brand-lightest-slate mb-1">📊 Visão Geral</h4>
              <p className="text-xs text-brand-slate">
                Resumo de famílias, materiais, tiers e penalidades
              </p>
            </div>
            <div className="p-3 bg-brand-light-navy/50 rounded-lg">
              <h4 className="text-sm font-semibold text-brand-lightest-slate mb-1">🏆 Top 5 Famílias</h4>
              <p className="text-xs text-brand-slate">
                Famílias com maior movimentação e distribuição
              </p>
            </div>
            <div className="p-3 bg-brand-light-navy/50 rounded-lg">
              <h4 className="text-sm font-semibold text-brand-lightest-slate mb-1">📈 Análise de Tiers</h4>
              <p className="text-xs text-brand-slate">
                Analytics por tier: materiais, penalidades e disponibilidade
              </p>
            </div>
          </div>
        </div>
      </Card>

      {/* Charts */}
      <BusinessMetricsChart materialId={selectedMaterial} />
    </div>
  );
}

