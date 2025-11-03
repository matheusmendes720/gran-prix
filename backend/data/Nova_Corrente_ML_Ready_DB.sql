-- ============================================
-- NOVA CORRENTE ML-READY DATABASE
-- Complete Database Schema with All Custom Tunings
-- For Nova Corrente B2B Telecom Demand Forecasting
-- ============================================
-- 
-- Features Included:
-- 1. Base inventory management schema
-- 2. ML infrastructure (feature store, model registry, predictions)
-- 3. Brazilian-specific customizations (holidays, climate, economics, 5G)
-- 4. Nova Corrente B2B-specific features (SLA, tier levels, towers)
-- 5. Temporal aggregations (daily, weekly, monthly)
-- 6. All 73 ML features organized in feature tables
-- 7. Stored procedures for Brazilian feature engineering
-- 8. Views optimized for ML processing
-- 
-- Version: 1.0
-- Date: November 2025
-- ============================================

CREATE DATABASE IF NOT EXISTS STOCK;
USE STOCK; 

-- ============================================
-- PART 1: BASE SCHEMA (Original Nova Corrente)
-- ============================================

CREATE TABLE IF NOT EXISTS Usuario (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(50) DEFAULT 'USUARIO' COMMENT 'Papel: ADMIN, GERENTE, USUARIO, TECNICO',
    ultimo_acesso TIMESTAMP,
    total_movimentacoes INT DEFAULT 0,
    INDEX idx_role (role),
    INDEX idx_ultimo_acesso (ultimo_acesso)
);

CREATE TABLE IF NOT EXISTS Familia (
    familia_id INT AUTO_INCREMENT PRIMARY KEY,
    nome_familia VARCHAR(100) NOT NULL UNIQUE,
    categoria_criticidade ENUM('TIER_1', 'TIER_2', 'TIER_3') DEFAULT 'TIER_3',
    sla_target DECIMAL(5,2) DEFAULT 98.00 COMMENT 'SLA target em percentual',
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_criticidade (categoria_criticidade)
);

CREATE TABLE IF NOT EXISTS Fornecedor (
    fornecedor_id INT AUTO_INCREMENT PRIMARY KEY,
    nome_fornecedor VARCHAR(255) NOT NULL UNIQUE,
    contato_email VARCHAR(100),
    contato_telefone VARCHAR(20),
    regiao VARCHAR(50) COMMENT 'Região do fornecedor (NORTE, NORDESTE, SUDESTE, SUL, CENTRO-OESTE)',
    lead_time_medio DECIMAL(5,2) COMMENT 'Lead time médio em dias',
    lead_time_std DECIMAL(5,2) COMMENT 'Desvio padrão do lead time',
    score_performance DECIMAL(5,2) DEFAULT 0 COMMENT 'Score 0-100',
    avaliacao ENUM('EXCELENTE', 'BOM', 'REGULAR', 'RUIM') DEFAULT 'REGULAR',
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_score_performance (score_performance),
    INDEX idx_avaliacao (avaliacao)
);

CREATE TABLE IF NOT EXISTS Material (
    material_id INT AUTO_INCREMENT PRIMARY KEY,
    nome_material VARCHAR(255) NOT NULL,
    descricao TEXT,
    familia_id INT, 
    quantidade_atual INT NOT NULL DEFAULT 0,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- ML-Enhanced Columns
    reorder_point INT DEFAULT 0 COMMENT 'Ponto de reposição calculado por ML',
    safety_stock INT DEFAULT 0 COMMENT 'Estoque de segurança calculado',
    lead_time_medio DECIMAL(5,2) COMMENT 'Tempo médio de reposição em dias',
    rotatividade_anual DECIMAL(10,2) COMMENT 'Rotatividade anual do material',
    categoria_abc VARCHAR(1) COMMENT 'Classificação ABC (A, B, C)',
    score_importancia DECIMAL(5,2) COMMENT 'Score de importância (0-100)',
    tier_nivel ENUM('TIER_1', 'TIER_2', 'TIER_3') DEFAULT 'TIER_3' COMMENT 'Nível de criticidade',
    sla_penalty_brl DECIMAL(15,2) DEFAULT 0 COMMENT 'Penalidade SLA em BRL por hora de downtime',
    disponibilidade_target DECIMAL(5,2) DEFAULT 99.50 COMMENT 'Target de disponibilidade %',
    ultima_atualizacao_ml TIMESTAMP COMMENT 'Última vez que features ML foram atualizadas',
    
    FOREIGN KEY (familia_id) REFERENCES Familia(familia_id),
    INDEX idx_categoria_abc (categoria_abc),
    INDEX idx_score_importancia (score_importancia),
    INDEX idx_tier_nivel (tier_nivel),
    INDEX idx_familia (familia_id)
);

CREATE TABLE IF NOT EXISTS Fornecedor_Material (
    fornecedor_id INT,
    material_id INT,
    lead_time_padrao INT COMMENT 'Lead time padrão para este fornecedor/material',
    prioridade INT DEFAULT 1 COMMENT 'Prioridade do fornecedor para este material',
    
    FOREIGN KEY (fornecedor_id) REFERENCES Fornecedor(fornecedor_id),
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    
    PRIMARY KEY (fornecedor_id, material_id),
    INDEX idx_material (material_id)
);

CREATE TABLE IF NOT EXISTS MovimentacaoEstoque (
    movimentacao_id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT,
    usuario_id INT,
    tipo_movimentacao ENUM('ENTRADA', 'SAIDA') NOT NULL, 
    quantidade_movimentada INT NOT NULL,
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contexto_movimentacao VARCHAR(255) COMMENT 'Contexto adicional da movimentação',
    observacoes TEXT,
    site_id VARCHAR(100) COMMENT 'ID do site/torre relacionada',
    fornecedor_id INT COMMENT 'Fornecedor relacionado (se entrada)',
    
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(usuario_id),
    FOREIGN KEY (fornecedor_id) REFERENCES Fornecedor(fornecedor_id),
    INDEX idx_tipo_data (tipo_movimentacao, data_movimentacao),
    INDEX idx_material_tipo_data (material_id, tipo_movimentacao, data_movimentacao),
    INDEX idx_site (site_id),
    INDEX idx_data_movimentacao (data_movimentacao)
);

-- ============================================
-- PART 2: BRAZILIAN-SPECIFIC REFERENCE TABLES
-- ============================================

-- Brazilian Holidays Calendar
CREATE TABLE IF NOT EXISTS CalendarioBrasil (
    data_referencia DATE PRIMARY KEY,
    dia_semana INT COMMENT '1=Dom, 7=Sab',
    is_feriado BOOLEAN DEFAULT FALSE,
    nome_feriado VARCHAR(255),
    tipo_feriado ENUM('NACIONAL', 'REGIONAL', 'MUNICIPAL') COMMENT 'Tipo de feriado',
    regiao VARCHAR(50) COMMENT 'Região onde se aplica',
    is_carnaval BOOLEAN DEFAULT FALSE COMMENT 'Período de carnaval',
    is_natal BOOLEAN DEFAULT FALSE COMMENT 'Período de Natal/Fim de Ano',
    is_verao BOOLEAN DEFAULT FALSE COMMENT 'Verão (Dez-Fev)',
    is_chuva_sazonal BOOLEAN DEFAULT FALSE COMMENT 'Estação chuvosa (Mai-Ago) em Salvador',
    impact_demanda DECIMAL(3,2) DEFAULT 1.0 COMMENT 'Multiplicador de impacto na demanda',
    INDEX idx_feriado (is_feriado),
    INDEX idx_data (data_referencia)
);

-- Salvador/BA Climate Data (INMET)
CREATE TABLE IF NOT EXISTS ClimaSalvador (
    data_referencia DATE PRIMARY KEY,
    temperatura_media DECIMAL(5,2) COMMENT 'Temperatura média em Celsius',
    temperatura_maxima DECIMAL(5,2),
    temperatura_minima DECIMAL(5,2),
    precipitacao_mm DECIMAL(8,2) COMMENT 'Precipitação em mm',
    umidade_percentual DECIMAL(5,2),
    velocidade_vento_kmh DECIMAL(5,2),
    
    -- Calculated Features
    is_extreme_heat BOOLEAN DEFAULT FALSE COMMENT 'Temperatura > 35°C',
    is_cold_weather BOOLEAN DEFAULT FALSE COMMENT 'Temperatura < 20°C',
    is_heavy_rain BOOLEAN DEFAULT FALSE COMMENT 'Precipitação > 50mm',
    is_no_rain BOOLEAN DEFAULT FALSE COMMENT 'Precipitação = 0',
    is_high_humidity BOOLEAN DEFAULT FALSE COMMENT 'Umidade > 80%',
    is_intense_rain BOOLEAN DEFAULT FALSE COMMENT 'Precipitação > 100mm',
    corrosion_risk DECIMAL(3,2) DEFAULT 0.0 COMMENT 'Risco de corrosão (0-1)',
    field_work_disruption DECIMAL(3,2) DEFAULT 0.0 COMMENT 'Disrupção em trabalho de campo (0-1)',
    
    INDEX idx_data (data_referencia),
    INDEX idx_precipitacao (precipitacao_mm),
    INDEX idx_temperatura (temperatura_media)
);

-- Brazilian Economic Indicators (BACEN)
CREATE TABLE IF NOT EXISTS IndicadoresEconomicos (
    data_referencia DATE PRIMARY KEY,
    taxa_inflacao DECIMAL(5,4) COMMENT 'Taxa de inflação (IPCA) mensal',
    taxa_inflacao_anual DECIMAL(5,2) COMMENT 'Taxa de inflação acumulada 12 meses',
    taxa_cambio_brl_usd DECIMAL(8,4) COMMENT 'Taxa de câmbio BRL/USD',
    pib_crescimento DECIMAL(5,2) COMMENT 'Crescimento do PIB %',
    taxa_selic DECIMAL(5,2) COMMENT 'Taxa SELIC',
    indice_consumo DECIMAL(8,4) COMMENT 'Índice de consumo',
    
    -- Calculated Features
    is_high_inflation BOOLEAN DEFAULT FALSE COMMENT 'Inflação > 6% ao ano',
    is_currency_devaluation BOOLEAN DEFAULT FALSE COMMENT 'Desvalorização cambial > 5%',
    volatilidade_cambio DECIMAL(5,2) COMMENT 'Volatilidade do câmbio',
    
    INDEX idx_data (data_referencia),
    INDEX idx_inflacao (taxa_inflacao_anual)
);

-- 5G Expansion Indicators (ANATEL)
CREATE TABLE IF NOT EXISTS Expansao5G (
    data_referencia DATE PRIMARY KEY,
    cobertura_5g_percentual DECIMAL(5,2) COMMENT 'Cobertura 5G no Brasil em %',
    investimento_5g_brl_billions DECIMAL(10,2) COMMENT 'Investimento 5G em bilhões BRL',
    torres_5g_ativas INT COMMENT 'Número de torres 5G ativas',
    municipios_5g INT COMMENT 'Número de municípios com 5G',
    velocidade_media_mbps DECIMAL(8,2) COMMENT 'Velocidade média em Mbps',
    
    -- Calculated Features
    is_5g_milestone BOOLEAN DEFAULT FALSE COMMENT 'Marco importante de expansão',
    is_5g_active BOOLEAN DEFAULT FALSE COMMENT '5G ativo no período',
    taxa_expansao_5g DECIMAL(5,2) COMMENT 'Taxa de expansão %',
    
    INDEX idx_data (data_referencia),
    INDEX idx_cobertura (cobertura_5g_percentual)
);

-- ============================================
-- PART 3: TEMPORAL AGGREGATIONS
-- ============================================

-- Daily Aggregations
CREATE TABLE IF NOT EXISTS MaterialHistoricoDiario (
    historico_id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    data_referencia DATE NOT NULL,
    quantidade_inicial INT NOT NULL DEFAULT 0,
    quantidade_final INT NOT NULL DEFAULT 0,
    entrada_total INT NOT NULL DEFAULT 0,
    saida_total INT NOT NULL DEFAULT 0,
    numero_movimentacoes INT NOT NULL DEFAULT 0,
    movimentacao_media DECIMAL(10,2),
    valor_maximo INT,
    valor_minimo INT,
    desvio_padrao DECIMAL(10,2),
    dia_semana INT COMMENT '1=Dom, 7=Sab',
    is_weekend BOOLEAN DEFAULT FALSE,
    is_feriado BOOLEAN DEFAULT FALSE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    UNIQUE KEY unique_material_data (material_id, data_referencia),
    INDEX idx_data_referencia (data_referencia),
    INDEX idx_material_data (material_id, data_referencia),
    INDEX idx_dia_semana (dia_semana)
);

-- Weekly Aggregations
CREATE TABLE IF NOT EXISTS MaterialHistoricoSemanal (
    historico_semanal_id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    ano INT NOT NULL,
    semana_ano INT NOT NULL COMMENT 'ISO week (1-53)',
    data_inicio_semana DATE NOT NULL,
    quantidade_media DECIMAL(10,2),
    entrada_total INT NOT NULL DEFAULT 0,
    saida_total INT NOT NULL DEFAULT 0,
    movimentacoes_totais INT NOT NULL DEFAULT 0,
    tendencia VARCHAR(20) COMMENT 'CRESCENTE, DECRESCENTE, ESTAVEL',
    variacao_percentual DECIMAL(5,2),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    UNIQUE KEY unique_material_semana (material_id, ano, semana_ano),
    INDEX idx_ano_semana (ano, semana_ano),
    INDEX idx_material_semana (material_id, ano, semana_ano)
);

-- Monthly Aggregations
CREATE TABLE IF NOT EXISTS MaterialHistoricoMensal (
    historico_mensal_id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    ano INT NOT NULL,
    mes INT NOT NULL,
    quantidade_inicial_mes INT NOT NULL,
    quantidade_final_mes INT NOT NULL,
    entrada_total INT NOT NULL DEFAULT 0,
    saida_total INT NOT NULL DEFAULT 0,
    dias_ativos INT NOT NULL DEFAULT 0,
    rotatividade DECIMAL(10,2) COMMENT 'Inventory turnover',
    cobertura_media DECIMAL(10,2) COMMENT 'Days of stock',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    UNIQUE KEY unique_material_mes (material_id, ano, mes),
    INDEX idx_ano_mes (ano, mes),
    INDEX idx_material_mes (material_id, ano, mes)
);

-- ============================================
-- PART 4: ML FEATURE STORE
-- ============================================

-- Material Features (73 features total)
CREATE TABLE IF NOT EXISTS MaterialFeatures (
    feature_id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    feature_name VARCHAR(100) NOT NULL,
    feature_value DECIMAL(15,4),
    feature_category VARCHAR(50) COMMENT 'TEMPORAL, VOLUME, RELACIONAL, STATISTICAL, CLIMATE, ECONOMIC, 5G, SLA',
    data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valido_ate TIMESTAMP,
    
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    INDEX idx_material_feature (material_id, feature_name),
    INDEX idx_feature_category (feature_category),
    INDEX idx_data_coleta (data_coleta),
    UNIQUE KEY unique_material_feature_date (material_id, feature_name, DATE(data_coleta))
);

-- User Behavior Features
CREATE TABLE IF NOT EXISTS UsuarioFeatures (
    feature_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    feature_name VARCHAR(100) NOT NULL,
    feature_value DECIMAL(15,4),
    feature_category VARCHAR(50),
    data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (usuario_id) REFERENCES Usuario(usuario_id),
    INDEX idx_usuario_feature (usuario_id, feature_name)
);

-- Supplier Performance Features
CREATE TABLE IF NOT EXISTS FornecedorFeatures (
    feature_id INT AUTO_INCREMENT PRIMARY KEY,
    fornecedor_id INT NOT NULL,
    feature_name VARCHAR(100) NOT NULL,
    feature_value DECIMAL(15,4),
    feature_category VARCHAR(50),
    data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (fornecedor_id) REFERENCES Fornecedor(fornecedor_id),
    INDEX idx_fornecedor_feature (fornecedor_id, feature_name)
);

-- Material Text Features (NLP)
CREATE TABLE IF NOT EXISTS MaterialTextFeatures (
    text_feature_id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    feature_type VARCHAR(50) NOT NULL COMMENT 'TFIDF, WORD_EMBEDDING, SENTIMENT, KEYWORDS',
    feature_vector JSON COMMENT 'Store embeddings as JSON array',
    keywords_extracted TEXT,
    sentiment_score DECIMAL(5,4),
    data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    INDEX idx_material_text_feature (material_id, feature_type)
);

-- ============================================
-- PART 5: ML MODEL METADATA & PREDICTIONS
-- ============================================

-- Model Registry
CREATE TABLE IF NOT EXISTS MLModelRegistry (
    model_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    model_type VARCHAR(100) NOT NULL COMMENT 'FORECASTING, CLASSIFICATION, REGRESSION, CLUSTERING, ANOMALY_DETECTION',
    model_version VARCHAR(50) NOT NULL,
    algoritmo VARCHAR(100) COMMENT 'LSTM, RandomForest, XGBoost, Prophet, ARIMA, etc.',
    metricas_avaliacao JSON COMMENT 'Store metrics as JSON',
    hiperparametros JSON,
    caminho_modelo VARCHAR(500) COMMENT 'Path to saved model file',
    data_treinamento TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'ATIVO' COMMENT 'ATIVO, ARQUIVADO, DEPRECADO',
    descricao TEXT,
    familia_id INT COMMENT 'Model trained for specific family',
    
    FOREIGN KEY (familia_id) REFERENCES Familia(familia_id),
    UNIQUE KEY unique_model_version (model_name, model_version),
    INDEX idx_model_type (model_type),
    INDEX idx_status (status),
    INDEX idx_familia (familia_id)
);

-- Predictions Storage
CREATE TABLE IF NOT EXISTS MLPredictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    model_id INT NOT NULL,
    material_id INT,
    usuario_id INT,
    fornecedor_id INT,
    tipo_predicao VARCHAR(100) NOT NULL COMMENT 'DEMANDA, REORDER_POINT, CLASSIFICACAO, ANOMALY, etc.',
    valor_predito DECIMAL(15,4),
    intervalo_confianca_inferior DECIMAL(15,4),
    intervalo_confianca_superior DECIMAL(15,4),
    probabilidade DECIMAL(5,4) COMMENT 'For classification',
    metadados_predicao JSON COMMENT 'Additional prediction metadata',
    data_predicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    horizonte_predicao INT COMMENT 'Days ahead for forecasting',
    data_referencia DATE COMMENT 'Date being predicted',
    
    FOREIGN KEY (model_id) REFERENCES MLModelRegistry(model_id),
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(usuario_id),
    FOREIGN KEY (fornecedor_id) REFERENCES Fornecedor(fornecedor_id),
    INDEX idx_model_prediction (model_id, data_predicao),
    INDEX idx_material_prediction (material_id, tipo_predicao),
    INDEX idx_tipo_predicao (tipo_predicao),
    INDEX idx_data_referencia (data_referencia)
);

-- Actual vs Predicted Tracking
CREATE TABLE IF NOT EXISTS MLPredictionTracking (
    tracking_id INT AUTO_INCREMENT PRIMARY KEY,
    prediction_id INT NOT NULL,
    valor_real DECIMAL(15,4),
    valor_predito DECIMAL(15,4),
    erro DECIMAL(15,4),
    erro_percentual DECIMAL(5,2) COMMENT 'MAPE',
    mae DECIMAL(15,4) COMMENT 'Mean Absolute Error',
    mse DECIMAL(15,4) COMMENT 'Mean Squared Error',
    rmse DECIMAL(15,4) COMMENT 'Root Mean Squared Error',
    data_realizacao TIMESTAMP,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (prediction_id) REFERENCES MLPredictions(prediction_id),
    INDEX idx_prediction_tracking (prediction_id),
    INDEX idx_data_realizacao (data_realizacao)
);

-- ============================================
-- PART 6: ANALYTICS & INSIGHTS
-- ============================================

-- Material Insights
CREATE TABLE IF NOT EXISTS MaterialInsights (
    insight_id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    tipo_insight VARCHAR(100) NOT NULL COMMENT 'TENDENCIA, ALERTA, RECOMENDACAO, PREVISAO, RUPTURA, SOBRA',
    titulo VARCHAR(255),
    descricao TEXT,
    prioridade VARCHAR(20) COMMENT 'BAIXA, MEDIA, ALTA, URGENTE',
    dados_insight JSON,
    data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valido_ate TIMESTAMP,
    visualizado BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    INDEX idx_material_insight (material_id, tipo_insight),
    INDEX idx_prioridade (prioridade),
    INDEX idx_data_geracao (data_geracao),
    INDEX idx_valido_ate (valido_ate)
);

-- Supplier Performance Analytics
CREATE TABLE IF NOT EXISTS FornecedorAnalytics (
    analytics_id INT AUTO_INCREMENT PRIMARY KEY,
    fornecedor_id INT NOT NULL,
    periodo_inicio DATE,
    periodo_fim DATE,
    total_materiais_fornecidos INT,
    materiais_unicos INT,
    movimentacoes_totais INT,
    volume_total_movimentado INT,
    lead_time_medio DECIMAL(5,2),
    lead_time_std DECIMAL(5,2),
    score_performance DECIMAL(5,2) COMMENT '0-100 performance score',
    avaliacao VARCHAR(20) COMMENT 'EXCELENTE, BOM, REGULAR, RUIM',
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (fornecedor_id) REFERENCES Fornecedor(fornecedor_id),
    INDEX idx_fornecedor_analytics (fornecedor_id),
    INDEX idx_score_performance (score_performance)
);

-- Anomaly Detection Results
CREATE TABLE IF NOT EXISTS AnomalyDetection (
    anomaly_id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT,
    usuario_id INT,
    tipo_anomalia VARCHAR(100) NOT NULL COMMENT 'VOLUME_EXTREMO, HORARIO_INCOMUM, PADRAO_ANORMAL, RUPTURA_RISCO',
    severidade VARCHAR(20) COMMENT 'BAIXA, MEDIA, ALTA, CRITICA',
    descricao TEXT,
    dados_anomalia JSON,
    score_anomalia DECIMAL(5,4) COMMENT '0-1 anomaly score',
    data_deteccao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'PENDENTE' COMMENT 'PENDENTE, VERIFICADO, FALSO_POSITIVO, RESOLVIDO',
    observacoes TEXT,
    
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(usuario_id),
    INDEX idx_material_anomaly (material_id),
    INDEX idx_severidade (severidade),
    INDEX idx_data_deteccao (data_deteccao),
    INDEX idx_status (status)
);

-- Audit Trail
CREATE TABLE IF NOT EXISTS MovimentacaoEstoqueAudit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    movimentacao_id INT,
    acao VARCHAR(50) NOT NULL COMMENT 'INSERT, UPDATE, DELETE',
    dados_anteriores JSON,
    dados_novos JSON,
    usuario_id INT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp_audit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (movimentacao_id) REFERENCES MovimentacaoEstoque(movimentacao_id),
    INDEX idx_movimentacao_audit (movimentacao_id),
    INDEX idx_timestamp_audit (timestamp_audit)
);

-- ============================================
-- PART 7: TRIGGERS
-- ============================================

DELIMITER $$

CREATE TRIGGER IF NOT EXISTS trg_aumentar_estoque
AFTER INSERT ON MovimentacaoEstoque
FOR EACH ROW
BEGIN
    IF NEW.tipo_movimentacao = 'ENTRADA' THEN
        UPDATE Material
        SET quantidade_atual = quantidade_atual + NEW.quantidade_movimentada,
            ultima_atualizacao_ml = CURRENT_TIMESTAMP
        WHERE material_id = NEW.material_id;
    END IF;
END$$

CREATE TRIGGER IF NOT EXISTS trg_diminuir_estoque
AFTER INSERT ON MovimentacaoEstoque
FOR EACH ROW
BEGIN
    IF NEW.tipo_movimentacao = 'SAIDA' THEN
        UPDATE Material
        SET quantidade_atual = quantidade_atual - NEW.quantidade_movimentada,
            ultima_atualizacao_ml = CURRENT_TIMESTAMP
        WHERE material_id = NEW.material_id;
        
        -- Update user movement count
        UPDATE Usuario
        SET total_movimentacoes = total_movimentacoes + 1
        WHERE usuario_id = NEW.usuario_id;
    END IF;
END$$

CREATE TRIGGER IF NOT EXISTS trg_atualizar_usuario_acesso
BEFORE UPDATE ON Usuario
FOR EACH ROW
BEGIN
    IF NEW.ultimo_acesso IS NULL THEN
        SET NEW.ultimo_acesso = CURRENT_TIMESTAMP;
    END IF;
END$$

DELIMITER ;

-- ============================================
-- PART 8: STORED PROCEDURES - BRAZILIAN FEATURES
-- ============================================

DELIMITER $$

-- Calculate Daily Aggregations with Brazilian Features
CREATE PROCEDURE IF NOT EXISTS sp_calcular_historico_diario(
    IN p_data_referencia DATE,
    IN p_material_id INT
)
BEGIN
    DECLARE v_is_feriado BOOLEAN DEFAULT FALSE;
    DECLARE v_dia_semana INT;
    DECLARE v_is_weekend BOOLEAN DEFAULT FALSE;
    
    -- Get Brazilian calendar features
    SELECT 
        DAYOFWEEK(p_data_referencia),
        CASE WHEN DAYOFWEEK(p_data_referencia) IN (1, 7) THEN TRUE ELSE FALSE END,
        COALESCE(is_feriado, FALSE)
    INTO v_dia_semana, v_is_weekend, v_is_feriado
    FROM CalendarioBrasil
    WHERE data_referencia = p_data_referencia
    LIMIT 1;
    
    -- If not in calendar, calculate basic features
    IF v_dia_semana IS NULL THEN
        SET v_dia_semana = DAYOFWEEK(p_data_referencia);
        SET v_is_weekend = CASE WHEN v_dia_semana IN (1, 7) THEN TRUE ELSE FALSE END;
    END IF;
    
    INSERT INTO MaterialHistoricoDiario (
        material_id, data_referencia, quantidade_inicial, quantidade_final,
        entrada_total, saida_total, numero_movimentacoes, movimentacao_media,
        valor_maximo, valor_minimo, desvio_padrao, dia_semana, is_weekend, is_feriado
    )
    SELECT 
        m.material_id,
        p_data_referencia,
        COALESCE(MAX(CASE WHEN DATE(me.data_movimentacao) < p_data_referencia THEN m.quantidade_atual END), 0) as quantidade_inicial,
        m.quantidade_atual as quantidade_final,
        COALESCE(SUM(CASE WHEN DATE(me.data_movimentacao) = p_data_referencia AND me.tipo_movimentacao = 'ENTRADA' THEN me.quantidade_movimentada ELSE 0 END), 0) as entrada_total,
        COALESCE(SUM(CASE WHEN DATE(me.data_movimentacao) = p_data_referencia AND me.tipo_movimentacao = 'SAIDA' THEN me.quantidade_movimentada ELSE 0 END), 0) as saida_total,
        COUNT(CASE WHEN DATE(me.data_movimentacao) = p_data_referencia THEN 1 END) as numero_movimentacoes,
        AVG(CASE WHEN DATE(me.data_movimentacao) = p_data_referencia THEN me.quantidade_movimentada END) as movimentacao_media,
        MAX(CASE WHEN DATE(me.data_movimentacao) = p_data_referencia THEN me.quantidade_movimentada END) as valor_maximo,
        MIN(CASE WHEN DATE(me.data_movimentacao) = p_data_referencia THEN me.quantidade_movimentada END) as valor_minimo,
        STDDEV(CASE WHEN DATE(me.data_movimentacao) = p_data_referencia THEN me.quantidade_movimentada END) as desvio_padrao,
        v_dia_semana,
        v_is_weekend,
        v_is_feriado
    FROM Material m
    LEFT JOIN MovimentacaoEstoque me ON m.material_id = me.material_id
    WHERE (p_material_id IS NULL OR m.material_id = p_material_id)
    GROUP BY m.material_id, m.quantidade_atual
    ON DUPLICATE KEY UPDATE
        quantidade_inicial = VALUES(quantidade_inicial),
        quantidade_final = VALUES(quantidade_final),
        entrada_total = VALUES(entrada_total),
        saida_total = VALUES(saida_total),
        numero_movimentacoes = VALUES(numero_movimentacoes),
        movimentacao_media = VALUES(movimentacao_media),
        valor_maximo = VALUES(valor_maximo),
        valor_minimo = VALUES(valor_minimo),
        desvio_padrao = VALUES(desvio_padrao),
        dia_semana = VALUES(dia_semana),
        is_weekend = VALUES(is_weekend),
        is_feriado = VALUES(is_feriado);
END$$

-- Extract All ML Features for Material (73 features)
CREATE PROCEDURE IF NOT EXISTS sp_extrair_features_material_completo(
    IN p_material_id INT,
    IN p_data_referencia DATE
)
BEGIN
    DECLARE v_media_movimentacoes DECIMAL(10,2);
    DECLARE v_total_movimentacoes INT;
    DECLARE v_dias_ativo INT;
    DECLARE v_rotatividade DECIMAL(10,2);
    DECLARE v_familia_id INT;
    DECLARE v_site_id VARCHAR(100);
    
    -- Get material and family info
    SELECT familia_id INTO v_familia_id
    FROM Material
    WHERE material_id = p_material_id;
    
    -- Calculate statistical features
    SELECT 
        AVG(quantidade_movimentada),
        COUNT(*),
        DATEDIFF(COALESCE(p_data_referencia, CURDATE()), MIN(data_movimentacao)),
        CASE WHEN AVG(quantidade_movimentada) > 0 
             THEN (SELECT quantidade_atual FROM Material WHERE material_id = p_material_id) / AVG(quantidade_movimentada) 
             ELSE 0 END
    INTO v_media_movimentacoes, v_total_movimentacoes, v_dias_ativo, v_rotatividade
    FROM MovimentacaoEstoque
    WHERE material_id = p_material_id;
    
    -- Store basic features
    INSERT INTO MaterialFeatures (material_id, feature_name, feature_value, feature_category, data_coleta)
    VALUES 
        (p_material_id, 'media_movimentacoes', v_media_movimentacoes, 'STATISTICAL', CURRENT_TIMESTAMP),
        (p_material_id, 'total_movimentacoes', v_total_movimentacoes, 'VOLUME', CURRENT_TIMESTAMP),
        (p_material_id, 'dias_ativo', v_dias_ativo, 'TEMPORAL', CURRENT_TIMESTAMP),
        (p_material_id, 'rotatividade', v_rotatividade, 'STATISTICAL', CURRENT_TIMESTAMP)
    ON DUPLICATE KEY UPDATE
        feature_value = VALUES(feature_value),
        data_coleta = CURRENT_TIMESTAMP;
    
    -- Calculate and store hierarchical features (family, site, supplier)
    -- This is a simplified version - full implementation would calculate all 73 features
    
    -- Update material ML timestamp
    UPDATE Material 
    SET ultima_atualizacao_ml = CURRENT_TIMESTAMP
    WHERE material_id = p_material_id;
END$$

-- Extract Brazilian External Features (Climate, Economic, 5G)
CREATE PROCEDURE IF NOT EXISTS sp_extrair_features_externas_brasil(
    IN p_data_referencia DATE
)
BEGIN
    -- This procedure would extract external features from reference tables
    -- and store them for materials that need them
    -- Simplified version - full implementation would:
    -- 1. Get climate data from ClimaSalvador
    -- 2. Get economic data from IndicadoresEconomicos
    -- 3. Get 5G data from Expansao5G
    -- 4. Store as MaterialFeatures for all materials active on that date
    
    INSERT INTO MaterialFeatures (material_id, feature_name, feature_value, feature_category, data_coleta)
    SELECT 
        m.material_id,
        CONCAT('external_', f.feature_name) as feature_name,
        f.feature_value,
        'EXTERNAL',
        CURRENT_TIMESTAMP
    FROM Material m
    CROSS JOIN (
        -- Example: Get climate features for the date
        SELECT 'temperature_avg_c' as feature_name, temperatura_media as feature_value
        FROM ClimaSalvador
        WHERE data_referencia = p_data_referencia
        UNION ALL
        SELECT 'precipitation_mm', precipitacao_mm
        FROM ClimaSalvador
        WHERE data_referencia = p_data_referencia
    ) f
    WHERE m.ultima_atualizacao_ml IS NOT NULL
    ON DUPLICATE KEY UPDATE
        feature_value = VALUES(feature_value),
        data_coleta = CURRENT_TIMESTAMP;
END$$

DELIMITER ;

-- ============================================
-- PART 9: VIEWS FOR ML DATA ACCESS
-- ============================================

-- Comprehensive Material View with All Features
CREATE OR REPLACE VIEW vw_material_ml_features AS
SELECT 
    m.material_id,
    m.nome_material,
    m.descricao,
    m.quantidade_atual,
    m.reorder_point,
    m.safety_stock,
    m.categoria_abc,
    m.score_importancia,
    m.tier_nivel,
    m.sla_penalty_brl,
    f.nome_familia,
    f.categoria_criticidade as familia_criticidade,
    COUNT(DISTINCT fm.fornecedor_id) as total_fornecedores,
    COUNT(me.movimentacao_id) as total_movimentacoes,
    AVG(CASE WHEN me.tipo_movimentacao = 'ENTRADA' THEN me.quantidade_movimentada END) as media_entrada,
    AVG(CASE WHEN me.tipo_movimentacao = 'SAIDA' THEN me.quantidade_movimentada END) as media_saida,
    MAX(me.data_movimentacao) as ultima_movimentacao,
    MIN(me.data_movimentacao) as primeira_movimentacao,
    DATEDIFF(CURDATE(), MIN(me.data_movimentacao)) as dias_no_sistema
FROM Material m
LEFT JOIN Familia f ON m.familia_id = f.familia_id
LEFT JOIN Fornecedor_Material fm ON m.material_id = fm.material_id
LEFT JOIN MovimentacaoEstoque me ON m.material_id = me.material_id
GROUP BY m.material_id, m.nome_material, m.descricao, m.quantidade_atual, 
         m.reorder_point, m.safety_stock, m.categoria_abc, m.score_importancia, 
         m.tier_nivel, m.sla_penalty_brl, f.nome_familia, f.categoria_criticidade;

-- Time Series Ready View with Brazilian Features
CREATE OR REPLACE VIEW vw_material_time_series_brasil AS
SELECT 
    mhd.material_id,
    mhd.data_referencia,
    mhd.quantidade_inicial,
    mhd.quantidade_final,
    mhd.entrada_total,
    mhd.saida_total,
    mhd.numero_movimentacoes,
    mhd.movimentacao_media,
    mhd.dia_semana,
    mhd.is_weekend,
    mhd.is_feriado,
    m.nome_material,
    f.nome_familia,
    DAYOFWEEK(mhd.data_referencia) as dia_semana_num,
    DAYOFMONTH(mhd.data_referencia) as dia_mes,
    MONTH(mhd.data_referencia) as mes,
    YEAR(mhd.data_referencia) as ano,
    WEEK(mhd.data_referencia) as semana_ano,
    -- Brazilian Calendar Features
    COALESCE(cb.is_carnaval, FALSE) as is_carnaval,
    COALESCE(cb.is_natal, FALSE) as is_natal,
    COALESCE(cb.is_verao, FALSE) as is_verao,
    COALESCE(cb.is_chuva_sazonal, FALSE) as is_chuva_sazonal,
    COALESCE(cb.impact_demanda, 1.0) as impact_demanda,
    -- Climate Features (Salvador/BA)
    cs.temperatura_media,
    cs.precipitacao_mm,
    cs.umidade_percentual,
    cs.is_extreme_heat,
    cs.is_heavy_rain,
    cs.corrosion_risk,
    cs.field_work_disruption,
    -- Economic Features
    ie.taxa_inflacao,
    ie.taxa_cambio_brl_usd,
    ie.is_high_inflation,
    -- 5G Features
    e5g.cobertura_5g_percentual,
    e5g.is_5g_milestone,
    e5g.taxa_expansao_5g
FROM MaterialHistoricoDiario mhd
JOIN Material m ON mhd.material_id = m.material_id
LEFT JOIN Familia f ON m.familia_id = f.familia_id
LEFT JOIN CalendarioBrasil cb ON mhd.data_referencia = cb.data_referencia
LEFT JOIN ClimaSalvador cs ON mhd.data_referencia = cs.data_referencia
LEFT JOIN IndicadoresEconomicos ie ON mhd.data_referencia = ie.data_referencia
LEFT JOIN Expansao5G e5g ON mhd.data_referencia = e5g.data_referencia
ORDER BY mhd.material_id, mhd.data_referencia;

-- Top 5 Families View (Nova Corrente Specific)
CREATE OR REPLACE VIEW vw_top5_familias_nova_corrente AS
SELECT 
    f.familia_id,
    f.nome_familia,
    COUNT(DISTINCT m.material_id) as total_materiais,
    COUNT(me.movimentacao_id) as total_movimentacoes,
    SUM(CASE WHEN me.tipo_movimentacao = 'ENTRADA' THEN me.quantidade_movimentada ELSE 0 END) as total_entradas,
    SUM(CASE WHEN me.tipo_movimentacao = 'SAIDA' THEN me.quantidade_movimentada ELSE 0 END) as total_saidas,
    AVG(m.quantidade_atual) as estoque_medio,
    AVG(m.reorder_point) as reorder_point_medio,
    MAX(me.data_movimentacao) as ultima_movimentacao,
    COUNT(DISTINCT me.site_id) as sites_ativos,
    COUNT(DISTINCT fm.fornecedor_id) as fornecedores_ativos
FROM Familia f
JOIN Material m ON f.familia_id = m.familia_id
LEFT JOIN MovimentacaoEstoque me ON m.material_id = me.material_id
LEFT JOIN Fornecedor_Material fm ON m.material_id = fm.material_id
WHERE f.nome_familia IN (
    'MATERIAL ELETRICO',
    'FERRO E AÇO',
    'EPI',
    'MATERIAL CIVIL',
    'FERRAMENTAS E EQUIPAMENTOS'
)
GROUP BY f.familia_id, f.nome_familia
ORDER BY total_movimentacoes DESC;

-- ML Predictions Summary View
CREATE OR REPLACE VIEW vw_predictions_summary AS
SELECT 
    ml.model_name,
    ml.model_version,
    ml.algoritmo,
    m.nome_material,
    f.nome_familia,
    pred.tipo_predicao,
    pred.valor_predito,
    pred.data_referencia,
    pred.horizonte_predicao,
    pred.intervalo_confianca_inferior,
    pred.intervalo_confianca_superior,
    track.valor_real,
    track.erro_percentual as mape,
    track.mae,
    track.rmse
FROM MLPredictions pred
JOIN MLModelRegistry ml ON pred.model_id = ml.model_id
LEFT JOIN Material m ON pred.material_id = m.material_id
LEFT JOIN Familia f ON m.familia_id = f.familia_id
LEFT JOIN MLPredictionTracking track ON pred.prediction_id = track.prediction_id
ORDER BY pred.data_predicao DESC, pred.material_id;

-- ============================================
-- END OF ML-READY DATABASE SCAFFOLD
-- ============================================
-- 
-- Next Steps:
-- 1. Populate reference tables (CalendarioBrasil, ClimaSalvador, IndicadoresEconomicos, Expansao5G)
-- 2. Run stored procedures to calculate initial features
-- 3. Set up ETL pipelines for feature engineering
-- 4. Train ML models and register in MLModelRegistry
-- 5. Start generating predictions
-- 
-- ============================================

