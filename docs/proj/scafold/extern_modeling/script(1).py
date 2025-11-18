
import pandas as pd

# Create a comprehensive summary table of ALL download links
summary_table = {
    'Data Category': [
        'IPCA (Inflação)', 'IPCA (Inflação)', 'Câmbio USD/BRL', 'Câmbio USD/BRL', 'Selic (Juros)',
        'PIB Trimestral', 'PIB Anual', 'Desemprego', 'População',
        'ICMS (Imposto Estadual)', 'PIS/COFINS (Federal)', 'ISS (Municipal)',
        'Frete Global (WCI)', 'Frete Global (FBX)', 'Frete Global (BDI)',
        'Cobertura 5G', 'Investimentos Telecom', 'Resoluções Anatel',
        'Clima (Temperatura)', 'Clima (Precipitação)', 'Importações Brasil',
        'Exportações Brasil', 'Drawback/Defesa', 'Tarifa MERCOSUR',
        'CDS Brasil', 'PPP (FMI)', 'Índice Desemprego Global'
    ],
    'URL Primária': [
        'https://sidra.ibge.gov.br/acervo#/q/Q1737C',
        'https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/',  # ERRATA: correto é IBGE
        'https://olinda.bcb.gov.br/olinda/servico/PTAX/',
        'https://www.bcb.gov.br/pom/moc/',
        'https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/',
        'https://sidra.ibge.gov.br/acervo#/q/Q12462C',
        'https://sidra.ibge.gov.br/acervo#/q/Q5932C',
        'https://sidra.ibge.gov.br/acervo#/q/Q6385C',
        'https://sidra.ibge.gov.br/acervo#/q/Q29168C',
        'https://www1.confaz.fazenda.gov.br/confaz/public/cf',
        'https://www.receita.gov.br/legislacao/IN1700',
        'https://www.ibpt.org.br/',
        'https://www.drewry.co.uk/',
        'https://www.freightos.com/freight-resources/freight-rate-index/',
        'https://www.balticexchange.com/en/data-services.html',
        'https://informacoes.anatel.gov.br/paineis/acessibilidade',
        'https://informacoes.anatel.gov.br/paineis/investimentos',
        'https://informacoes.anatel.gov.br/documentos',
        'https://portal.inmet.gov.br/',
        'https://bdmep.inmet.gov.br/',
        'https://aliceweb2.mdic.gov.br/',
        'https://aliceweb2.mdic.gov.br/',
        'https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior',
        'https://www.mercosur.int/',
        'https://www.tradingeconomics.com/brazil/sovereign-cds-spread',
        'https://www.imf.org/external/datamapper/',
        'https://fred.stlouisfed.org/search?st=unemployment+brazil'
    ],
    'Fonte Oficial': [
        'IBGE', 'BACEN', 'BACEN', 'BACEN', 'BACEN',
        'IBGE', 'IBGE', 'IBGE', 'IBGE',
        'CONFAZ', 'Receita Federal', 'IBPT/Municípios',
        'Drewry', 'Freightos', 'Baltic Exchange',
        'ANATEL', 'ANATEL', 'ANATEL',
        'INMET', 'INMET', 'MDIC',
        'MDIC', 'MDIC', 'MERCOSUR',
        'Trading Economics', 'IMF', 'FRED/St.Louis'
    ],
    'Frequência': [
        'Mensal', 'Diária', 'Diária', 'Diária', 'Bimestral',
        'Trimestral', 'Anual', 'Mensal', 'Anual',
        'Anual', 'Legal', 'Anual',
        'Semanal', 'Diária', 'Diária',
        'Trimestral', 'Trimestral', 'Contínuo',
        'Diária', 'Diária', 'Real-time',
        'Real-time', 'Irregular', 'Anual',
        'Diária', 'Trimestral', 'Mensal'
    ],
    'Autenticação': [
        'Pública', 'Pública', 'Pública', 'Pública', 'Pública',
        'Pública', 'Pública', 'Pública', 'Pública',
        'Pública', 'Pública', 'Requer Cadastro',
        'Parcial', 'Parcial', 'Assinatura',
        'Pública', 'Pública', 'Pública',
        'Pública', 'Requer Cadastro', 'Login Gratuito',
        'Login Gratuito', 'Pública', 'Pública',
        'API Key', 'Pública', 'Pública'
    ],
    'Tipo Download': [
        'CSV/API', 'API JSON', 'API OData', 'Excel/CSV', 'API JSON',
        'CSV/Excel', 'CSV/Excel', 'CSV/Excel', 'CSV/Excel',
        'Web/PDF', 'PDF', 'Web',
        'Web Scrape', 'Excel/CSV', 'Web Scrape',
        'Dashboard', 'Dashboard', 'PDF',
        'CSV/API', 'CSV/API', 'CSV/Excel',
        'CSV/Excel', 'PDF/Web', 'PDF',
        'Web/API', 'API/JSON', 'CSV/API'
    ],
    'Observações': [
        'Tabela 1737 SIDRA | PIB relacionado',
        'Inflação acumulada 12 meses',
        'Spot, compra, venda, bid-ask',
        'Taxa média operacional',
        'Meta e expectativas de mercado',
        'Variação trimestral',
        'Crescimento anual',
        'Taxa desocupação nacional',
        'Estimativa anual',
        'ICMS Bahia = 18%',
        'IN 1700/2017 | PIS 1,65% + COFINS 7,6%',
        'Varia por município',
        'Shanghai→Rotterdam principalmente',
        'Container rates China→Brasil',
        'Dry bulk (correlação com frete)',
        'Cidades com 5G habilitada',
        'CAPEX por operadora',
        'Resoluções 780/2025 em diante',
        'Temp média, máxima, mínima',
        'Chuva acumulada, umidade',
        'HS codes 8517, 8525, 8526...',
        'HS codes telecom',
        'Prorrogação até 2028 confirmada',
        'TEC atual, exceções (LETEC)',
        'Risco soberano (bps)',
        'Poder de compra relativo',
        'Desemprego EUA vs Brasil (proxy)'
    ]
}

df_summary = pd.DataFrame(summary_table)

# Salvar em CSV
df_summary.to_csv('master_download_links.csv', index=False, encoding='utf-8')

print("📊 TABELA MASTER DE LINKS DE DOWNLOAD")
print("=" * 200)
print(df_summary.to_string(index=False, max_rows=50, max_colwidth=50))
print("\n✅ Salvo em: master_download_links.csv")
print(f"Total: {len(df_summary)} fontes de dados catalogadas")
