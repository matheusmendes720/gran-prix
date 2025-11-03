"""
Streamlit dashboard for demand forecasting system.
Interactive dashboard for visualizing forecasts and inventory metrics.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from demand_forecasting.data.loader import DataLoader
from demand_forecasting.models.ensemble import EnsembleForecaster
from demand_forecasting.inventory.reorder_point import ReorderPointCalculator
from demand_forecasting.inventory.alerts import AlertSystem
from demand_forecasting.reporting.visualization import Visualization
from demand_forecasting.utils.config import Config
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Demand Forecasting Dashboard",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("📈 Demand Forecasting System - Nova Corrente")
st.markdown("---")

# Load configuration
config = Config()

# Sidebar
st.sidebar.header("Configuration")

# Data file upload
data_file = st.sidebar.file_uploader(
    "Upload Data File (CSV/Excel)",
    type=['csv', 'xlsx', 'xls']
)

# Forecast parameters
col1, col2, col3 = st.sidebar.columns(3)
forecast_steps = col1.number_input("Forecast Days", min_value=7, max_value=365, value=30)
lead_time = col2.number_input("Lead Time", min_value=1, max_value=90, value=14)
service_level = col3.number_input("Service Level", min_value=0.0, max_value=1.0, value=0.95, step=0.01)

# Model selection
st.sidebar.subheader("Models")
use_arima = st.sidebar.checkbox("ARIMA", value=True)
use_prophet = st.sidebar.checkbox("Prophet", value=True)
use_lstm = st.sidebar.checkbox("LSTM", value=True)

# Main content
if data_file is not None:
    # Load data
    with st.spinner("Loading data..."):
        # Save uploaded file temporarily
        temp_path = f"temp_{data_file.name}"
        with open(temp_path, "wb") as f:
            f.write(data_file.getbuffer())
        
        try:
            loader = DataLoader(temp_path)
            data_dict = loader.preprocess(
                external_features=config.get('data.external_features', True),
                min_years=1  # Reduced for demo
            )
            st.success(f"Data loaded successfully! {len(data_dict)} items found.")
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.stop()
    
    # Item selection
    if data_dict:
        items = list(data_dict.keys())
        selected_item = st.selectbox("Select Item", items)
        
        if selected_item:
            df = data_dict[selected_item]
            
            # Display data info
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Data Points", len(df))
            col2.metric("Start Date", df.index.min().strftime('%Y-%m-%d'))
            col3.metric("End Date", df.index.max().strftime('%Y-%m-%d'))
            col4.metric("Days", (df.index.max() - df.index.min()).days)
            
            st.markdown("---")
            
            # Get quantity column
            quantity_col = None
            for col in ['Quantity_Consumed', 'quantity', 'demand', 'sales']:
                if col in df.columns:
                    quantity_col = col
                    break
            
            if quantity_col is None:
                quantity_col = df.select_dtypes(include=['number']).columns[0]
            
            # Current stock input
            col1, col2 = st.columns(2)
            current_stock = col1.number_input(
                f"Current Stock for {selected_item}",
                min_value=0,
                value=100,
                step=1
            )
            
            # Process button
            if st.button("Generate Forecast", type="primary"):
                with st.spinner("Processing..."):
                    try:
                        # Split data
                        train, test = loader.train_test_split(df, test_size=0.2)
                        
                        # External regressors
                        exog = None
                        exog_cols = ['temperature', 'holiday']
                        available_exog = [col for col in exog_cols if col in df.columns]
                        if available_exog:
                            exog = df[available_exog]
                        
                        # Fit models
                        ensemble_weights = {}
                        if use_arima:
                            ensemble_weights['ARIMA'] = 0.4 if use_lstm else 0.5
                        if use_prophet:
                            ensemble_weights['Prophet'] = 0.3 if use_lstm else 0.5
                        if use_lstm and use_lstm:
                            ensemble_weights['LSTM'] = 0.3
                        
                        if not ensemble_weights:
                            st.error("Please select at least one model.")
                            st.stop()
                        
                        ensemble = EnsembleForecaster(weights=ensemble_weights, use_lstm=use_lstm)
                        
                        train_exog = exog.loc[train.index] if exog is not None else None
                        fit_results = ensemble.fit(train, quantity_col, train_exog)
                        
                        # Generate forecast
                        future_exog = None
                        if exog is not None:
                            future_exog = pd.DataFrame({
                                col: [exog[col].tail(30).mean()] * forecast_steps
                                for col in available_exog
                            })
                        
                        forecast = ensemble.forecast(forecast_steps, train, future_exog, quantity_col)
                        
                        # Calculate reorder point
                        pp_calc = ReorderPointCalculator(service_level=service_level)
                        pp_metrics = pp_calc.compute_all(forecast, lead_time, current_stock)
                        
                        # Check alerts
                        alert_system = AlertSystem()
                        alert = alert_system.check_reorder_alert(
                            current_stock,
                            pp_metrics['reorder_point'],
                            pp_metrics['days_to_rupture'],
                            selected_item
                        )
                        
                        # Display results
                        st.markdown("### 📊 Forecast Results")
                        
                        col1, col2, col3, col4, col5 = st.columns(5)
                        col1.metric("Current Stock", f"{pp_metrics['current_stock']:.0f}")
                        col2.metric("Reorder Point", f"{pp_metrics['reorder_point']:.0f}")
                        col3.metric("Safety Stock", f"{pp_metrics['safety_stock']:.0f}")
                        col4.metric("Avg Daily Demand", f"{pp_metrics['avg_daily_demand']:.2f}")
                        col5.metric("Days to Rupture", f"{pp_metrics['days_to_rupture']:.1f}")
                        
                        # Alert
                        if alert['alert_triggered']:
                            st.warning(f"⚠️ {alert['urgency'].upper()} ALERT: {alert['message']}")
                        
                        st.markdown("---")
                        
                        # Visualizations
                        st.markdown("### 📈 Forecast Visualization")
                        
                        viz = Visualization()
                        historical = train[quantity_col] if quantity_col in train.columns else train.iloc[:, 0]
                        
                        # Create forecast plot
                        fig = viz.plot_forecast(historical, forecast, item_id=selected_item)
                        st.pyplot(fig)
                        
                        # Ensemble components
                        if ensemble.forecasts:
                            st.markdown("### 🔍 Ensemble Model Components")
                            fig2 = viz.plot_ensemble_components(
                                ensemble.forecasts,
                                item_id=selected_item
                            )
                            st.pyplot(fig2)
                        
                        # Inventory metrics
                        st.markdown("### 📦 Inventory Metrics")
                        fig3 = viz.plot_inventory_metrics(pp_metrics, item_id=selected_item)
                        st.pyplot(fig3)
                        
                        # Forecast table
                        st.markdown("### 📋 Forecast Table")
                        forecast_dates = pd.date_range(
                            start=datetime.now(),
                            periods=len(forecast),
                            freq='D'
                        )
                        forecast_df = pd.DataFrame({
                            'Date': forecast_dates,
                            'Forecasted Demand': forecast.values
                        })
                        st.dataframe(forecast_df, use_container_width=True)
                        
                        # Download forecast
                        csv = forecast_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Forecast CSV",
                            data=csv,
                            file_name=f"forecast_{selected_item}_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                        
                        # Evaluation on test set
                        if len(test) > 0 and len(test) >= 7:
                            st.markdown("### ✅ Model Evaluation")
                            
                            from demand_forecasting.validation.metrics import ValidationMetrics
                            metrics = ValidationMetrics()
                            
                            test_exog = exog.loc[test.index] if exog is not None else None
                            test_forecast = ensemble.forecast(len(test), train, test_exog, quantity_col)
                            
                            test_quantity = test[quantity_col] if quantity_col in test.columns else test.iloc[:, 0]
                            eval_metrics = metrics.calculate_all(test_quantity, test_forecast)
                            
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("MAPE", f"{eval_metrics['MAPE_percent']:.2f}%")
                            col2.metric("RMSE", f"{eval_metrics['RMSE']:.2f}")
                            col3.metric("MAE", f"{eval_metrics['MAE']:.2f}")
                            col4.metric("R²", f"{eval_metrics['R2']:.2f}")
                    
                    except Exception as e:
                        st.error(f"Error: {e}")
                        import traceback
                        st.code(traceback.format_exc())
else:
    st.info("👈 Please upload a data file to get started.")
    
    # Show sample data format
    with st.expander("📝 Sample Data Format"):
        st.code("""
date,Item_ID,Quantity_Consumed,Site_ID,Lead_Time
2022-01-01,CONN-001,15,SITE-001,14
2022-01-02,CONN-001,18,SITE-001,14
2022-01-03,CONN-001,12,SITE-001,14
...
        """)
        
        # Create sample data option
        if st.button("Generate Sample Data"):
            sample_data = create_sample_data_df()
            csv = sample_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Sample CSV",
                data=csv,
                file_name="sample_demand_data.csv",
                mime="text/csv"
            )


def create_sample_data_df():
    """Create sample data DataFrame."""
    dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')
    np.random.seed(42)
    
    data = []
    items = ['CONN-001', 'CABO-001']
    
    for item in items:
        base_demand = 10 if item == 'CONN-001' else 15
        trend = np.linspace(0, 5, len(dates))
        seasonal = 3 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        noise = np.random.normal(0, 2, len(dates))
        
        demand = base_demand + trend + seasonal + noise
        demand = np.maximum(demand, 1)
        
        for date, qty in zip(dates, demand):
            data.append({
                'date': date,
                'Item_ID': item,
                'Quantity_Consumed': qty,
                'Site_ID': 'SITE-001',
                'Lead_Time': 14
            })
    
    return pd.DataFrame(data)

