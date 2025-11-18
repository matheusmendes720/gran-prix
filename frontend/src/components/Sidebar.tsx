
import React from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { DashboardIcon, ReportIcon, AnalyticsIcon, SettingsIcon } from './icons';

interface NavItemProps {
  icon: React.ReactNode;
  label: string;
  active?: boolean;
  onClick: () => void;
}

const NavItem: React.FC<NavItemProps> = ({ icon, label, active, onClick }) => {
  const baseClasses = "flex items-center p-3 my-2 space-x-4 rounded-lg transition-all duration-200 cursor-pointer w-full text-left transform";
  const activeClasses = "bg-brand-cyan/10 text-brand-cyan shadow-inner shadow-cyan-500/10";
  const inactiveClasses = "text-brand-slate hover:bg-brand-light-navy/50 hover:text-brand-lightest-slate hover:translate-x-1";
  
  return (
    <button onClick={onClick} className={`${baseClasses} ${active ? activeClasses : inactiveClasses}`}>
      {icon}
      <span className="font-semibold">{label}</span>
    </button>
  );
};

interface SidebarProps {
  activePage: string;
  setActivePage: (page: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activePage, setActivePage }) => {
  const pathname = usePathname();
  const router = useRouter();
  const isOnMainPage = pathname?.startsWith('/main') || pathname === '/';
  const isOnFeaturesPage = pathname?.startsWith('/features');

  const navItems = [
    { label: 'Dashboard', icon: <DashboardIcon /> },
    { label: 'Relatórios', icon: <ReportIcon /> },
    { label: 'Análises', icon: <AnalyticsIcon /> },
    { label: 'Configurações', icon: <SettingsIcon /> },
  ];

  const handleMainNavClick = (page: string) => {
    if (isOnFeaturesPage) {
      // If we're on a features page, navigate to /main first
      router.push('/main');
      // Store the target page in sessionStorage to restore after navigation
      sessionStorage.setItem('targetPage', page);
    } else {
      // If we're already on /main, just update the active page
      setActivePage(page);
    }
  };

  return (
    <div className="hidden lg:block w-64 bg-brand-navy/75 backdrop-blur-xl border-r border-brand-cyan/40 h-screen sticky top-0 p-4 animate-subtle-glow">
      <div className="flex items-center space-x-2 mb-10">
        <div className="w-10 h-10 bg-cyan-400/10 rounded-lg flex items-center justify-center border border-brand-cyan/20">
            <svg className="w-6 h-6 text-brand-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
        </div>
        <h1 className="text-xl font-bold text-brand-lightest-slate">Nova Corrente</h1>
      </div>
      <nav>
        {navItems.map(item => (
          <NavItem
            key={item.label}
            icon={item.icon}
            label={item.label}
            active={activePage === item.label && isOnMainPage}
            onClick={() => handleMainNavClick(item.label)}
          />
        ))}
      </nav>
      <div className="mt-8 border-t border-brand-light-navy/50 pt-4">
        <p className="text-xs text-brand-slate mb-3 px-3 uppercase tracking-wider">ML Features</p>
        <nav className="space-y-1">
          <Link href="/features/temporal" className="flex items-center p-2 rounded-lg text-sm text-brand-slate hover:bg-brand-light-navy/50 hover:text-brand-lightest-slate transition-colors">
            <span className="ml-3">📅 Temporal</span>
          </Link>
          <Link href="/features/climate" className="flex items-center p-2 rounded-lg text-sm text-brand-slate hover:bg-brand-light-navy/50 hover:text-brand-lightest-slate transition-colors">
            <span className="ml-3">🌦️ Climate</span>
          </Link>
          <Link href="/features/economic" className="flex items-center p-2 rounded-lg text-sm text-brand-slate hover:bg-brand-light-navy/50 hover:text-brand-lightest-slate transition-colors">
            <span className="ml-3">💰 Economic</span>
          </Link>
          <Link href="/features/5g" className="flex items-center p-2 rounded-lg text-sm text-brand-slate hover:bg-brand-light-navy/50 hover:text-brand-lightest-slate transition-colors">
            <span className="ml-3">📡 5G</span>
          </Link>
          <Link href="/features/lead-time" className="flex items-center p-2 rounded-lg text-sm text-brand-slate hover:bg-brand-light-navy/50 hover:text-brand-lightest-slate transition-colors">
            <span className="ml-3">⏱️ Lead Time</span>
          </Link>
          <Link href="/features/sla" className="flex items-center p-2 rounded-lg text-sm text-brand-slate hover:bg-brand-light-navy/50 hover:text-brand-lightest-slate transition-colors">
            <span className="ml-3">🎯 SLA</span>
          </Link>
          <Link href="/features/hierarchical" className="flex items-center p-2 rounded-lg text-sm text-brand-slate hover:bg-brand-light-navy/50 hover:text-brand-lightest-slate transition-colors">
            <span className="ml-3">🏗️ Hierarchical</span>
          </Link>
          <Link href="/features/categorical" className="flex items-center p-2 rounded-lg text-sm text-brand-slate hover:bg-brand-light-navy/50 hover:text-brand-lightest-slate transition-colors">
            <span className="ml-3">🏷️ Categorical</span>
          </Link>
          <Link href="/features/business" className="flex items-center p-2 rounded-lg text-sm text-brand-slate hover:bg-brand-light-navy/50 hover:text-brand-lightest-slate transition-colors">
            <span className="ml-3">🏢 Business</span>
          </Link>
        </nav>
      </div>
      <div className="absolute bottom-4 left-4 right-4 p-4 rounded-lg glass-card text-center animate-subtle-glow">
        <h3 className="font-bold text-brand-lightest-slate">Upgrade to Pro</h3>
        <p className="text-sm text-brand-slate mt-1 mb-3">Get access to all features and advanced analytics.</p>
        <button className="w-full bg-brand-cyan text-brand-navy font-bold py-2 px-4 rounded-lg hover:bg-opacity-80 transition-all duration-300 shadow-lg shadow-brand-cyan/20 hover:shadow-brand-cyan/40">
            Upgrade
        </button>
      </div>
    </div>
  );
};

export default Sidebar;