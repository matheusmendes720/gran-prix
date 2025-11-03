import { http, HttpResponse } from 'msw';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

// Mock health endpoint
const healthHandler = http.get(`${API_BASE_URL}/health`, () => {
  return HttpResponse.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    service: 'nova-corrente-api',
  });
});

// Mock feature endpoints - Temporal
const temporalFeaturesHandler = http.get(`${API_BASE_URL}/api/v1/features/temporal`, ({ request }) => {
  const url = new URL(request.url);
  // Check for invalid params
  if (url.searchParams.get('limit') === 'invalid') {
    return HttpResponse.json(
      { detail: 'Validation error' },
      { status: 422 }
    );
  }
  
  return HttpResponse.json({
    status: 'success',
    data: [
      {
        material_id: 1,
        data_referencia: '2025-01-01',
        day_of_week: 1,
        day_of_month: 1,
        week_of_year: 1,
        month: 1,
        quarter: 1,
        is_weekend: false,
        is_holiday: true,
        days_since_start: 0,
      },
    ],
    metadata: {
      total_count: 1,
      last_updated: new Date().toISOString(),
    },
  });
});

const temporalCalendarHandler = http.get(`${API_BASE_URL}/api/v1/features/temporal/calendar`, () => {
  return HttpResponse.json([
    {
      data_referencia: '2025-01-01',
      is_feriado: true,
      tipo_feriado: 'Nacional',
      nome_feriado: 'Confraternização Universal',
    },
  ]);
});

// Mock feature endpoints - Climate
const climateFeaturesHandler = http.get(`${API_BASE_URL}/api/v1/features/climate`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [
      {
        material_id: 1,
        data_referencia: '2025-01-01',
        temperatura_media: 28.5,
        precipitacao_mm: 150.0,
        umidade_relativa: 75.0,
      },
    ],
    metadata: {
      total_count: 1,
      last_updated: new Date().toISOString(),
    },
  });
});

const climateSalvadorHandler = http.get(`${API_BASE_URL}/api/v1/features/climate/salvador`, () => {
  return HttpResponse.json([
    {
      data_referencia: '2025-01-01',
      temperatura_media: 28.5,
      precipitacao_mm: 150.0,
      umidade_relativa: 75.0,
    },
  ]);
});

const climateRisksHandler = http.get(`${API_BASE_URL}/api/v1/features/climate/risks`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [],
  });
});

// Mock feature endpoints - Economic
const economicFeaturesHandler = http.get(`${API_BASE_URL}/api/v1/features/economic`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [
      {
        material_id: 1,
        data_referencia: '2025-01-01',
        inflation_rate: 0.04,
        exchange_rate_brl_usd: 5.2,
        gdp_growth_rate: 0.02,
        selic_rate: 0.11,
      },
    ],
    metadata: {
      total_count: 1,
      last_updated: new Date().toISOString(),
    },
  });
});

const bacenIndicatorsHandler = http.get(`${API_BASE_URL}/api/v1/features/economic/bacen`, () => {
  return HttpResponse.json([
    {
      data_referencia: '2025-01-01',
      ipca: 0.04,
      cambio_usd_brl: 5.2,
      selic_percent: 0.11,
      pib_variacao: 0.02,
    },
  ]);
});

// Mock feature endpoints - 5G
const fivegFeaturesHandler = http.get(`${API_BASE_URL}/api/v1/features/5g`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [
      {
        material_id: 1,
        data_referencia: '2025-01-01',
        towers_5g: 1000,
        coverage_percent: 45.0,
      },
    ],
    metadata: {
      total_count: 1,
      last_updated: new Date().toISOString(),
    },
  });
});

const fivegExpansionHandler = http.get(`${API_BASE_URL}/api/v1/features/5g/expansion`, () => {
  return HttpResponse.json([
    {
      data_referencia: '2025-01-01',
      towers_5g: 1000,
      coverage_percent: 45.0,
    },
  ]);
});

const fivegMilestonesHandler = http.get(`${API_BASE_URL}/api/v1/features/5g/milestones`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [],
  });
});

const fivegDemandImpactHandler = http.get(`${API_BASE_URL}/api/v1/features/5g/demand-impact`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [],
  });
});

// Mock feature endpoints - Lead Time
const leadTimeFeaturesHandler = http.get(`${API_BASE_URL}/api/v1/features/lead-time`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [
      {
        material_id: 1,
        supplier_id: 1,
        lead_time_days: 30,
        lead_time_std: 5.0,
      },
    ],
    metadata: {
      total_count: 1,
      last_updated: new Date().toISOString(),
    },
  });
});

const supplierLeadTimesHandler = http.get(`${API_BASE_URL}/api/v1/features/lead-time/suppliers`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [],
  });
});

// Mock feature endpoints - SLA
const slaFeaturesHandler = http.get(`${API_BASE_URL}/api/v1/features/sla`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [
      {
        material_id: 1,
        tier_nivel: 'TIER1',
        availability_target: 0.99,
        sla_penalty_brl: 1000.0,
      },
    ],
    metadata: {
      total_count: 1,
      last_updated: new Date().toISOString(),
    },
  });
});

const slaPenaltiesHandler = http.get(`${API_BASE_URL}/api/v1/features/sla/penalties`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [],
  });
});

const slaViolationsHandler = http.get(`${API_BASE_URL}/api/v1/features/sla/violations`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [],
  });
});

// Mock feature endpoints - Hierarchical
const hierarchicalFeaturesHandler = http.get(`${API_BASE_URL}/api/v1/features/hierarchical`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [
      {
        material_id: 1,
        family_demand_ma_7: 100.0,
        family_demand_ma_30: 95.0,
        site_demand_ma_7: 50.0,
        supplier_frequency: 10.0,
      },
    ],
    metadata: {
      total_count: 1,
      last_updated: new Date().toISOString(),
    },
  });
});

const familyAggregationsHandler = http.get(`${API_BASE_URL}/api/v1/features/hierarchical/family`, () => {
  return HttpResponse.json([
    {
      familia_id: 1,
      familia_nome: 'Test Family',
      total_movimentacoes: 100,
      demanda_media_7d: 50.0,
      demanda_media_30d: 45.0,
      total_materiais: 10,
    },
  ]);
});

const siteAggregationsHandler = http.get(`${API_BASE_URL}/api/v1/features/hierarchical/site`, () => {
  return HttpResponse.json([
    {
      site_id: 'SITE001',
      total_movimentacoes: 50,
      demanda_media_7d: 25.0,
      demanda_media_30d: 20.0,
      total_materiais: 5,
    },
  ]);
});

const supplierAggregationsHandler = http.get(`${API_BASE_URL}/api/v1/features/hierarchical/supplier`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [
      {
        fornecedor_id: 1,
        fornecedor_nome: 'Test Supplier',
        supplier_frequency: 20.0,
        supplier_lead_time_mean: 30.0,
        supplier_lead_time_std: 5.0,
      },
    ],
    metadata: {
      total_count: 1,
      last_updated: new Date().toISOString(),
    },
  });
});

// Mock feature endpoints - Categorical
const categoricalFeaturesHandler = http.get(`${API_BASE_URL}/api/v1/features/categorical`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [
      {
        material_id: 1,
        familia: 'Test Family',
        familia_encoded: 1,
        deposito: 'DEP001',
        site_id: 'SITE001',
        fornecedor: 'Test Supplier',
      },
    ],
    metadata: {
      total_count: 1,
      last_updated: new Date().toISOString(),
    },
  });
});

const familyEncodingsHandler = http.get(`${API_BASE_URL}/api/v1/features/categorical/families`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [],
  });
});

const siteEncodingsHandler = http.get(`${API_BASE_URL}/api/v1/features/categorical/sites`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [],
  });
});

const supplierEncodingsHandler = http.get(`${API_BASE_URL}/api/v1/features/categorical/suppliers`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [],
  });
});

// Mock feature endpoints - Business
const businessFeaturesHandler = http.get(`${API_BASE_URL}/api/v1/features/business`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [
      {
        material_id: 1,
        material: 'Test Material',
        produto_servico: 'PRODUCT',
        quantidade: 100,
        unidade_medida: 'UN',
      },
    ],
    metadata: {
      total_count: 1,
      last_updated: new Date().toISOString(),
    },
  });
});

const top5FamiliesHandler = http.get(`${API_BASE_URL}/api/v1/features/business/top5-families`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [],
  });
});

const tierAnalyticsHandler = http.get(`${API_BASE_URL}/api/v1/features/business/tiers`, () => {
  return HttpResponse.json({
    status: 'success',
    data: [],
  });
});

// Error handlers
const invalidEndpointHandler = http.get(`${API_BASE_URL}/api/v1/features/invalid-endpoint`, () => {
  return HttpResponse.json(
    { detail: 'Not Found' },
    { status: 404 }
  );
});

// Invalid params handler is now integrated into temporalFeaturesHandler

export const handlers = [
  healthHandler,
  temporalFeaturesHandler,
  temporalCalendarHandler,
  climateFeaturesHandler,
  climateSalvadorHandler,
  climateRisksHandler,
  economicFeaturesHandler,
  bacenIndicatorsHandler,
  fivegFeaturesHandler,
  fivegExpansionHandler,
  fivegMilestonesHandler,
  fivegDemandImpactHandler,
  leadTimeFeaturesHandler,
  supplierLeadTimesHandler,
  slaFeaturesHandler,
  slaPenaltiesHandler,
  slaViolationsHandler,
  hierarchicalFeaturesHandler,
  familyAggregationsHandler,
  siteAggregationsHandler,
  supplierAggregationsHandler,
  categoricalFeaturesHandler,
  familyEncodingsHandler,
  siteEncodingsHandler,
  supplierEncodingsHandler,
  businessFeaturesHandler,
  top5FamiliesHandler,
  tierAnalyticsHandler,
  invalidEndpointHandler,
];

