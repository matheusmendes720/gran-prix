"""
Alert system for low stock situations.
Generates and sends alerts when reorder points are reached.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class AlertSystem:
    """Generate and send alerts for low stock situations."""
    
    def __init__(self, email_config: Optional[Dict] = None):
        """
        Initialize alert system.
        
        Args:
            email_config: Dictionary with email settings:
                {
                    'smtp_server': 'smtp.gmail.com',
                    'smtp_port': 587,
                    'sender_email': 'alerts@novacorrente.com',
                    'sender_password': 'password',
                    'recipients': ['manager@novacorrente.com']
                }
        """
        self.email_config = email_config or {}
        self.alerts_log = []
    
    def check_reorder_alert(self, current_stock: float, reorder_point: float,
                           days_to_rupture: float, item_id: str, 
                           urgency_threshold: Dict = None) -> Dict:
        """
        Check if reorder alert should be triggered.
        
        Args:
            current_stock: Current inventory level
            reorder_point: Calculated reorder point
            days_to_rupture: Days until stock rupture
            item_id: Item identifier
            urgency_threshold: Dict with urgency thresholds:
                {'critical': 7, 'high': 14, 'medium': 30}
        
        Returns:
            Dictionary with alert information
        """
        if urgency_threshold is None:
            urgency_threshold = {'critical': 7, 'high': 14, 'medium': 30}
        
        alert_triggered = current_stock <= reorder_point
        
        # Determine urgency
        if days_to_rupture < urgency_threshold.get('critical', 7):
            urgency = 'critical'
        elif days_to_rupture < urgency_threshold.get('high', 14):
            urgency = 'high'
        elif days_to_rupture < urgency_threshold.get('medium', 30):
            urgency = 'medium'
        else:
            urgency = 'low'
        
        # Calculate recommended order quantity
        units_needed = max(0, int(reorder_point - current_stock + (reorder_point * 0.2)))
        
        alert = {
            'item_id': item_id,
            'timestamp': datetime.now().isoformat(),
            'current_stock': current_stock,
            'reorder_point': reorder_point,
            'days_to_rupture': days_to_rupture,
            'alert_triggered': alert_triggered,
            'urgency': urgency,
            'units_needed': units_needed,
            'message': self._generate_message(item_id, current_stock, reorder_point, 
                                            days_to_rupture, units_needed, urgency)
        }
        
        if alert_triggered:
            self.alerts_log.append(alert)
        
        return alert
    
    def _generate_message(self, item_id: str, current_stock: float,
                         reorder_point: float, days_to_rupture: float,
                         units_needed: int, urgency: str) -> str:
        """Generate alert message."""
        urgency_emoji = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }
        
        emoji = urgency_emoji.get(urgency, '⚪')
        
        message = f"""
ALERT: Reorder Required for {item_id} {emoji}

Current Stock: {current_stock:.0f} units
Reorder Point: {reorder_point:.0f} units
Days to Rupture: {days_to_rupture:.1f} days
Urgency Level: {urgency.upper()}

Recommended Order Quantity: {units_needed} units

Action Required: Place order immediately to prevent stockout.
"""
        return message.strip()
    
    def send_email_alert(self, alert: Dict) -> bool:
        """
        Send email alert.
        
        Args:
            alert: Alert dictionary from check_reorder_alert()
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.email_config or not alert['alert_triggered']:
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config.get('sender_email')
            recipients = self.email_config.get('recipients', [])
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = f"Stock Alert: {alert['item_id']} - {alert['urgency'].upper()}"
            
            msg.attach(MIMEText(alert['message'], 'plain'))
            
            server = smtplib.SMTP(
                self.email_config.get('smtp_server', 'smtp.gmail.com'),
                self.email_config.get('smtp_port', 587)
            )
            server.starttls()
            server.login(
                self.email_config.get('sender_email'),
                self.email_config.get('sender_password')
            )
            server.send_message(msg)
            server.quit()
            
            return True
        
        except Exception as e:
            print(f"Email alert failed: {e}")
            return False
    
    def generate_batch_alerts(self, items_data: List[Dict]) -> List[Dict]:
        """
        Generate alerts for multiple items.
        
        Args:
            items_data: List of dictionaries with item data:
                [
                    {
                        'item_id': 'CONN-001',
                        'current_stock': 100,
                        'reorder_point': 150,
                        'days_to_rupture': 10
                    },
                    ...
                ]
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        for item_data in items_data:
            alert = self.check_reorder_alert(
                item_data['current_stock'],
                item_data['reorder_point'],
                item_data['days_to_rupture'],
                item_data['item_id']
            )
            alerts.append(alert)
            
            if alert['alert_triggered'] and self.email_config:
                self.send_email_alert(alert)
        
        return alerts
    
    def get_alerts_summary(self) -> Dict:
        """Get summary of all alerts."""
        if not self.alerts_log:
            return {'total_alerts': 0, 'by_urgency': {}}
        
        by_urgency = {}
        for alert in self.alerts_log:
            urgency = alert['urgency']
            by_urgency[urgency] = by_urgency.get(urgency, 0) + 1
        
        return {
            'total_alerts': len(self.alerts_log),
            'by_urgency': by_urgency,
            'latest_alerts': self.alerts_log[-10:]  # Last 10 alerts
        }

