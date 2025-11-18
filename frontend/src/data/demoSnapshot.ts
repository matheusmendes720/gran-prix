/**
 * Demo Snapshot - Deterministic Mock Data for Nova Corrente Dashboard
 * Version: 1.0.0
 * Generated: 2025-11-12T09:30:00Z
 * Purpose: Go-Horse Roadshow Demo - Production-ready visuals without backend dependency
 */

// =============================================================================
// GLOBAL INTERFACES
// =============================================================================

export interface KPIData {
  id: string;
  label: string;
  value: number;
  unit: string;
  delta: number;
  deltaType: 'increase' | 'decrease';
  target?: number;
  status?: 'success' | 'warning' | 'critical';
}

export interface ForecastDataPoint {
  date: string;
  actual: number;
  predicted: number;
  upper?: number;
  lower?: number;
  eventId?: string;
}

export interface AlertData {
  id: string;
  severity: 'info' | 'warning' | 'critical';
  title: string;
  message: string;
  daysToStockout?: number;
  recommendation?: string;
  tags?: string[];
  material?: string;
  quantity?: number;
  urgency?: 'immediate' | 'urgent' | 'normal';
}

export interface ExternalDriver {
  factor: string;
  impactPct: number;
  description: string;
  confidence: number;
  timeframe: string;
  trend?: 'increasing' | 'decreasing' | 'stable';
}

export interface ScenarioMatrix {
  budget: number; // -100 to +100
  weather: number; // 0 to 100 (severity)
  currency: number; // -50 to +50 (FX shock)
  sla: number; // 95 to 99.9
  outputs: {
    mape: number;
    stockoutPrevention: number;
    capitalSavings: number;
    roi: number;
    paybackMonths: number;
  };
}

export interface ROIMetrics {
  paybackMonths: number;
  year1ROI: number;
  cumulativeSavings: number;
  annualSavings: number;
  capitalReduction: number;
  slaImprovement: number;
}

export interface GeoInventory {
  id: string;
  name: string;
  lat: number;
  lng: number;
  status: 'operational' | 'at-risk' | 'critical' | 'offline';
  materials: number;
  sla: number;
  lastMaintenance: string;
  riskScore: number;
  clusterId?: string;
}

// =============================================================================
// MAIN TABS INTERFACES (New additions for Formulas, Clustering, Models)
// =============================================================================

export interface FormulaTabConfig {
  id: 'pp' | 'ss' | 'mape' | 'rmse' | 'mae' | 'ensemble';
  title: string;
  latex: string;
  summary: string;
  defaultInputs: Record<string, number>;
  inputs: Array<{
    id: string; 
    label: string; 
    type: 'number' | 'slider' | 'select'; 
    min?: number; 
    max?: number; 
    step?: number; 
    value: number; 
    options?: Array<{ label: string; value: number }>;
  }>;
  resultExpression: string;
  scenarios: Array<{
    name: string; 
    inputs: Record<string, number>; 
    output: number; 
    narrative: string 
  }>;
  chartSeries: Array<{
    label: string;
    color?: string;
    data: Array<{ x: string | number; y: number }>;
  }>;
  insights: string[];
  actions: Array<{ label: string; route: string }>;
}

export interface ClusterConfig {
  clusters: Array<{
    id: string; 
    label: string; 
    type: 'Falha' | 'Performance'; 
    size: number; 
    slaRisk: number; 
    avgDowntime: number; 
    demandImpact: number; 
    color: string;
    narrative: string; 
    recommendedAction: string;
  }>;
  scatterPoints: Array<{ 
    clusterId: string; 
    x: number; 
    y: number; 
    label: string;
    size?: number;
  }>;
  timeline: Array<{
    date: string; 
    clusterId: string; 
    event: string;
  }>;
  table: Array<{
    clusterId: string; 
    material: string; 
    towers: number; 
    penaltyRisk: number; 
    recommendation: string;
  }>;
}

export interface ModelsConfig {
  ensemble: Array<{
    model: string; 
    weight: number; 
    mape: number; 
    rmse: number; 
    mae: number;
    confidence: number;
  }>;
  accuracyTrend: Array<{
    date: string; 
    mape: number; 
    rmse: number;
    targetMAPE?: number;
  }>;
  retraining: Array<{
    date: string; 
    model: string; 
    trigger: string; 
    note: string;
  }>;
  alerts: Array<{
    severity: 'warning' | 'info' | 'critical'; 
    message: string; 
    recommendation: string;
    category: 'drift' | 'performance' | 'volatility';
  }>;
  confidence: { 
    score: number; 
    narrative: string; 
    factors: string[];
  };
}

// =============================================================================
// DETERMINISTIC DEMO DATA
// =============================================================================

export const demoSnapshot = {
  generatedAt: '2025-11-12T09:30:00Z',
  version: '1.0.0-go-horse',
  
  // HERO OVERVIEW
  hero: {
    kpis: [
      { 
        id: 'forecast_accuracy', 
        label: 'Forecast Accuracy', 
        value: 92.7, 
        unit: '%', 
        delta: 2.5, 
        deltaType: 'increase',
        target: 95,
        status: 'success'
      },
      { 
        id: 'stockout_prevention', 
        label: 'Stockout Prevention', 
        value: 80.3, 
        unit: '%', 
        delta: 5.2, 
        deltaType: 'increase',
        target: 90,
        status: 'warning'
      },
      { 
        id: 'capital_savings', 
        label: 'Capital Savings', 
        value: 18.4, 
        unit: '%', 
        delta: 3.1, 
        deltaType: 'increase',
        target: 25,
        status: 'success'
      },
      { 
        id: 'sla_health', 
        label: 'SLA Availability', 
        value: 99.2, 
        unit: '%', 
        delta: 0.4, 
        deltaType: 'increase',
        target: 99.5,
        status: 'success'
      }
    ],
    narrative: 'IA assegura 60% menos rupturas e preserva SLAs 99%+ sob clima extremo.',
    lastUpdated: '2025-11-12T08:15:00Z'
  },

  // DEMAND SERIES
  demandSeries: {
    historical: Array.from({ length: 60 }, (_, i) => {
      const date = new Date(2025, 9, 12 - 59 + i); // 60 days back
      const base = 340;
      const seasonal = Math.sin((i / 60) * 2 * Math.PI) * 50;
      const noise = (Math.random() - 0.5) * 20;
      const value = Math.max(0, base + seasonal + noise);
      
      return {
        date: date.toISOString().split('T')[0],
        actual: Math.round(value),
        predicted: Math.round(value + (Math.random() - 0.5) * 15),
        eventId: i === 45 ? 'storm_001' : i === 30 ? 'carnaval_2025' : undefined
      };
    }),
    forecast: Array.from({ length: 30 }, (_, i) => {
      const date = new Date(2025, 9, 12 + i);
      const base = 340;
      const seasonal = Math.sin(((i + 60) / 60) * 2 * Math.PI) * 50;
      const value = Math.max(0, base + seasonal);
      
      return {
        date: date.toISOString().split('T')[0],
        predicted: Math.round(value),
        upper: Math.round(value + 20),
        lower: Math.round(value - 20)
      };
    })
  },

  // REORDER THRESHOLD
  reorderThreshold: {
    currentStock: 156,
    reorderPoint: 132,
    safetyStock: 20,
    dailyDemand: 8,
    leadTimeDays: 14,
    daysToStockout: 3,
    trend: 'decreasing'
  },

  // ALERTS
  alerts: [
    {
      id: 'alert_001',
      severity: 'critical',
      title: 'Conector Óptico SC/APC',
      message: 'Ruptura em 3 dias; comprar 250 unidades urgentemente',
      daysToStockout: 3,
      recommendation: 'Gerar ordem de compra imediata',
      tags: ['SLA', 'Finance'],
      material: 'Conector Óptico SC/APC',
      quantity: 250,
      urgency: 'immediate'
    },
    {
      id: 'alert_002',
      severity: 'warning',
      title: 'Refrigeração RF',
      message: 'Greve transporte → lead time +12 dias',
      recommendation: 'Aumentar safety stock em 40%',
      tags: ['Logística'],
      urgency: 'urgent'
    },
    {
      id: 'alert_003',
      severity: 'info',
      title: 'Expansão 5G',
      message: '18 cidades novas exigem kits RF em 15 dias',
      recommendation: 'Planejar expansão de inventário',
      tags: ['Crescimento'],
      urgency: 'normal'
    }
  ],

  // EXTERNAL DRIVERS
  externalDrivers: [
    {
      factor: 'Rainfall',
      impactPct: 18,
      description: 'Chuva >50mm: +40% demanda estrutural',
      confidence: 0.87,
      timeframe: 'Próximos 7 dias',
      trend: 'increasing'
    },
    {
      factor: 'USD/BRL Volatility',
      impactPct: 12,
      description: 'Câmbio variou 11% em 30 dias',
      confidence: 0.92,
      timeframe: 'Este mês',
      trend: 'increasing'
    },
    {
      factor: '5G Rollout',
      impactPct: 9,
      description: 'Cobertura 5G libera upgrades planejados',
      confidence: 0.95,
      timeframe: 'Próximos 30 dias',
      trend: 'stable'
    },
    {
      factor: 'SLA Renewal Cycle',
      impactPct: 15,
      description: 'Jan/Jul renovação aumenta preventivas em 30%',
      confidence: 0.89,
      timeframe: 'Próximo trimestre',
      trend: 'stable'
    }
  ],

  // SCENARIO MATRIX
  scenarioMatrix: {
    // Function to calculate outputs based on inputs
    calculate: (budget: number, weather: number, currency: number, sla: number) => {
      const baseMAPE = 10.5;
      const baseStockout = 75;
      const baseSavings = 15;
      
      const weatherImpact = weather * 0.3; // Weather severity affects MAPE
      const currencyImpact = Math.abs(currency) * 0.1; // FX volatility affects performance
      const slaImpact = (100 - sla) * 0.5; // Higher SLA = higher cost
      
      const mape = Math.max(5, baseMAPE + weatherImpact + currencyImpact);
      const stockoutPrevention = Math.min(95, baseStockout - weatherImpact + slaImpact);
      const capitalSavings = baseSavings + (budget > 0 ? budget * 0.05 : -budget * 0.03);
      const roi = (stockoutPrevention * capitalSavings) / 100;
      
      return {
        mape: Math.round(mape * 10) / 10,
        stockoutPrevention: Math.round(stockoutPrevention),
        capitalSavings: Math.round(capitalSavings),
        roi: Math.round(roi * 100) / 100,
        paybackMonths: Math.max(0.5, 12 / (roi / 100))
      };
    }
  } as ScenarioMatrix,

  // ROI METRICS
  roi: {
    paybackMonths: 0.8,
    year1ROI: 1.6,
    cumulativeSavings: 280000,
    annualSavings: 56000000, // R$ 56M/ano
    capitalReduction: 20,
    slaImprovement: 2.3
  },

  // GEO INVENTORY
  geoInventory: [
    {
      id: 'tower_001',
      name: 'Torre Salvador Centro',
      lat: -12.9714,
      lng: -38.5014,
      status: 'operational',
      materials: 156,
      sla: 99.8,
      lastMaintenance: '2025-10-15',
      riskScore: 15,
      clusterId: 'cluster_performance_a'
    },
    {
      id: 'tower_002',
      name: 'Torre Feira de Santana',
      lat: -12.5668,
      lng: -38.9568,
      status: 'at-risk',
      materials: 89,
      sla: 98.5,
      lastMaintenance: '2025-09-20',
      riskScore: 67,
      clusterId: 'cluster_failure_b'
    },
    {
      id: 'tower_003',
      name: 'Torre Vitória',
      lat: -20.2976,
      lng: -40.2957,
      status: 'operational',
      materials: 134,
      sla: 99.2,
      lastMaintenance: '2025-11-01',
      riskScore: 23,
      clusterId: 'cluster_performance_a'
    },
    {
      id: 'tower_004',
      name: 'Torre Aracaju',
      lat: -10.9095,
      lng: -37.0748,
      status: 'critical',
      materials: 45,
      sla: 96.8,
      lastMaintenance: '2025-08-10',
      riskScore: 89,
      clusterId: 'cluster_failure_a'
    },
    {
      id: 'tower_005',
      name: 'Torre Maceió',
      lat: -9.6658,
      lng: -35.7352,
      status: 'at-risk',
      materials: 112,
      sla: 98.9,
      lastMaintenance: '2025-10-28',
      riskScore: 45,
      clusterId: 'cluster_performance_b'
    },
    {
      id: 'tower_006',
      name: 'Torre Recife',
      lat: -8.0476,
      lng: -34.8770,
      status: 'operational',
      materials: 178,
      sla: 99.6,
      lastMaintenance: '2025-11-05',
      riskScore: 12,
      clusterId: 'cluster_performance_b'
    }
  ],

  // MAIN TABS DATA (New additions for Formulas, Clustering, Models)
  mainTabs: {
    formulas: {
      pp: {
        id: 'pp',
        title: 'Ponto de Pedido (PP)',
        latex: 'PP = (D \\times LT) + SS',
        summary: 'Calcula o nível de estoque ideal para acionar compras antes da ruptura',
        defaultInputs: {
          demand: 8,
          leadTime: 14,
          safetyStock: 20,
          reliability: 1.0
        },
        inputs: [
          {
            id: 'demand',
            label: 'Demanda Diária',
            type: 'number',
            value: 8,
            min: 1,
            max: 100,
            step: 1
          },
          {
            id: 'leadTime',
            label: 'Lead Time (dias)',
            type: 'number',
            value: 14,
            min: 1,
            max: 90,
            step: 1
          },
          {
            id: 'safetyStock',
            label: 'Safety Stock',
            type: 'slider',
            value: 20,
            min: 0,
            max: 200,
            step: 5
          },
          {
            id: 'reliability',
            label: 'Confiabilidade do Fornecedor',
            type: 'slider',
            value: 1.0,
            min: 0.8,
            max: 1.2,
            step: 0.05
          }
        ],
        resultExpression: '(demand * leadTime * reliability) + safetyStock',
        scenarios: [
          {
            name: 'Base',
            inputs: { demand: 8, leadTime: 14, safetyStock: 20, reliability: 1.0 },
            output: 132,
            narrative: 'Condições normais de operação'
          },
          {
            name: 'Chuva Forte',
            inputs: { demand: 8, leadTime: 17, safetyStock: 35, reliability: 0.9 },
            output: 149,
            narrative: 'Chuva intensa aumenta lead time e necessidade de buffer'
          },
          {
            name: 'Expansão 5G',
            inputs: { demand: 12, leadTime: 14, safetyStock: 25, reliability: 0.95 },
            output: 194,
            narrative: 'Expansão de cobertura eleva demanda em 50%'
          }
        ],
        chartSeries: [
          {
            label: 'Projeção de Estoque',
            color: '#0CD1A0',
            data: Array.from({ length: 21 }, (_, i) => ({
              x: i,
              y: Math.max(0, 156 - (8 * i))
            }))
          },
          {
            label: 'Ponto de Pedido',
            color: '#FFB03A',
            data: Array.from({ length: 21 }, () => ({ x: 0, y: 132 }))
          }
        ],
        insights: [
          'Alerta de compra disparará em 3 dias',
          'Safety stock atual cobre 95% das variações',
          'Fornecedor confiável sem ajustes necessários'
        ],
        actions: [
          { label: 'Ver Fornecedores', route: '/features/lead-time' },
          { label: 'Criar Ordem de Compra', route: '/main/prescritivo' }
        ]
      } as FormulaTabConfig,

      ss: {
        id: 'ss',
        title: 'Estoque de Segurança (SS)',
        latex: 'SS = Z \\times \\sigma \\times \\sqrt{LT}',
        summary: 'Proteção contra variabilidade da demanda e do fornecedor',
        defaultInputs: {
          z: 1.65,
          sigma: 3.2,
          leadTime: 14,
          demandVariance: 1.2
        },
        inputs: [
          {
            id: 'z',
            label: 'Fator Z (Nível de Serviço)',
            type: 'select',
            value: 1.65,
            options: [
              { label: '90% (Z=1.28)', value: 1.28 },
              { label: '95% (Z=1.65)', value: 1.65 },
              { label: '99% (Z=2.33)', value: 2.33 }
            ]
          },
          {
            id: 'sigma',
            label: 'Desvio Padrão da Demanda',
            type: 'slider',
            value: 3.2,
            min: 0.5,
            max: 10,
            step: 0.1
          },
          {
            id: 'leadTime',
            label: 'Lead Time (dias)',
            type: 'number',
            value: 14,
            min: 1,
            max: 90
          },
          {
            id: 'demandVariance',
            label: 'Variabilidade da Demanda',
            type: 'slider',
            value: 1.2,
            min: 0.5,
            max: 3,
            step: 0.1
          }
        ],
        resultExpression: 'z * sigma * Math.sqrt(leadTime) * demandVariance',
        scenarios: [
          {
            name: 'Base',
            inputs: { z: 1.65, sigma: 3.2, leadTime: 14, demandVariance: 1.2 },
            output: 23,
            narrative: 'Nível de serviço 95% com variabilidade atual'
          },
          {
            name: 'Alta Volatilidade',
            inputs: { z: 1.65, sigma: 5.8, leadTime: 14, demandVariance: 2.1 },
            output: 47,
            narrative: 'Volatilidade elevada exige buffer maior'
          }
        ],
        chartSeries: [
          {
            label: 'Capital vs. Proteção',
            color: '#1B2A4B',
            data: [
              { x: 0, y: 23 },
              { x: 1, y: 35 },
              { x: 2, y: 47 }
            ]
          }
        ],
        insights: [
          'Safety stock atual protege contra 95% dos riscos',
          'Aumento de volatilidade eleva capital em 104%',
          'Considerar upgrade para 99% de serviço'
        ],
        actions: [
          { label: 'Ajustar Estoque', route: '/main/analises-aprofundadas' },
          { label: 'Exportar Cálculo', route: '#' }
        ]
      } as FormulaTabConfig,

      mape: {
        id: 'mape',
        title: 'MAPE (Mean Absolute Percentage Error)',
        latex: 'MAPE = \\frac{1}{n} \\sum |\\frac{|A_t - F_t|}{A_t}| \\times 100',
        summary: 'Precisão média das previsões em percentual',
        defaultInputs: {
          horizon: 30,
          segment: 'global'
        },
        inputs: [
          {
            id: 'horizon',
            label: 'Horizonte (dias)',
            type: 'select',
            value: 30,
            options: [
              { label: '7 dias', value: 7 },
              { label: '30 dias', value: 30 },
              { label: '60 dias', value: 60 }
            ]
          },
          {
            id: 'segment',
            label: 'Segmento',
            type: 'select',
            value: 'global',
            options: [
              { label: 'Global', value: 'global' },
              { label: 'Conectores', value: 'conectores' },
              { label: 'Torretas', value: 'torretas' }
            ]
          }
        ],
        resultExpression: '10.5',
        scenarios: [
          {
            name: 'Atual',
            inputs: { horizon: 30, segment: 'global' },
            output: 10.5,
            narrative: 'MAPE atual de 10.5% está acima da meta'
          },
          {
            name: 'Carnaval',
            inputs: { horizon: 7, segment: 'conectores' },
            output: 8.2,
            narrative: 'Período de Carnaval melhora precisão para 8.2%'
          }
        ],
        chartSeries: [
          {
            label: 'Real vs. Previsto',
            color: '#0CD1A0',
            data: Array.from({ length: 30 }, (_, i) => {
              const real = 340 + Math.sin((i / 30) * 2 * Math.PI) * 30;
              const pred = real + (Math.random() - 0.5) * 40;
              return { x: i, y: Math.abs(real - pred) / real * 100 };
            })
          }
        ],
        insights: [
          'LSTM alcançou 10.5% MAPE, 2x melhor que benchmark 20%',
          'Precisão por segmento: Conectores 8.2%, Torretas 12.1%',
          'MAPE estável nos últimos 60 dias'
        ],
        actions: [
          { label: 'Ver Detalhes', route: '/features/hierarchical' },
          { label: 'Relatório de Precisão', route: '#' }
        ]
      } as FormulaTabConfig
    },

    clustering: {
      clusters: [
        {
          id: 'cluster_failure_a',
          label: 'Falhas Elétricas',
          type: 'Falha',
          size: 47,
          slaRisk: 0.23,
          avgDowntime: 4.2,
          demandImpact: 0.18,
          color: '#FFB03A',
          narrative: 'Cluster crítico de falhas elétricas durante temporadas chuvosas',
          recommendedAction: 'Agendar inspeção preventiva em 15 dias'
        },
        {
          id: 'cluster_failure_b',
          label: 'Corrosão Acelerada',
          type: 'Falha',
          size: 23,
          slaRisk: 0.31,
          avgDowntime: 6.8,
          demandImpact: 0.25,
          color: '#E11D48',
          narrative: 'Alta umidade em regiões litorâneas acelera corrosão',
          recommendedAction: 'Aumentar estoque de anticorrosivos em 40%'
        },
        {
          id: 'cluster_performance_a',
          label: 'Alta Performance',
          type: 'Performance',
          size: 156,
          slaRisk: 0.02,
          avgDowntime: 0.8,
          demandImpact: 0.05,
          color: '#10B981',
          narrative: 'Torres com performance consistente e SLA estável',
          recommendedAction: 'Manter plano de manutenção atual'
        },
        {
          id: 'cluster_performance_b',
          label: 'Performance Moderada',
          type: 'Performance',
          size: 89,
          slaRisk: 0.08,
          avgDowntime: 2.1,
          demandImpact: 0.12,
          color: '#F59E0B',
          narrative: 'Torres operacionais com risco moderado de degradação',
          recommendedAction: 'Monitorar indicadores de performance'
        }
      ],
      scatterPoints: [
        { clusterId: 'cluster_failure_a', x: 12, y: 4.2, label: 'Falhas Elétricas', size: 47 },
        { clusterId: 'cluster_failure_b', x: 23, y: 6.8, label: 'Corrosão', size: 23 },
        { clusterId: 'cluster_performance_a', x: 3, y: 0.8, label: 'Alta Performance', size: 156 },
        { clusterId: 'cluster_performance_b', x: 8, y: 2.1, label: 'Performance Moderada', size: 89 }
      ],
      timeline: [
        { date: '2025-10-15', clusterId: 'cluster_failure_a', event: 'Início temporada chuvosa' },
        { date: '2025-10-28', clusterId: 'cluster_failure_b', event: 'Pico de umidade' },
        { date: '2025-11-05', clusterId: 'cluster_performance_a', event: 'Manutenção preventiva concluída' }
      ],
      table: [
        { clusterId: 'cluster_failure_a', material: 'Conectores Ópticos', towers: 12, penaltyRisk: 23000, recommendation: 'Inspeção quinzenal' },
        { clusterId: 'cluster_failure_b', material: 'Anticorrosivos', towers: 8, penaltyRisk: 15000, recommendation: 'Aumentar estoque' },
        { clusterId: 'cluster_performance_a', material: 'Kits RF', towers: 67, penaltyRisk: 2000, recommendation: 'Manutenção padrão' },
        { clusterId: 'cluster_performance_b', material: 'Estruturas', towers: 34, penaltyRisk: 8000, recommendation: 'Monitoramento' }
      ]
    } as ClusterConfig,

    models: {
      ensemble: [
        { model: 'ARIMA', weight: 0.30, mape: 12.1, rmse: 28.4, mae: 19.2, confidence: 0.85 },
        { model: 'Prophet', weight: 0.30, mape: 10.8, rmse: 24.7, mae: 17.3, confidence: 0.89 },
        { model: 'LSTM', weight: 0.40, mape: 9.2, rmse: 21.3, mae: 15.8, confidence: 0.92 }
      ],
      accuracyTrend: Array.from({ length: 90 }, (_, i) => {
        const date = new Date(2025, 7, 12 - 89 + i);
        const baseMAPE = 11.5;
        const improvement = i * 0.015; // Gradual improvement
        const mape = Math.max(8, baseMAPE - improvement + (Math.random() - 0.5) * 1.5);
        
        return {
          date: date.toISOString().split('T')[0],
          mape: Math.round(mape * 10) / 10,
          rmse: Math.round(mape * 2.7),
          targetMAPE: 10.0
        };
      }),
      retraining: [
        { date: '2025-09-15', model: 'LSTM', trigger: 'Scheduled retraining', note: 'Monthly cadence maintained' },
        { date: '2025-10-20', model: 'Ensemble', trigger: 'Data drift detected', note: 'FX volatility > 10%' },
        { date: '2025-11-01', model: 'Prophet', trigger: 'Seasonality adjustment', note: 'Carnaval effect incorporated' }
      ],
      alerts: [
        { severity: 'warning', message: 'FX volatility > 10% - Consider increasing LSTM weight', recommendation: 'Ajustar pesos do ensemble', category: 'volatility' },
        { severity: 'info', message: 'Model confidence stable above 0.85', recommendation: 'Manter cadência de retreinamento', category: 'performance' },
        { severity: 'critical', message: 'RMSE spike detected on cluster A', recommendation: 'Investigar fontes de dados', category: 'drift' }
      ],
      confidence: { 
        score: 0.87, 
        narrative: 'Confiabilidade alta: MAPE <12%, RMSE estável, ensemble bem balanceado', 
        factors: ['Precisão <12%', 'RMSE estável', 'Pesos otimizados']
      }
    } as ModelsConfig
  }
};

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

export const loadMainTabs = () => demoSnapshot.mainTabs;
export const loadHeroKPIs = () => demoSnapshot.hero.kpis;
export const loadDemandSeries = () => demoSnapshot.demandSeries;
export const loadAlerts = () => demoSnapshot.alerts;
export const loadScenarioMatrix = () => demoSnapshot.scenarioMatrix;
export const loadROIMetrics = () => demoSnapshot.roi;
export const loadGeoInventory = () => demoSnapshot.geoInventory;

export const getFormulaById = (id: string): FormulaTabConfig | undefined => {
  return demoSnapshot.mainTabs.formulas[id as keyof typeof demoSnapshot.mainTabs.formulas];
};

export const getClusterById = (id: string): any => {
  return demoSnapshot.mainTabs.clustering.clusters.find(c => c.id === id);
};

export const getModelWeights = () => demoSnapshot.mainTabs.models.ensemble;