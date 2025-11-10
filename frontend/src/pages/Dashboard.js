import React from 'react';
import { useQuery } from 'react-query';
import { format } from 'date-fns';
import { tr } from 'date-fns/locale';
import {
  FireIcon,
  BeakerIcon,
  SunIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  CpuChipIcon
} from '@heroicons/react/24/outline';

import { apiService } from '../services/api';
import MetricCard from '../components/MetricCard';
import SensorDataTable from '../components/SensorDataTable';
import AlertPanel from '../components/AlertPanel';
import RecommendationCard from '../components/RecommendationCard';

const Dashboard = () => {
  const { data: analytics, isLoading: analyticsLoading } = useQuery(
    'dashboard-analytics',
    apiService.getDashboardAnalytics,
    { refetchInterval: 30000 }
  );

  const { data: latestData, isLoading: dataLoading } = useQuery(
    'latest-data',
    apiService.getLatestData,
    { refetchInterval: 30000 }
  );

  const { data: alerts, isLoading: alertsLoading } = useQuery(
    'alerts',
    () => apiService.getAlerts({ active_only: true }),
    { refetchInterval: 30000 }
  );

  const { data: recommendations, isLoading: recommendationsLoading } = useQuery(
    'recommendations',
    () => apiService.getRecommendations({ active_only: true }),
    { refetchInterval: 60000 }
  );

  if (analyticsLoading || dataLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <div className="text-sm text-gray-500">
          {format(new Date(), 'dd MMMM yyyy HH:mm', { locale: tr })}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Aktif Sensörler"
          value={analytics?.active_nodes || 0}
          total={analytics?.total_nodes || 0}
          icon={<CpuChipIcon className="h-6 w-6" />}
          color="blue"
        />
        
        <MetricCard
          title="Ortalama Sıcaklık"
          value={`${analytics?.average_temperature || 0}°C`}
          icon={<FireIcon className="h-6 w-6" />}
          color="orange"
        />
        
        <MetricCard
          title="Ortalama Nem"
          value={`${analytics?.average_humidity || 0}%`}
          icon={<BeakerIcon className="h-6 w-6" />}
          color="cyan"
        />
        
        <MetricCard
          title="Aktif Öneriler"
          value={analytics?.active_recommendations || 0}
          icon={<SunIcon className="h-6 w-6" />}
          color="green"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Son Sensör Verileri
            </h2>
            <SensorDataTable data={latestData?.data || []} />
          </div>
        </div>

        <div className="space-y-6">
          <AlertPanel 
            alerts={alerts?.data || []} 
            isLoading={alertsLoading}
          />
          
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Son Öneriler
            </h2>
            <div className="space-y-3">
              {recommendations?.data?.slice(0, 3).map((rec) => (
                <RecommendationCard key={rec.id} recommendation={rec} />
              ))}
              {(!recommendations?.data || recommendations.data.length === 0) && (
                <p className="text-gray-500 text-sm">
                  Henüz öneri bulunmuyor.
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Sistem Durumu
          </h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">LoRa Gateway</span>
              <span className="flex items-center text-green-600">
                <CheckCircleIcon className="h-4 w-4 mr-1" />
                Aktif
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">AI Motoru</span>
              <span className="flex items-center text-green-600">
                <CheckCircleIcon className="h-4 w-4 mr-1" />
                Çalışıyor
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Veritabanı</span>
              <span className="flex items-center text-green-600">
                <CheckCircleIcon className="h-4 w-4 mr-1" />
                Bağlı
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Hızlı İstatistikler
          </h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Toplam Veri Noktası</span>
              <span className="text-sm font-medium text-gray-900">
                {analytics?.total_data_points || 0}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Son 24 Saat Uyarı</span>
              <span className="text-sm font-medium text-gray-900">
                {analytics?.recent_alerts || 0}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Ortalama Toprak Nemi</span>
              <span className="text-sm font-medium text-gray-900">
                {Math.round(analytics?.average_soil_moisture || 0)}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow p-6 text-white">
          <h3 className="text-lg font-semibold mb-4">
            Tarım Önerisi
          </h3>
          <div className="space-y-2">
            <p className="text-sm opacity-90">
              🌱 Bu hafta bitkileriniz için ideal koşullar devam ediyor.
            </p>
            <p className="text-sm opacity-90">
              💧 Sulama programınızı mevcut nem seviyelerine göre ayarlayın.
            </p>
            <p className="text-sm opacity-90">
              🌡️ Sıcaklık artışına karşı önlemler alın.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
