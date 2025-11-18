'use client';

import React from 'react';
import { Card } from '../../../ui/card';
import { loadMainTabs, ClusterConfig, ModelsConfig } from '../../../../data/demoSnapshot';

export default function AnalisesAprofundadasPage() {
  const mainTabs = loadMainTabs();
  
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Análises Aprofundadas</h1>
          <p className="text-lg text-gray-600">
            Inteligência preditiva com fórmulas interativas, agrupamentos de falhas e métricas de ensemble
          </p>
      </div>
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Análises Aprofundadas</h1>
            <p className="text-lg text-gray-600">
              Inteligência preditiva com fórmulas interativas, agrupamentos de falhas e métricas de ensemble
            </p>
          </div>
          
          {/* Tab Navigation */}
          <div className="flex space-x-1 mb-8 border-b border-gray-200">
            {[
              { id: 'formulas', label: 'Fórmulas', active: true },
              { id: 'clustering', label: 'Clustering', active: false },
              { id: 'modelos', label: 'Modelos', active: false }
            ].map((tab) => (
              <button
                key={tab.id}
                className={`pb-4 px-6 text-sm font-medium border-b-2 transition-colors ${
                  tab.active
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
          
          {/* FÓRMULAS TAB CONTENT */}
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* PP Calculator */}
              <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Ponto de Pedido (PP)</h3>
                <div className="bg-blue-50 p-4 rounded-lg mb-4">
                  <h4 className="text-center text-blue-800 font-mono mb-2">PP = (D × LT) + SS</h4>
                  <div className="text-center text-gray-600 text-sm">Nível ideal para acionar compras antes da ruptura</div>
                </div>
                
                <div className="mt-4 space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-700">Demanda Diária:</span>
                    <span className="font-bold">8 unidades</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-700">Lead Time:</span>
                    <span className="font-bold">14 dias</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-700">Safety Stock:</span>
                    <span className="font-bold">20 unidades</span>
                  </div>
                </div>
                
                <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-800">132 unidades</div>
                    <div className="text-sm text-green-600">Ponto de Pedido Atual</div>
                    <div className="text-xs text-green-600 mt-2">Compra recomendada em 3 dias</div>
                  </div>
                </div>
              </div>
              
              {/* Safety Stock Calculator */}
              <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Estoque de Segurança (SS)</h3>
                <div className="bg-yellow-50 p-4 rounded-lg mb-4">
                  <h4 className="text-center text-yellow-800 font-mono mb-2">SS = Z × σ × √LT</h4>
                  <div className="text-center text-gray-600 text-sm">Proteção contra variabilidade da demanda e do fornecedor</div>
                </div>
                
                <div className="mt-4 space-y-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Nível de Serviço</label>
                      <select className="w-full p-2 border border-gray-300 rounded-md">
                        <option value="1.28">90% (Z=1.28)</option>
                        <option value="1.65" selected>95% (Z=1.65)</option>
                        <option value="2.33">99% (Z=2.33)</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Desvio Padrão</label>
                      <input type="number" value="3.2" className="w-full p-2 border border-gray-300 rounded-md" />
                    </div>
                  </div>
                </div>
                
                <div className="bg-yellow-100 p-4 rounded-lg">
                  <div className="text-center">
                    <div className="text-xl font-bold text-yellow-800">42 unidades</div>
                    <div className="text-sm text-yellow-600">Safety Stock Calculado</div>
                    <div className="text-xs text-yellow-600 mt-2">Protege para 95% dos riscos</div>
                  </div>
                </div>
              </div>
              
              {/* MAPE Display */}
              <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">MAPE - Precisão da Previsão</h3>
                <div className="bg-green-50 p-4 rounded-lg mb-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-800">10.5%</div>
                    <div className="text-sm text-green-600">MAPE Atual</div>
                    <div className="text-xs text-green-600 mt-2">Meta: &lt;15% | ✅ ABAIXO DA META</div>
                  </div>
                </div>
                
                <div className="mt-4">
                  <h4 className="text-md font-semibold text-gray-800 mb-2">Comparação por Modelo</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span>ARIMA</span>
                      <span className="font-bold text-red-600">12.1%</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Prophet</span>
                      <span className="font-bold text-yellow-600">10.8%</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>LSTM</span>
                      <span className="font-bold text-green-600">8.6%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Insights Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                <h4 className="font-semibold text-gray-900 mb-2">📊 Insights de Precisão</h4>
                <div className="space-y-2 text-sm text-gray-700">
                  <p>• LSTM atingiu 10.5% MAPE, 2x melhor que benchmark 20%</p>
                  <p>• MAPE estável nos últimos 60 dias</p>
                  <p>• Ensemble reduziu erro em 23% vs. modelos individuais</p>
                </div>
              </div>
              
              <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                <h4 className="font-semibold text-gray-900 mb-2">⚠️ Ações Recomendadas</h4>
                <div className="space-y-2 text-sm text-gray-700">
                  <p>• Manter pesos atuais durante estabilidade</p>
                  <p>• Aumentar peso LSTM em cenários de volatilidade</p>
                  <p>• Retreinar mensalmente com dados sazonais</p>
                </div>
              </div>
              
              <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                <h4 className="font-semibold text-gray-900 mb-2">🔗 Navegação Relacionada</h4>
                <div className="space-y-2">
                  <button className="w-full px-3 py-2 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
                    Ver Detalhes Hierárquicos
                  </button>
                  <button className="w-full px-3 py-2 bg-green-600 text-white rounded text-sm hover:bg-green-700 mt-2">
                    Exportar Relatório
                  </button>
                </div>
              </div>
            </div>
            
            {/* Preview of other tabs (disabled for now) */}
            <div className="space-y-6">
              <div className="bg-gray-50 p-8 rounded-lg border border-gray-200">
                <div className="text-center">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">🗺️ Clustering</h3>
                  <p className="text-gray-600 mb-4">Análise de falhas e performance por torre (em breve)</p>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="p-4 bg-white rounded border">
                      <h4 className="font-semibold mb-2">Falhas Elétricas</h4>
                      <div className="text-2xl font-bold text-red-600">47 torres</div>
                      <div className="text-sm text-gray-600">Risco SLA: 23%</div>
                    </div>
                    <div className="p-4 bg-white rounded border">
                      <h4 className="font-semibold mb-2">Corrosão Acelerada</h4>
                      <div className="text-2xl font-bold text-orange-600">23 torres</div>
                      <div className="text-sm text-gray-600">Risco SLA: 31%</div>
                    </div>
                    <div className="p-4 bg-white rounded border">
                      <h4 className="font-semibold mb-2">Performance Consistente</h4>
                      <div className="text-2xl font-bold text-green-600">245 torres</div>
                      <div className="text-sm text-gray-600">Risco SLA: 5%</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-50 p-8 rounded-lg border border-gray-200">
                <div className="text-center">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">🤖 Modelos Ensemble</h3>
                  <p className="text-gray-600 mb-4">Métricas de performance e governança de ML (em breve)</p>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 bg-white rounded border">
                      <h4 className="font-semibold mb-2">Tendência de Precisão</h4>
                      <div className="text-xl font-bold text-blue-600">↑ 8.2%</div>
                      <div className="text-sm text-green-600">Meta Atingida</div>
                    </div>
                    <div className="p-4 bg-white rounded border">
                      <h4 className="font-semibold mb-2">Confiança do Ensemble</h4>
                      <div className="text-xl font-bold text-green-600">0.87</div>
                      <div className="text-sm text-gray-600">Muito Confiável</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
  const [activePage, setActivePage] = useState('Dashboard');
  const [searchTerm, setSearchTerm] = useState('');
  const [analyticsTargetState, setAnalyticsTargetState] = useState<string | null>(null);

  const handlePageChange = (page: string) => {
    setAnalyticsTargetState(null);
    setActivePage(page);
  };

  const handleSelectAlert = (stateId: string) => {
    setAnalyticsTargetState(stateId);
    setActivePage('Análises');
  };

  const renderContent = () => {
    switch (activePage) {
      case 'Dashboard':
        return <Dashboard searchTerm={searchTerm} onSelectAlert={handleSelectAlert} />;
      case 'Relatórios':
        return <Reports searchTerm={searchTerm} />;
      case 'Análises':
        return <Analytics initialSelectedState={analyticsTargetState} />;
      case 'Configurações':
        return <Settings searchTerm={searchTerm} />;
      default:
        return <Dashboard searchTerm={searchTerm} onSelectAlert={handleSelectAlert}/>;
    }
  };

  const currentPageDetails = pageDetails[activePage as keyof typeof pageDetails] || pageDetails['Dashboard'];

  return (
    <ToastProvider>
      <div className="min-h-screen text-brand-lightest-slate font-sans">
        <div className="flex">
          <Sidebar activePage={activePage} setActivePage={handlePageChange} />
          <main className="flex-1 p-4 sm:p-6 lg:p-8">
            <Header
              title={currentPageDetails.title}
              subtitle={currentPageDetails.subtitle}
              searchTerm={searchTerm}
              setSearchTerm={setSearchTerm}
            />
            <div className="mt-6 animate-fade-in-up" key={activePage}>
              {renderContent()}
            </div>
          </main>
        </div>
        <ToastContainer />
      </div>
    </ToastProvider>
  );
}

