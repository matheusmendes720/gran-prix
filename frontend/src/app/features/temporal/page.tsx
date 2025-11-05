'use client';

import React, { useState, useEffect } from 'react';
import TemporalFeaturesChart from '../../../components/charts/TemporalFeaturesChart';
import Card from '../../../components/Card';
import { apiClient } from '../../../lib/api';
import { useToast } from '../../../hooks/useToast';

export default function TemporalFeaturesPage() {
  const [startDate, setStartDate] = useState<string>(
    new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  );
  const [endDate, setEndDate] = useState<string>(
    new Date().toISOString().split('T')[0]
  );
  const [selectedMaterial, setSelectedMaterial] = useState<number | undefined>();
  const { addToast } = useToast();

  const handleDateRangeChange = () => {
    if (new Date(startDate) > new Date(endDate)) {
      addToast('Data inicial deve ser anterior à data final', 'error');
      return;
    }
  };

  return (
    <div className="w-full space-y-6 p-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-brand-lightest-slate">Features Temporais</h1>
          <p className="text-sm text-brand-slate mt-1">
            Visualização de features temporais incluindo calendário brasileiro e codificação cíclica
          </p>
        </div>
        <div className="flex gap-4">
          <div className="flex gap-2 items-center">
            <label className="text-sm text-brand-slate">De:</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              onBlur={handleDateRangeChange}
              className="px-3 py-2 bg-brand-light-navy border border-brand-navy rounded-lg text-brand-lightest-slate focus:border-brand-cyan focus:outline-none"
            />
          </div>
          <div className="flex gap-2 items-center">
            <label className="text-sm text-brand-slate">Até:</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              onBlur={handleDateRangeChange}
              className="px-3 py-2 bg-brand-light-navy border border-brand-navy rounded-lg text-brand-lightest-slate focus:border-brand-cyan focus:outline-none"
            />
          </div>
        </div>
      </div>

      {/* Story Card */}
      <Card>
        <div className="p-4">
          <h3 className="text-lg font-bold text-brand-lightest-slate mb-2">📅 Sobre Features Temporais</h3>
          <p className="text-sm text-brand-slate mb-3">
            Features temporais capturam padrões sazonais, ciclos e eventos específicos do calendário brasileiro que 
            afetam a demanda de materiais. Incluem feriados, período de carnaval, verão, e épocas de chuva sazonal.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
            <div className="bg-brand-navy p-3 rounded-lg">
              <p className="text-xs text-brand-slate mb-1">Calendário Brasileiro</p>
              <p className="text-lg font-bold text-brand-cyan">Feriados & Eventos</p>
            </div>
            <div className="bg-brand-navy p-3 rounded-lg">
              <p className="text-xs text-brand-slate mb-1">Codificação Cíclica</p>
              <p className="text-lg font-bold text-brand-cyan">Sin/Cos Encoding</p>
            </div>
            <div className="bg-brand-navy p-3 rounded-lg">
              <p className="text-xs text-brand-slate mb-1">Sazonalidade</p>
              <p className="text-lg font-bold text-brand-cyan">Padrões Temporais</p>
            </div>
          </div>
        </div>
      </Card>

      {/* Main Chart */}
      <TemporalFeaturesChart
        materialId={selectedMaterial}
        startDate={startDate}
        endDate={endDate}
      />

      {/* Additional Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-bold text-brand-lightest-slate mb-4">📊 Insights Temporais</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-brand-slate">Períodos de Alta Demanda</span>
              <span className="text-brand-cyan font-semibold">Carnaval, Verão</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-brand-slate">Períodos de Baixa Demanda</span>
              <span className="text-brand-light-slate font-semibold">Quartas-feiras</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-brand-slate">Sazonalidade Detectada</span>
              <span className="text-brand-cyan font-semibold">Alta</span>
            </div>
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-bold text-brand-lightest-slate mb-4">🎯 Recomendações</h3>
          <ul className="space-y-2 text-sm text-brand-slate">
            <li className="flex items-start gap-2">
              <span className="text-brand-cyan">•</span>
              <span>Antecipe pedidos antes de períodos de carnaval e verão</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-brand-cyan">•</span>
              <span>Reduza estoque durante períodos de baixa demanda</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-brand-cyan">•</span>
              <span>Considere padrões sazonais ao calcular pontos de reordenação</span>
            </li>
          </ul>
        </Card>
      </div>
    </div>
  );
}








