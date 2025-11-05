"""
Nova Corrente - Create Star Schema Dimension Tables
================================================
Script 1 of 6: Foundation dimension tables from dadosSuprimentos.xlsx

Purpose:
- Create Dim_Calendar (temporal hierarchy with cyclical features)
- Create Dim_Part (material master with ABC classification)
- Create Dim_Site (warehouse/site master with customer mappings)
- Create Dim_Supplier (supplier master with lead time statistics)
- Create Dim_Maintenance_Type (preventive/corrective classification)

Expected Output:
- 5 dimension CSV files in data/processed/nova_corrente/dimensions/
- Summary JSON with row counts and validation results

Author: Nova Corrente Grand Prix SENAI Team
Date: 2025-11-05
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
from pathlib import Path

# Configuration
EXCEL_FILE = r'c:\Users\User\Desktop\Nc\gran-prix\docs\proj\dadosSuprimentos.xlsx'
OUTPUT_DIR = r'c:\Users\User\Desktop\Nc\gran-prix\data\processed\nova_corrente\dimensions'
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def create_dim_calendar(start_date='2013-11-01', end_date='2025-12-31'):
    """
    Create calendar dimension with temporal hierarchy and cyclical features
    
    Returns:
        pd.DataFrame with ~4,400 rows (2013-2025)
    """
    print("\n📅 Creating Dim_Calendar...")
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    calendar = pd.DataFrame({
        'date_id': dates.strftime('%Y%m%d').astype(int),
        'full_date': dates,
        'year': dates.year,
        'quarter': dates.quarter,
        'month': dates.month,
        'week_of_year': dates.isocalendar().week,
        'day_of_month': dates.day,
        'day_of_year': dates.dayofyear,
        'weekday': dates.dayofweek,  # 0=Monday, 6=Sunday
        'is_weekend': dates.dayofweek >= 5
    })
    
    # Cyclical features (for ML models to understand seasonality)
    calendar['month_sin'] = np.sin(2 * np.pi * calendar['month'] / 12)
    calendar['month_cos'] = np.cos(2 * np.pi * calendar['month'] / 12)
    calendar['day_of_year_sin'] = np.sin(2 * np.pi * calendar['day_of_year'] / 365)
    calendar['day_of_year_cos'] = np.cos(2 * np.pi * calendar['day_of_year'] / 365)
    
    # Brazilian federal holidays (2024-2025)
    holidays = [
        # 2024
        '2024-01-01',  # New Year
        '2024-02-12', '2024-02-13', '2024-02-14',  # Carnaval
        '2024-03-29',  # Good Friday
        '2024-04-21',  # Tiradentes
        '2024-05-01',  # Labor Day
        '2024-05-30',  # Corpus Christi
        '2024-09-07',  # Independence Day
        '2024-10-12',  # Nossa Senhora Aparecida
        '2024-11-02',  # Finados
        '2024-11-15',  # Proclamação da República
        '2024-12-25',  # Christmas
        # 2025
        '2025-01-01',  # New Year
        '2025-03-03', '2025-03-04', '2025-03-05',  # Carnaval
        '2025-04-18',  # Good Friday
        '2025-04-21',  # Tiradentes
        '2025-05-01',  # Labor Day
        '2025-06-19',  # Corpus Christi
        '2025-09-07',  # Independence Day
        '2025-10-12',  # Nossa Senhora Aparecida
        '2025-11-02',  # Finados
        '2025-11-15',  # Proclamação da República
        '2025-12-25',  # Christmas
    ]
    
    calendar['is_holiday'] = calendar['full_date'].astype(str).isin(holidays)
    calendar['holiday_name'] = calendar['full_date'].astype(str).map({
        '2024-01-01': 'Ano Novo', '2025-01-01': 'Ano Novo',
        '2024-02-12': 'Carnaval', '2024-02-13': 'Carnaval', '2024-02-14': 'Carnaval',
        '2025-03-03': 'Carnaval', '2025-03-04': 'Carnaval', '2025-03-05': 'Carnaval',
        '2024-04-21': 'Tiradentes', '2025-04-21': 'Tiradentes',
        '2024-05-01': 'Dia do Trabalho', '2025-05-01': 'Dia do Trabalho',
        '2024-09-07': 'Independência', '2025-09-07': 'Independência',
        '2024-10-12': 'Nossa Senhora', '2025-10-12': 'Nossa Senhora',
        '2024-11-15': 'Proclamação', '2025-11-15': 'Proclamação',
        '2024-12-25': 'Natal', '2025-12-25': 'Natal',
    })
    
    # Brazilian context flags
    calendar['is_carnival'] = calendar['full_date'].astype(str).str.contains('2024-02-1[234]|2025-03-0[345]', regex=True)
    calendar['is_fiscal_year_end'] = (calendar['month'] == 12) & (calendar['day_of_month'] == 31)
    
    print(f"   ✅ Created {len(calendar)} calendar days ({start_date} to {end_date})")
    print(f"   📊 Holidays: {calendar['is_holiday'].sum()} days")
    print(f"   📊 Weekends: {calendar['is_weekend'].sum()} days")
    
    return calendar


def create_dim_part(custo_df):
    """
    Create part/material master dimension with ABC classification
    
    Args:
        custo_df: DataFrame from "CUSTO DE MATERIAL E SERVIÇOS" sheet
        
    Returns:
        pd.DataFrame with ~872 unique parts
    """
    print("\n📦 Creating Dim_Part...")
    
    # Base part information
    parts = custo_df[['PRODUTO/SERVIÇO', 'MATERIAL', 'FAMÍLIA', 'U.M.']].drop_duplicates()
    parts = parts.rename(columns={
        'PRODUTO/SERVIÇO': 'part_id',
        'MATERIAL': 'material',
        'FAMÍLIA': 'familia',
        'U.M.': 'unit_of_measure'
    })
    
    # Calculate demand statistics per part
    demand_stats = custo_df.groupby('PRODUTO/SERVIÇO').agg({
        'QUANTIDADE': ['sum', 'mean', 'std', 'count']
    }).reset_index()
    demand_stats.columns = ['part_id', 'total_demand', 'avg_demand', 'std_demand', 'order_frequency']
    
    # Coefficient of variation (for demand pattern classification)
    demand_stats['demand_cv'] = demand_stats['std_demand'] / demand_stats['avg_demand']
    demand_stats['demand_cv'] = demand_stats['demand_cv'].fillna(0)
    
    # Demand pattern classification
    def classify_demand_pattern(cv, frequency):
        if cv < 0.5:
            return 'SMOOTH'
        elif cv < 1.0:
            return 'ERRATIC'
        elif frequency < 10:
            return 'INTERMITTENT'
        else:
            return 'LUMPY'
    
    demand_stats['demand_pattern'] = demand_stats.apply(
        lambda x: classify_demand_pattern(x['demand_cv'], x['order_frequency']), 
        axis=1
    )
    
    # Merge demand stats
    parts = parts.merge(demand_stats, on='part_id', how='left')
    
    # ABC Classification (Pareto 80-15-5 rule)
    part_value = custo_df.groupby('PRODUTO/SERVIÇO')['QUANTIDADE'].sum().sort_values(ascending=False)
    cumulative_pct = (part_value.cumsum() / part_value.sum() * 100).to_dict()
    
    def assign_abc_class(part_id):
        pct = cumulative_pct.get(part_id, 100)
        if pct <= 80:
            return 'A'
        elif pct <= 95:
            return 'B'
        else:
            return 'C'
    
    parts['abc_class'] = parts['part_id'].apply(assign_abc_class)
    
    # Criticality (simple heuristic: A=High, B=Medium, C=Low)
    parts['criticality'] = parts['abc_class'].map({'A': 'H', 'B': 'M', 'C': 'L'})
    
    # Fill missing values
    parts['material'] = parts['material'].fillna('Unknown')
    parts['familia'] = parts['familia'].fillna('UNKNOWN')
    parts['unit_of_measure'] = parts['unit_of_measure'].fillna('UN')
    
    print(f"   ✅ Created {len(parts)} parts")
    print(f"   📊 ABC Distribution: A={len(parts[parts['abc_class']=='A'])}, "
          f"B={len(parts[parts['abc_class']=='B'])}, C={len(parts[parts['abc_class']=='C'])}")
    print(f"   📊 Top families: {parts['familia'].value_counts().head(3).to_dict()}")
    
    return parts


def create_dim_site(custo_df, dados_df):
    """
    Create site/warehouse master dimension
    
    Args:
        custo_df: DataFrame from "CUSTO DE MATERIAL E SERVIÇOS" sheet
        dados_df: DataFrame from "DADOS" sheet
        
    Returns:
        pd.DataFrame with ~191 unique sites + 268 customer mappings
    """
    print("\n🏢 Creating Dim_Site...")
    
    # Sites from DEPOSITO (warehouse)
    sites_from_deposito = custo_df[['DEPÓSITO']].dropna().drop_duplicates()
    sites_from_deposito['site_type'] = 'DEPOSITO'
    sites_from_deposito = sites_from_deposito.rename(columns={'DEPÓSITO': 'site_id'})
    
    # Sites from DADOS sheet (customer mappings)
    # First, clean the column names (remove leading/trailing spaces)
    dados_df.columns = dados_df.columns.str.strip()
    
    # Skip header rows if needed (check if first rows are headers)
    if dados_df.iloc[0].isna().all() or 'SITE' in str(dados_df.iloc[0].values):
        dados_df = dados_df.iloc[2:].reset_index(drop=True)
    
    # Find actual column indices
    site_col = None
    cliente_col = None
    id_cliente_col = None
    
    for i, col in enumerate(dados_df.columns):
        if 'SITE' in str(dados_df[col].iloc[0]) or i == 2:
            site_col = col
        if 'CLIENTE' in str(dados_df[col].iloc[0]) or i == 4:
            cliente_col = col
        if 'ID' in str(dados_df[col].iloc[0]) and i > 3:
            id_cliente_col = col
    
    if site_col is not None:
        sites_from_dados = dados_df[[site_col, cliente_col, id_cliente_col]].dropna(subset=[site_col])
        sites_from_dados.columns = ['site_id', 'client_type', 'client_id']
        sites_from_dados['site_type'] = 'SITE'
        sites_from_dados = sites_from_dados[sites_from_dados['site_id'].notna()]
    else:
        sites_from_dados = pd.DataFrame(columns=['site_id', 'site_type', 'client_type', 'client_id'])
    
    # Merge all sites
    sites = pd.concat([
        sites_from_deposito,
        sites_from_dados
    ], ignore_index=True)
    
    # Remove duplicates (keep first occurrence)
    sites = sites.drop_duplicates(subset=['site_id'], keep='first')
    
    # Add placeholder columns for future enrichment
    sites['site_name'] = sites['site_id']
    sites['region_id'] = None
    sites['state_code'] = None
    sites['municipality'] = None
    sites['latitude'] = None
    sites['longitude'] = None
    sites['tower_type'] = None
    sites['technology'] = None
    sites['is_active'] = True
    
    print(f"   ✅ Created {len(sites)} sites")
    print(f"   📊 Site types: {sites['site_type'].value_counts().to_dict()}")
    
    return sites


def create_dim_supplier(custo_df):
    """
    Create supplier master dimension with lead time statistics
    
    Args:
        custo_df: DataFrame from "CUSTO DE MATERIAL E SERVIÇOS" sheet
        
    Returns:
        pd.DataFrame with ~468 unique suppliers
    """
    print("\n🏭 Creating Dim_Supplier...")
    
    # Base supplier information
    suppliers = custo_df[['NOME FORNEC.']].dropna().drop_duplicates()
    suppliers = suppliers.reset_index(drop=True)
    suppliers['supplier_id'] = range(1, len(suppliers) + 1)
    suppliers = suppliers.rename(columns={'NOME FORNEC.': 'supplier_name'})
    
    # Calculate lead time statistics
    custo_df_copy = custo_df.copy()
    custo_df_copy['data_solicitado_dt'] = pd.to_datetime(custo_df_copy['DATA SOLICITADO'], errors='coerce')
    custo_df_copy['data_compra_dt'] = pd.to_datetime(custo_df_copy['DATA DE COMPRA'], errors='coerce')
    
    custo_df_copy['lead_time_days'] = (
        custo_df_copy['data_compra_dt'] - custo_df_copy['data_solicitado_dt']
    ).dt.days
    
    # Filter out negative/invalid lead times
    custo_df_copy = custo_df_copy[
        (custo_df_copy['lead_time_days'].notna()) & 
        (custo_df_copy['lead_time_days'] >= 0) & 
        (custo_df_copy['lead_time_days'] <= 365)  # Max 1 year
    ]
    
    supplier_stats = custo_df_copy.groupby('NOME FORNEC.')['lead_time_days'].agg([
        ('avg_lead_time_days', 'mean'),
        ('std_lead_time_days', 'std'),
        ('min_lead_time_days', 'min'),
        ('max_lead_time_days', 'max'),
        ('order_count', 'count')
    ]).reset_index()
    supplier_stats = supplier_stats.rename(columns={'NOME FORNEC.': 'supplier_name'})
    
    # Merge stats
    suppliers = suppliers.merge(supplier_stats, on='supplier_name', how='left')
    
    # Add placeholder columns
    suppliers['supplier_code'] = suppliers['supplier_id'].apply(lambda x: f'SUP{x:05d}')
    suppliers['supplier_type'] = None  # To be enriched
    suppliers['tier'] = None
    suppliers['on_time_delivery_pct'] = None
    suppliers['quality_score'] = None
    suppliers['strike_risk_score'] = None
    suppliers['geographic_risk_score'] = None
    
    print(f"   ✅ Created {len(suppliers)} suppliers")
    print(f"   📊 Avg lead time: {suppliers['avg_lead_time_days'].mean():.1f} days")
    print(f"   📊 Top suppliers by order count: {supplier_stats.nlargest(3, 'order_count')['supplier_name'].tolist()}")
    
    return suppliers


def create_dim_maintenance_type():
    """
    Create maintenance type dimension
    
    Returns:
        pd.DataFrame with 2 maintenance types
    """
    print("\n🔧 Creating Dim_Maintenance_Type...")
    
    maintenance_types = pd.DataFrame({
        'maintenance_type_id': [1, 2],
        'type_code': ['PREV', 'CORR'],
        'type_name': ['Preventiva', 'Corretiva'],
        'is_preventive': [True, False],
        'sla_hours': [48, 4],  # Preventive: 48h, Corrective: 4h
        'priority': [2, 1],  # Corrective higher priority
        'description': [
            'Manutenção preventiva planejada',
            'Manutenção corretiva emergencial'
        ]
    })
    
    print(f"   ✅ Created {len(maintenance_types)} maintenance types")
    
    return maintenance_types


def main():
    """
    Main execution function
    """
    print("=" * 80)
    print("🚀 Nova Corrente - Star Schema Dimension Creation")
    print("=" * 80)
    
    start_time = datetime.now()
    
    # Load Excel file
    print(f"\n📂 Loading Excel file: {EXCEL_FILE}")
    try:
        custo_df = pd.read_excel(EXCEL_FILE, sheet_name='CUSTO DE MATERIAL E SERVIÇOS')
        dados_df = pd.read_excel(EXCEL_FILE, sheet_name='DADOS')
        print(f"   ✅ Loaded CUSTO sheet: {len(custo_df)} rows")
        print(f"   ✅ Loaded DADOS sheet: {len(dados_df)} rows")
    except Exception as e:
        print(f"   ❌ Error loading Excel: {e}")
        return
    
    # Create dimension tables
    dim_calendar = create_dim_calendar()
    dim_part = create_dim_part(custo_df)
    dim_site = create_dim_site(custo_df, dados_df)
    dim_supplier = create_dim_supplier(custo_df)
    dim_maintenance_type = create_dim_maintenance_type()
    
    # Save to CSV
    print(f"\n💾 Saving dimension tables to: {OUTPUT_DIR}")
    
    files_created = {}
    
    try:
        dim_calendar.to_csv(f'{OUTPUT_DIR}/dim_calendar.csv', index=False)
        files_created['dim_calendar'] = len(dim_calendar)
        print(f"   ✅ Saved dim_calendar.csv ({len(dim_calendar)} rows)")
        
        dim_part.to_csv(f'{OUTPUT_DIR}/dim_part.csv', index=False)
        files_created['dim_part'] = len(dim_part)
        print(f"   ✅ Saved dim_part.csv ({len(dim_part)} rows)")
        
        dim_site.to_csv(f'{OUTPUT_DIR}/dim_site.csv', index=False)
        files_created['dim_site'] = len(dim_site)
        print(f"   ✅ Saved dim_site.csv ({len(dim_site)} rows)")
        
        dim_supplier.to_csv(f'{OUTPUT_DIR}/dim_supplier.csv', index=False)
        files_created['dim_supplier'] = len(dim_supplier)
        print(f"   ✅ Saved dim_supplier.csv ({len(dim_supplier)} rows)")
        
        dim_maintenance_type.to_csv(f'{OUTPUT_DIR}/dim_maintenance_type.csv', index=False)
        files_created['dim_maintenance_type'] = len(dim_maintenance_type)
        print(f"   ✅ Saved dim_maintenance_type.csv ({len(dim_maintenance_type)} rows)")
        
    except Exception as e:
        print(f"   ❌ Error saving files: {e}")
        return
    
    # Create summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    summary = {
        'script': '01_create_star_schema_dimensions.py',
        'execution_date': end_time.isoformat(),
        'duration_seconds': duration,
        'status': 'SUCCESS',
        'dimensions_created': files_created,
        'total_rows': sum(files_created.values()),
        'output_directory': OUTPUT_DIR
    }
    
    summary_file = f'{OUTPUT_DIR}/dimension_creation_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📊 Summary saved to: {summary_file}")
    
    # Final report
    print("\n" + "=" * 80)
    print("✅ DIMENSION CREATION COMPLETE")
    print("=" * 80)
    print(f"   ⏱️  Duration: {duration:.1f} seconds")
    print(f"   📦 Files created: {len(files_created)}")
    print(f"   📊 Total rows: {sum(files_created.values()):,}")
    print(f"   📁 Output directory: {OUTPUT_DIR}")
    print("\n🎯 Next Steps:")
    print("   1. Review dimension tables for data quality")
    print("   2. Run 02_create_fact_demand_daily.py to create fact table")
    print("   3. Run 03_integrate_climate_data.py for external enrichment")
    print("=" * 80)


if __name__ == '__main__':
    main()
