'use client';

import React, { useState } from 'react';
import FamilyDemandChart from '../../../components/charts/FamilyDemandChart';
import SiteAggregationChart from '../../../components/charts/SiteAggregationChart';
import SupplierAggregationChart from '../../../components/charts/SupplierAggregationChart';
import Card from '../../../components/Card';

export default function HierarchicalFeaturesPage() {
  const [selectedFamily, setSelectedFamily] = useState<number | undefined>();
  const [selectedSite, setSelectedSite] = useState<string | undefined>();
  const [selectedSupplier, setSelectedSupplier] = useState<number | undefined>();
  const [activeLevel, setActiveLevel] = useState<'family' | 'site' | 'supplier'>('family');

  const handleFamilyClick = (familyId: number) => {
    setSelectedFamily(familyId);
    // Navigate to family detail or update charts
  };

  const handleSiteClick = (siteId: string) => {
    setSelectedSite(siteId);
    // Navigate to site detail or update charts
  };

  const handleSupplierClick = (supplierId: number) => {
    setSelectedSupplier(supplierId);
    // Navigate to supplier detail or update charts
  };

  return (
    <div className="w-full space-y-6 p-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-brand-lightest-slate">Features Hierárquicas</h1>
          <p className="text-sm text-brand-slate mt-1">
            Agregações por família, site/torre e fornecedor
          </p>
        </div>
      </div>

      {/* Story Card */}
      <Card>
        <div className="p-4">
          <h3 className="text-lg font-bold text-brand-lightest-slate mb-2">🏗️ Sobre Features Hierárquicas</h3>
          <p className="text-sm text-brand-slate mb-3">
            Agregações hierárquicas permitem análise de demanda em múltiplos níveis: por família de materiais, 
            por site/torre (18,000+ torres), e por fornecedor. Use drill-down para explorar detalhes.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
            <div className="p-3 bg-brand-light-navy/50 rounded-lg">
              <h4 className="text-sm font-semibold text-brand-lightest-slate mb-1">👨‍👩‍👧 Por Família</h4>
              <p className="text-xs text-brand-slate">
                Análise de demanda agregada por família de materiais
              </p>
            </div>
            <div className="p-3 bg-brand-light-navy/50 rounded-lg">
              <h4 className="text-sm font-semibold text-brand-lightest-slate mb-1">📍 Por Site/Torre</h4>
              <p className="text-xs text-brand-slate">
                18,000+ torres cadastradas com análise de movimentações
              </p>
            </div>
            <div className="p-3 bg-brand-light-navy/50 rounded-lg">
              <h4 className="text-sm font-semibold text-brand-lightest-slate mb-1">🏭 Por Fornecedor</h4>
              <p className="text-xs text-brand-slate">
                Análise de fornecedores, lead times e confiabilidade
              </p>
            </div>
          </div>
        </div>
      </Card>

      {/* Navigation Tabs */}
      <Card>
        <div className="border-b border-brand-light-navy/50">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveLevel('family')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeLevel === 'family'
                  ? 'border-brand-cyan text-brand-cyan'
                  : 'border-transparent text-brand-slate hover:text-brand-lightest-slate'
              }`}
            >
              Por Família
            </button>
            <button
              onClick={() => setActiveLevel('site')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeLevel === 'site'
                  ? 'border-brand-cyan text-brand-cyan'
                  : 'border-transparent text-brand-slate hover:text-brand-lightest-slate'
              }`}
            >
              Por Site/Torre
            </button>
            <button
              onClick={() => setActiveLevel('supplier')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeLevel === 'supplier'
                  ? 'border-brand-cyan text-brand-cyan'
                  : 'border-transparent text-brand-slate hover:text-brand-lightest-slate'
              }`}
            >
              Por Fornecedor
            </button>
          </nav>
        </div>
      </Card>

      {/* Charts */}
      {activeLevel === 'family' && (
        <FamilyDemandChart familyId={selectedFamily} onFamilyClick={handleFamilyClick} />
      )}

      {activeLevel === 'site' && (
        <SiteAggregationChart siteId={selectedSite} onSiteClick={handleSiteClick} />
      )}

      {activeLevel === 'supplier' && (
        <SupplierAggregationChart supplierId={selectedSupplier} onSupplierClick={handleSupplierClick} />
      )}
    </div>
  );
}

