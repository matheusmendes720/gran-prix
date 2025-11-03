'use client';

import React, { useState } from 'react';
import CategoricalEncodingChart from '../../../components/charts/CategoricalEncodingChart';
import Card from '../../../components/Card';

export default function CategoricalFeaturesPage() {
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
          <h1 className="text-3xl font-bold text-brand-lightest-slate">Features Categóricas</h1>
          <p className="text-sm text-brand-slate mt-1">
            Encodings categóricos de famílias, sites e fornecedores
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
          <h3 className="text-lg font-bold text-brand-lightest-slate mb-2">🏷️ Sobre Features Categóricas</h3>
          <p className="text-sm text-brand-slate mb-3">
            Features categóricas representam famílias de materiais, sites/torres e fornecedores através de 
            encodings numéricos para uso em modelos de ML. Esses encodings permitem que algoritmos processem 
            informações categóricas como variáveis numéricas.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
            <div className="p-3 bg-brand-light-navy/50 rounded-lg">
              <h4 className="text-sm font-semibold text-brand-lightest-slate mb-1">👨‍👩‍👧 Famílias</h4>
              <p className="text-xs text-brand-slate">
                Encodings de famílias de materiais e quantidade de materiais por família
              </p>
            </div>
            <div className="p-3 bg-brand-light-navy/50 rounded-lg">
              <h4 className="text-sm font-semibold text-brand-lightest-slate mb-1">📍 Sites</h4>
              <p className="text-xs text-brand-slate">
                Encodings de sites/torres e quantidade de materiais por site
              </p>
            </div>
            <div className="p-3 bg-brand-light-navy/50 rounded-lg">
              <h4 className="text-sm font-semibold text-brand-lightest-slate mb-1">🏭 Fornecedores</h4>
              <p className="text-xs text-brand-slate">
                Encodings de fornecedores e quantidade de materiais por fornecedor
              </p>
            </div>
          </div>
        </div>
      </Card>

      {/* Charts */}
      <CategoricalEncodingChart materialId={selectedMaterial} startDate={startDate} endDate={endDate} />
    </div>
  );
}

