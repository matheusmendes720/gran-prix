
# Criar uma análise completa e resumida dos 3 pilares com Python
# Gerar visualizações de dados e pipeline

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# ============================================
# ANÁLISE 1: Modelo de Negócio B2B
# ============================================

business_model = {
    "tipo": "B2B (Business-to-Business)",
    "clientes_principais": [
        "Claro/Vivo/TIM (operadoras)",
        "Oi Telecom",
        "Algar Telecom",
        "American Tower Company (Sharing)",
        "SBA Communications (Sharing)",
        "Concessionárias de energia"
    ],
    "servicos": [
        "Manutenção Preventiva (O&M)",
        "Manutenção Corretiva (emergencial)",
        "Implantação de novos sites",
        "Vistoria de torres",
        "Inspeção com drone",
        "Reforço estrutural"
    ],
    "sla_critico": {
        "disponibilidade_minima": "99%+",
        "tempo_resposta": "4-8 horas",
        "consequencia_falha": "Multa + perda de cliente",
        "porque_previsibilidade_importa": "Ruptura estoque = falha SLA = multa"
    }
}

print("=" * 70)
print("MODELO DE NEGÓCIO - NOVA CORRENTE")
print("=" * 70)
print(f"Tipo: {business_model['tipo']}\n")
print("Clientes Principais:")
for cliente in business_model['clientes_principais']:
    print(f"  • {cliente}")
print("\nServiços:")
for servico in business_model['servicos']:
    print(f"  • {servico}")
print("\nSLA Crítico:")
for chave, valor in business_model['sla_critico'].items():
    print(f"  • {chave.replace('_', ' ').title()}: {valor}")

# ============================================
# ANÁLISE 2: Os 3 Pilares da Solução
# ============================================

print("\n" + "=" * 70)
print("OS 3 PILARES DA SOLUÇÃO")
print("=" * 70)

pilares = {
    "Pilar 1 - IA Prevê DEMANDA": {
        "o_que_faz": "Analisa histórico diário de consumo",
        "saida": "Quantidade que será consumida amanhã (ex: 8 conectores)",
        "nao_faz": "Não prevê nível de estoque",
        "formula": "AI_Output = f(historical_demand, seasonality, external_factors)",
        "exemplo": {
            "data": "2025-11-07",
            "estoque_atual": 100,
            "previsao_consumo": 8,
            "estoque_projetado": 92,
            "resultado": "Normalizou porque 92 > Reorder Point (90)"
        }
    },
    "Pilar 2 - Alerta em Reorder Point": {
        "o_que_faz": "Calcula quando COMPRAR (não quando falta)",
        "formula": "PP = (Demanda_Diária × Lead_Time) + Safety_Stock",
        "parametros": {
            "demanda_diaria": "Fornecida pela IA",
            "lead_time": "Dias para fornecedor entregar (ex: 14 dias)",
            "safety_stock": "Buffer de proteção (ex: 20 unidades)"
        },
        "exemplo_calculo": {
            "demanda_diaria": 8,
            "lead_time_dias": 14,
            "safety_stock": 20,
            "reorder_point": 132,
            "interpretacao": "Compre quando estoque ≤ 132 unidades"
        },
        "por_que_critico": "Se esperar estoque mínimo (20), já perdeu 14 dias = ruptura"
    },
    "Pilar 3 - Previsão DIÁRIA": {
        "o_que_faz": "Prevê demanda para cada dia (não mês inteiro)",
        "por_que": "Necessário para calcular dias até ruptura, PP recalculado diariamente",
        "exemplo_30_dias": {
            "dia_1": 8,
            "dia_2": 7,
            "dia_3": 9,
            "dia_4": 8,
            "total_4_dias": 32,
            "mais_preciso_que_media": "Captura variabilidade dia a dia"
        },
        "saidas": [
            "Alerta: Faltam 7 dias até ruptura",
            "Recomendação: Compre 250 unidades em 2 dias",
            "Relatório semanal com projeção 30 dias"
        ]
    }
}

for pilar, detalhes in pilares.items():
    print(f"\n{pilar}")
    print("-" * 70)
    for chave, valor in detalhes.items():
        if isinstance(valor, dict):
            print(f"  {chave}:")
            for k, v in valor.items():
                print(f"    • {k}: {v}")
        elif isinstance(valor, list):
            print(f"  {chave}:")
            for item in valor:
                print(f"    • {item}")
        else:
            print(f"  {chave}: {valor}")

# ============================================
# ANÁLISE 3: Fatores Externos
# ============================================

print("\n" + "=" * 70)
print("FATORES EXTERNOS QUE IMPACTAM A DEMANDA")
print("=" * 70)

fatores_externos = {
    "Climáticos": {
        "Calor Extremo (>32°C)": {
            "impacto": "+30% demanda",
            "materiais": ["Refrigeração", "Conectores", "Baterias"],
            "lead_time_ajuste": "+2-3 dias"
        },
        "Chuva Intensa": {
            "impacto": "+40% demanda",
            "materiais": ["Estrutura", "Revestimento", "Isolamento"],
            "lead_time_ajuste": "+3-5 dias"
        },
        "Umidade Alta": {
            "impacto": "+20% demanda",
            "materiais": ["Parafusos", "Conectores metálicos"],
            "lead_time_ajuste": "+5-7 dias"
        },
        "Tempestades/Ventos": {
            "impacto": "+50% demanda (URGENTE)",
            "materiais": ["Reforço estrutural", "Parafusos"],
            "lead_time_ajuste": "+5-10 dias"
        }
    },
    "Econômicos": {
        "Desvalorização BRL": {
            "impacto": "Fornecedor reduz entregas",
            "lead_time_ajuste": "7 → 14 dias",
            "acao": "Antecipar compra em 3-5 dias"
        },
        "Greve de Transportes": {
            "impacto": "-100% entregas",
            "lead_time_ajuste": "14 → 21+ dias",
            "acao": "Aumentar safety stock em 50%"
        },
        "Restrição de Importação": {
            "impacto": "Falta de componentes",
            "lead_time_ajuste": "× 2-3",
            "acao": "Comprar no Brasil (premium) ou estocar"
        }
    },
    "Tecnológicos": {
        "Expansão 5G": {
            "impacto": "+15-20% demanda anual",
            "novo_material": ["Transceivers", "Amplificadores"],
            "acao": "Antecipar compra de novo material"
        },
        "Migração Fibra Óptica": {
            "impacto": "Reduz 30% de cabo simples, +50% fibra",
            "materiais_fora": ["Cabo simples"],
            "materiais_dentro": ["Fibra óptica", "Conectores SC/APC"]
        }
    },
    "Operacionais": {
        "Férias Julho": {
            "impacto": "-25% demanda",
            "acao": "Reduzir previsão, estoque aumenta"
        },
        "Feriados Prolongados": {
            "impacto": "-20% demanda",
            "acao": "Ajustar PP downward"
        },
        "Renovação SLA (Jan/Jul)": {
            "impacto": "+25% demanda",
            "acao": "Aumentar estoque 3-4 semanas antes"
        }
    }
}

for categoria, fatores in fatores_externos.items():
    print(f"\n{categoria}:")
    for fator, detalhe in fatores.items():
        print(f"\n  🔸 {fator}")
        for chave, valor in detalhe.items():
            print(f"     • {chave}: {valor}")

# ============================================
# ANÁLISE 4: Pipeline de Processamento
# ============================================

print("\n" + "=" * 70)
print("PIPELINE COMPLETO DE PROCESSAMENTO")
print("=" * 70)

pipeline = {
    "Entrada (Input Layer)": [
        "✓ Histórico de consumo diário (2+ anos)",
        "✓ Lead times por fornecedor",
        "✓ Previsão meteorológica (INMET)",
        "✓ Calendário (feriados, férias, renovação SLA)",
        "✓ Indicadores econômicos (câmbio, inflação)",
        "✓ Dados de 5G expansion"
    ],
    "Processamento (ML Layer)": [
        "1. EDA - Análise Exploratória",
        "2. Feature Engineering (sazonalidade, trend)",
        "3. Seleção de Modelo (ARIMA/Prophet/LSTM)",
        "4. Treinamento com ajustes externos",
        "5. Validação (MAPE < 15%)",
        "6. Ensemble de múltiplos modelos"
    ],
    "Cálculos Determinísticos": [
        "PP = (Demanda_Diária × Lead_Time) + Safety_Stock",
        "SS = Z × σd × √(LT)  [fórmula estatística]",
        "Dias_até_Ruptura = (Estoque_Atual - SS) / Demanda_Diária",
        "Lead_Time_Ajustado = Lead_Time_Base × (1 + Risco_Externo)"
    ],
    "Saída (Output Layer)": [
        "✓ Previsão 30 dias (com confidence intervals)",
        "✓ Reorder Point calculado",
        "✓ Alerta quando Estoque ≤ PP",
        "✓ Dias até ruptura",
        "✓ Recomendação: 'Compre X unidades em Y dias'",
        "✓ Relatório semanal com cenários"
    ]
}

for etapa, items in pipeline.items():
    print(f"\n{etapa}:")
    for item in items:
        print(f"  {item}")

# ============================================
# ANÁLISE 5: Exemplo Prático Completo
# ============================================

print("\n" + "=" * 70)
print("EXEMPLO PRÁTICO: CONECTOR ÓPTICO")
print("=" * 70)

exemplo_completo = pd.DataFrame({
    'Data': pd.date_range('2025-10-20', periods=10),
    'Estoque_Atual': [85, 77, 70, 68, 60, 52, 50, 42, 35, 27],
    'Consumo_Real': [8, 7, 2, 8, 8, 2, 8, 8, 7, 8],
    'Previsao_IA': [8.2, 7.1, 8.3, 8.0, 7.9, 8.1, 8.2, 7.8, 8.0, 8.5]
})

# Calcular Reorder Point
demanda_diaria = 8
lead_time = 14
safety_stock = 20
reorder_point = (demanda_diaria * lead_time) + safety_stock

exemplo_completo['Reorder_Point'] = reorder_point
exemplo_completo['Status'] = exemplo_completo['Estoque_Atual'].apply(
    lambda x: '🔴 ALERTA - COMPRE JÁ' if x <= reorder_point else 
    ('🟡 ATENÇÃO' if x <= reorder_point * 1.2 else '✅ OK')
)

print("\nTabela de Acompanhamento:")
print(exemplo_completo.to_string(index=False))

print(f"\n\nParâmetros:")
print(f"  • Demanda diária: {demanda_diaria} conectores")
print(f"  • Lead time: {lead_time} dias")
print(f"  • Safety stock: {safety_stock} unidades")
print(f"  • REORDER POINT: {reorder_point} unidades")
print(f"\n✅ Quando estoque ≤ {reorder_point}, alerta dispara!")
print(f"   Isso dá {lead_time} dias para fornecedor + {safety_stock} de buffer")

# ============================================
# Exportar como CSV
# ============================================

exemplo_completo.to_csv('exemplo_reorder_point.csv', index=False)
print(f"\n✓ Arquivo 'exemplo_reorder_point.csv' criado")

