import React from 'react';
import { CheckCircleIcon, LightBulbIcon } from '@heroicons/react/24/outline';

const RecommendationCard = ({ recommendation }) => {
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critical':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'high':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-blue-100 text-blue-800 border-blue-200';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'irrigation':
        return '💧';
      case 'fertilizer':
        return '🌱';
      case 'pest_control':
        return '🐛';
      case 'weather_protection':
        return '🌤️';
      default:
        return '💡';
    }
  };

  const getPriorityText = (priority) => {
    switch (priority) {
      case 'critical': return 'Kritik';
      case 'high': return 'Yüksek';
      case 'medium': return 'Orta';
      case 'low': return 'Düşük';
      default: return 'Normal';
    }
  };

  return (
    <div className="p-4 rounded-lg border border-gray-200 bg-white hover:shadow-md transition-shadow">
      <div className="flex items-start">
        <div className="flex-shrink-0 text-2xl">
          {getTypeIcon(recommendation.recommendation_type)}
        </div>
        <div className="ml-3 flex-1">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-semibold text-gray-900">
              {recommendation.title}
            </h3>
            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getPriorityColor(recommendation.priority)}`}>
              {getPriorityText(recommendation.priority)}
            </span>
          </div>
          <p className="text-xs text-gray-600 mb-2">
            {recommendation.description}
          </p>
          <div className="flex items-center justify-between">
            <div className="flex items-center text-xs text-gray-500">
              <LightBulbIcon className="h-3 w-3 mr-1" />
              {recommendation.confidence_score}% güven
            </div>
            <div className="text-xs text-gray-400">
              {new Date(recommendation.created_at).toLocaleDateString('tr-TR')}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecommendationCard;
