# 🔬 ALGORITMOS MATEMÁTICOS COMPLETOS
## Sistema de Previsão de Demanda - Nova Corrente

---

## 📋 ÍNDICE DE ALGORITMOS

1. [Preprocessing Algorithms](#1-preprocessing-algorithms)
2. [Feature Engineering](#2-feature-engineering)
3. [Model Training](#3-model-training)
4. [Forecasting](#4-forecasting)
5. [Ensemble Methods](#5-ensemble-methods)
6. [Alert System](#6-alert-system)
7. [Optimization](#7-optimization)
8. [Validation](#8-validation)

---

## 1. PREPROCESSING ALGORITHMS

### 1.1 Data Cleaning

```python
ALGORITMO: Data_Cleaning
INPUT: Raw dataset D
OUTPUT: Cleaned dataset D_clean

1. // Detect missing values
2. missing_cols ← Get_Missing_Columns(D)
3. 
4. FOR each col in missing_cols DO
5.     IF col is time_series THEN
6.         D[col] ← Forward_Fill(D[col])
7.     ELSE IF col is categorical THEN
8.         D[col] ← Mode_Fill(D[col])
9.     ELSE IF col is numerical THEN
10.        D[col] ← Mean_Fill(D[col])
11.    END IF
12. END FOR
13. 
14. // Detect and handle outliers
15. FOR each numerical_col in D DO
16.     Q1 ← Quantile(D[numerical_col], 0.25)
17.     Q3 ← Quantile(D[numerical_col], 0.75)
18.     IQR ← Q3 - Q1
19.     LB ← Q1 - 1.5 × IQR
20.     UB ← Q3 + 1.5 × IQR
21.     
22.     outliers ← WHERE (D[numerical_col] < LB OR D[numerical_col] > UB)
23.     D ← Remove_Rows(D, outliers)
24. END FOR
25. 
26. // Standardize formats
27. D.date ← Parse_Date(D.date)
28. D.numerical_cols ← Convert_To_Numeric(D.numerical_cols)
29. 
30. RETURN D
```

---

### 1.2 Data Aggregation

```python
ALGORITMO: Aggregate_To_Daily
INPUT: Dataset D with granularity G (hourly/weekly/monthly)
OUTPUT: Daily aggregated dataset D_daily

1. // Group by date and aggregate
2. aggregation_functions ← {
3.     'quantity': 'sum',
4.     'cost': 'sum',
5.     'temperature': 'mean',
6.     'precipitation': 'sum',
7.     'humidity': 'mean'
8. }
9. 
10. D_daily ← D.groupby(['date', 'item_id', 'site_id']).agg(aggregation_functions)
11. 
12. RETURN D_daily
```

---

### 1.3 Time Series Stationarity

```python
ALGORITMO: Make_Stationary
INPUT: Time series D_t, method (diff/log/boxcox)
OUTPUT: Stationary series D_stationary

1. // ADF Test
2. (statistic, pvalue, is_stationary) ← ADF_Test(D_t)
3. 
4. IF is_stationary THEN
5.     RETURN D_t
6. END IF
7. 
8. // Apply transformation
9. IF method == 'log' THEN
10.    D_stationary ← log(D_t + 1)  // +1 to avoid log(0)
11. ELSE IF method == 'diff' THEN
12.    D_stationary ← D_t - D_t.shift(1)
13. ELSE IF method == 'boxcox' THEN
14.    (D_stationary, lambda_param) ← boxcox(D_t)
15. ELSE IF method == 'seasonal_diff' THEN
16.    D_stationary ← D_t - D_t.shift(seasonal_period)
17. END IF
18. 
19. RETURN D_stationary
```

---

## 2. FEATURE ENGINEERING

### 2.1 Temporal Features

```python
ALGORITMO: Create_Temporal_Features
INPUT: Dataset D with date column
OUTPUT: Dataset D with temporal features

1. // Extract time components
2. D['year'] ← Extract_Year(D.date)
3. D['month'] ← Extract_Month(D.date)
4. D['day'] ← Extract_Day(D.date)
5. D['weekday'] ← Extract_Weekday(D.date)
6. D['week'] ← Extract_Week(D.date)
7. D['quarter'] ← Extract_Quarter(D.date)
8. 
9. // Cyclical encoding
10. D['month_sin'] ← sin(2 × π × D.month / 12)
11. D['month_cos'] ← cos(2 × π × D.month / 12)
12. D['weekday_sin'] ← sin(2 × π × D.weekday / 7)
13. D['weekday_cos'] ← cos(2 × π × D.weekday / 7)
14. 
15. // Flags
16. D['is_weekend'] ← (D.weekday >= 5) ? 1 : 0
17. D['is_holiday'] ← Check_Holiday(D.date)
18. D['is_month_end'] ← (D.day >= 25) ? 1 : 0
19. 
20. RETURN D
```

---

### 2.2 Lag Features

```python
ALGORITMO: Create_Lag_Features
INPUT: Time series D_t, max_lag L
OUTPUT: Dataset with lag features

1. // Create lags
2. FOR lag IN [1, 2, ..., L] DO
3.     D['lag_' + str(lag)] ← D['quantity'].shift(lag)
4. END FOR
5. 
6. // Create rolling statistics
7. D['rolling_mean_7'] ← D['quantity'].rolling(window=7).mean()
8. D['rolling_std_7'] ← D['quantity'].rolling(window=7).std()
9. D['rolling_mean_30'] ← D['quantity'].rolling(window=30).mean()
10. D['rolling_std_30'] ← D['quantity'].rolling(window=30).std()
11. 
12. // Exponentially weighted
13. D['ewm_mean_7'] ← D['quantity'].ewm(span=7).mean()
14. D['ewm_std_7'] ← D['quantity'].ewm(span=7).std()
15. 
16. RETURN D
```

---

### 2.3 External Factors Integration

```python
ALGORITMO: Add_External_Factors
INPUT: Dataset D, External data sources
OUTPUT: Dataset D with external factors

1. // Climate data
2. climate_data ← Load_Climate_API(date_range)
3. FOR each row in D DO
4.     D[row].temperature ← climate_data[row.date].temp
5.     D[row].precipitation ← climate_data[row.date].precip
6.     D[row].humidity ← climate_data[row.date].humidity
7.     
8.     // Climate flags
9.     D[row].extreme_heat ← (D[row].temperature > 35) ? 1 : 0
10.    D[row].heavy_rain ← (D[row].precipitation > 50) ? 1 : 0
11.    D[row].high_humidity ← (D[row].humidity > 80) ? 1 : 0
12. END FOR
13. 
14. // Economic data
15. economic_data ← Load_Economic_API(date_range)
16. FOR each row in D DO
17.     D[row].exchange_rate ← economic_data[row.date].usd_brl
18.     D[row].inflation ← economic_data[row.date].inflation
19.     D[row].gdp_growth ← economic_data[row.date].gdp
20.     
21.     // Economic flags
22.     D[row].high_inflation ← (D[row].inflation > 5) ? 1 : 0
23.     D[row].currency_devaluation ← (D[row].exchange_rate > 5.5) ? 1 : 0
24. END FOR
25. 
26. // Calculate impact scores
27. FOR each row in D DO
28.     D[row].climate_impact ← Calculate_Climate_Score(row)
29.     D[row].economic_impact ← Calculate_Economic_Score(row)
30.     D[row].operational_impact ← Calculate_Operational_Score(row)
31. END FOR
32. 
33. RETURN D
```

---

## 3. MODEL TRAINING

### 3.1 ARIMA Training

```python
ALGORITMO: Train_ARIMA
INPUT: Time series D_train, max_order (p_max, d_max, q_max)
OUTPUT: Best ARIMA model

1. // Find optimal differencing
2. d ← 0
3. is_stationary ← False
4. WHILE d <= d_max AND NOT is_stationary DO
5.     D_diff ← Difference(D_train, order=d)
6.     (stat, pval, is_stationary) ← ADF_Test(D_diff)
7.     IF NOT is_stationary THEN
8.         d ← d + 1
9.     END IF
10. END WHILE
11. 
12. // Grid search for (p, q)
13. best_aic ← infinity
14. best_model ← None
15. 
16. FOR p IN range(0, p_max+1) DO
17.     FOR q IN range(0, q_max+1) DO
18.         TRY:
19.             model ← ARIMA(D_train, order=(p, d, q))
20.             fitted_model ← model.fit()
21.             aic ← fitted_model.aic
22.             
23.             IF aic < best_aic THEN
24.                 best_aic ← aic
25.                 best_model ← fitted_model
26.                 best_order ← (p, d, q)
27.             END IF
28.         EXCEPT:
29.             CONTINUE  // Skip if model fails
30.         END TRY
31.     END FOR
32. END FOR
33. 
34. RETURN best_model, best_order, best_aic
```

---

### 3.2 Prophet Training

```python
ALGORITMO: Train_Prophet
INPUT: Dataset D (columns: ds, y), external_regressors R
OUTPUT: Fitted Prophet model

1. // Initialize Prophet model
2. model ← Prophet(
3.     yearly_seasonality=True,
4.     weekly_seasonality=True,
5.     daily_seasonality=False,
6.     seasonality_mode='additive',  // or 'multiplicative'
7.     changepoint_prior_scale=0.05
8. )
9. 
10. // Add external regressors
11. FOR each regressor r in R DO
12.     model.add_regressor(r)
13. END FOR
14. 
15. // Fit model (Stan backend - Bayesian inference)
16. fitted_model ← model.fit(D)
17. 
18. // Validate (optional)
19. cross_validation ← model_cross_validation(
20.     fitted_model,
21.     horizon='30 days',
22.     period='10 days',
23.     initial='730 days'
24. )
25. 
26. RETURN fitted_model, cross_validation
```

---

### 3.3 LSTM Training

```python
ALGORITMO: Train_LSTM
INPUT: Time series D_train, look_back L, hidden_units H
OUTPUT: Trained LSTM model

1. // Normalization
2. scaler ← MinMaxScaler(feature_range=(0, 1))
3. D_scaled ← scaler.fit_transform(D_train)
4. 
5. // Create sliding windows
6. X, y ← []
7. FOR i IN range(L, len(D_scaled)) DO
8.     X.append(D_scaled[i-L:i])
9.     y.append(D_scaled[i])
10. END FOR
11. 
12. X ← np.array(X).reshape((len(X), L, 1))
13. y ← np.array(y)
14. 
15. // Train/validation split
16. split_idx ← int(0.8 × len(X))
17. X_train, X_val ← X[:split_idx], X[split_idx:]
18. y_train, y_val ← y[:split_idx], y[split_idx:]
19. 
20. // Build LSTM architecture
21. model ← Sequential()
22. model.add(LSTM(H, return_sequences=True, input_shape=(L, 1)))
23. model.add(Dropout(0.2))
24. model.add(LSTM(H, return_sequences=False))
25. model.add(Dropout(0.2))
26. model.add(Dense(1))
27. 
28. // Compile
29. model.compile(
30.     optimizer=Adam(learning_rate=0.001),
31.     loss='mse',
32.     metrics=['mae']
33. )
34. 
35. // Train with early stopping
36. early_stop ← EarlyStopping(
37.     monitor='val_loss',
38.     patience=10,
39.     restore_best_weights=True
40. )
41. 
42. history ← model.fit(
43.     X_train, y_train,
44.     validation_data=(X_val, y_val),
45.     epochs=100,
46.     batch_size=32,
47.     callbacks=[early_stop],
48.     verbose=1
49. )
50. 
51. RETURN model, scaler, history
```

---

## 4. FORECASTING

### 4.1 ARIMA Forecasting

```python
ALGORITMO: Forecast_ARIMA
INPUT: Fitted ARIMA model, horizon h
OUTPUT: Forecast with confidence intervals

1. // Generate forecast
2. forecast_result ← model.get_forecast(steps=h)
3. 
4. // Extract results
5. forecast_mean ← forecast_result.predicted_mean
6. forecast_conf_int ← forecast_result.conf_int()
7. 
8. // Optional: dynamic forecast vs static
9. IF dynamic THEN
10.    forecast_mean ← []
11.    FOR step IN range(1, h+1) DO
12.        next_pred ← model.forecast(steps=1)
13.        forecast_mean.append(next_pred[0])
14.        model ← model.update(next_obs)  // Re-train with new obs
15.    END FOR
16. END IF
17. 
18. RETURN forecast_mean, forecast_conf_int
```

---

### 4.2 Prophet Forecasting

```python
ALGORITMO: Forecast_Prophet
INPUT: Fitted Prophet model, horizon h, future_regressors R
OUTPUT: Forecast with components

1. // Create future dataframe
2. future ← model.make_future_dataframe(periods=h)
3. 
4. // Add future external regressors
5. FOR each regressor r in R DO
6.     future[r] ← Get_Future_Values(r, h)
7. END FOR
8. 
9. // Generate forecast
10. forecast ← model.predict(future)
11. 
12. // Extract components
13. forecast_mean ← forecast['yhat']
14. forecast_lower ← forecast['yhat_lower']
15. forecast_upper ← forecast['yhat_upper']
16. trend_component ← forecast['trend']
17. seasonal_component ← forecast['yearly'] + forecast['weekly']
18. 
19. // Return future predictions only
20. future_forecast ← forecast.tail(h)
21. 
22. RETURN future_forecast
```

---

### 4.3 LSTM Forecasting

```python
ALGORITMO: Forecast_LSTM
INPUT: Trained LSTM model, scaler, last L observations, horizon h
OUTPUT: Forecast

1. // Prepare last window
2. last_window ← last_L_observations
3. last_window_scaled ← scaler.transform(last_window)
4. 
5. // Initialize
6. forecast ← []
7. current_window ← last_window_scaled.reshape(1, L, 1)
8. 
9. // Iterative forecasting
10. FOR step IN range(1, h+1) DO
11.     // Predict next value
12.     next_pred_scaled ← model.predict(current_window)
13.     forecast.append(next_pred_scaled[0, 0])
14.     
15.     // Slide window
16.     current_window ← np.append(
17.         current_window[:, 1:, :],
18.         next_pred_scaled.reshape(1, 1, 1),
19.         axis=1
20.     )
21. END FOR
22. 
23. // Denormalize
24. forecast_rescaled ← scaler.inverse_transform(np.array(forecast).reshape(-1, 1))
25. 
26. RETURN forecast_rescaled.flatten()
```

---

## 5. ENSEMBLE METHODS

### 5.1 Weighted Average Ensemble

```python
ALGORITMO: Weighted_Ensemble
INPUT: Forecasts [F_1, F_2, ..., F_M], performance_metrics
OUTPUT: Ensemble forecast

1. // Calculate inverse error weights
2. errors ← []
3. FOR each forecast F_i DO
4.     error_i ← Calculate_RMSE(F_i, actual_values)
5.     errors.append(error_i)
6. END FOR
7. 
8. // Weight inversely proportional to error
9. inverse_errors ← [1/e for e in errors]
10. weights ← inverse_errors / sum(inverse_errors)
11. 
12. // Alternative: optimized weights (least squares)
13. // Solve: min ||y - sum(w_i * F_i)||^2 subject to sum(w_i) = 1
14. 
15. weights ← Optimize_Weights_MinLS([F_1, ..., F_M], actual_values)
16. 
17. // Generate ensemble forecast
18. ensemble_forecast ← sum([w_i * F_i for w_i, F_i in zip(weights, [F_1, ..., F_M])])
19. 
20. RETURN ensemble_forecast, weights
```

---

### 5.2 Stacking Ensemble

```python
ALGORITMO: Stacking_Ensemble
INPUT: Base models [M_1, ..., M_k], training data D, validation split
OUTPUT: Meta-learner model

1. // Split data
2. train_idx, val_idx ← TimeSeriesSplit(D, n_splits=5)
3. 
4. // Generate base model predictions on validation set
5. base_predictions ← []
6. FOR fold_idx IN range(len(train_idx)) DO
7.     fold_train ← D[train_idx[fold_idx]]
8.     fold_val ← D[val_idx[fold_idx]]
9.     
10.    fold_predictions ← []
11.    FOR model M_i IN [M_1, ..., M_k] DO
12.        M_i.fit(fold_train)
13.        pred_i ← M_i.predict(fold_val)
14.        fold_predictions.append(pred_i)
15.    END FOR
16.    
17.    base_predictions.append(fold_predictions)
18. END FOR
19. 
20. // Stack horizontally: [F1_val, F2_val, ..., Fk_val]
21. meta_X ← Stack_Horizontal(base_predictions)
22. meta_y ← Get_Actual_Values(val_idx)
23. 
24. // Train meta-learner
25. meta_learner ← RidgeRegression(alpha=0.1)
26. meta_learner.fit(meta_X, meta_y)
27. 
28. // Final prediction
29. FOR model M_i IN [M_1, ..., M_k] DO
30.    M_i.fit(full_training_data)
31.    F_i ← M_i.predict(test_data)
32.    final_base_predictions.append(F_i)
33. END FOR
34. 
35. ensemble_forecast ← meta_learner.predict(
36.     Stack_Horizontal(final_base_predictions)
37. )
38. 
39. RETURN ensemble_forecast
```

---

## 6. ALERT SYSTEM

### 6.1 Reorder Point Calculation

```python
ALGORITMO: Calculate_Reorder_Point
INPUT: Forecast D_forecast, lead_time LT, service_level SL
OUTPUT: Reorder point PP

1. // Calculate demand statistics
2. D_avg ← mean(D_forecast)
3. D_std ← std(D_forecast)
4. 
5. // Calculate Z-score for service level
6. Z_alpha ← norm.ppf(SL)  // e.g., 0.95 -> 1.65
7. 
8. // Safety stock
9. SS ← Z_alpha × D_std × sqrt(LT)
10. 
11. // Reorder point
12. PP ← (D_avg × LT) + SS
13. 
14. RETURN PP, SS
```

---

### 6.2 Alert Generation

```python
ALGORITMO: Check_And_Generate_Alert
INPUT: Current stock S, Reorder point PP, Forecast
OUTPUT: Alert or None

1. // Calculate days until rupture
2. D_avg ← mean(Forecast)
3. safety_stock ← Calculate_Safety_Stock(Forecast, LT)
4. 
5. IF S > PP THEN
6.     RETURN None  // No alert needed
7. END IF
8. 
9. // Calculate metrics
10. days_to_rupture ← (S - safety_stock) / D_avg
11. reorder_quantity ← PP - S + 0.1 × PP  // Add 10% buffer
12. 
13. // Determine priority
14. IF days_to_rupture < 3 THEN
15.     priority ← 'CRITICAL'
16.     action_required ← 'ORDER TODAY'
17. ELSE IF days_to_rupture < 7 THEN
18.     priority ← 'HIGH'
19.     action_required ← 'ORDER WITHIN 2 DAYS'
20. ELSE IF days_to_rupture < 14 THEN
21.     priority ← 'MEDIUM'
22.     action_required ← 'ORDER THIS WEEK'
23. ELSE
24.     priority ← 'LOW'
25.     action_required ← 'PLAN FOR ORDER'
26. END IF
27. 
28. // Create alert object
29. alert ← {
30.     'item_id': Item_ID,
31.     'timestamp': current_time,
32.     'current_stock': S,
33.     'reorder_point': PP,
34.     'days_to_rupture': days_to_rupture,
35.     'reorder_quantity': reorder_quantity,
36.     'priority': priority,
37.     'action_required': action_required,
38.     'forecast_avg_demand': D_avg
39. }
40. 
41. // Send notification
42. Send_Email_Alert(alert)
43. Send_SMS_Alert(alert)  // if critical
44. Log_To_Dashboard(alert)
45. 
46. RETURN alert
```

---

## 7. OPTIMIZATION

### 7.1 Bayesian Optimization for Hyperparameters

```python
ALGORITMO: Bayesian_Optimization
INPUT: Objective function f, search space, n_iterations
OUTPUT: Best hyperparameters

1. // Initialize with random samples
2. samples ← Random_Sample(search_space, n_initial=10)
3. results ← [f(x) for x in samples]
4. 
5. // Build Gaussian Process surrogate
6. gp_model ← GaussianProcessRegressor(kernel=RBF())
7. gp_model.fit(samples, results)
8. 
9. // Iterative optimization
10. FOR iteration IN range(n_iterations) DO
11.     // Maximize acquisition function (EI)
12.     best_x ← Optimize_Acquisition_Function(gp_model, search_space, method='EI')
13.     
14.     // Evaluate objective
15.     best_y ← f(best_x)
16.     
17.     // Update GP
18.     samples ← np.append(samples, [best_x], axis=0)
19.     results ← np.append(results, [best_y])
20.     gp_model.fit(samples, results)
21. END FOR
22. 
23. // Find best result
24. best_idx ← argmin(results)
25. best_params ← samples[best_idx]
26. best_score ← results[best_idx]
27. 
28. RETURN best_params, best_score
```

---

## 8. VALIDATION

### 8.1 Walk-Forward Validation

```python
ALGORITMO: Walk_Forward_Validation
INPUT: Time series D, Model M, n_splits, test_size
OUTPUT: Validation metrics

1. metrics ← []
2. forecasts ← []
3. actuals ← []
4. 
5. // Time series split
6. FOR split IN range(n_splits) DO
7.     // Determine split points
8.     total_size ← len(D)
9.     train_end ← total_size - (n_splits - split) × test_size
10.    test_start ← train_end + 1
11.    test_end ← min(test_start + test_size - 1, total_size)
12.    
13.    // Split data
14.    D_train ← D[:train_end]
15.    D_test ← D[test_start:test_end]
16.    
17.    // Train model
18.    M.fit(D_train)
19.    
20.    // Forecast
21.    forecast ← M.forecast(len(D_test))
22.    
23.    // Evaluate
24.    mape ← Calculate_MAPE(D_test, forecast)
25.    rmse ← Calculate_RMSE(D_test, forecast)
26.    mae ← Calculate_MAE(D_test, forecast)
27.    
28.    // Store
29.    metrics.append({'MAPE': mape, 'RMSE': rmse, 'MAE': mae})
30.    forecasts.extend(forecast)
31.    actuals.extend(D_test)
32. END FOR
33. 
34. // Aggregate results
35. avg_mape ← mean([m['MAPE'] for m in metrics])
36. avg_rmse ← mean([m['RMSE'] for m in metrics])
37. avg_mae ← mean([m['MAE'] for m in metrics])
38. 
39. RETURN {
40.     'individual_metrics': metrics,
41.     'average_MAPE': avg_mape,
42.     'average_RMSE': avg_rmse,
43.     'average_MAE': avg_mae,
44.     'all_forecasts': forecasts,
45.     'all_actuals': actuals
46. }
```

---

## ✅ CONCLUSÃO

Este documento contém **algoritmos completos** para:
1. ✅ Preprocessamento de dados
2. ✅ Feature Engineering
3. ✅ Treinamento de modelos (ARIMA, Prophet, LSTM)
4. ✅ Forecasting
5. ✅ Ensemble Methods
6. ✅ Sistema de Alertas
7. ✅ Otimização Bayesiana
8. ✅ Validação Cruzada Temporal

**Total:** 20+ algoritmos detalhados em pseudocódigo

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

