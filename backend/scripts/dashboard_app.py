"""
Streamlit Dashboard for Nova Corrente Demand Forecasting System
Interactive web dashboard for visualization and analysis
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
from datetime import datetime, timedelta

# Add demand_forecasting to path
sys.path.insert(0, str(Path(__file__).parent))

from demand_forecasting import DemandForecastingPipeline
from demand_forecasting.data_loader import DataLoader
from demand_forecasting.pp_calculator import PPCalculator


# Page config
st.set_page_config(
    page_title="Nova Corrente - Demand Forecasting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-box {
        background-color: #fee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #efe;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(file_path):
    """Load and cache data."""
    loader = DataLoader()
    return loader.load_and_preprocess(file_path)


@st.cache_data
def generate_forecast(data_dict, config):
    """Generate forecast with caching."""
    pipeline = DemandForecastingPipeline(config=config)
    
    # Prepare models
    pipeline.prepare_models(data_dict)
    
    # Train models
    pipeline.train_models(data_dict)
    
    # Generate forecasts
    forecasts = pipeline.generate_forecasts(data_dict)
    
    return forecasts


def main():
    """Main dashboard application."""
    
    # Header
    st.markdown('<div class="main-header">📊 Nova Corrente Demand Forecasting System</div>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("⚙️ Configuration")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV file",
        type=['csv'],
        help="Upload demand data CSV file"
    )
    
    # Configuration
    service_level = st.sidebar.slider(
        "Service Level",
        min_value=0.80,
        max_value=0.99,
        value=0.95,
        step=0.01,
        help="Desired service level (e.g., 0.95 for 95%)"
    )
    
    forecast_horizon = st.sidebar.number_input(
        "Forecast Horizon (days)",
        min_value=7,
        max_value=90,
        value=30,
        step=7,
        help="Number of days to forecast ahead"
    )
    
    use_ensemble = st.sidebar.checkbox(
        "Use Ensemble Model",
        value=True,
        help="Combine ARIMA, Prophet, and LSTM"
    )
    
    # Ensemble weights
    if use_ensemble:
        st.sidebar.subheader("Ensemble Weights")
        arima_weight = st.sidebar.slider("ARIMA", 0.0, 1.0, 0.4, 0.1)
        prophet_weight = st.sidebar.slider("Prophet", 0.0, 1.0, 0.3, 0.1)
        lstm_weight = st.sidebar.slider("LSTM", 0.0, 1.0, 0.3, 0.1)
        
        # Normalize weights
        total = arima_weight + prophet_weight + lstm_weight
        if total > 0:
            ensemble_weights = {
                'ARIMA': arima_weight / total,
                'Prophet': prophet_weight / total,
                'LSTM': lstm_weight / total
            }
        else:
            ensemble_weights = {'ARIMA': 0.4, 'Prophet': 0.3, 'LSTM': 0.3}
    else:
        ensemble_weights = {'ARIMA': 1.0, 'Prophet': 0.0, 'LSTM': 0.0}
    
    # Configuration dict
    config = {
        'service_level': service_level,
        'ensemble_weights': ensemble_weights,
        'forecast_horizon': forecast_horizon,
        'use_ensemble': use_ensemble,
        'external_features': True
    }
    
    # Main content
    if uploaded_file is not None:
        # Save uploaded file
        temp_file = f"temp_upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(temp_file, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            # Load data
            with st.spinner("Loading and preprocessing data..."):
                data_dict = load_data(temp_file)
            
            # Item selection
            items = list(data_dict.keys())
            selected_item = st.selectbox("Select Item", items)
            
            if selected_item:
                item_df = data_dict[selected_item]
                
                # Tabs
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📊 Overview",
                    "📈 Forecasts",
                    "⚠️ Reorder Points",
                    "📄 Reports"
                ])
                
                with tab1:
                    st.subheader(f"Overview: {selected_item}")
                    
                    # Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        avg_demand = item_df['Quantity_Consumed'].mean()
                        st.metric("Avg Daily Demand", f"{avg_demand:.2f}")
                    
                    with col2:
                        total_demand = item_df['Quantity_Consumed'].sum()
                        st.metric("Total Demand", f"{total_demand:.0f}")
                    
                    with col3:
                        std_demand = item_df['Quantity_Consumed'].std()
                        st.metric("Std Deviation", f"{std_demand:.2f}")
                    
                    with col4:
                        date_range = (item_df.index.max() - item_df.index.min()).days
                        st.metric("Data Range (days)", f"{date_range}")
                    
                    # Historical demand chart
                    st.subheader("Historical Demand")
                    fig = px.line(
                        item_df.reset_index(),
                        x='date',
                        y='Quantity_Consumed',
                        title=f"Historical Demand for {selected_item}"
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab2:
                    st.subheader("Demand Forecasts")
                    
                    # Lead time and current stock
                    col1, col2 = st.columns(2)
                    with col1:
                        lead_time = st.number_input("Lead Time (days)", min_value=1, max_value=60, value=14)
                    with col2:
                        current_stock = st.number_input("Current Stock", min_value=0, value=100)
                    
                    # Generate forecast
                    if st.button("Generate Forecast", type="primary"):
                        with st.spinner("Generating forecast..."):
                            forecasts = generate_forecast(data_dict, config)
                            
                            if selected_item in forecasts:
                                forecast_df = forecasts[selected_item]
                                
                                # Forecast chart
                                fig = go.Figure()
                                
                                # Historical
                                fig.add_trace(go.Scatter(
                                    x=item_df.index[-90:],
                                    y=item_df['Quantity_Consumed'].values[-90:],
                                    mode='lines',
                                    name='Historical',
                                    line=dict(color='blue')
                                ))
                                
                                # Forecast
                                forecast_dates = pd.date_range(
                                    start=item_df.index.max() + timedelta(days=1),
                                    periods=len(forecast_df),
                                    freq='D'
                                )
                                
                                fig.add_trace(go.Scatter(
                                    x=forecast_dates,
                                    y=forecast_df['forecast'],
                                    mode='lines',
                                    name='Forecast',
                                    line=dict(color='green', dash='dash')
                                ))
                                
                                # Confidence interval
                                if 'lower' in forecast_df.columns and 'upper' in forecast_df.columns:
                                    fig.add_trace(go.Scatter(
                                        x=forecast_dates,
                                        y=forecast_df['upper'],
                                        mode='lines',
                                        name='Upper CI',
                                        line=dict(color='gray', width=0),
                                        showlegend=False
                                    ))
                                    fig.add_trace(go.Scatter(
                                        x=forecast_dates,
                                        y=forecast_df['lower'],
                                        mode='lines',
                                        name='Lower CI',
                                        fill='tonexty',
                                        line=dict(color='gray', width=0),
                                        fillcolor='rgba(128,128,128,0.2)',
                                        showlegend=False
                                    ))
                                
                                fig.update_layout(
                                    title=f"Demand Forecast for {selected_item}",
                                    xaxis_title="Date",
                                    yaxis_title="Quantity",
                                    height=500
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Forecast table
                                st.subheader("Forecast Details")
                                forecast_display = pd.DataFrame({
                                    'Date': forecast_dates,
                                    'Forecast': forecast_df['forecast'].values,
                                    'Lower CI': forecast_df.get('lower', forecast_df['forecast'] * 0.9).values,
                                    'Upper CI': forecast_df.get('upper', forecast_df['forecast'] * 1.1).values
                                })
                                st.dataframe(forecast_display, use_container_width=True)
                            
                            else:
                                st.error(f"No forecast generated for {selected_item}")
                
                with tab3:
                    st.subheader("Reorder Point Calculation")
                    
                    # PP Calculator
                    calculator = PPCalculator(service_level=service_level)
                    
                    if 'forecasts' in locals() and selected_item in forecasts:
                        forecast_df = forecasts[selected_item]
                        
                        # Calculate PP
                        pp_info = calculator.calculate_reorder_point(
                            forecast=forecast_df,
                            lead_time=lead_time,
                            current_stock=current_stock,
                            std_demand=item_df['Quantity_Consumed'].std()
                        )
                        
                        # Display PP info
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Reorder Point (PP)", f"{pp_info['reorder_point']:.1f}")
                        
                        with col2:
                            st.metric("Safety Stock", f"{pp_info['safety_stock']:.1f}")
                        
                        with col3:
                            st.metric("Days to Rupture", f"{pp_info['days_to_rupture']:.1f}")
                        
                        with col4:
                            status_color = "🔴" if pp_info['stock_status'] == 'critical' else "🟢"
                            st.metric("Status", f"{status_color} {pp_info['stock_status'].upper()}")
                        
                        # Alert
                        alert = calculator.check_alert(pp_info)
                        if alert:
                            st.markdown(f'<div class="alert-box">{alert}</div>', 
                                      unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="success-box">✅ Stock level is above reorder point</div>', 
                                      unsafe_allow_html=True)
                    
                    else:
                        st.info("Generate forecast first to calculate Reorder Point")
                
                with tab4:
                    st.subheader("Reports")
                    
                    if st.button("Generate Reports"):
                        with st.spinner("Generating reports..."):
                            pipeline = DemandForecastingPipeline(config=config)
                            pipeline.prepare_models(data_dict)
                            pipeline.train_models(data_dict)
                            forecasts = pipeline.generate_forecasts(data_dict)
                            
                            # Calculate PP for all items
                            lead_times = {item: 14 for item in items}
                            current_stocks = {item: 100 for item in items}
                            
                            pp_results = pipeline.calculate_reorder_points(
                                forecasts=forecasts,
                                lead_times=lead_times,
                                current_stocks=current_stocks
                            )
                            
                            # Generate reports
                            report_files = pipeline.generate_reports(output_dir='dashboard_output')
                            
                            # Display reports
                            for report_type, file_path in report_files.items():
                                st.subheader(report_type.replace('_', ' ').title())
                                report_df = pd.read_csv(file_path)
                                st.dataframe(report_df, use_container_width=True)
                                
                                # Download button
                                csv = report_df.to_csv(index=False)
                                st.download_button(
                                    label=f"Download {report_type}",
                                    data=csv,
                                    file_name=Path(file_path).name,
                                    mime='text/csv'
                                )
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.exception(e)
    
    else:
        # Welcome screen
        st.info("👈 Please upload a CSV file to get started")
        
        # Sample data format
        st.subheader("Expected Data Format")
        sample_data = pd.DataFrame({
            'date': pd.date_range('2022-01-01', periods=5, freq='D'),
            'Item_ID': ['CONN-001'] * 5,
            'Quantity_Consumed': [8, 9, 8, 10, 9],
            'Site_ID': ['SITE-001'] * 5,
            'Lead_Time': [14] * 5
        })
        st.dataframe(sample_data)
        
        st.subheader("Features")
        st.markdown("""
        - ✅ **Multiple Models**: ARIMA, Prophet, LSTM
        - ✅ **Ensemble Forecasting**: Weighted combination
        - ✅ **Reorder Point Calculation**: PP with Safety Stock
        - ✅ **Alert System**: Automatic alerts when stock ≤ PP
        - ✅ **Interactive Charts**: Plotly visualizations
        - ✅ **Report Generation**: CSV exports
        """)


if __name__ == "__main__":
    main()

