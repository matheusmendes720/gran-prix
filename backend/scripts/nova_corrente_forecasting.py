#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nova Corrente Demand Forecasting System
Sistema de Previsibilidade de Demanda - Grand Prix SENAI

Discovery Coding Approach: Understand by implementing
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

# ============================================================================
# PARTE 1: CORE MATHEMATICAL FUNCTIONS
# ============================================================================

def calculate_safety_stock(avg_demand: float, std_demand: float, 
                          lead_time: int, service_level: float = 0.95) -> float:
    """
    Safety Stock básico.
    
    SS = Z_α × σ_D × √LT
    """
    z_score = stats.norm.ppf(service_level)
    ss = z_score * std_demand * np.sqrt(lead_time)
    return ss


def calculate_safety_stock_advanced(avg_demand: float, std_demand: float,
                                    avg_lead_time: float, std_lead_time: float,
                                    service_level: float = 0.95) -> float:
    """
    Safety Stock com variabilidade de lead time.
    
    SS = Z_α × √(LT × σ_D² + D_avg² × σ_LT²)
    """
    z_score = stats.norm.ppf(service_level)
    variance = avg_lead_time * (std_demand**2) + (avg_demand**2) * (std_lead_time**2)
    ss = z_score * np.sqrt(variance)
    return ss


def calculate_reorder_point(avg_demand: float, lead_time: int, 
                           safety_stock: float, adjustment_factor: float = 1.0) -> float:
    """
    Calculate reorder point with optional adjustment factors.
    
    PP = (D_avg × AF × LT) + SS
    """
    pp = (avg_demand * adjustment_factor * lead_time) + safety_stock
    return pp


def calculate_eoq(annual_demand: float, ordering_cost: float, 
                 holding_cost: float) -> float:
    """
    Economic Order Quantity.
    
    Q* = √(2DS/H)
    """
    eoq = np.sqrt(2 * annual_demand * ordering_cost / holding_cost)
    return eoq


# ============================================================================
# PARTE 2: INVENTORY ALERT SYSTEM
# ============================================================================

def check_inventory_alert(current_stock: float, reorder_point: float,
                         avg_demand: float, safety_stock: float) -> Dict:
    """
    Sistema completo de alertas de estoque.
    """
    alert_triggered = current_stock <= reorder_point
    days_until_stockout = (current_stock - safety_stock) / avg_demand if avg_demand > 0 else 0
    
    # Determine status
    if days_until_stockout <= 3:
        status = "🔴 CRÍTICO"
        recommendation = "Compre urgentemente"
    elif days_until_stockout <= 7:
        status = "🟡 ATENÇÃO"
        recommendation = "Compre em 2-3 dias"
    elif alert_triggered:
        status = "🟢 MONITORAR"
        recommendation = "Compre na próxima semana"
    else:
        status = "✅ OK"
        recommendation = "Situação normal"
    
    return {
        "alert": alert_triggered,
        "current_stock": current_stock,
        "reorder_point": reorder_point,
        "days_until_stockout": max(0, days_until_stockout),
        "status": status,
        "recommendation": recommendation
    }


# ============================================================================
# PARTE 3: DEMAND FORECASTING MODELS
# ============================================================================

def simulate_demand_arima_simple(data: np.array, forecast_horizon: int = 30) -> np.array:
    """
    Simulação simplificada de ARIMA.
    
    Usa médias móveis e tendência simples para demonstrar conceito.
    """
    if len(data) < 7:
        return np.full(forecast_horizon, np.mean(data))
    
    # Média móvel de 7 dias
    ma_7 = np.mean(data[-7:])
    
    # Tendência simples
    if len(data) >= 14:
        trend = np.mean(data[-7:]) - np.mean(data[-14:-7])
    else:
        trend = 0
    
    # Previsão
    forecast = []
    for i in range(forecast_horizon):
        value = max(0, ma_7 + trend * i + np.random.normal(0, np.std(data) * 0.1))  # Não permitir negativos
        forecast.append(value)
    
    return np.array(forecast)


def calculate_mape(actual: np.array, forecast: np.array) -> float:
    """
    Mean Absolute Percentage Error.
    """
    mask = actual != 0
    if np.sum(mask) == 0:
        return 0.0
    mape = np.mean(np.abs((actual[mask] - forecast[mask]) / actual[mask])) * 100
    return mape


# ============================================================================
# PARTE 4: COMPLETE SYSTEM INTEGRATION
# ============================================================================

class NovaCorrenteForecastingSystem:
    """
    Sistema completo de previsão para Nova Corrente.
    """
    
    def __init__(self):
        self.materials = {}
        self.forecasts = {}
        self.alerts = {}
    
    def add_material(self, material_id: str, avg_demand: float, std_demand: float,
                    lead_time: int, std_lead_time: float = 0,
                    current_stock: float = 0, service_level: float = 0.95):
        """
        Adicionar material ao sistema.
        """
        # Calculate safety stock and reorder point
        if std_lead_time > 0:
            ss = calculate_safety_stock_advanced(
                avg_demand, std_demand, lead_time, std_lead_time, service_level
            )
        else:
            ss = calculate_safety_stock(avg_demand, std_demand, lead_time, service_level)
        
        pp = calculate_reorder_point(avg_demand, lead_time, ss)
        
        # Store material info
        self.materials[material_id] = {
            'avg_demand': avg_demand,
            'std_demand': std_demand,
            'lead_time': lead_time,
            'std_lead_time': std_lead_time,
            'safety_stock': ss,
            'reorder_point': pp,
            'current_stock': current_stock,
            'service_level': service_level
        }
        
        return ss, pp
    
    def check_all_alerts(self) -> Dict:
        """
        Verificar alertas para todos os materiais.
        """
        all_alerts = {}
        
        for material_id, material in self.materials.items():
            alert = check_inventory_alert(
                material['current_stock'],
                material['reorder_point'],
                material['avg_demand'],
                material['safety_stock']
            )
            all_alerts[material_id] = alert
            self.alerts[material_id] = alert
        
        return all_alerts
    
    def forecast(self, material_id: str, historical_data: np.array, 
                horizon: int = 30) -> Dict:
        """
        Gerar previsão completa para um material.
        """
        if material_id not in self.materials:
            raise ValueError(f"Material {material_id} não encontrado")
        
        # Forecast
        forecast_values = simulate_demand_arima_simple(historical_data, horizon)
        
        # Store
        self.forecasts[material_id] = {
            'values': forecast_values,
            'dates': pd.date_range(start=datetime.now(), periods=horizon, freq='D'),
            'mean': np.mean(forecast_values),
            'std': np.std(forecast_values)
        }
        
        return self.forecasts[material_id]
    
    def get_summary(self) -> pd.DataFrame:
        """
        Resumo completo do sistema.
        """
        rows = []
        
        for material_id, material in self.materials.items():
            alert = self.alerts.get(material_id, {})
            forecast = self.forecasts.get(material_id, {})
            
            rows.append({
                'Material': material_id,
                'Demanda_Media': material['avg_demand'],
                'Lead_Time': material['lead_time'],
                'Safety_Stock': round(material['safety_stock'], 1),
                'Reorder_Point': round(material['reorder_point'], 1),
                'Estoque_Atual': material['current_stock'],
                'Status': alert.get('status', 'N/A'),
                'Dias_Ate_Ruptura': round(alert.get('days_until_stockout', 0), 1),
                'Previsao_Media': round(forecast.get('mean', 0), 2)
            })
        
        return pd.DataFrame(rows)


# ============================================================================
# PARTE 5: DESCOBERTA E TESTES
# ============================================================================

def test_nova_corrente_system():
    """
    Teste completo do sistema - Discovery Coding em ação!
    """
    print("=" * 80)
    print("NOVA CORRENTE - Sistema de Previsão de Demanda")
    print("=" * 80)
    
    # Criar sistema
    system = NovaCorrenteForecastingSystem()
    
    # Adicionar materiais (descoberta através de teste)
    print("\n1. Configurando Materiais...")
    print("-" * 80)
    
    # Material 1: Conector Óptico
    ss1, pp1 = system.add_material(
        material_id='CONN-001',
        avg_demand=8,
        std_demand=2.5,
        lead_time=14,
        std_lead_time=1.5,
        current_stock=85,
        service_level=0.95
    )
    print(f"CONN-001 - Safety Stock: {ss1:.1f}, Reorder Point: {pp1:.1f}")
    
    # Material 2: Cabo Óptico
    ss2, pp2 = system.add_material(
        material_id='CABLE-001',
        avg_demand=2,
        std_demand=0.8,
        lead_time=21,
        current_stock=50
    )
    print(f"CABLE-001 - Safety Stock: {ss2:.1f}, Reorder Point: {pp2:.1f}")
    
    # Material 3: Estrutura Metálica
    ss3, pp3 = system.add_material(
        material_id='ESTR-001',
        avg_demand=3,
        std_demand=1.2,
        lead_time=10,
        current_stock=30
    )
    print(f"ESTR-001 - Safety Stock: {ss3:.1f}, Reorder Point: {pp3:.1f}")
    
    # Verificar alertas (descoberta de problemas!)
    print("\n2. Verificando Alertas...")
    print("-" * 80)
    alerts = system.check_all_alerts()
    
    for material_id, alert in alerts.items():
        print(f"{material_id}: {alert['status']}")
        print(f"  {alert['recommendation']}")
        print(f"  Dias até ruptura: {alert['days_until_stockout']:.1f}")
        print()
    
    # Gerar previsões (descobrir padrões)
    print("3. Gerando Previsões...")
    print("-" * 80)
    
    # Dados sintéticos para teste
    np.random.seed(42)
    for material_id in system.materials.keys():
        historical = np.random.normal(
            system.materials[material_id]['avg_demand'],
            system.materials[material_id]['std_demand'],
            100
        )
        forecast = system.forecast(material_id, historical, horizon=30)
        print(f"{material_id}: Média previsão {forecast['mean']:.2f} ± {forecast['std']:.2f}")
    
    # Resumo completo (descoberta de insights!)
    print("\n4. Resumo Completo do Sistema")
    print("=" * 80)
    summary = system.get_summary()
    print(summary.to_string(index=False))
    
    return system


def explore_demand_patterns():
    """
    Explorar padrões de demanda - Discovery approach!
    """
    print("\n" + "=" * 80)
    print("EXPLORAÇÃO DE PADRÕES DE DEMANDA")
    print("=" * 80)
    
    # Criar dados sintéticos representando demanda real
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=365, freq='D')
    
    # Simular padrões reais
    base_demand = 10
    
    # Sazonalidade semanal
    weekly_pattern = np.sin(2 * np.pi * np.arange(365) / 7) * 2
    
    # Sazonalidade anual
    annual_pattern = np.sin(2 * np.pi * np.arange(365) / 365) * 3
    
    # Tendência de crescimento
    trend = np.linspace(0, 5, 365)
    
    # Ruído
    noise = np.random.normal(0, 2, 365)
    
    # Demanda total
    demand = base_demand + weekly_pattern + annual_pattern + trend + noise
    
    # Criar DataFrame
    df = pd.DataFrame({'date': dates, 'demand': demand})
    
    print("\nEstatísticas Descritivas:")
    print(df.describe())
    
    print("\nPadrões Detectados:")
    print(f"Média: {df['demand'].mean():.2f}")
    print(f"Std Dev: {df['demand'].std():.2f}")
    print(f"Min: {df['demand'].min():.2f}")
    print(f"Max: {df['demand'].max():.2f}")
    
    # Visualização simples (text-based)
    print("\nHistograma de Demanda:")
    bins = 20
    hist, bins_edges = np.histogram(df['demand'], bins=bins)
    max_hist = max(hist)
    
    for i in range(len(hist)):
        bar_length = int(50 * hist[i] / max_hist)
        bar = '█' * bar_length
        print(f"{bins_edges[i]:6.1f} - {bins_edges[i+1]:6.1f}: {bar}")
    
    return df


# ============================================================================
# PARTE 6: EXECUTAR E DESCOBRIR
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║  NOVA CORRENTE - Sistema de Previsão de Demanda                      ║
    ║  Grand Prix SENAI                                                     ║
    ║  Discovery Coding: Descobrir implementando!                           ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Executar testes descobertos
    system = test_nova_corrente_system()
    
    # Explorar padrões
    df_patterns = explore_demand_patterns()
    
    print("\n" + "=" * 80)
    print("✅ SISTEMA FUNCIONANDO!")
    print("=" * 80)
    print("\nPróximos passos:")
    print("1. Integrar com dados reais da Nova Corrente")
    print("2. Treinar modelos ARIMA/Prophet/LSTM reais")
    print("3. Criar dashboard interativo")
    print("4. Ganhar o Grand Prix! 🏆")
    print("\n")

