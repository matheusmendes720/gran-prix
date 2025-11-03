'use client';

import React, { useState, useEffect } from 'react';
import Card from './Card';
import { apiClient } from '../lib/api';

interface BackendStatusProps {
  onStatusChange?: (isOnline: boolean) => void;
}

const BackendStatus: React.FC<BackendStatusProps> = ({ onStatusChange }) => {
  const [isOnline, setIsOnline] = useState<boolean | null>(null);
  const [isChecking, setIsChecking] = useState(false);

  useEffect(() => {
    const checkBackend = async () => {
      setIsChecking(true);
      try {
        // Try to fetch health endpoint directly
        const response = await fetch('http://localhost:5000/health');
        const data = await response.json();
        setIsOnline(response.ok && (data.status === 'ok' || data.status === 'healthy'));
      } catch (error) {
        setIsOnline(false);
      } finally {
        setIsChecking(false);
        if (onStatusChange) {
          onStatusChange(isOnline ?? false);
        }
      }
      // eslint-disable-next-line react-hooks/exhaustive-deps
    };

    // Check immediately
    checkBackend();

    // Check every 30 seconds
    const interval = setInterval(checkBackend, 30000);

    return () => clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [onStatusChange]);

  if (isChecking || isOnline === null) {
    return null; // Don't show anything while checking
  }

  if (!isOnline) {
    return (
      <div className="fixed top-4 right-4 z-50 animate-slide-in-right">
        <Card>
          <div className="p-4 bg-red-900/20 border border-red-500/50 rounded-lg">
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
              <div>
                <h4 className="text-sm font-semibold text-red-400">Backend Offline</h4>
                <p className="text-xs text-red-300 mt-1">
                  O servidor backend não está rodando. Inicie o servidor em <code className="bg-red-900/50 px-1 rounded">backend</code> com:
                </p>
                <code className="text-xs text-red-200 mt-2 block bg-red-900/30 p-2 rounded font-mono">
                  uvicorn app.main:app --reload --port 5000
                </code>
              </div>
            </div>
          </div>
        </Card>
      </div>
    );
  }

  return null; // Don't show anything when online
};

export default BackendStatus;

