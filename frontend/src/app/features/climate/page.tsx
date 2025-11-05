'use client';

import React, { useState } from 'react';
import ClimateTimeSeriesChart from '../../../components/charts/ClimateTimeSeriesChart';
import Card from '../../../components/Card';

export default function ClimateFeaturesPage() {
  const [startDate, setStartDate] = useState<string>(
    new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  );
  const [endDate, setEndDate] = useState<string>(
    new Date().toISOString().split('T')[0]
  );

  return (
    <div className="w-full space-y-6 p-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-brand-lightest-slate">Features Climáticas</h1>
          <p className="text-sm text-brand-slate mt-1">
            Dados climáticos de Salvador/BA e impactos na operação
          </p>
        </div>
        <div className="flex gap-4">
          <div className="flex gap-2 items-center">
            <label className="text-sm text-brand-slate">De:</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="px-3 py-2 bg-brand-light-navy border border-brand-navy rounded-lg text-brand-lightest-slate focus:border-brand-cyan focus:outline-none"
            />
          </div>
          <div className="flex gap-2 items-center">
            <label className="text-sm text-brand-slate">Até:</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="px-3 py-2 bg-brand-light-navy border border-brand-navy rounded-lg text-brand-lightest-slate focus:border-brand-cyan focus:outline-none"
            />
          </div>
        </div>
      </div>

      <Card>
        <div className="p-4">
          <h3 className="text-lg font-bold text-brand-lightest-slate mb-2">🌦️ Sobre Features Climáticas</h3>
          <p className="text-sm text-brand-slate mb-3">
            Dados climáticos de Salvador/BA afetam diretamente a operação, especialmente riscos de corrosão e 
            interrupção de trabalho de campo. Monitoramos temperatura, precipitação, umidade e vento.
          </p>
        </div>
      </Card>

      <ClimateTimeSeriesChart startDate={startDate} endDate={endDate} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card>
          <h3 className="text-lg font-bold text-brand-lightest-slate mb-2">🌡️ Temperatura</h3>
          <p className="text-sm text-brand-slate">Média: 27°C</p>
          <p className="text-sm text-brand-slate">Máxima: 32°C</p>
        </Card>
        <Card>
          <h3 className="text-lg font-bold text-brand-lightest-slate mb-2">🌧️ Precipitação</h3>
          <p className="text-sm text-brand-slate">Média: 120mm/mês</p>
          <p className="text-sm text-brand-slate">Período chuvoso: Maio-Ago</p>
        </Card>
        <Card>
          <h3 className="text-lg font-bold text-brand-lightest-slate mb-2">⚠️ Riscos</h3>
          <p className="text-sm text-brand-slate">Corrosão: Médio</p>
          <p className="text-sm text-brand-slate">Interrupção: Baixo</p>
        </Card>
      </div>
    </div>
  );
}







