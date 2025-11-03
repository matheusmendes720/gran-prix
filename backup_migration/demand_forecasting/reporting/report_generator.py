"""
Report generation module.
Creates CSV and PDF reports with forecasts, reorder points, and alerts.
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: reportlab not available. PDF reports cannot be generated.")
import warnings
warnings.filterwarnings('ignore')


class ReportGenerator:
    """Generate reports in CSV and PDF formats."""
    
    def __init__(self):
        """Initialize report generator."""
        pass
    
    def generate_csv_report(self, results: Dict, output_path: str) -> str:
        """
        Generate CSV report with forecasts and inventory metrics.
        
        Args:
            results: Dictionary with results for each item:
                {
                    'item_id': {
                        'forecast': pd.Series,
                        'pp_metrics': dict,
                        'alert': dict
                    },
                    ...
                }
            output_path: Path to save CSV file
        
        Returns:
            Path to generated CSV file
        """
        report_data = []
        
        for item_id, item_results in results.items():
            forecast = item_results.get('forecast', pd.Series())
            pp_metrics = item_results.get('pp_metrics', {})
            alert = item_results.get('alert', {})
            
            # Summary row
            report_data.append({
                'Item_ID': item_id,
                'Date': datetime.now().strftime('%Y-%m-%d'),
                'Type': 'Summary',
                'Current_Stock': pp_metrics.get('current_stock', 0),
                'Reorder_Point': pp_metrics.get('reorder_point', 0),
                'Safety_Stock': pp_metrics.get('safety_stock', 0),
                'Avg_Daily_Demand': pp_metrics.get('avg_daily_demand', 0),
                'Days_to_Rupture': pp_metrics.get('days_to_rupture', 0),
                'Alert_Triggered': alert.get('alert_triggered', False),
                'Urgency': alert.get('urgency', 'low')
            })
            
            # Forecast rows
            if len(forecast) > 0:
                for i, value in enumerate(forecast):
                    forecast_date = (datetime.now() + pd.Timedelta(days=i+1)).strftime('%Y-%m-%d')
                    report_data.append({
                        'Item_ID': item_id,
                        'Date': forecast_date,
                        'Type': 'Forecast',
                        'Forecasted_Demand': value,
                        'Current_Stock': '',
                        'Reorder_Point': '',
                        'Safety_Stock': '',
                        'Avg_Daily_Demand': '',
                        'Days_to_Rupture': '',
                        'Alert_Triggered': '',
                        'Urgency': ''
                    })
        
        df = pd.DataFrame(report_data)
        df.to_csv(output_path, index=False)
        
        return output_path
    
    def generate_pdf_report(self, results: Dict, output_path: str, 
                           title: str = "Demand Forecasting Report") -> str:
        """
        Generate PDF report with forecasts and inventory metrics.
        
        Args:
            results: Dictionary with results for each item
            output_path: Path to save PDF file
            title: Report title
        
        Returns:
            Path to generated PDF file
        
        Raises:
            ImportError: If reportlab not available
        """
        if not REPORTLAB_AVAILABLE:
            raise ImportError("reportlab is required for PDF report generation")
        
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_para = Paragraph(title, styles['Title'])
        story.append(title_para)
        story.append(Spacer(1, 12))
        
        # Date
        date_para = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                             styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 20))
        
        # Summary table
        summary_data = [['Item ID', 'Current Stock', 'Reorder Point', 
                         'Days to Rupture', 'Alert Status', 'Urgency']]
        
        for item_id, item_results in results.items():
            pp_metrics = item_results.get('pp_metrics', {})
            alert = item_results.get('alert', {})
            
            summary_data.append([
                item_id,
                f"{pp_metrics.get('current_stock', 0):.0f}",
                f"{pp_metrics.get('reorder_point', 0):.0f}",
                f"{pp_metrics.get('days_to_rupture', 0):.1f}",
                'Yes' if alert.get('alert_triggered', False) else 'No',
                alert.get('urgency', 'low').upper()
            ])
        
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Detailed information for each item
        for item_id, item_results in results.items():
            forecast = item_results.get('forecast', pd.Series())
            pp_metrics = item_results.get('pp_metrics', {})
            alert = item_results.get('alert', {})
            
            # Item header
            item_header = Paragraph(f"<b>{item_id}</b>", styles['Heading2'])
            story.append(item_header)
            story.append(Spacer(1, 12))
            
            # Metrics
            metrics_text = f"""
            Current Stock: {pp_metrics.get('current_stock', 0):.0f} units<br/>
            Reorder Point: {pp_metrics.get('reorder_point', 0):.0f} units<br/>
            Safety Stock: {pp_metrics.get('safety_stock', 0):.0f} units<br/>
            Average Daily Demand: {pp_metrics.get('avg_daily_demand', 0):.2f} units<br/>
            Days to Rupture: {pp_metrics.get('days_to_rupture', 0):.1f} days
            """
            
            if alert.get('alert_triggered', False):
                metrics_text += f"<br/><b>ALERT: {alert.get('urgency', 'low').upper()}</b>"
            
            metrics_para = Paragraph(metrics_text, styles['Normal'])
            story.append(metrics_para)
            story.append(Spacer(1, 12))
            
            # Forecast table (show first 10 days)
            if len(forecast) > 0:
                forecast_header = Paragraph("<b>30-Day Forecast</b>", styles['Heading3'])
                story.append(forecast_header)
                story.append(Spacer(1, 6))
                
                forecast_data = [['Day', 'Date', 'Forecasted Demand']]
                for i, value in enumerate(forecast[:30]):  # First 30 days
                    forecast_date = datetime.now() + pd.Timedelta(days=i+1)
                    forecast_data.append([
                        str(i+1),
                        forecast_date.strftime('%Y-%m-%d'),
                        f"{value:.2f}"
                    ])
                
                forecast_table = Table(forecast_data)
                forecast_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8)
                ]))
                
                story.append(forecast_table)
                story.append(Spacer(1, 20))
        
        # Build PDF
        doc.build(story)
        
        return output_path

