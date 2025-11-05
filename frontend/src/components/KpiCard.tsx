// frontend/src/components/KPICard.tsx
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowUpIcon, ArrowDownIcon } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string;
  change: number; // Positive for increase, negative for decrease
  format?: 'percentage' | 'currency' | 'number';
}

export function KPICard({ title, value, change, format = 'number' }: KPICardProps) {
  const formatValue = (val: string, fmt: string) => {
    switch (fmt) {
      case 'percentage':
        return val;
      case 'currency':
        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(Number(val));
      default:
        return val;
    }
  };

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardDescription>{title}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{formatValue(value, format)}</div>
      </CardContent>
      <CardFooter className="flex items-center justify-between">
        <div className={`flex items-center text-sm ${change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          {change >= 0 ? (
            <ArrowUpIcon className="h-4 w-4 mr-1" />
          ) : (
            <ArrowDownIcon className="h-4 w-4 mr-1" />
          )}
          <span>{Math.abs(change)}%</span>
        </div>
        <div className="text-xs text-gray-500">vs previous</div>
      </CardFooter>
    </Card>
  );
}