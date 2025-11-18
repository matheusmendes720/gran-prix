'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar';
import Dashboard from '../../components/Dashboard';
import Reports from '../../components/Reports';
import Analytics from '../../components/Analytics';
import Settings from '../../components/Settings';
import Header from '../../components/Header';
import { ToastProvider } from '../../contexts/ToastContext';
import ToastContainer from '../../components/ToastContainer';

const pageDetails = {
  'Dashboard': { title: 'Dashboard de Análise Preditiva', subtitle: 'Bem-vindo, aqui está um resumo da sua operação.' },
  'Relatórios': { title: 'Relatórios', subtitle: 'Gere e visualize relatórios sobre sua operação.' },
  'Análises': { title: 'Análises Aprofundadas', subtitle: 'Explore as métricas e descubra novos insights.' },
  'Configurações': { title: 'Configurações', subtitle: 'Gerencie seu perfil, usuários e preferências do sistema.' },
};

export default function MainPage() {
  const [activePage, setActivePage] = useState('Dashboard');
  const [searchTerm, setSearchTerm] = useState('');
  const [analyticsTargetState, setAnalyticsTargetState] = useState<string | null>(null);

  // Check for target page from sessionStorage when component mounts
  useEffect(() => {
    const targetPage = sessionStorage.getItem('targetPage');
    if (targetPage && pageDetails[targetPage as keyof typeof pageDetails]) {
      setActivePage(targetPage);
      sessionStorage.removeItem('targetPage'); // Clear after use
    }
  }, []);

  const handlePageChange = (page: string) => {
    setAnalyticsTargetState(null);
    setActivePage(page);
  };

  const handleSelectAlert = (stateId: string) => {
    setAnalyticsTargetState(stateId);
    setActivePage('Análises');
  };

  const renderContent = () => {
    switch (activePage) {
      case 'Dashboard':
        return <Dashboard searchTerm={searchTerm} onSelectAlert={handleSelectAlert} />;
      case 'Relatórios':
        return <Reports searchTerm={searchTerm} />;
      case 'Análises':
        return <Analytics initialSelectedState={analyticsTargetState} />;
      case 'Configurações':
        return <Settings searchTerm={searchTerm} />;
      default:
        return <Dashboard searchTerm={searchTerm} onSelectAlert={handleSelectAlert}/>;
    }
  };

  const currentPageDetails = pageDetails[activePage as keyof typeof pageDetails] || pageDetails['Dashboard'];

  return (
    <ToastProvider>
      <div className="min-h-screen text-brand-lightest-slate font-sans">
        <div className="flex">
          <Sidebar activePage={activePage} setActivePage={handlePageChange} />
          <main className="flex-1 p-4 sm:p-6 lg:p-8">
            <Header
              title={currentPageDetails.title}
              subtitle={currentPageDetails.subtitle}
              searchTerm={searchTerm}
              setSearchTerm={setSearchTerm}
            />
            <div className="mt-6 animate-fade-in-up" key={activePage}>
              {renderContent()}
            </div>
          </main>
        </div>
        <ToastContainer />
      </div>
    </ToastProvider>
  );
}

