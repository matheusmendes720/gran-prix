"""
Feature category schemas for ML features API
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


class DateRange(BaseModel):
    """Date range filter"""
    start: Optional[date] = None
    end: Optional[date] = None


class FeatureMetadata(BaseModel):
    """Feature response metadata"""
    total_count: int
    date_range: Optional[Dict[str, str]] = None
    last_updated: str


class FeatureCategoryResponse(BaseModel):
    """Generic feature category response"""
    status: str = "success"
    data: List[Dict[str, Any]]
    metadata: FeatureMetadata


# Temporal Features
class TemporalFeatures(BaseModel):
    """Temporal features model"""
    material_id: Optional[int] = None
    year: int
    month: int
    day: int
    weekday: int
    quarter: int
    day_of_year: int
    month_sin: float
    month_cos: float
    day_of_year_sin: float
    day_of_year_cos: float
    is_weekend: bool
    is_holiday: bool
    is_carnival: bool
    is_verao: bool
    is_chuva_sazonal: bool
    data_referencia: str


class CalendarFeatures(BaseModel):
    """Brazilian calendar features"""
    data_referencia: date
    is_feriado: bool
    is_carnaval: bool
    is_natal: bool
    is_verao: bool
    is_chuva_sazonal: bool
    impact_demanda: float
    descricao: Optional[str] = None


# Climate Features
class ClimateFeatures(BaseModel):
    """Climate features model"""
    material_id: Optional[int] = None
    data_referencia: str
    temperature_avg_c: float
    precipitation_mm: float
    humidity_percent: float
    wind_speed_kmh: float
    extreme_heat: bool
    cold_weather: bool
    heavy_rain: bool
    no_rain: bool
    is_intense_rain: bool
    is_high_humidity: bool
    corrosion_risk: float  # 0-1
    field_work_disruption: float  # 0-1


class SalvadorClimate(BaseModel):
    """Salvador/BA climate data"""
    data_referencia: date
    temperatura_media: float
    precipitacao_mm: float
    umidade_percentual: float
    velocidade_vento_kmh: float
    is_extreme_heat: bool
    is_heavy_rain: bool
    corrosion_risk: float
    field_work_disruption: float


class ClimateRisk(BaseModel):
    """Climate risk indicators"""
    material_id: int
    material_name: str
    corrosion_risk: float
    field_work_disruption: float
    risk_level: str  # LOW, MEDIUM, HIGH


# Economic Features
class EconomicFeatures(BaseModel):
    """Economic features model"""
    material_id: Optional[int] = None
    data_referencia: str
    inflation_rate: float
    exchange_rate_brl_usd: float
    gdp_growth_rate: float
    selic_rate: float
    high_inflation: bool
    currency_devaluation: bool


class BACENIndicators(BaseModel):
    """BACEN economic indicators"""
    data_referencia: date
    taxa_inflacao: float
    taxa_cambio_brl_usd: float
    pib_crescimento: float
    taxa_selic: float
    is_high_inflation: bool
    is_currency_devaluation: bool


# 5G Features
class FiveGFeatures(BaseModel):
    """5G features model"""
    material_id: Optional[int] = None
    data_referencia: str
    coverage_5g_percentual: float
    investment_5g_brl_billions: float
    is_5g_milestone: bool
    is_5g_active: bool
    expansion_5g_rate: float


class FiveGExpansion(BaseModel):
    """5G expansion metrics"""
    data_referencia: date
    cobertura_5g_percentual: float
    investimento_5g_brl_billions: float
    torres_5g_ativas: int
    municipios_5g: int
    is_5g_milestone: bool
    taxa_expansao_5g: float


class LeadTimeCategory(str, Enum):
    """Lead time categories"""
    FAST = "FAST"  # <7 days
    NORMAL = "NORMAL"  # 7-14 days
    SLOW = "SLOW"  # 14-30 days
    VERY_SLOW = "VERY_SLOW"  # >30 days


# Lead Time Features
class LeadTimeFeatures(BaseModel):
    """Lead time features model"""
    material_id: Optional[int] = None
    lead_time_days: float
    base_lead_time_days: float
    total_lead_time_days: float
    customs_delay_days: float
    strike_risk: float
    is_critical_lead_time: bool
    lead_time_category: LeadTimeCategory
    supplier_lead_time_mean: float
    supplier_lead_time_std: float


class SupplierLeadTime(BaseModel):
    """Supplier lead time analytics"""
    fornecedor_id: int
    fornecedor_nome: str
    lead_time_medio: float
    lead_time_std: float
    lead_time_min: float
    lead_time_max: float
    total_pedidos: int
    reliability_score: float


# SLA Features
class SLAFeatures(BaseModel):
    """SLA features model"""
    material_id: int
    material_name: str
    tier_nivel: str
    sla_penalty_brl: float
    availability_target: float
    downtime_hours_monthly: float
    sla_violation_risk: float
    availability_actual: Optional[float] = None


class SLAPenalty(BaseModel):
    """SLA penalty by material/tier"""
    material_id: int
    material_name: str
    tier_nivel: str
    sla_penalty_brl: float
    availability_target: float
    availability_actual: Optional[float] = None
    penalty_risk_brl: float


class SLAViolation(BaseModel):
    """SLA violation risk"""
    material_id: int
    material_name: str
    tier_nivel: str
    sla_violation_risk: float
    violation_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    estimated_penalty_brl: float


# Hierarchical Features
class HierarchicalLevel(str, Enum):
    """Hierarchical aggregation levels"""
    FAMILY = "family"
    SITE = "site"
    SUPPLIER = "supplier"


class HierarchicalFeatures(BaseModel):
    """Hierarchical features model"""
    material_id: Optional[int] = None
    family_demand_ma_7: float
    family_demand_ma_30: float
    family_demand_std_7: float
    family_demand_std_30: float
    family_frequency: float
    site_demand_ma_7: float
    site_demand_ma_30: float
    site_frequency: float
    supplier_frequency: float
    supplier_lead_time_mean: float
    supplier_lead_time_std: float


class FamilyAggregation(BaseModel):
    """Family-level aggregation"""
    familia_id: int
    familia_nome: str
    total_movimentacoes: int
    demanda_media_7d: float
    demanda_media_30d: float
    demanda_std_7d: float
    demanda_std_30d: float
    frequency: float
    total_materiais: int


class SiteAggregation(BaseModel):
    """Site/tower-level aggregation"""
    site_id: str
    total_movimentacoes: int
    demanda_media_7d: float
    demanda_media_30d: float
    frequency: float
    total_materiais: int


# Categorical Features
class CategoricalFeatures(BaseModel):
    """Categorical features model"""
    material_id: int
    familia: str
    familia_encoded: int
    deposito: str
    site_id: str
    fornecedor: str
    fornecedor_encoded: Optional[int] = None


class FamilyEncoding(BaseModel):
    """Family encoding"""
    familia_id: int
    familia_nome: str
    familia_encoded: int
    total_materiais: int


class SiteEncoding(BaseModel):
    """Site encoding"""
    site_id: str
    site_nome: Optional[str] = None
    total_materiais: int


class SupplierEncoding(BaseModel):
    """Supplier encoding"""
    fornecedor_id: int
    fornecedor_nome: str
    fornecedor_encoded: Optional[int] = None
    total_materiais: int


# Business Features
class BusinessFeatures(BaseModel):
    """Business features model"""
    material_id: int
    item_id: str
    material: str
    produto_servico: str
    quantidade: float
    unidade_medida: str
    solicitacao: str
    data_requisitada: Optional[date] = None
    data_solicitado: date
    data_compra: date
    familia_nome: str
    fornecedor_nome: str
    site_id: str


class Top5Family(BaseModel):
    """Top 5 family statistics"""
    familia_id: int
    familia_nome: str
    total_movimentacoes: int
    percentual: float
    items_unicos: int
    sites: int
    demanda_media: float


class TierAnalytics(BaseModel):
    """Tier-based analytics"""
    tier_nivel: str
    total_materiais: int
    avg_sla_penalty_brl: float
    avg_availability_target: float
    total_penalty_risk_brl: float
    critical_materials: int


# ============================================
# EXPANDED FEATURE TYPES (NEW - 52+ features)
# ============================================

# Transport Features (10 features)
class TransportFeatures(BaseModel):
    """Transport features model"""
    material_id: Optional[int] = None
    data_referencia: str
    transport_cost_index: float
    logistics_performance: float
    highway_congestion: float
    port_congestion: float
    port_wait_time_hours: float
    delivery_impact_factor: float
    total_congestion: float
    logistics_efficiency_score: float
    transport_cost_multiplier: float
    delivery_delay_risk: float


# Trade Features (8 features)
class TradeFeatures(BaseModel):
    """Trade features model"""
    material_id: Optional[int] = None
    data_referencia: str
    import_volume: float
    export_volume: float
    trade_balance: float
    port_activity_index: float
    customs_delay_days: int
    trade_activity_level: float
    import_export_ratio: float
    customs_delay_risk: float


# Energy Features (6 features)
class EnergyFeatures(BaseModel):
    """Energy features model"""
    material_id: Optional[int] = None
    data_referencia: str
    energy_consumption_mwh: float
    power_outages_count: int
    grid_reliability: float
    energy_price: float
    power_outage_risk: float
    grid_stability_score: float


# Employment Features (4 features)
class EmploymentFeatures(BaseModel):
    """Employment features model"""
    material_id: Optional[int] = None
    data_referencia: str
    employment_rate: float
    net_employment_change: int
    labor_availability: float
    hiring_activity: float


# Construction Features (5 features)
class ConstructionFeatures(BaseModel):
    """Construction features model"""
    material_id: Optional[int] = None
    data_referencia: str
    construction_activity_index: float
    material_demand_forecast: float
    regional_growth_rate: float
    infrastructure_investment: float
    construction_demand_multiplier: float


# Industrial Features (5 features)
class IndustrialFeatures(BaseModel):
    """Industrial features model"""
    material_id: Optional[int] = None
    data_referencia: str
    industrial_production_index: float
    electrical_equipment_production: float
    component_demand: float
    production_demand_ratio: float
    industrial_activity_level: float
