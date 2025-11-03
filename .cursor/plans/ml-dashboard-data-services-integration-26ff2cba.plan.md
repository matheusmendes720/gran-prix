<!-- 26ff2cba-65ea-418c-b541-da7102ca5d20 53249d13-b431-43d4-a98b-fcd255596fca -->
# ML Dashboard Data Services Integration

Transform the dashboard into an intelligent, real-time ML feature visualization platform connecting to the ML-ready database with interactive charts, drill-down capabilities, and advanced data storytelling.

## Architecture Overview

### Backend API Layer Extensions

**Location:** `backend/app/api/v1/routes/`

New API endpoints organized by ML feature categories:

#### 1. Temporal Features API (`temporal_features.py`)

- `GET /api/v1/features/temporal` - Get temporal features for materials
- `GET /api/v1/features/temporal/{material_id}` - Get temporal features for specific material
- `GET /api/v1/features/temporal/calendar` - Get Brazilian calendar features (holidays, carnival, etc.)
- `GET /api/v1/features/temporal/cyclical` - Get cyclical encoding (sin/cos) features

**Data Sources:**

- `CalendarioBrasil` table
- `MaterialFeatures` where `feature_category = 'TEMPORAL'`
- `vw_material_time_series_brasil` view

#### 2. Climate Features API (`climate_features.py`)

- `GET /api/v1/features/climate` - Get climate features
- `GET /api/v1/features/climate/salvador` - Get Salvador/BA climate data
- `GET /api/v1/features/climate/risks` - Get calculated climate risks (corrosion, field work disruption)
- `GET /api/v1/features/climate/trends` - Get climate trends over time

**Data Sources:**

- `ClimaSalvador` table
- `MaterialFeatures` where `feature_category = 'CLIMATE'`

#### 3. Economic Features API (`economic_features.py`)

- `GET /api/v1/features/economic` - Get economic indicators
- `GET /api/v1/features/economic/bacen` - Get BACEN indicators (inflation, exchange, GDP, SELIC)
- `GET /api/v1/features/economic/trends` - Get economic trends over time
- `GET /api/v1/features/economic/impacts` - Get calculated economic impacts

**Data Sources:**

- `IndicadoresEconomicos` table
- `MaterialFeatures` where `feature_category = 'ECONOMIC'`

#### 4. 5G Features API (`5g_features.py`)

- `GET /api/v1/features/5g` - Get 5G expansion features
- `GET /api/v1/features/5g/expansion` - Get 5G expansion metrics (coverage, investment)
- `GET /api/v1/features/5g/milestones` - Get 5G expansion milestones
- `GET /api/v1/features/5g/demand-impact` - Get 5G impact on material demand

**Data Sources:**

- `Expansao5G` table
- `MaterialFeatures` where `feature_category = '5G'`

#### 5. Lead Time Features API (`lead_time_features.py`)

- `GET /api/v1/features/lead-time` - Get lead time features
- `GET /api/v1/features/lead-time/suppliers` - Get supplier lead time analytics
- `GET /api/v1/features/lead-time/materials` - Get material-specific lead times
- `GET /api/v1/features/lead-time/risks` - Get lead time risk indicators

**Data Sources:**

- `Fornecedor`, `Fornecedor_Material` tables
- `MaterialFeatures` where `feature_category = 'LEAD_TIME'`

#### 6. SLA Features API (`sla_features.py`)

- `GET /api/v1/features/sla` - Get SLA features
- `GET /api/v1/features/sla/penalties` - Get SLA penalties by material/tier
- `GET /api/v1/features/sla/availability` - Get availability targets and actuals
- `GET /api/v1/features/sla/violations` - Get SLA violation risks

**Data Sources:**

- `Material` table (tier_nivel, sla_penalty_brl, disponibilidade_target)
- `MaterialFeatures` where `feature_category = 'SLA'`

#### 7. Hierarchical Features API (`hierarchical_features.py`)

- `GET /api/v1/features/hierarchical` - Get hierarchical aggregations
- `GET /api/v1/features/hierarchical/family` - Get family-level aggregations
- `GET /api/v1/features/hierarchical/site` - Get site/tower-level aggregations
- `GET /api/v1/features/hierarchical/supplier` - Get supplier-level aggregations

**Data Sources:**

- `MaterialFeatures` where `feature_category = 'HIERARCHICAL'`
- `MovimentacaoEstoque` with aggregations by family/site/supplier

#### 8. Categorical Features API (`categorical_features.py`)

- `GET /api/v1/features/categorical` - Get categorical features
- `GET /api/v1/features/categorical/families` - Get family encodings
- `GET /api/v1/features/categorical/sites` - Get site encodings
- `GET /api/v1/features/categorical/suppliers` - Get supplier encodings

**Data Sources:**

- `MaterialFeatures` where `feature_category = 'CATEGORICAL'`
- `Familia`, `Material`, `Fornecedor` tables

#### 9. Business Features API (`business_features.py`)

- `GET /api/v1/features/business` - Get Nova Corrente business features
- `GET /api/v1/features/business/top5-families` - Get top 5 families statistics
- `GET /api/v1/features/business/tiers` - Get tier-based analytics
- `GET /api/v1/features/business/materials` - Get material business context

**Data Sources:**

- `MaterialFeatures` where `feature_category = 'BUSINESS'`
- `vw_top5_familias_nova_corrente` view
- `Material` table with tier information

### Frontend Pages & Routes

**Location:** `frontend/src/app/`

New pages organized by feature categories:

#### Page Structure

```
/app/
  /features/
    /temporal/page.tsx          - Temporal features dashboard
    /climate/page.tsx            - Climate features dashboard
    /economic/page.tsx           - Economic features dashboard
    /5g/page.tsx                 - 5G features dashboard
    /lead-time/page.tsx          - Lead time features dashboard
    /sla/page.tsx                - SLA features dashboard
    /hierarchical/page.tsx       - Hierarchical features dashboard
    /categorical/page.tsx        - Categorical features dashboard
    /business/page.tsx           - Business features dashboard
  /material/[id]/page.tsx        - Material detail with all features
```

### Interactive Chart Components

**Location:** `frontend/src/components/charts/`

New intelligent chart components:

#### 1. Time Series Charts

- `TemporalFeaturesChart.tsx` - Brazilian calendar, cyclical encoding visualization
- `ClimateTimeSeriesChart.tsx` - Climate trends over time with risk indicators
- `EconomicTimeSeriesChart.tsx` - Economic indicators trends
- `5GExpansionChart.tsx` - 5G coverage and investment trends

#### 2. Hierarchical Charts

- `FamilyDemandChart.tsx` - Family-level demand aggregations with drill-down
- `SiteDemandChart.tsx` - Site/tower-level aggregations with drill-down
- `SupplierPerformanceChart.tsx` - Supplier lead time and performance metrics

#### 3. Comparative Charts

- `TierComparisonChart.tsx` - TIER_1/2/3 comparison with SLA metrics
- `Top5FamiliesChart.tsx` - Top 5 families comparison
- `LeadTimeCategoryChart.tsx` - Lead time distribution by category

#### 4. Risk & Impact Charts

- `ClimateRiskHeatmap.tsx` - Corrosion risk, field work disruption heatmap
- `SLAViolationRiskChart.tsx` - SLA violation risk by material/tier
- `LeadTimeRiskChart.tsx` - Lead time risk indicators

#### 5. Interactive Maps

- `ClimateMap.tsx` - Salvador/BA climate visualization
- `SiteMap.tsx` - 18,000+ towers visualization with material demand
- `RegionalDemandMap.tsx` - Regional demand aggregations

### API Client Extensions

**Location:** `frontend/src/lib/api.ts`

Extend ApiClient with methods for all 9 feature categories:

```typescript
// Temporal features
async getTemporalFeatures(materialId?: number): Promise<TemporalFeaturesResponse>
async getBrazilianCalendar(dateRange?: DateRange): Promise<CalendarFeaturesResponse>

// Climate features
async getClimateFeatures(materialId?: number): Promise<ClimateFeaturesResponse>
async getSalvadorClimate(dateRange?: DateRange): Promise<SalvadorClimateResponse>
async getClimateRisks(): Promise<ClimateRisksResponse>

// Economic features
async getEconomicFeatures(dateRange?: DateRange): Promise<EconomicFeaturesResponse>
async getBACENIndicators(): Promise<BACENIndicatorsResponse>

// 5G features
async get5GFeatures(): Promise<FiveGFeaturesResponse>
async get5GExpansion(): Promise<FiveGExpansionResponse>

// Lead time features
async getLeadTimeFeatures(materialId?: number): Promise<LeadTimeFeaturesResponse>
async getSupplierLeadTimes(): Promise<SupplierLeadTimesResponse>

// SLA features
async getSLAFeatures(materialId?: number): Promise<SLAFeaturesResponse>
async getSLAPenalties(): Promise<SLAPenaltiesResponse>
async getSLAViolations(): Promise<SLAViolationsResponse>

// Hierarchical features
async getHierarchicalFeatures(level: 'family' | 'site' | 'supplier'): Promise<HierarchicalFeaturesResponse>
async getFamilyAggregations(familyId?: number): Promise<FamilyAggregationsResponse>
async getSiteAggregations(siteId?: string): Promise<SiteAggregationsResponse>

// Categorical features
async getCategoricalFeatures(): Promise<CategoricalFeaturesResponse>

// Business features
async getBusinessFeatures(): Promise<BusinessFeaturesResponse>
async getTop5Families(): Promise<Top5FamiliesResponse>
async getTierAnalytics(): Promise<TierAnalyticsResponse>
```

### Data Visualization Best Practices

#### 1. Storytelling Components

- **Feature Story Cards** - Explain what each feature category means for Nova Corrente
- **Insight Panels** - Highlight key insights from each feature category
- **Trend Indicators** - Visual indicators for increasing/decreasing trends
- **Risk Alerts** - Prominent alerts for high-risk situations

#### 2. Interactive Features

- **Drill-Down** - Click family → materials → sites → individual towers
- **Filter Panels** - Date ranges, families, tiers, sites, suppliers
- **Comparison Mode** - Compare multiple materials/families side-by-side
- **Export** - Download charts as images/PDF, data as CSV

#### 3. Real-Time Updates

- **WebSocket/SSE** - Real-time updates for critical metrics
- **Auto-Refresh** - Configurable auto-refresh intervals (30s, 1min, 5min)
- **Live Indicators** - Visual indicators showing data freshness

#### 4. Responsive Design

- **Mobile-First** - Optimized for mobile devices
- **Responsive Charts** - Charts adapt to screen size
- **Touch Interactions** - Swipe, pinch, tap gestures for mobile

### TypeScript Types

**Location:** `frontend/src/types/`

New type definitions:

```typescript
// Feature category types
export interface TemporalFeatures {
  year: number;
  month: number;
  day: number;
  weekday: number;
  quarter: number;
  day_of_year: number;
  month_sin: number;
  month_cos: number;
  day_of_year_sin: number;
  day_of_year_cos: number;
  is_weekend: boolean;
  is_holiday: boolean;
  is_carnival: boolean;
  is_verao: boolean;
  is_chuva_sazonal: boolean;
}

export interface ClimateFeatures {
  temperature_avg_c: number;
  precipitation_mm: number;
  humidity_percent: number;
  wind_speed_kmh: number;
  extreme_heat: boolean;
  cold_weather: boolean;
  heavy_rain: boolean;
  no_rain: boolean;
  is_intense_rain: boolean;
  is_high_humidity: boolean;
  corrosion_risk: number; // 0-1
  field_work_disruption: number; // 0-1
}

export interface EconomicFeatures {
  inflation_rate: number;
  exchange_rate_brl_usd: number;
  gdp_growth_rate: number;
  selic_rate: number;
  high_inflation: boolean;
  currency_devaluation: boolean;
}

export interface FiveGFeatures {
  '5g_coverage_pct': number;
  '5g_investment_brl_billions': number;
  is_5g_milestone: boolean;
  is_5g_active: boolean;
  '5g_expansion_rate': number;
}

export interface LeadTimeFeatures {
  lead_time_days: number;
  base_lead_time_days: number;
  total_lead_time_days: number;
  customs_delay_days: number;
  strike_risk: number;
  is_critical_lead_time: boolean;
  lead_time_category: 'FAST' | 'NORMAL' | 'SLOW' | 'VERY_SLOW';
  supplier_lead_time_mean: number;
  supplier_lead_time_std: number;
}

export interface SLAFeatures {
  sla_penalty_brl: number;
  availability_target: number;
  downtime_hours_monthly: number;
  sla_violation_risk: number;
}

export interface HierarchicalFeatures {
  family_demand_ma_7: number;
  family_demand_ma_30: number;
  family_demand_std_7: number;
  family_demand_std_30: number;
  family_frequency: number;
  site_demand_ma_7: number;
  site_demand_ma_30: number;
  site_frequency: number;
  supplier_frequency: number;
}

export interface CategoricalFeatures {
  familia: string;
  familia_encoded: number;
  deposito: string;
  site_id: string;
  fornecedor: string;
}

export interface BusinessFeatures {
  item_id: string;
  material: string;
  produto_servico: string;
  quantidade: number;
  unidade_medida: string;
  solicitacao: string;
  data_requisitada: Date;
  data_solicitado: Date;
  data_compra: Date;
}

// Filter types
export interface FeatureFilters {
  dateRange?: {
    start: Date;
    end: Date;
  };
  materialIds?: number[];
  familyIds?: number[];
  siteIds?: string[];
  supplierIds?: number[];
  tiers?: ('TIER_1' | 'TIER_2' | 'TIER_3')[];
}

// Response types
export interface FeatureCategoryResponse<T> {
  status: string;
  data: T[];
  metadata: {
    total_count: number;
    date_range: {
      start: string;
      end: string;
    };
    last_updated: string;
  };
}
```

### Implementation Steps

#### Phase 1: Backend API Extensions (Week 1)

1. Create API route files for all 9 feature categories
2. Implement database queries using DatabaseService
3. Create response models/schemas for each feature category
4. Add filtering, pagination, and date range support
5. Test all endpoints with sample data

#### Phase 2: Frontend API Client (Week 1)

1. Extend ApiClient with methods for all 9 categories
2. Add TypeScript interfaces for all feature types
3. Implement error handling and retry logic
4. Add caching for frequently accessed data

#### Phase 3: Chart Components (Week 2)

1. Create base chart component with common styling
2. Implement time series charts for temporal/climate/economic/5G
3. Implement hierarchical charts for family/site/supplier
4. Implement risk/impact charts for climate/SLA/lead time
5. Add drill-down functionality to all charts

#### Phase 4: Feature Pages (Week 2)

1. Create page structure for all 9 feature categories
2. Implement feature pages with tabs/subtabs
3. Add filter panels and date range selectors
4. Add export functionality
5. Implement responsive layouts

#### Phase 5: Interactive Features (Week 3)

1. Implement drill-down navigation (family → material → site)
2. Add real-time updates (WebSocket/SSE)
3. Implement advanced filtering
4. Add comparison mode
5. Add export functionality (images, PDF, CSV)

#### Phase 6: Data Storytelling (Week 3)

1. Create feature story cards explaining each category
2. Add insight panels highlighting key metrics
3. Implement trend indicators
4. Add risk alerts for critical situations
5. Create tooltips and help text

#### Phase 7: Testing & Optimization (Week 4)

1. Test all API endpoints with real database
2. Test chart interactions and drill-downs
3. Optimize performance (lazy loading, pagination)
4. Test responsive design on multiple devices
5. User acceptance testing

### Technical Specifications

#### Backend

- **Framework:** FastAPI (extending existing structure)
- **Database:** MySQL with SQLAlchemy ORM
- **Caching:** Redis for frequently accessed features (optional)
- **Real-time:** WebSocket/SSE for live updates

#### Frontend

- **Framework:** Next.js 14 (App Router)
- **Charts:** Recharts (existing library)
- **Styling:** Tailwind CSS (existing styles preserved)
- **State Management:** Zustand (existing)
- **Real-time:** WebSocket client / EventSource for SSE

#### Data Sources

- **Primary:** MySQL database with ML-ready schema
- **Views:** `vw_material_ml_features`, `vw_material_time_series_brasil`, `vw_top5_familias_nova_corrente`
- **Tables:** `MaterialFeatures`, `CalendarioBrasil`, `ClimaSalvador`, `IndicadoresEconomicos`, `Expansao5G`, etc.
- **Stored Procedures:** `sp_calcular_historico_diario`, `sp_extrair_features_material_completo`, `sp_extrair_features_externas_brasil`

### Color Scheme & Styling

**Preserve existing brand colors:**

- Background: `#0a192f` (brand-blue)
- Cards: `#172a45` (brand-light-navy), `#112240` (brand-navy)
- Text: `#ccd6f6` (brand-lightest-slate), `#a8b2d1` (brand-light-slate), `#8892b0` (brand-slate)
- Accent: `#64ffda` (brand-cyan)

**Chart colors:**

- Primary: `#64ffda` (cyan)
- Secondary: `#8884d8` (purple)
- Success: `#4ade80` (green)
- Warning: `#fbbf24` (yellow)
- Danger: `#f87171` (red)
- Info: `#60a5fa` (blue)

### Performance Considerations

1. **Lazy Loading:** Load charts only when tabs/pages are accessed
2. **Pagination:** Paginate large datasets (100 items per page)
3. **Caching:** Cache API responses for 30 seconds (existing implementation)
4. **Debouncing:** Debounce filter inputs (300ms delay)
5. **Virtualization:** Use virtual scrolling for large lists
6. **Data Aggregation:** Pre-aggregate data in database views

### Documentation

1. **API Documentation:** OpenAPI/Swagger docs for all new endpoints
2. **Component Documentation:** JSDoc comments for all chart components
3. **User Guide:** Documentation for end users explaining each feature category
4. **Developer Guide:** Setup instructions and architecture overview

### Success Metrics

1. **Performance:**

   - API response time < 500ms for filtered queries
   - Chart render time < 200ms
   - Page load time < 2s

2. **Usability:**

   - All 9 feature categories accessible via navigation
   - Drill-down works smoothly (family → material → site)
   - Filters work correctly with date ranges
   - Real-time updates refresh every 30 seconds

3. **Data Quality:**

   - All charts display real data from database (no mock data)
   - Data is up-to-date (last updated timestamp displayed)
   - Missing data handled gracefully

### To-dos

- [ ] Create backend API endpoints for temporal features - GET /api/v1/features/temporal with calendar and cyclical features support
- [ ] Create backend API endpoints for climate features - GET /api/v1/features/climate with Salvador/BA data and risk calculations
- [ ] Create backend API endpoints for economic features - GET /api/v1/features/economic with BACEN indicators
- [ ] Create backend API endpoints for 5G features - GET /api/v1/features/5g with expansion and milestone tracking
- [ ] Create backend API endpoints for lead time features - GET /api/v1/features/lead-time with supplier and material analytics
- [ ] Create backend API endpoints for SLA features - GET /api/v1/features/sla with penalties and violation tracking
- [ ] Create backend API endpoints for hierarchical features - GET /api/v1/features/hierarchical with family/site/supplier aggregations
- [ ] Create backend API endpoints for categorical features - GET /api/v1/features/categorical with family/site/supplier encodings
- [ ] Create backend API endpoints for business features - GET /api/v1/features/business with top 5 families and tier analytics
- [ ] Extend frontend API client (api.ts) with methods for all 9 feature categories and add TypeScript interfaces
- [ ] Create TypeScript type definitions for all 9 feature categories and filter interfaces
- [ ] Create temporal features chart components - Brazilian calendar and cyclical encoding visualizations
- [ ] Create climate features chart components - time series and risk heatmaps
- [ ] Create hierarchical charts with drill-down - family/site/supplier aggregations
- [ ] Create comparative charts - tier comparison, top 5 families, lead time categories
- [ ] Create feature category pages - 9 pages with tabs/subtabs for temporal, climate, economic, 5G, lead-time, SLA, hierarchical, categorical, business
- [ ] Implement drill-down functionality - family → material → site navigation with state management
- [ ] Implement advanced filtering - date ranges, families, tiers, sites, suppliers with debouncing
- [ ] Implement real-time updates - WebSocket/SSE connection with auto-refresh indicators
- [ ] Create data storytelling components - feature story cards, insight panels, trend indicators, risk alerts
- [ ] Implement export functionality - charts as images/PDF, data as CSV with download buttons
- [ ] Test all backend API endpoints with real database queries and validate response formats
- [ ] Test frontend integration - API calls, chart rendering, drill-downs, filters with real data
- [ ] Optimize performance - lazy loading, pagination, caching, debouncing, virtualization for large datasets
- [ ] Test responsive design - mobile-first layouts, touch interactions, responsive charts on multiple devices