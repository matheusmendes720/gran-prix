
import pandas as pd
import json

# Criar dados estruturados para o Kick Off - Fase 1: Frase de Efeito e Problema

kick_off_data = {
    "SETOR_TELECOM_BRASIL": {
        "receita_bruta_2024": "R$ 318 bilhões",
        "investimentos_2024": "R$ 34,6 bilhões",
        "crescimento_2024": "4,9% (acumulado)",
        "tendencia_crescimento": "2,4% (acumulado 12 meses até julho 2025)",
        "foco_principal": "Expansão 5G e banda larga fixa",
        "investimentos_futuro_2025_2027": "R$ 100 bilhões"
    },
    "MERCADO_5G": {
        "cidades_5g_cobertura": "812 municípios",
        "crescimento_cidades": "131% em relação período anterior",
        "antenas_5g_instaladas": "37.639 antenas",
        "crescimento_antenas": "dobro do período anterior (de 18.408 para 37.639)",
        "acessos_5g": "40 milhões (duplicou em 1 ano)",
        "populacao_coberta_5g": "~70% população brasileira"
    },
    "MERCADO_BANDAS_INFRAESTRUTURA": {
        "banda_larga_fixa_acessos": "52 milhões",
        "crescimento_banda_larga": "10,1%",
        "crescimento_fibra_optica": "13,5%",
        "velocidade_media": "440 Mbps",
        "torre_empresas_independentes": "81.567 torres",
        "lider_market_share": "American Tower - 22.800 torres (27,9%)"
    },
    "OPERADORES_PRINCIPAIS": {
        "operadoras": ["Claro", "Vivo", "TIM", "Oi"],
        "tower_companies": ["American Tower", "SBA Communications", "IHS Towers"],
        "servicos_operacao_manutencao": ["Nova Corrente", "Softmig", "TIVIT"]
    }
}

# Dados sobre o Problema: Falta de Previsibilidade
problema_data = {
    "PROBLEMA_CENTRAL": {
        "titulo": "FALTA DE PREVISIBILIDADE DE DEMANDA",
        "descricao": "Gestão manual de estoque com reação a rupturas, não prevenção"
    },
    "SITUACAO_ATUAL_NOVA_CORRENTE": {
        "torres_sob_manutencao": "18.000 torres",
        "posicoes_ativas_salvador": "100 posições",
        "projecao_2026": "150 posições",
        "gestao_inventario": "Manual e baseada em intuição"
    },
    "DESAFIOS_ESPECIFICOS": [
        "Rupturas de Estoque - Peça crítica em falta leva a: manutença atrasada, falha SLA, multa",
        "Estoque Exagerado - Capital travado em peças que não movimentam",
        "Lead Times Variáveis - Fornecedores diferentes têm tempos distintos (7-60+ dias)",
        "Sazonalidade - Padrões de consumo variam ao longo do ano",
        "Fatores Externos - Clima, economia, eventos tecnológicos afetam demanda",
        "Crescimento - Expansão rápida de 50 posições até 2026 exige planejamento preciso"
    ]
}

# Criar DataFrame para visualização
dados_evidencias = {
    "CATEGORIA": [
        "Receita Setor Telecom",
        "Investimentos 2024",
        "Cidades com 5G",
        "Crescimento 5G",
        "Torres Brasil",
        "Multa SLA (Vivo)",
        "Multa SLA (Oi - Móvel)",
        "Impacto Mercado (Falhas Previsão)"
    ],
    "METRICA": [
        "R$ 318 bilhões",
        "R$ 34,6 bilhões",
        "812 municípios",
        "131% crescimento",
        "81.567 torres",
        "R$ 3,9 milhões",
        "R$ 34,2 milhões",
        "76% empresas impactadas"
    ],
    "RELEVANCIA_KICK_OFF": [
        "Mercado aquecido, investimentos contínuos",
        "Forte demanda por serviços de manutenção",
        "Expansão agressiva = mais torres = mais demanda",
        "Demanda crescente por manutenção preventiva",
        "Gigantesco volume sob gerenciamento",
        "Casos reais de penalidades por falhas SLA",
        "Escala de multa que pode comprometer operações",
        "Falhas previsibilidade prejudicam valor mercado"
    ]
}

df_evidencias = pd.DataFrame(dados_evidencias)

# Salvar como CSV para exportação
df_evidencias.to_csv('evidencias_kick_off_pitch_deck.csv', index=False, encoding='utf-8')

print("=" * 80)
print("DADOS PARA KICK OFF - PITCH DECK NOVA CORRENTE")
print("Frase de Efeito + Problema: Falta de Previsibilidade de Demanda")
print("=" * 80)
print("\n")

print("1. CONTEXTO DO SETOR - MERCADO AQUECIDO")
print("-" * 80)
print(f"  • Receita bruta 2024: {kick_off_data['SETOR_TELECOM_BRASIL']['receita_bruta_2024']}")
print(f"  • Investimentos 2024: {kick_off_data['SETOR_TELECOM_BRASIL']['investimentos_2024']}")
print(f"  • Crescimento 2024: {kick_off_data['SETOR_TELECOM_BRASIL']['crescimento_2024']}")
print(f"  • Investimentos futuros (2025-2027): {kick_off_data['SETOR_TELECOM_BRASIL']['investimentos_futuro_2025_2027']}")
print(f"  • Foco: {kick_off_data['SETOR_TELECOM_BRASIL']['foco_principal']}")
print("\n")

print("2. EXPLOSÃO DE 5G - DEMANDA CRESCENTE")
print("-" * 80)
print(f"  • {kick_off_data['MERCADO_5G']['cidades_5g_cobertura']} com cobertura 5G (+131%)")
print(f"  • {kick_off_data['MERCADO_5G']['antenas_5g_instaladas']} antenas instaladas (dobro)")
print(f"  • {kick_off_data['MERCADO_5G']['acessos_5g']} acessos 5G (superou 3G em 1 ano)")
print(f"  • ~70% da população brasileira com cobertura")
print(f"  • Banda larga fixa: {kick_off_data['MERCADO_BANDAS_INFRAESTRUTURA']['banda_larga_fixa_acessos']} acessos (+10,1%)")
print(f"  • Fibra óptica: crescimento de 13,5%")
print("\n")

print("3. INFRAESTRUTURA DE TORRES - ESCALA MASSIVA")
print("-" * 80)
print(f"  • Total: {kick_off_data['MERCADO_BANDAS_INFRAESTRUTURA']['torre_empresas_independentes']} torres no Brasil")
print(f"  • Líder: {kick_off_data['MERCADO_BANDAS_INFRAESTRUTURA']['lider_market_share']}")
print(f"  • Operadoras: {', '.join(kick_off_data['OPERADORES_PRINCIPAIS']['operadoras'])}")
print(f"  • Tower Companies: {', '.join(kick_off_data['OPERADORES_PRINCIPAIS']['tower_companies'])}")
print(f"  • Nova Corrente: 18.000 torres sob manutenção, 100 posições em Salvador, projeção 150 até 2026")
print("\n")

print("4. PROBLEMA CENTRAL - DADOS & EVIDÊNCIAS PARA KICK OFF")
print("=" * 80)
print("\nPROBLEMA: Falta de Previsibilidade de Demanda")
print("Sintoma: Gestão manual, reativa, baseada em intuição")
print("\nDESAFIOS OPERACIONAIS:")
for i, desafio in enumerate(problema_data['DESAFIOS_ESPECIFICOS'], 1):
    print(f"  {i}. {desafio}")
print("\n")

print("5. IMPACTO FINANCEIRO - MULTAS E RUPTURA SLA")
print("=" * 80)
print("\nCasos Reais de Multas por Falhas:")
print(f"  • Vivo (2013): Multa de R$ 3,9 MILHÕES - descumprimento qualidade telefonia fixa")
print(f"  • Oi (2013): Multa de R$ 34,2 MILHÕES - descumprimento metas qualidade")
print(f"  • Oi (2013): Multa de R$ 4,6 MILHÕES - descumprimento metas PGMU")
print("\nSLA B2B Telecom:")
print(f"  • Target: 99% disponibilidade")
print(f"  • Penalidade: 2-10% do valor do contrato POR RUPTURA")
print(f"  • Cascata de Impacto: Ruptura > Manutenção Atrasada > Falha SLA > MULTA > Perda Cliente Recorrente")
print(f"  • Em B2B, perda de cliente = perda de receita recorrente SUBSTANCIAL (contrato 3-10 anos)")
print("\n")

print("6. IMPACTO DE FALHAS EM PREVISÃO - ESTUDO KPMG (FEV 2025)")
print("=" * 80)
print(f"  • 21% empresas com queda > 10% em ações")
print(f"  • 5,4% empresas com perdas > 20%")
print(f"  • 76% impactam direto valor de mercado")
print(f"  • Custo: Desorganização operacional, capital travado, emergências custosas")
print("\n")

print("7. FATORES EXTERNOS - SAZONALIDADE & IMPACTOS")
print("=" * 80)
print("\nFATORES CLIMÁTICOS (Bahia):")
print(f"  • Chuva (Nov-Abr): +40% demanda estrutural, +60% impermeabilização, lead time dobra")
print(f"  • Calor (Dez-Mar): +25% refrigeração, +20% corrosão")
print(f"  • Tempestades: +50% emergência, 5-10 dias lead time")
print(f"  • Carnaval (Fev): -30% manutenção, +50% demanda pós-festival")
print("\nFATORES TECNOLÓGICOS:")
print(f"  • Expansão 5G: +15-20% demanda anual, planejado")
print(f"  • Migração Fibra: -30% cabo simples, +30% componentes ópticos")
print(f"  • Renovação SLA (Jan-Jul): +25% demanda imediata por 30-45 dias")
print("\nFATORES ECONÔMICOS:")
print(f"  • Desvalorização BRL: Pode adicionar 7-14 dias lead time")
print(f"  • Inflação: 10-15% pode requerer compra antecipada")
print(f"  • Greves Transporte: -100% disponibilidade, 14-21 dias lead time")
print("\n")

print("\n" + "=" * 80)
print("FRASE DE EFEITO PARA ABERTURA DO PITCH DECK:")
print("=" * 80)
print("""
"O Brasil investe R$ 34,6 bilhões ao ano em telecomunicações, com 5G chegando
a 812 municípios e crescimento de 131%. Nova Corrente gerencia 18.000 torres.

MAS: Gestão manual de demanda deixa 81.567 torres brasileiras vulneráveis a
RUPTURAS DE ESTOQUE que geram multas de R$ 34,2 MILHÕES e perda de contratos
multimilionários. 

A falta de PREVISIBILIDADE DE DEMANDA não é mais um problema operacional –
é um RISCO DE NEGÓCIO com impacto de 76% no valor de mercado."
""")
print("=" * 80)

# Criar um JSON estruturado para facilitar exportação
evidencias_json = {
    "kick_off_contexto_mercado": kick_off_data,
    "problema_central": problema_data,
    "casos_multas": [
        {
            "empresa": "Vivo",
            "multa_valor": "R$ 3,9 milhões",
            "motivo": "Descumprimento qualidade telefonia fixa",
            "ano": 2013
        },
        {
            "empresa": "Oi - Móvel",
            "multa_valor": "R$ 34,2 milhões",
            "motivo": "Descumprimento metas qualidade",
            "ano": 2013
        },
        {
            "empresa": "Oi - Fixa",
            "multa_valor": "R$ 4,6 milhões",
            "motivo": "Descumprimento metas PGMU",
            "ano": 2013
        }
    ],
    "sla_metricas": {
        "target_disponibilidade": "99%",
        "penalidade_percentual": "2-10% do valor contrato",
        "tempo_resposta_emergencia": "4-8 horas",
        "downtime_maximo_mes": "1 hora"
    },
    "estudo_kpmg_fevereiro_2025": {
        "empresas_queda_10pct": "21%",
        "empresas_queda_20pct": "5,4%",
        "impacto_valor_mercado": "76%"
    }
}

with open('evidencias_kick_off_completo.json', 'w', encoding='utf-8') as f:
    json.dump(evidencias_json, f, ensure_ascii=False, indent=2)

print("\n\nJSON EXPORTADO: evidencias_kick_off_completo.json")
print("CSV EXPORTADO: evidencias_kick_off_pitch_deck.csv")
