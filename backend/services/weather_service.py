from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import requests
import logging

from database.models import WeatherForecast
from api.schemas import WeatherForecastResponse

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = None
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_forecast(self, db: Session, location: str, days: int = 7) -> List[WeatherForecastResponse]:
        try:
            cached_forecast = self._get_cached_forecast(db, location, days)
            if cached_forecast:
                return cached_forecast
            
            forecast_data = self._fetch_weather_forecast(location, days)
            if forecast_data:
                self._save_forecast(db, location, forecast_data)
                return self._get_cached_forecast(db, location, days)
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting weather forecast for {location}: {e}")
            return []
    
    def _fetch_weather_forecast(self, location: str, days: int) -> Optional[List[dict]]:
        try:
            if not self.api_key:
                return self._generate_mock_forecast(location, days)
            
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_weather_data(data, location)
            else:
                logger.warning(f"Weather API returned status {response.status_code}")
                return self._generate_mock_forecast(location, days)
                
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return self._generate_mock_forecast(location, days)
    
    def _parse_weather_data(self, data: dict, location: str) -> List[dict]:
        forecast_list = []
        
        for item in data['list']:
            forecast_date = datetime.fromtimestamp(item['dt'])
            
            forecast = {
                'location': location,
                'date': forecast_date,
                'temperature_min': item['main']['temp_min'],
                'temperature_max': item['main']['temp_max'],
                'humidity': item['main']['humidity'],
                'precipitation_probability': item.get('pop', 0) * 100,
                'precipitation_amount': item.get('rain', {}).get('3h', 0),
                'wind_speed': item['wind']['speed'],
                'description': item['weather'][0]['description']
            }
            
            forecast_list.append(forecast)
        
        return forecast_list
    
    def _generate_mock_forecast(self, location: str, days: int) -> List[dict]:
        forecast_list = []
        base_date = datetime.now()
        
        import random
        
        for day in range(days):
            forecast_date = base_date + timedelta(days=day)
            
            forecast = {
                'location': location,
                'date': forecast_date,
                'temperature_min': random.uniform(10, 20),
                'temperature_max': random.uniform(25, 35),
                'humidity': random.uniform(40, 80),
                'precipitation_probability': random.uniform(0, 60),
                'precipitation_amount': random.uniform(0, 10) if random.random() > 0.7 else 0,
                'wind_speed': random.uniform(5, 20),
                'description': random.choice(['Açık', 'Parçalı Bulutlu', 'Bulutlu', 'Hafif Yağmurlu'])
            }
            
            forecast_list.append(forecast)
        
        return forecast_list
    
    def _save_forecast(self, db: Session, location: str, forecast_data: List[dict]):
        try:
            for forecast in forecast_data:
                weather_forecast = WeatherForecast(**forecast)
                db.add(weather_forecast)
            
            db.commit()
            logger.info(f"Saved {len(forecast_data)} forecast records for {location}")
            
        except Exception as e:
            logger.error(f"Error saving forecast data: {e}")
            db.rollback()
    
    def _get_cached_forecast(self, db: Session, location: str, days: int) -> Optional[List[WeatherForecastResponse]]:
        try:
            cutoff_date = datetime.now() - timedelta(hours=6)
            
            forecasts = db.query(WeatherForecast).filter(
                WeatherForecast.location == location,
                WeatherForecast.created_at >= cutoff_date,
                WeatherForecast.date >= datetime.now().date(),
                WeatherForecast.date <= datetime.now().date() + timedelta(days=days)
            ).order_by(WeatherForecast.date).all()
            
            if len(forecasts) >= days:
                return forecasts
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached forecast: {e}")
            return None
    
    def get_agricultural_recommendations(self, forecast: List[WeatherForecastResponse]) -> List[dict]:
        recommendations = []
        
        if not forecast:
            return recommendations
        
        next_3_days = forecast[:3]
        
        high_temp_days = [f for f in next_3_days if f.temperature_max > 35]
        if high_temp_days:
            recommendations.append({
                'title': 'Yüksek Sıcaklık Uyarısı',
                'description': f'Önümüzdeki {len(high_temp_days)} günde 35°C üzeri sıcaklık bekleniyor. Ek sulama ve gölgelik sağlayın.',
                'priority': 'high',
                'recommendation_type': 'weather'
            })
        
        frost_days = [f for f in next_3_days if f.temperature_min < 5]
        if frost_days:
            recommendations.append({
                'title': 'Don Riski',
                'description': f'Önümüzdeki {len(frost_days)} günde don riski var. Koruyucu önlemler alın.',
                'priority': 'high',
                'recommendation_type': 'weather'
            })
        
        rainy_days = [f for f in next_3_days if f.precipitation_probability > 70]
        if rainy_days:
            recommendations.append({
                'title': 'Yağmurlu Hava',
                'description': f'Önümüzdeki {len(rainy_days)} günde yağış bekleniyor. Sulama programını ayarlayın.',
                'priority': 'medium',
                'recommendation_type': 'weather'
            })
        
        high_humidity_days = [f for f in next_3_days if f.humidity > 85]
        if high_humidity_days:
            recommendations.append({
                'title': 'Yüksek Nem',
                'description': 'Yüksek nem oranı mantar hastalıkları riskini artırıyor. Preventif önlemler alın.',
                'priority': 'medium',
                'recommendation_type': 'weather'
            })
        
        return recommendations
    
    def analyze_weather_patterns(self, db: Session, location: str, days: int = 30) -> dict:
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            forecasts = db.query(WeatherForecast).filter(
                WeatherForecast.location == location,
                WeatherForecast.date >= cutoff_date
            ).all()
            
            if not forecasts:
                return {}
            
            avg_temp_max = sum(f.temperature_max for f in forecasts) / len(forecasts)
            avg_temp_min = sum(f.temperature_min for f in forecasts) / len(forecasts)
            avg_humidity = sum(f.humidity for f in forecasts) / len(forecasts)
            total_precipitation = sum(f.precipitation_amount for f in forecasts)
            
            patterns = {
                'average_temperature_max': round(avg_temp_max, 2),
                'average_temperature_min': round(avg_temp_min, 2),
                'average_humidity': round(avg_humidity, 2),
                'total_precipitation': round(total_precipitation, 2),
                'rainy_days': len([f for f in forecasts if f.precipitation_amount > 0]),
                'hot_days': len([f for f in forecasts if f.temperature_max > 30]),
                'frost_days': len([f for f in forecasts if f.temperature_min < 5])
            }
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing weather patterns: {e}")
            return {}
