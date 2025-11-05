'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';

interface Recommendation {
  recommendation_id: number;
  item_id: number;
  site_id: number;
  type: string; // 'REORDER', 'PROMO', 'REALLOCATE', 'HOLD', 'EXPEDITE'
  priority: string; // 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
  message: string;
  action_date: string;
  quantity_recommended: number;
  created_at: string;
  acknowledged_at: string | null;
  acknowledged_by: string | null;
}

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [priorityFilter, setPriorityFilter] = useState('');
  const [siteIdFilter, setSiteIdFilter] = useState<number | ''>('');

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await apiClient.getRecommendations({
          priority: priorityFilter || undefined,
          site_id: siteIdFilter ? Number(siteIdFilter) : undefined,
          limit: 50
        });
        setRecommendations(response.data || []);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [priorityFilter, siteIdFilter]);

  const acknowledgeRecommendation = async (recId: number) => {
    try {
      await apiClient.acknowledgeRecommendation(recId);
      // Update the local state to reflect the change
      setRecommendations(recommendations.map(rec => 
        rec.recommendation_id === recId 
          ? { ...rec, acknowledged_at: new Date().toISOString(), acknowledged_by: 'Current User' } 
          : rec
      ));
    } catch (error) {
      console.error('Error acknowledging recommendation:', error);
    }
  };

  // Get unique site IDs for filter dropdown
  const siteIds = [...new Set(recommendations.map(rec => rec.site_id))].filter(Boolean);

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Recommendations</h1>
      </div>

      {/* Filters */}
      <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
          <select
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
          >
            <option value="">All Priorities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Site ID</label>
          <select
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            value={siteIdFilter}
            onChange={(e) => setSiteIdFilter(e.target.value ? Number(e.target.value) : '')}
          >
            <option value="">All Sites</option>
            {siteIds.map(siteId => (
              <option key={siteId} value={siteId}>{siteId}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Recommendations List */}
      <div className="bg-white shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Priority
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Item ID
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Site ID
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Message
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Quantity
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th scope="col" className="relative px-6 py-3">
                <span className="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {recommendations.map((rec) => (
              <tr key={rec.recommendation_id} className={rec.priority === 'CRITICAL' ? 'bg-red-50' : rec.priority === 'HIGH' ? 'bg-yellow-50' : ''}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                    ${rec.priority === 'CRITICAL' ? 'bg-red-100 text-red-800' : 
                      rec.priority === 'HIGH' ? 'bg-orange-100 text-orange-800' : 
                      rec.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' : 
                      'bg-green-100 text-green-800'}`}>
                    {rec.priority}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {rec.type}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {rec.item_id}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {rec.site_id}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {rec.message}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {rec.quantity_recommended}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(rec.created_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {rec.acknowledged_at ? 'Acknowledged' : 'Pending'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  {!rec.acknowledged_at && (
                    <button
                      onClick={() => acknowledgeRecommendation(rec.recommendation_id)}
                      className="text-indigo-600 hover:text-indigo-900"
                    >
                      Acknowledge
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}