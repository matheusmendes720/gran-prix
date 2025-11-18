'use client';

import React from 'react';
import Card from './Card';
import { useGeoSummary } from '@/hooks/use-api';
import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';
import { scaleSequential } from 'd3-scale';
import { interpolateYlOrRd } from 'd3-scale-chromatic';

const BRAZIL_GEO_URL =
  'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson';

const GeoHeatmap: React.FC = () => {
  const { data, error, isLoading } = useGeoSummary();
  const regions = data?.regions ?? [];

  const maxRisk = Math.max(...regions.map((r) => r.corrosion_risk_pct), 1);
  const colorScale = scaleSequential(interpolateYlOrRd).domain([0, maxRisk || 1]);

  return (
    <Card className="h-full flex flex-col">
      <div className="flex justify-between items-center mb-4">
        <div>
          <h3 className="text-xl font-bold text-brand-lightest-slate">Mapa de Risco Corrosivo</h3>
          {data?.generated_at && (
            <p className="text-xs text-brand-slate mt-1">
              Snapshot: {new Date(data.generated_at).toLocaleString('pt-BR')}
            </p>
          )}
        </div>
        <span className="text-xs text-brand-slate/80">
          Fonte: storytelling &nbsp;/&nbsp; unified_brazilian_telecom_nova_corrente_enriched.csv
        </span>
      </div>

      <div className="flex-1 min-h-[360px]" role="region" aria-label="Mapa de risco corrosivo por região">
        {error && (
          <div className="text-sm text-red-400 bg-red-900/20 border border-red-500/40 rounded-lg p-4">
            Não foi possível carregar dados geográficos: {error.message}
          </div>
        )}

        {isLoading && !error && (
          <div className="h-full flex items-center justify-center">
            <div className="w-48 h-48 bg-brand-light-navy/30 rounded-full animate-pulse" />
          </div>
        )}

        {!isLoading && !error && (
          <ComposableMap
            projection="geoMercator"
            projectionConfig={{
              center: [-55, -15],
              scale: 650,
            }}
            style={{ width: '100%', height: '100%' }}
          >
            <Geographies geography={BRAZIL_GEO_URL}>
              {({ geographies }) =>
                geographies.map((geo) => (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    fill="#0f172a"
                    stroke="#1e293b"
                    strokeWidth={0.5}
                  />
                ))
              }
            </Geographies>

            {regions.map((region) => (
              <Marker key={region.region} coordinates={[region.longitude, region.latitude]}>
                <g transform="translate(-12, -12)">
                  <circle
                    r={10}
                    fill={colorScale(region.corrosion_risk_pct)}
                    opacity={0.8}
                  />
                  <text
                    textAnchor="middle"
                    y={-14}
                    className="text-xs font-semibold fill-brand-lightest-slate"
                  >
                    {region.region.replace('_', ' ')}
                  </text>
                </g>

                <text
                  textAnchor="middle"
                  y={20}
                  className="text-[10px] fill-brand-lightest-slate/80"
                >
                  {region.corrosion_risk_pct.toFixed(1)}% risco
                </text>
              </Marker>
            ))}
          </ComposableMap>
        )}
      </div>

      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-brand-slate/90">
        {regions.map((region) => (
          <div
            key={`legend-${region.region}`}
            className="bg-brand-light-navy/40 rounded-lg px-3 py-2 border border-brand-light-navy/60"
          >
            <div className="flex justify-between">
              <span className="font-semibold text-brand-lightest-slate">
                {region.region.replace('_', ' ').toUpperCase()}
              </span>
              <span>{region.corrosion_risk_pct.toFixed(1)}% risco</span>
            </div>
            <div className="mt-1 grid grid-cols-3 gap-2">
              <span>Temp: {region.avg_temperature.toFixed(1)}°C</span>
              <span>Umid: {region.avg_humidity.toFixed(0)}%</span>
              <span>Chuva: {region.avg_precipitation.toFixed(1)}mm</span>
            </div>
            <div className="mt-1">
              Multiplicador de demanda: {region.demand_multiplier.toFixed(2)}x
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};

export default GeoHeatmap;

