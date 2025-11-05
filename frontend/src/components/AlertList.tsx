// frontend/src/components/AlertList.tsx
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertTriangle, Bell } from 'lucide-react';

interface AlertItem {
  alert_id: number;
  item_id: number;
  site_id: number;
  level: string; // 'NORMAL', 'WARNING', 'CRITICAL'
  category: string;
  message: string;
  created_at: string;
  read_at: string | null;
}

interface AlertListProps {
  alerts: AlertItem[];
}

export function AlertList({ alerts }: AlertListProps) {
  if (!alerts || alerts.length === 0) {
    return (
      <div className="text-center py-4 text-gray-500">
        No alerts to display
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {alerts.map((alert) => {
        let variant = 'default';
        let icon = Bell;
        
        if (alert.level === 'CRITICAL') {
          variant = 'destructive';
          icon = AlertTriangle;
        } else if (alert.level === 'WARNING') {
          variant = 'warning';
        }
        
        return (
          <Alert key={alert.alert_id} className={variant === 'destructive' ? 'border-red-200 bg-red-50' : variant === 'warning' ? 'border-yellow-200 bg-yellow-50' : ''}>
            <icon className="h-4 w-4" />
            <AlertTitle>
              {alert.level} - {alert.category}
            </AlertTitle>
            <AlertDescription>
              <div className="font-medium">Item ID: {alert.item_id}</div>
              <div>Site ID: {alert.site_id}</div>
              <div className="mt-1">{alert.message}</div>
              <div className="text-xs text-gray-500 mt-1">
                {new Date(alert.created_at).toLocaleString()}
              </div>
            </AlertDescription>
          </Alert>
        );
      })}
    </div>
  );
}