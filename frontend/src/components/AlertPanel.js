import React from 'react';
import { ExclamationTriangleIcon, XCircleIcon } from '@heroicons/react/24/outline';

const AlertPanel = ({ alerts, isLoading }) => {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'high':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'warning':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default:
        return 'bg-blue-100 text-blue-800 border-blue-200';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical':
        return <XCircleIcon className="h-4 w-4" />;
      default:
        return <ExclamationTriangleIcon className="h-4 w-4" />;
    }
  };

  const getSeverityText = (severity) => {
    switch (severity) {
      case 'critical': return 'Kritik';
      case 'high': return 'Yüksek';
      case 'warning': return 'Uyarı';
      default: return 'Bilgi';
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Aktif Uyarılar
        </h2>
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Aktif Uyarılar
      </h2>
      <div className="space-y-3">
        {alerts && alerts.length > 0 ? (
          alerts.slice(0, 5).map((alert) => (
            <div
              key={alert.id}
              className={`p-3 rounded-lg border ${getSeverityColor(alert.severity)}`}
            >
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  {getSeverityIcon(alert.severity)}
                </div>
                <div className="ml-3 flex-1">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium">
                      {alert.alert_type?.replace('_', ' ').toUpperCase()}
                    </p>
                    <span className="text-xs opacity-75">
                      {getSeverityText(alert.severity)}
                    </span>
                  </div>
                  <p className="text-xs mt-1 opacity-90">
                    {alert.message}
                  </p>
                  <p className="text-xs mt-2 opacity-75">
                    {alert.node_id}
                  </p>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-8">
            <div className="text-green-500 mb-2">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-sm text-gray-600">
              Aktif uyarı bulunmuyor
            </p>
          </div>
        )}
      </div>
      {alerts && alerts.length > 5 && (
        <div className="mt-4 text-center">
          <button className="text-sm text-green-600 hover:text-green-800 font-medium">
            Tüm {alerts.length} uyarıyı görüntüle →
          </button>
        </div>
      )}
    </div>
  );
};

export default AlertPanel;
