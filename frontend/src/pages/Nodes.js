import React from 'react';
import { useQuery } from 'react-query';
import { apiService } from '../services/api';

const Nodes = () => {
  const { data: nodes, isLoading } = useQuery('nodes', apiService.getNodes, {
    refetchInterval: 30000
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Sensör Nodları</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {nodes?.nodes?.map((node) => (
          <div key={node.nodeId} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">{node.nodeId}</h3>
              <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                node.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              }`}>
                {node.status === 'active' ? 'Aktif' : 'Pasif'}
              </span>
            </div>
            <div className="space-y-2 text-sm text-gray-600">
              <p><strong>Tip:</strong> {node.nodeType}</p>
              <p><strong>Konum:</strong> {node.location || 'Belirtilmemiş'}</p>
              <p><strong>Son Görülme:</strong> {node.lastSeen ? new Date(node.lastSeen).toLocaleString('tr-TR') : '-'}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Nodes;
