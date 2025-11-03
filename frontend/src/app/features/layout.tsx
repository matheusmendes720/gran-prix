'use client';

import React, { useState } from 'react';
import Sidebar from '../../components/Sidebar';
import Header from '../../components/Header';
import BackendStatus from '../../components/BackendStatus';
import ErrorBoundary from '../../components/ErrorBoundary';
import { ToastProvider } from '../../contexts/ToastContext';
import ToastContainer from '../../components/ToastContainer';

export default function FeaturesLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [activePage, setActivePage] = useState('Features');
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <ToastProvider>
      <ErrorBoundary>
        <div className="min-h-screen text-brand-lightest-slate font-sans">
          <div className="flex">
            <Sidebar activePage={activePage} setActivePage={setActivePage} />
            <main className="flex-1 p-4 sm:p-6 lg:p-8">
              <Header
                title="ML Features Dashboard"
                subtitle="Visualização de features de machine learning para previsão de demanda"
                searchTerm={searchTerm}
                setSearchTerm={setSearchTerm}
              />
              <div className="mt-6 animate-fade-in-up">
                <ErrorBoundary>
                  {children}
                </ErrorBoundary>
              </div>
            </main>
          </div>
          <BackendStatus />
          <ToastContainer />
        </div>
      </ErrorBoundary>
    </ToastProvider>
  );
}

