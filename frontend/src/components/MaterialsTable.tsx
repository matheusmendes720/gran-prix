/**
 * Materials/Items Table Component
 * Displays filterable table of items from dim_item
 */

'use client';

import React, { useState } from 'react';
import { useItems } from '@/hooks/use-api';
import type { Item } from '@/lib/api-client';

interface MaterialsTableProps {
  onSelectItem?: (item: Item) => void;
}

export function MaterialsTable({ onSelectItem }: MaterialsTableProps) {
  const [family, setFamily] = useState<string>('');
  const [abcClass, setAbcClass] = useState<'A' | 'B' | 'C' | ''>('');
  const [page, setPage] = useState(0);
  const itemsPerPage = 20;

  const { data, error, isLoading } = useItems({
    limit: itemsPerPage,
    offset: page * itemsPerPage,
    family: family || undefined,
    abc_class: abcClass || undefined,
  });

  const items = data?.data ?? [];
  const totalCount = data?.metadata?.total_count ?? 0;
  const totalPages = Math.ceil(totalCount / itemsPerPage);

  const families = ['ELECTRICAL', 'TELECOM', 'HARDWARE', 'CABLE', 'CONNECTOR'];

  const getAbcClassColor = (abcClass: string) => {
    switch (abcClass) {
      case 'A': return 'bg-red-100 text-red-800';
      case 'B': return 'bg-yellow-100 text-yellow-800';
      case 'C': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getCriticalityColor = (criticality: number) => {
    if (criticality >= 8) return 'text-red-600 font-semibold';
    if (criticality >= 5) return 'text-yellow-600 font-medium';
    return 'text-green-600';
  };

  return (
    <div className="bg-white rounded-lg shadow">
      {/* Filters */}
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Catálogo de Materiais</h2>
        
        <div className="flex flex-wrap gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Família
            </label>
            <select
              value={family}
              onChange={(e) => {
                setFamily(e.target.value);
                setPage(0);
              }}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todas</option>
              {families.map((f) => (
                <option key={f} value={f}>{f}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Classe ABC
            </label>
            <select
              value={abcClass}
              onChange={(e) => {
                setAbcClass(e.target.value as 'A' | 'B' | 'C' | '');
                setPage(0);
              }}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todas</option>
              <option value="A">A</option>
              <option value="B">B</option>
              <option value="C">C</option>
            </select>
          </div>
        </div>

        <div className="mt-4 text-sm text-gray-600">
          {isLoading ? (
            <span>Carregando...</span>
          ) : (
            <span>Mostrando {items.length} de {totalCount} materiais</span>
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
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  SKU
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nome
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Família
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Classe ABC
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Criticidade
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {items.map((item: Item) => (
                <tr 
                  key={item.item_id} 
                  className="hover:bg-gray-50 transition-colors"
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {item.sku}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {item.name || item.sku}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {item.family}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-semibold rounded ${getAbcClassColor(item.abc_class)}`}>
                      {item.abc_class}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={getCriticalityColor(item.criticality)}>
                      {item.criticality}/10
                    </span>
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

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
          <button
            onClick={() => setPage(Math.max(0, page - 1))}
            disabled={page === 0}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Anterior
          </button>

          <span className="text-sm text-gray-700">
            Página {page + 1} de {totalPages}
          </span>

          <button
            onClick={() => setPage(Math.min(totalPages - 1, page + 1))}
            disabled={page >= totalPages - 1}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Próxima
          </button>
        </div>
      )}
    </div>
  );
}

export default MaterialsTable;
