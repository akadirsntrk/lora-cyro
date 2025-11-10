import React from 'react';

const MetricCard = ({ title, value, total, icon, color = 'blue' }) => {
  const colorClasses = {
    blue: 'bg-blue-500',
    orange: 'bg-orange-500',
    cyan: 'bg-cyan-500',
    green: 'bg-green-500',
    red: 'bg-red-500',
    purple: 'bg-purple-500',
  };

  const bgClasses = {
    blue: 'bg-blue-50',
    orange: 'bg-orange-50',
    cyan: 'bg-cyan-50',
    green: 'bg-green-50',
    red: 'bg-red-50',
    purple: 'bg-purple-50',
  };

  const textClasses = {
    blue: 'text-blue-600',
    orange: 'text-orange-600',
    cyan: 'text-cyan-600',
    green: 'text-green-600',
    red: 'text-red-600',
    purple: 'text-purple-600',
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center">
        <div className={`flex-shrink-0 ${bgClasses[color]} p-3 rounded-lg`}>
          <div className={`${textClasses[color]}`}>
            {icon}
          </div>
        </div>
        <div className="ml-4 flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {total && (
            <p className="text-xs text-gray-500">
              Toplam: {total}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default MetricCard;
