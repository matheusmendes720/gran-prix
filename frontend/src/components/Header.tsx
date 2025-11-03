import React from 'react';
import NotificationBell from './NotificationBell';
import { NotificationItem } from '../types';

interface HeaderProps {
    title: string;
    subtitle: string;
    searchTerm: string;
    setSearchTerm: (term: string) => void;
}

const Header: React.FC<HeaderProps> = ({ title, subtitle, searchTerm, setSearchTerm }) => {
  const handleViewDetails = React.useCallback((notification: NotificationItem) => {
    // Placeholder: integrate with routing or modal when available
    console.info('Abrir detalhes da notificação', notification);
  }, []);

  return (
    <header className="sticky top-0 z-40 flex items-center justify-between py-4 bg-brand-blue/85 backdrop-blur-xl -mx-8 px-8 border-b border-brand-cyan/40 animate-subtle-glow">
      <div>
        <h1 className="text-2xl font-bold text-brand-lightest-slate">{title}</h1>
        <p className="text-brand-slate">{subtitle}</p>
      </div>
      <div className="flex items-center space-x-4">
        <div className="relative hidden md:block">
          <input 
            type="text" 
            placeholder="Buscar..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="bg-brand-light-navy/50 border border-white/10 rounded-lg py-2 px-4 pl-10 text-brand-lightest-slate focus:outline-none focus:ring-2 focus:ring-brand-cyan transition-all w-48 focus:w-64"
          />
          <svg className="w-5 h-5 text-brand-slate absolute left-3 top-1/2 transform -translate-y-1/2 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        </div>
        <NotificationBell theme="dark" onViewDetails={handleViewDetails} />
        <div className="flex items-center space-x-3 p-1 rounded-full bg-brand-light-navy/50 border border-white/10">
            <img src="https://picsum.photos/40/40" alt="User Avatar" className="w-9 h-9 rounded-full" />
            <div className='hidden sm:block pr-2'>
                <p className="font-semibold text-brand-lightest-slate text-sm">Admin</p>
                <p className="text-xs text-brand-slate">Nova Corrente</p>
            </div>
        </div>
      </div>
    </header>
  );
};

export default Header;