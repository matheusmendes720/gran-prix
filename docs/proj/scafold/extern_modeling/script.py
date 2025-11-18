
import pandas as pd
import json
from datetime import datetime

# Criar um mapa abrangente de variáveis MICRO-MES-MACRO com tributação, cambiais e indicadores avançados
# integrando os 4 documentos anexados + dados recentes pesquisados

variables_expanded = {
    'LEVEL': [],
    'CATEGORY': [],
    'VARIABLE': [],
    'DESCRIPTION': [],
    'IMPACT_EXPECTED': [],
    'DATA_SOURCE': [],
    'FREQUENCY': [],
    'ML_FEATURE_NAME': [],
    'RELATION_TYPE': [],
    'CRITICAL_THRESHOLD': [],
    'NOTES': []
}

# ============ MACRO-ECONOMIC LEVEL ============

# Seção 1: TRIBUTOS E ESTRUTURA FISCAL (Nova - Crítica)
macro_tributos = [
    {
        'LEVEL': 'MACRO',
        'CATEGORY': 'Fiscal - Tributos Federais',
        'VARIABLE': 'PIS/COFINS (Contribuições Sociais)',
        'DESCRIPTION': 'PIS 1.65% + COFINS 7.6% = 9.25% sobre receita bruta (regime não-cumulativo) ou 0.65%+3% (cumulativo). Incidem sobre todos serviços telecom.',
        'IMPACT_EXPECTED': '+11.75% custo marginal em regime cumulativo; -5-8% se transição para IBS/CBS até 2026',
        'DATA_SOURCE': 'Receita Federal, MDIC, Instrução Normativa 1.700/2017',
        'FREQUENCY': 'Diário (aplicação contínua); Mudanças legislativas anuais',
        'ML_FEATURE_NAME': 'pis_cofins_rate_combined, pis_cofins_regime_flag',
        'RELATION_TYPE': 'Linear stepwise com quebras legislativas; Lag 0-30 dias para aplicação contábil',
        'CRITICAL_THRESHOLD': 'Mudança regime > 3% impacto direto; Transição IBS (2026) = grande disruption',
        'NOTES': 'Reforma Tributária EC 132/2023 vai substituir por IBS+CBS a partir 2026; sem créditos totais hoje em muitos casos'
    },
    {
        'LEVEL': 'MACRO',
        'CATEGORY': 'Fiscal - Tributos Estaduais',
        'VARIABLE': 'ICMS (Imposto Circulação Mercadorias e Serviços)',
        'DESCRIPTION': 'Imposto estadual 17-18% sobre telecomunicações (pacificado STF/REsp LC 194/2022). Antes chegava 25-30%. Alíquota varia por Estado (Bahia = 18%).',
        'IMPACT_EXPECTED': '+18-25% custo conforme estado; -5-10% se incentivos mantidos; Risco: fim incentivos até 2032',
        'DATA_SOURCE': 'Secretarias Fazenda Estados, STF Decisão RE 574.706, CONFAZ',
        'FREQUENCY': 'Anual (alíquotas); Mudanças legislativas esporádicas; Incentivos: fase-out gradual 2026-2032',
        'ML_FEATURE_NAME': 'icms_rate_state, icms_incentive_status, icms_benefit_end_countdown',
        'RELATION_TYPE': 'Stepwise (mudanças alíquotas); Linear decay (extinção incentivos 6-7 anos)',
        'CRITICAL_THRESHOLD': 'Redução incentivo >2% ao ano = impacto acumulativo; Final 2032 = full rate choque',
        'NOTES': 'Bahia 18% (LC 194); Reforma tributária vai eliminar ICMS até 2033, substituir por IBS; Oportunidade: mapeamento incentivos por região'
    },
    {
        'LEVEL': 'MACRO',
        'CATEGORY': 'Fiscal - Tributos Municipais',
        'VARIABLE': 'ISS (Imposto Sobre Serviços)',
        'DESCRIPTION': 'Imposto municipal 2-5% sobre alguns serviços. Telecomunicações geral paga ICMS, mas serviços acessórios podem cair em ISS (zona cinzenta).',
        'IMPACT_EXPECTED': '+2-5% custo serviços específicos; -1-3% se reclassificação para ICMS; Reforma: eliminado até 2033',
        'DATA_SOURCE': 'Prefeituras municipais, Códigos Municipais, LC 116/2003',
        'FREQUENCY': 'Anual/Biênio; Mudanças legislativas municipais esporádicas',
        'ML_FEATURE_NAME': 'iss_rate_municipal, iss_reclassification_risk, iss_exemption_flag',
        'RELATION_TYPE': 'Stepwise por mudança alíquota; Binary flags para reclassificação',
        'CRITICAL_THRESHOLD': 'Reclassificação serviço = mudança +/-3-5% custo imediato',
        'NOTES': 'Baixo impacto comparado PIS/COFINS+ICMS; Reforma pode abrir planejamento tributário para serviços'
    },
    {
        'LEVEL': 'MACRO',
        'CATEGORY': 'Fiscal - Impostos Específicos Telecom',
        'VARIABLE': 'FUST + FUNTTEL + Condecine + TFI/TFF',
        'DESCRIPTION': 'FUST 0.5% receita (Fundo Universalização); FUNTTEL 0.5% (Fundo Desenvolvimento Tecnológico); Condecine (audiovisual); TFI/TFF (taxas Anatel)',
        'IMPACT_EXPECTED': '+4-5% custo operacional combinado; Variação por tipo serviço (TV paga +Condecine)',
        'DATA_SOURCE': 'Anatel, Ministério das Comunicações, Regulamento FUST/FUNTTEL',
        'FREQUENCY': 'Anual; Revisão orçamentária de 2-4 anos',
        'ML_FEATURE_NAME': 'fust_rate, funttel_rate, condecine_flag, anatel_fee_rate',
        'RELATION_TYPE': 'Linear; Condecine = binary para operadoras TV',
        'CRITICAL_THRESHOLD': 'Aumento FUST >0.2% ou TFI reviravolta = impacto +1-2%',
        'NOTES': 'Soma ~4% carga tributária; Parte do custo não-tributável na Reforma; Pode ser otimizado com transição IBS'
    }
]

# Seção 2: CAMBIAL E VOLATILIDADE
macro_cambial = [
    {
        'LEVEL': 'MACRO',
        'CATEGORY': 'Cambial - Taxas Principais',
        'VARIABLE': 'USD/BRL Taxa de Câmbio',
        'DESCRIPTION': 'Taxa spot diária USD→BRL. Nov 2025: 6.19 BRL/USD (↓27.9% em 2024). Crítica: 60% de fornecedores em USD (China, USA, Europa).',
        'IMPACT_EXPECTED': '+15-20% custo import com desvalorização 10%; +20-25% estoque antecipação se volatilidade >5%',
        'DATA_SOURCE': 'BACEN PTAX API (daily), OpenDataBCB, Trading Economics',
        'FREQUENCY': 'Diário (RT); Volatilidade analisada 7d, 30d, 90d',
        'ML_FEATURE_NAME': 'usd_brl_spot, usd_brl_volatility_30d, usd_brl_trend_3m, currency_crisis_flag',
        'RELATION_TYPE': 'Nonlinear; Exponential weighting recentes; Threshold effects >2% daily',
        'CRITICAL_THRESHOLD': 'Volatilidade >5% (monthly std) = panic buying +15-20%; Crisis (vol>10%) = supply shock',
        'NOTES': 'Principal driver de custo import; Correlação demand antecipada 0.78 (forte); Lag 0-7 dias para decisão compra'
    },
    {
        'LEVEL': 'MACRO',
        'CATEGORY': 'Cambial - Taxas Secundárias',
        'VARIABLE': 'CNY/BRL + EUR/BRL Taxa de Câmbio',
        'DESCRIPTION': 'Taxa CNY→BRL e EUR→BRL (fornecedores China, Europa). CNY dominante (60% suppliers telecom); EUR (40% importação europeia).',
        'IMPACT_EXPECTED': '+10-15% (CNY), +8-12% (EUR) custo separadamente; Correlação USD-CNY 0.92 (alta)',
        'DATA_SOURCE': 'BACEN API, OpenDataBCB, Bloomberg (CNY proxy SE Xangai)',
        'FREQUENCY': 'Diário',
        'ML_FEATURE_NAME': 'cny_brl_spot, eur_brl_spot, foreign_exchange_index_basket',
        'RELATION_TYPE': 'Nonlinear; CNY-USD correlation muy alta',
        'CRITICAL_THRESHOLD': 'Divergência CNY vs USD >3% = oportunidade arbitragem sourcing',
        'NOTES': 'CNY mais volátil por restrições China; EUR mais estável. Diversificação cambial reduz risco 15-20%'
    },
    {
        'LEVEL': 'MACRO',
        'CATEGORY': 'Cambial - Indicadores Estruturais',
        'VARIABLE': 'PPP (Purchasing Power Parity) + Risco País (CDS)',
        'DESCRIPTION': 'PPP ajusta taxa real com inflação relativa; CDS (credit default swaps) mede risco soberano Brasil. CDS Brasil ~130 bps (Nov 2025).',
        'IMPACT_EXPECTED': '+5-10% custo capital se CDS sobe; Efeito indireto em taxas empréstimo fornecedores',
        'DATA_SOURCE': 'IMF PPP Database, Bloomberg CDS, BNDES spreads',
        'FREQUENCY': 'Trimestral (PPP); Diário (CDS)',
        'ML_FEATURE_NAME': 'ppp_adjustment, cds_brazil_bps, sovereign_risk_premium',
        'RELATION_TYPE': 'Linear com lag; CDS Granger-causality com taxa câmbio (sig. 95%)',
        'CRITICAL_THRESHOLD': 'CDS >150 bps = sinal estresse; >200 bps = crise; PPP drift >3% = moeda desalinhada',
        'NOTES': 'CDS usado por investors como early warning; Correlação com demanda B2B -0.65 (quando risco ↑, contratações ↓)'
    }
]

# Seção 3: INFLAÇÃO E TAXA DE JUROS
macro_inflacao = [
    {
        'LEVEL': 'MACRO',
        'CATEGORY': 'Monetária - Inflação',
        'VARIABLE': 'IPCA (Índice Preços ao Consumidor Amplo) + IPCA-15 + IGP-M',
        'DESCRIPTION': 'IPCA oficial mensal (IBGE); IPCA-15 (prévia); IGP-M semanal (Fundação Getulio Vargas, index de preços). IPCA nov 2025: 5.17% YoY; meta 4.5% ± 1.5%.',
        'IMPACT_EXPECTED': '+8-12% demanda antecipação se IPCA >1% mês (inflação alta incentiva compra futura); -5% se IPCA<0.5% (postergação)',
        'DATA_SOURCE': 'IBGE (IPCA dashboard SIDRA, tabelas 1737, 1705, 1736); FGV (IGP-M semanal)',
        'FREQUENCY': 'Mensal (IPCA, IGP-M); 15º de cada mês (IPCA-15)',
        'ML_FEATURE_NAME': 'ipca_12m_accumulated, ipca_mom_latest, ipca_15_preview, igp_m_weekly, inflation_expectation_bacen',
        'RELATION_TYPE': 'Nonlinear; Threshold efeito >1% mês; Lag 1 mês para decisão compra antecipada',
        'CRITICAL_THRESHOLD': 'IPCA >1.0% mês = compras antecipadas +15%; IPCA <0.5% = postergação -5%; Expectativa ↑ vs realizado = demanda + (lag 30d)',
        'NOTES': 'Custo de espera = IPCA mensal / 30 dias; Interação com Selic: ambos afetam via taxa capital; Estoque mínimo sobe 5-8% p/ cada 1% IPCA'
    },
    {
        'LEVEL': 'MACRO',
        'CATEGORY': 'Monetária - Taxa de Juros',
        'VARIABLE': 'Selic (Taxa Básica de Juros)',
        'DESCRIPTION': 'Taxa meta de juro definida por BCB (COPOM meetings ~45 dias). Nov 2025: 15% (máxima em ciclo de aperto). Afeta custo capital, lease de estoque.',
        'IMPACT_EXPECTED': '-5-8% demanda quando tightening >100 bps (reduz credit access); +3-5% quando corte >100 bps (estimula)',
        'DATA_SOURCE': 'BACEN (https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/), decisões COPOM publicadas',
        'FREQUENCY': 'Bimensal (reuniões COPOM); Diário (acompanhamento taxa)',
        'ML_FEATURE_NAME': 'selic_rate_current, selic_rate_delta_3m, selic_expectation_bacen, monetary_policy_cycle_phase',
        'RELATION_TYPE': 'Nonlinear; Inverse demand relação; Lag 45-90 dias (COPOM → operações → decisão estoque)',
        'CRITICAL_THRESHOLD': 'Selic ↑ >150 bps em 3 meses = demanda -5-8%; Selic ↓ >150 bps = +5-8% (credit expansion); >20% = crise',
        'NOTES': 'Real interest rate importante (Selic - IPCA); Hoje real 9-10% (histórico alto); Custo capital estoque ~Selic/12 ao mês'
    }
]

for item in macro_tributos + macro_cambial + macro_inflacao:
    for key in variables_expanded.keys():
        variables_expanded[key].append(item.get(key, ''))

print(f"✓ MACRO-Economic (Fiscal, Cambial, Monetário): {len(macro_tributos + macro_cambial + macro_inflacao)} variáveis\n")

# Mais seções vão ser adicionadas...
print(f"Estrutura criada com {len(macro_tributos + macro_cambial + macro_inflacao)} variáveis MACRO de alto impacto\n")
print("DataFrame variables_expanded inicializado com:\n- Tributos (ICMS, PIS/COFINS, ISS, FUST, TFI/TFF)\n- Cambial (USD/BRL, CNY/BRL, EUR/BRL, PPP, CDS)\n- Monetária (IPCA, Selic)")

# Guardar para próxima fase
df_expanded = pd.DataFrame(variables_expanded)
print(f"\n✓ Total: {len(df_expanded)} variáveis catalogadas")
