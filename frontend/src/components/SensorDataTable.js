import React from 'react';
import { format } from 'date-fns';
import { tr } from 'date-fns/locale';

const SensorDataTable = ({ data }) => {
  const getNodeTypeColor = (nodeId) => {
    if (nodeId.includes('BASE_19007')) return 'bg-blue-100 text-blue-800';
    if (nodeId.includes('CORE_11300')) return 'bg-green-100 text-green-800';
    if (nodeId.includes('SENSOR_12005')) return 'bg-purple-100 text-purple-800';
    return 'bg-gray-100 text-gray-800';
  };

  const getNodeType = (nodeId) => {
    if (nodeId.includes('BASE_19007')) return 'Base';
    if (nodeId.includes('CORE_11300')) return 'Core';
    if (nodeId.includes('SENSOR_12005')) return 'Sensor';
    return 'Unknown';
  };

  const getSoilMoistureColor = (value) => {
    if (value < 300) return 'text-red-600 font-semibold';
    if (value < 500) return 'text-orange-600';
    return 'text-green-600';
  };

  const getTemperatureColor = (value) => {
    if (value > 35) return 'text-red-600 font-semibold';
    if (value > 30) return 'text-orange-600';
    if (value < 5) return 'text-blue-600 font-semibold';
    return 'text-green-600';
  };

  if (!data || data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>Henüz veri bulunmuyor.</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Sensör
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Sıcaklık
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Nem
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Toprak Nemi
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Işık
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Son Güncelleme
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((sensor) => (
            <tr key={sensor.id} className="hover:bg-gray-50">
              <td className="px-4 py-4 whitespace-nowrap">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getNodeTypeColor(sensor.node_id)}`}>
                      {getNodeType(sensor.node_id)}
                    </span>
                  </div>
                  <div className="ml-3">
                    <div className="text-sm font-medium text-gray-900">
                      {sensor.node_id}
                    </div>
                  </div>
                </div>
              </td>
              <td className="px-4 py-4 whitespace-nowrap">
                <div className={`text-sm ${getTemperatureColor(sensor.temperature)}`}>
                  {sensor.temperature ? `${sensor.temperature.toFixed(1)}°C` : '-'}
                </div>
              </td>
              <td className="px-4 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-900">
                  {sensor.humidity ? `${sensor.humidity.toFixed(1)}%` : '-'}
                </div>
              </td>
              <td className="px-4 py-4 whitespace-nowrap">
                <div className={`text-sm ${getSoilMoistureColor(sensor.soil_moisture)}`}>
                  {sensor.soil_moisture ? sensor.soil_moisture : '-'}
                </div>
              </td>
              <td className="px-4 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-900">
                  {sensor.light_intensity ? `${Math.round(sensor.light_intensity)} lx` : '-'}
                </div>
              </td>
              <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">
                {sensor.created_at ? 
                  format(new Date(sensor.created_at), 'HH:mm', { locale: tr }) : 
                  '-'
                }
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SensorDataTable;
