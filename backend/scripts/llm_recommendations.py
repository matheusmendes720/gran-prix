"""
LLM-Powered Prescriptive Recommendations System
Uses Gemini API for context-aware insights in Portuguese
"""
import os
import json
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Using mock recommendations.")


class LLMRecommendations:
    """Generate context-aware recommendations using Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize LLM recommendations generator.
        
        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None
        
        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini: {e}")
                self.model = None
        else:
            print("Using mock recommendations (Gemini not configured)")
    
    def generate_recommendations(
        self, 
        alerts: List[Dict], 
        climate_data: Optional[Dict] = None,
        sla_data: Optional[Dict] = None,
        geographic_data: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Generate intelligent recommendations from alerts and context.
        
        Args:
            alerts: List of current alerts
            climate_data: Current climate conditions
            sla_data: SLA and penalty information
            geographic_data: Regional/geographic context
            
        Returns:
            List of recommendation dictionaries
        """
        if not self.model:
            return self._generate_mock_recommendations(alerts)
        
        try:
            # Build context for LLM
            context = self._build_context(alerts, climate_data, sla_data, geographic_data)
            
            # Generate prompt
            prompt = self._build_prompt(context)
            
            # Get LLM response
            response = self.model.generate_content(prompt)
            
            # Parse recommendations
            recommendations = self._parse_response(response.text, alerts)
            
            return recommendations
            
        except Exception as e:
            print(f"Error generating LLM recommendations: {e}")
            return self._generate_mock_recommendations(alerts)
    
    def _build_context(
        self,
        alerts: List[Dict],
        climate_data: Optional[Dict],
        sla_data: Optional[Dict],
        geographic_data: Optional[Dict]
    ) -> str:
        """Build context string for LLM."""
        context_parts = []
        
        # Critical alerts
        critical_alerts = [a for a in alerts if a.get('level') == 'CRITICAL']
        if critical_alerts:
            context_parts.append(f"ALERTAS CRÍTICOS: {len(critical_alerts)} itens em risco de ruptura")
        
        # Climate context
        if climate_data:
            if climate_data.get('is_intense_rain'):
                context_parts.append("CHUVAS INTENSAS PREVISTAS: 30% acima da média em 48h")
            if climate_data.get('is_high_humidity'):
                context_parts.append("UMIDADE ALTA: >80% - risco de corrosão aumentado")
            if climate_data.get('corrosion_risk') == 'high':
                context_parts.append("RISCO ALTO DE CORROSÃO: região costeira com umidade elevada")
        
        # SLA context
        if sla_data:
            if sla_data.get('availability_actual', 1.0) < 0.99:
                penalty = sla_data.get('penalty_per_hour_avg', 0)
                context_parts.append(f"DISPONIBILIDADE BAIXA: risco de multa de R$ {penalty:,.0f}/hora")
        
        # Geographic context
        if geographic_data:
            region = geographic_data.get('region', 'Unknown')
            context_parts.append(f"REGIONAL: {region} - padrões específicos da região")
        
        return " | ".join(context_parts) if context_parts else "Situação operacional normal"
    
    def _build_prompt(self, context: str) -> str:
        """Build prompt for LLM."""
        return f"""
Você é um especialista em gestão de estoque e logística para telecomunicações no Brasil.
A empresa Nova Corrente mantém 18,000+ torres de telecomunicações para clientes B2B (Vivo, Claro, TIM, IHS Towers).

Contexto atual: {context}

Suas tarefas:
1. Analisar os alertas de estoque críticos
2. Considerar fatores climáticos (chuvas, umidade, corrosão)
3. Considerar SLA (multas de R$ 30k-50k/hora por downtime)
4. Fornecer recomendações ACIONÁVEIS em português brasileiro

Gere recomendações claras e específicas no formato:
ITEM | RECOMENDAÇÃO | URGÊNCIA | JUSTIFICATIVA

EXEMPLOS:
- "Transceptor 5G | Compra emergencial hoje | Crítico | 2.5 dias até ruptura, importação 20 dias"
- "Conector Óptico | Antecipar pedido em 48h | Alto | Chuvas intensas previstas (+30%), alta demanda em torres costeiras"
- "Cabo 4G Legacy | Reduzir estoque 30% | Média | Migração 5G reduz demanda em 70%"

Recomendações:
"""
    
    def _parse_response(self, response_text: str, alerts: List[Dict]) -> List[Dict]:
        """Parse LLM response into structured recommendations."""
        # Simple parsing - in production, use more robust parsing
        recommendations = []
        
        lines = response_text.strip().split('\n')
        for line in lines:
            if '|' in line and any(keyword in line.lower() for keyword in ['compra', 'antecipar', 'reduzir', 'aumentar', 'monitorar']):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    recommendations.append({
                        'item': parts[0],
                        'action': parts[1],
                        'urgency': parts[2] if len(parts) > 2 else 'Média',
                        'justification': parts[3] if len(parts) > 3 else ''
                    })
        
        # If no parsed recommendations, create contextual ones from alerts
        if not recommendations:
            recommendations = self._generate_mock_recommendations(alerts)
        
        return recommendations[:10]  # Limit to 10 recommendations
    
    def _generate_mock_recommendations(self, alerts: List[Dict]) -> List[Dict]:
        """Generate contextual mock recommendations when LLM is unavailable."""
        recommendations = []
        
        for alert in alerts[:10]:  # Top 10 critical items
            item = alert.get('item', 'Item')
            level = alert.get('level', 'NORMAL')
            days = alert.get('days_until_stockout', 0)
            current_stock = alert.get('current_stock', 0)
            reorder_point = alert.get('reorder_point', 0)
            
            # Generate context-aware recommendation
            if level == 'CRITICAL':
                action = f"COMPRA EMERGENCIAL IMEDIATA - {current_stock} unidades restantes, {days} dias até ruptura"
                urgency = "CRÍTICO"
                justification = f"Estoque abaixo do PP ({reorder_point}). Risco de multa SLA de R$ 30k-50k/hora por downtime."
            elif level == 'WARNING':
                action = f"ANTECIPAR PEDIDO EM 48H - Estoque {current_stock}, PP {reorder_point}, {days} dias disponíveis"
                urgency = "ALTO"
                justification = f"Estoque aproximando-se do PP. Lead time de importação de 10-20 dias requer ação preventiva."
            else:
                action = f"MONITORAR ESTOQUE - Mantém acima do PP"
                urgency = "BAIXA"
                justification = "Estoque em níveis seguros."
            
            recommendations.append({
                'item': item,
                'action': action,
                'urgency': urgency,
                'justification': justification,
                'type': 'LLM' if self.model else 'MOCK'
            })
        
        return recommendations
    
    def generate_executive_summary(
        self,
        kpis: Dict,
        alerts_summary: Dict,
        climate_summary: Optional[Dict] = None
    ) -> str:
        """
        Generate executive summary in Portuguese.
        
        Args:
            kpis: Key performance indicators
            alerts_summary: Summary of alerts (critical, warning, normal counts)
            climate_summary: Climate conditions summary
            
        Returns:
            Executive summary text
        """
        if not self.model:
            return self._generate_mock_summary(kpis, alerts_summary)
        
        try:
            prompt = f"""
Gere um resumo executivo curto (2-3 parágrafos) em português brasileiro para a Nova Corrente.

KPIs:
- Taxa de Ruptura: {kpis.get('stockout_rate', 'N/A')}
- Acurácia MAPE: {kpis.get('mape_accuracy', 'N/A')}
- Economia Anual: {kpis.get('annual_savings', 'N/A')}

Alertas:
- Críticos: {alerts_summary.get('critical', 0)}
- Avisos: {alerts_summary.get('warning', 0)}
- Normal: {alerts_summary.get('normal', 0)}

{climate_summary or ''}

Resumo:
"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._generate_mock_summary(kpis, alerts_summary)
    
    def _generate_mock_summary(self, kpis: Dict, alerts_summary: Dict) -> str:
        """Generate mock executive summary."""
        critical_count = alerts_summary.get('critical', 0)
        
        summary = f"""
Resumo Executivo - Nova Corrente Demand Forecasting

O sistema de previsão de demanda da Nova Corrente continua operando com excelência, mantendo taxa de ruptura de estoque em {kpis.get('stockout_rate', '6%')} e acurácia MAPE de {kpis.get('mape_accuracy', '10.5%')}. 

Atualmente, existem {critical_count} alertas críticos que requerem atenção imediata para evitar rupturas de estoque que poderiam impactar a disponibilidade das torres e gerar multas significativas de SLA (R$ 30k-50k/hora).

Com {kpis.get('annual_savings', 'R$ 1.2M')} em economia anual estimada através da otimização de estoque e redução de desperdícios, o sistema demonstra valor significativo para a operação da Nova Corrente.

"""
        return summary


# API integration function
def generate_recommendations_endpoint(
    alerts: List[Dict],
    context: Optional[Dict] = None
) -> Dict:
    """
    Generate recommendations via API endpoint format.
    
    Args:
        alerts: List of alerts
        context: Optional context data (climate, SLA, geographic)
        
    Returns:
        API response format
    """
    llm = LLMRecommendations()
    
    climate_data = context.get('climate') if context else None
    sla_data = context.get('sla') if context else None
    geographic_data = context.get('geographic') if context else None
    
    recommendations = llm.generate_recommendations(
        alerts=alerts,
        climate_data=climate_data,
        sla_data=sla_data,
        geographic_data=geographic_data
    )
    
    return {
        'status': 'success',
        'recommendations': recommendations,
        'timestamp': datetime.now().isoformat(),
        'llm_enabled': llm.model is not None
    }


if __name__ == '__main__':
    # Test recommendations
    test_alerts = [
        {
            'item': 'Transceptor 5G',
            'item_code': 'MAT_TRNS_5G',
            'current_stock': 22,
            'reorder_point': 50,
            'days_until_stockout': 2.5,
            'level': 'CRITICAL'
        },
        {
            'item': 'Conector Óptico SC/APC',
            'item_code': 'MAT_CONN_001',
            'current_stock': 65,
            'reorder_point': 132,
            'days_until_stockout': 8.1,
            'level': 'WARNING'
        }
    ]
    
    test_context = {
        'climate': {
            'is_intense_rain': True,
            'is_high_humidity': True,
            'corrosion_risk': 'high'
        },
        'sla': {
            'availability_actual': 0.985,
            'penalty_per_hour_avg': 40000
        },
        'geographic': {
            'region': 'Northeast',
            'is_coastal': True
        }
    }
    
    result = generate_recommendations_endpoint(test_alerts, test_context)
    print(json.dumps(result, indent=2, ensure_ascii=False))

