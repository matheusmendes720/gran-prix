# 🎯 PRÓXIMOS PASSOS: OTIMIZAÇÃO
## Nova Corrente - Analytics Engineering Roadmap

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** 📋 Plano de Ação Imediato  
**Prioridade:** 🔥 ALTA

---

## 📋 CONTEXTO

**Estado Atual:**
- ✅ Fase 1-2 completa (pré-processamento e feature engineering)
- ✅ 73 features implementadas
- ✅ Dataset ML-ready: 2.539 registros
- ✅ Quality score: 70%
- ⏳ Próximo: Otimização para atingir MAPE < 15%

---

## 🎯 OBJETIVOS IMEDIATOS

### Meta Principal
**Melhorar quality score de 70% → 90%+ e atingir MAPE < 15%**

### Objetivos Específicos
1. ✅ Imputar features externas (clima, economia, 5G)
2. ✅ Normalizar/scaling dos dados
3. ✅ Feature selection (73 → 30-40 features)
4. ✅ Otimizar hyperparameters dos modelos
5. ✅ Criar ensemble model
6. ✅ Validar MAPE < 15%

---

## 📅 PLANO DE AÇÃO (2 semanas)

### Semana 3: Otimização de Dados

#### Dia 1-2: Imputação de Features Externas

**Tarefas:**
- [ ] Identificar missing values por feature externa
- [ ] Implementar estratégias de imputação:
  - **Clima (INMET):** Forward fill (mesmo dia do ano anterior)
  - **Economia (BACEN):** Interpolação linear temporal
  - **5G (ANATEL):** Forward fill (última observação válida)
- [ ] Validar imputação (distribuição preservada)
- [ ] Documentar estratégias escolhidas

**Scripts a Criar:**
```python
# scripts/impute_external_features.py
def impute_climate_features(df):
    """Impute missing climate data"""
    # Forward fill from previous year same date
    pass

def impute_economic_features(df):
    """Impute missing economic indicators"""
    # Linear interpolation
    pass

def impute_5g_features(df):
    """Impute missing 5G expansion data"""
    # Forward fill last valid
    pass
```

**Checklist:**
- [ ] Missing values reduzidos de ~30% → <5%
- [ ] Distribuições preservadas
- [ ] Validação visual (histograms antes/depois)

---

#### Dia 3-4: Normalização/Scaling

**Tarefas:**
- [ ] Análise de distribuições das features numéricas
- [ ] Escolher estratégia por tipo:
  - **Normal distribution:** StandardScaler
  - **Skewed distribution:** Log transform + StandardScaler
  - **Bounded (0-1):** MinMaxScaler
  - **Categorical:** One-hot encoding ou Label encoding
- [ ] Aplicar scaling aos datasets train/val/test
- [ ] Salvar scalers para inference

**Scripts a Criar:**
```python
# scripts/normalize_features.py
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer

def create_preprocessing_pipeline():
    """Create preprocessing pipeline with scaling"""
    numeric_features = [...]  # Features numéricas
    categorical_features = [...]  # Features categóricas
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(), categorical_features)
        ]
    )
    return preprocessor
```

**Checklist:**
- [ ] Features numéricas normalizadas (mean=0, std=1)
- [ ] Features categóricas encoded
- [ ] Scalers salvos para uso em produção
- [ ] Validação: distribuições transformadas corretamente

---

#### Dia 5: Feature Selection

**Tarefas:**
- [ ] Análise de correlação entre features
- [ ] Feature importance (Random Forest)
- [ ] Mutual information score
- [ ] Seleção de top 30-40 features
- [ ] Documentar features selecionadas

**Scripts a Criar:**
```python
# scripts/feature_selection.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import mutual_info_regression

def select_features(X, y, n_features=35):
    """Select top N features using multiple methods"""
    # Method 1: Random Forest importance
    rf = RandomForestRegressor(n_estimators=100)
    rf.fit(X, y)
    rf_importance = rf.feature_importances_
    
    # Method 2: Mutual information
    mi_scores = mutual_info_regression(X, y)
    
    # Method 3: Correlation with target
    correlations = X.corrwith(y).abs()
    
    # Combine methods
    # Select top N features
    pass
```

**Checklist:**
- [ ] 73 features → 30-40 features selecionadas
- [ ] Features redundantes removidas
- [ ] Features relevantes preservadas
- [ ] Documentação das features finais

---

### Semana 4: Otimização de Modelos

#### Dia 6-7: Hyperparameter Tuning

**Tarefas:**
- [ ] Prophet: Grid search seasonality modes, changepoints
- [ ] ARIMA: auto_arima com validação cruzada
- [ ] LSTM: Hyperparameter tuning (units, layers, dropout, LR)
- [ ] Validar cada modelo otimizado

**Scripts a Criar:**
```python
# scripts/hyperparameter_tuning.py
from prophet import Prophet
from pmdarima import auto_arima
import optuna

def tune_prophet(train_data):
    """Tune Prophet hyperparameters"""
    study = optuna.create_study(direction='minimize')
    study.optimize(objective_prophet, n_trials=50)
    return study.best_params

def tune_arima(train_data):
    """Tune ARIMA using auto_arima"""
    model = auto_arima(
        train_data,
        seasonal=True,
        m=7,  # Weekly seasonality
        stepwise=True,
        trace=True
    )
    return model

def tune_lstm(X_train, y_train):
    """Tune LSTM hyperparameters"""
    study = optuna.create_study(direction='minimize')
    study.optimize(lambda trial: objective_lstm(trial, X_train, y_train), n_trials=30)
    return study.best_params
```

**Checklist:**
- [ ] Cada modelo otimizado individualmente
- [ ] MAPE melhorado em cada modelo
- [ ] Hyperparameters documentados
- [ ] Modelos salvos para ensemble

---

#### Dia 8-9: Ensemble Model

**Tarefas:**
- [ ] Weighted average dos 3 modelos
- [ ] Otimizar pesos por família de item
- [ ] Stacking com meta-learner (opcional)
- [ ] Validar ensemble no validation set

**Scripts a Criar:**
```python
# scripts/ensemble_model.py
class EnsembleForecaster:
    def __init__(self, prophet_model, arima_model, lstm_model):
        self.prophet = prophet_model
        self.arima = arima_model
        self.lstm = lstm_model
        self.weights = {}  # Por família de item
    
    def optimize_weights(self, val_data, families):
        """Optimize weights per family"""
        for family in families:
            family_data = val_data[val_data['family'] == family]
            weights = self._find_best_weights(family_data)
            self.weights[family] = weights
    
    def predict(self, X, family):
        """Ensemble prediction"""
        pred_prophet = self.prophet.predict(X)
        pred_arima = self.arima.predict(X)
        pred_lstm = self.lstm.predict(X)
        
        w = self.weights[family]
        ensemble = (w[0] * pred_prophet + 
                   w[1] * pred_arima + 
                   w[2] * pred_lstm)
        return ensemble
```

**Checklist:**
- [ ] Ensemble criado e testado
- [ ] Pesos otimizados por família
- [ ] MAPE ensemble < MAPE individual models
- [ ] Modelo ensemble salvo

---

#### Dia 10: Validação Final MAPE < 15%

**Tarefas:**
- [ ] Teste final no test set
- [ ] Backtesting histórico
- [ ] Análise de erros por família
- [ ] Relatório final de performance

**Scripts a Criar:**
```python
# scripts/final_validation.py
def validate_mape_threshold(model, test_data, threshold=15.0):
    """Validate MAPE < threshold"""
    predictions = model.predict(test_data)
    mape = calculate_mape(test_data['actual'], predictions)
    
    if mape < threshold:
        print(f"✅ MAPE {mape:.2f}% < {threshold}%")
        return True
    else:
        print(f"❌ MAPE {mape:.2f}% >= {threshold}%")
        return False

def backtest_historical(model, historical_data):
    """Backtest on historical data"""
    # Rolling window validation
    pass
```

**Checklist:**
- [ ] MAPE < 15% no test set ✅
- [ ] Backtesting passando
- [ ] Relatório de performance completo
- [ ] Pronto para Fase 2 (Analytics Layer)

---

## 📊 MÉTRICAS DE SUCESSO

### Quality Score
- **Atual:** 70%
- **Meta:** 90%+
- **Gap:** +20%

**Melhorias:**
- Imputação: +10%
- Normalização: +5%
- Validação: +5%

### Model Performance
- **Atual:** Não treinado ainda
- **Meta:** MAPE < 15%
- **Baseline esperado:** MAPE 20-25% (antes de otimização)

**Melhorias esperadas:**
- Feature selection: -3% MAPE
- Hyperparameter tuning: -5% MAPE
- Ensemble: -2% MAPE
- **Total esperado:** MAPE 10-12%

---

## 🔄 INTEGRAÇÃO COM PRÓXIMAS FASES

### Após Otimização (Semana 4+)

**Preparação para Fase 2 (Analytics Layer):**
- ✅ Modelos treinados e validados
- ✅ MAPE < 15% confirmado
- ✅ Pipeline de inferência funcionando
- ✅ Métricas de negócio calculáveis

**Próximos entregáveis:**
1. Gold layer (star schema) com previsões
2. dbt models para forecast metrics
3. Dashboards BI (Metabase/Superset)
4. Relatórios automáticos

---

## ✅ CHECKLIST GERAL

### Semana 3 (Otimização de Dados)
- [ ] Imputação de features externas
- [ ] Normalização/scaling
- [ ] Feature selection (73 → 30-40)
- [ ] Quality score: 70% → 90%+

### Semana 4 (Otimização de Modelos)
- [ ] Hyperparameter tuning (3 modelos)
- [ ] Ensemble model criado
- [ ] MAPE < 15% validado
- [ ] Modelos salvos e documentados
- [ ] Pronto para Fase 2

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Plano de Ação Imediato

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

