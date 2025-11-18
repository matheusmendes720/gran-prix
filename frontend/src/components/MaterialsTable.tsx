/**
 * Materials/Items Table Component
 * Displays filterable table of items from dim_item
 */

'use client';

import React, { useEffect, useMemo, useState } from 'react';
import { useBffForecasts } from '@/hooks/use-api';
import type { ForecastResponse } from '@/lib/api-client';

interface MaterialsTableProps {
  onSelectItem?: (item: {
    series_key: string;
    item_id: string;
    site_id?: number | null;
    familia?: string | null;
    latestForecast?: number | null;
    latestActual?: number | null;
  }) => void;
}

export function MaterialsTable({ onSelectItem }: MaterialsTableProps) {
  const [family, setFamily] = useState<string | undefined>(undefined);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const pageSize = 20;

  const { data, error, isLoading } = useBffForecasts(
    family ? { familia: family, limit: 200 } : { limit: 200 }
  );

  const items = useMemo(() => {
    if (!data) return [];

    return data.series.map((series) => {
      const latestPoint = series.points[series.points.length - 1];
      return {
        series_key: series.series_key,
        item_id: series.item_id ?? series.series_key,
        site_id: series.site_id,
        familia: series.familia,
        category: series.category,
        latestForecast: latestPoint?.forecast_qty ?? null,
        latestActual: latestPoint?.actual_qty ?? null,
      };
    });
  }, [data]);

  const filteredItems = useMemo(() => {
    if (!searchTerm) return items;
    const term = searchTerm.toLowerCase();
    return items.filter(
      (item) =>
        item.item_id.toLowerCase().includes(term) ||
        item.series_key.toLowerCase().includes(term) ||
        (item.familia ?? '').toLowerCase().includes(term)
    );
  }, [items, searchTerm]);

  useEffect(() => {
    setPage(1);
  }, [family, searchTerm, items.length]);

  const totalItems = filteredItems.length;
  const pageCount = Math.max(1, Math.ceil(totalItems / pageSize));
  const safePage = Math.min(page, pageCount);
  const paginatedItems = filteredItems.slice((safePage - 1) * pageSize, safePage * pageSize);

  useEffect(() => {
    if (page > pageCount) {
      setPage(pageCount);
    }
  }, [page, pageCount]);

  return (
    <div className="bg-white rounded-lg shadow">
      {/* Filters */}
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Catálogo de Materiais</h2>
        
        <div className="flex flex-wrap gap-4" role="group" aria-label="Filtros de materiais">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Família
            </label>
              <label className="sr-only" htmlFor="family-filter">
                Filtrar por família
              </label>
              <input
                id="family-filter"
              type="text"
              value={family ?? ''}
              onChange={(e) => setFamily(e.target.value || undefined)}
              placeholder="Ex: ABRASIVOS"
              className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Busca
            </label>
              <label className="sr-only" htmlFor="materials-search">
                Buscar materiais
              </label>
              <input
                id="materials-search"
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Filtrar por item ou série"
              className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div className="mt-4 text-sm text-gray-600">
          {isLoading ? (
            <span>Carregando...</span>
          ) : totalItems === 0 ? (
            <span>Nenhuma série encontrada</span>
          ) : (
            <span>
              Mostrando {(safePage - 1) * pageSize + 1} -{' '}
              {Math.min(safePage * pageSize, totalItems)} de {totalItems} séries de previsão
            </span>
          )}
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        {error ? (
          <div className="p-6 text-center text-red-600">
            Erro ao carregar materiais: {error.message}
          </div>
        ) : isLoading ? (
          <div className="p-6">
            <div className="animate-pulse space-y-4">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-12 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        ) : items.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            Nenhum material encontrado
          </div>
        ) : (
          <table className="min-w-full divide-y divide-gray-200" role="table" aria-label="Tabela de séries de previsão de materiais">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" scope="col">
                  Série
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" scope="col">
                  Item
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" scope="col">
                  Família
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sr-only" scope="col">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {paginatedItems.map((item) => (
                <tr 
                  key={item.item_id} 
                  className="hover:bg-gray-50 transition-colors"
                  tabIndex={0}
                  aria-label={`Série ${item.series_key} para o item ${item.item_id}`}
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {item.series_key}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {item.item_id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {item.familia ?? '—'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {onSelectItem && (
                      <button
                        onClick={() => onSelectItem(item)}
                        className="text-blue-600 hover:text-blue-800 font-medium"
                      >
                        Detalhes
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {!isLoading && !error && totalItems > 0 && (
        <div className="px-6 py-4 border-t border-gray-200 flex flex-col gap-3 md:flex-row md:items-center md:justify-between text-sm text-gray-600">
          <div>Página {safePage} de {pageCount}</div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              className="px-3 py-1 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:border-gray-400 transition-colors"
              onClick={() => setPage((prev) => Math.max(1, prev - 1))}
              disabled={safePage <= 1}
            >
              Anterior
            </button>
            <button
              type="button"
              className="px-3 py-1 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:border-gray-400 transition-colors"
              onClick={() => setPage((prev) => Math.min(pageCount, prev + 1))}
              disabled={safePage >= pageCount}
            >
              Próxima
            </button>
          </div>
        </div>
      )}

      {/* Snapshot summary */}
      <div className="px-6 py-4 border-t border-gray-200 text-sm text-gray-600">
        Snapshot gerado em{' '}
        {data?.generated_at
          ? new Date(data.generated_at).toLocaleString('pt-BR')
          : '—'}
      </div>
    </div>
  );
}

export default MaterialsTable;
