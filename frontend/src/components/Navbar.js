import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  HomeIcon, 
  CpuChipIcon, 
  ChartBarIcon, 
  LightBulbIcon, 
  CogIcon 
} from '@heroicons/react/24/outline';

const Navbar = () => {
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: HomeIcon },
    { name: 'Sensorler', href: '/nodes', icon: CpuChipIcon },
    { name: 'Analiz', href: '/analytics', icon: ChartBarIcon },
    { name: 'Öneriler', href: '/recommendations', icon: LightBulbIcon },
    { name: 'Ayarlar', href: '/settings', icon: CogIcon },
  ];

  return (
    <nav className="bg-green-600 shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <h1 className="text-white text-xl font-bold">
                🌾 Akıllı Tarım Sistemi
              </h1>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                {navigation.map((item) => {
                  const isActive = location.pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={`${
                        isActive
                          ? 'bg-green-700 text-white'
                          : 'text-green-100 hover:bg-green-500 hover:text-white'
                      } px-3 py-2 rounded-md text-sm font-medium flex items-center space-x-2 transition-colors`}
                    >
                      <item.icon className="h-4 w-4" />
                      <span>{item.name}</span>
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-green-100 text-sm">
              Son Güncelleme: {new Date().toLocaleTimeString('tr-TR')}
            </div>
            <div className="bg-green-700 rounded-full px-3 py-1">
              <span className="text-green-100 text-sm font-medium">
                🟢 Sistem Aktif
              </span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
