from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from database.models import Node, SensorData, Recommendation
from ai_model.ai_recommendation_engine import AgriculturalAIEngine
from api.schemas import RecommendationResponse

logger = logging.getLogger(__name__)

class AIRecommendationService:
    def __init__(self):
        self.ai_engine = AgriculturalAIEngine()
        self.model_trained = False
        
    def generate_recommendations(self, db: Session, node_id: str):
        try:
            recent_data = db.query(SensorData).filter(
                SensorData.node_id == node_id
            ).order_by(desc(SensorData.created_at)).limit(100).all()
            
            if len(recent_data) < 10:
                logger.info(f"Insufficient data for AI recommendations for node {node_id}")
                self._generate_rule_based_recommendations(db, node_id, recent_data[-1] if recent_data else None)
                return
            
            training_data = []
            for data in recent_data:
                training_data.append({
                    'temperature': data.temperature,
                    'humidity': data.humidity,
                    'soil_moisture': data.soil_moisture,
                    'soil_ph': data.soil_ph,
                    'light_intensity': data.light_intensity,
                    'pressure': data.pressure,
                    'rainfall': data.rainfall,
                    'timestamp': data.timestamp
                })
            
            if not self.model_trained:
                df = self.ai_engine.prepare_training_data(training_data)
                if len(df) > 20:
                    self.ai_engine.train_irrigation_model(df)
                    self.ai_engine.train_fertilizer_model(df)
                    self.ai_engine.train_pest_prediction_model(df)
                    self.model_trained = True
                    logger.info("AI models trained successfully")
            
            current_data = training_data[-1] if training_data else {}
            ai_recommendations = self.ai_engine.generate_comprehensive_recommendations(current_data)
            
            for rec in ai_recommendations:
                self._save_recommendation(db, node_id, rec)
            
            logger.info(f"Generated {len(ai_recommendations)} AI recommendations for node {node_id}")
            
        except Exception as e:
            logger.error(f"Error generating AI recommendations for node {node_id}: {e}")
            self._generate_rule_based_recommendations(db, node_id, None)
    
    def _generate_rule_based_recommendations(self, db: Session, node_id: str, latest_data: Optional[SensorData]):
        if not latest_data:
            return
        
        recommendations = []
        
        if latest_data.soil_moisture and latest_data.soil_moisture < 300:
            recommendations.append({
                'title': 'Acil Sulama Gerekli',
                'description': f'Toprak nemi kritik seviyede ({latest_data.soil_moisture}). Hemen sulama yapın.',
                'priority': 'critical',
                'recommendation_type': 'irrigation',
                'confidence': 85.0
            })
        elif latest_data.soil_moisture and latest_data.soil_moisture < 400:
            recommendations.append({
                'title': 'Sulama Planlayın',
                'description': f'Toprak nemi düşük ({latest_data.soil_moisture}). 24 saat içinde sulama yapın.',
                'priority': 'high',
                'recommendation_type': 'irrigation',
                'confidence': 75.0
            })
        
        if latest_data.soil_ph:
            if latest_data.soil_ph < 5.5:
                recommendations.append({
                    'title': 'Toprağı Kireçleyin',
                    'description': f'Toprak pH seviyesi çok asidik ({latest_data.soil_ph}). Kireç uygulaması yapın.',
                    'priority': 'high',
                    'recommendation_type': 'fertilizer',
                    'confidence': 90.0
                })
            elif latest_data.soil_ph > 8.0:
                recommendations.append({
                    'title': 'Toprak pH Düzeltme',
                    'description': f'Toprak pH seviyesi çok alkalik ({latest_data.soil_ph}). Kükürt veya asit uygulayın.',
                    'priority': 'high',
                    'recommendation_type': 'fertilizer',
                    'confidence': 90.0
                })
        
        if latest_data.temperature and latest_data.temperature > 35:
            recommendations.append({
                'title': 'Yüksek Sıcaklık Uyarısı',
                'description': f'Sıcaklık çok yüksek ({latest_data.temperature}°C). Gölgelik ve ek sulama sağlayın.',
                'priority': 'high',
                'recommendation_type': 'weather_protection',
                'confidence': 95.0
            })
        elif latest_data.temperature and latest_data.temperature < 5:
            recommendations.append({
                'title': 'Düşük Sıcaklık Korunması',
                'description': f'Sıcaklık çok düşük ({latest_data.temperature}°C). Don koruması sağlayın.',
                'priority': 'high',
                'recommendation_type': 'weather_protection',
                'confidence': 95.0
            })
        
        if latest_data.humidity and latest_data.humidity > 85:
            recommendations.append({
                'title': 'Havalandırma Gerekli',
                'description': f'Nem oranı çok yüksek ({latest_data.humidity}%). Havalandırma sağlayın.',
                'priority': 'medium',
                'recommendation_type': 'environment_control',
                'confidence': 80.0
            })
        
        if latest_data.rainfall and latest_data.rainfall > 30:
            recommendations.append({
                'title': 'Ağır Yağış Uyarısı',
                'description': f'Ağır yağış ({latest_data.rainfall}mm). Drenajı kontrol edin.',
                'priority': 'medium',
                'recommendation_type': 'weather_protection',
                'confidence': 85.0
            })
        
        for rec in recommendations:
            self._save_recommendation(db, node_id, rec)
        
        logger.info(f"Generated {len(recommendations)} rule-based recommendations for node {node_id}")
    
    def _save_recommendation(self, db: Session, node_id: str, rec_data: dict):
        existing_rec = db.query(Recommendation).filter(
            Recommendation.node_id == node_id,
            Recommendation.recommendation_type == rec_data['recommendation_type'],
            Recommendation.is_completed == False
        ).order_by(desc(Recommendation.created_at)).first()
        
        if existing_rec:
            time_diff = datetime.utcnow() - existing_rec.created_at
            if time_diff < timedelta(hours=6):
                return
        
        recommendation = Recommendation(
            node_id=node_id,
            recommendation_type=rec_data['recommendation_type'],
            title=rec_data['title'],
            description=rec_data['description'],
            priority=rec_data.get('priority', 'medium'),
            confidence_score=rec_data.get('confidence', 70.0),
            action_required=True,
            valid_until=datetime.utcnow() + timedelta(days=7)
        )
        
        db.add(recommendation)
        db.commit()
    
    def get_recommendations(
        self, 
        db: Session, 
        node_id: str, 
        active_only: bool = True
    ) -> List[RecommendationResponse]:
        query = db.query(Recommendation).filter(Recommendation.node_id == node_id)
        
        if active_only:
            query = query.filter(
                Recommendation.is_completed == False,
                Recommendation.valid_until > datetime.utcnow()
            )
        
        recommendations = query.order_by(
            desc(Recommendation.priority),
            desc(Recommendation.created_at)
        ).all()
        
        return recommendations
    
    def complete_recommendation(self, db: Session, recommendation_id: int) -> bool:
        recommendation = db.query(Recommendation).filter(
            Recommendation.id == recommendation_id
        ).first()
        
        if recommendation:
            recommendation.is_completed = True
            db.commit()
            logger.info(f"Recommendation {recommendation_id} marked as completed")
            return True
        
        return False
    
    def get_farm_overview_recommendations(self, db: Session) -> List[RecommendationResponse]:
        critical_recommendations = db.query(Recommendation).filter(
            Recommendation.priority == 'critical',
            Recommendation.is_completed == False,
            Recommendation.valid_until > datetime.utcnow()
        ).order_by(desc(Recommendation.created_at)).limit(10).all()
        
        return critical_recommendations
    
    def analyze_trends_and_suggest(self, db: Session, node_id: str, days: int = 7):
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        data = db.query(SensorData).filter(
            SensorData.node_id == node_id,
            SensorData.created_at >= cutoff_date
        ).order_by(SensorData.created_at).all()
        
        if len(data) < 5:
            return []
        
        trends = self._analyze_trends(data)
        suggestions = self._generate_trend_suggestions(trends, node_id)
        
        for suggestion in suggestions:
            self._save_recommendation(db, node_id, suggestion)
        
        return suggestions
    
    def _analyze_trends(self, data: List[SensorData]) -> dict:
        temperatures = [d.temperature for d in data if d.temperature is not None]
        humidities = [d.humidity for d in data if d.humidity is not None]
        soil_moistures = [d.soil_moisture for d in data if d.soil_moisture is not None]
        
        trends = {}
        
        if len(temperatures) > 1:
            temp_trend = temperatures[-1] - temperatures[0]
            trends['temperature'] = 'increasing' if temp_trend > 2 else 'decreasing' if temp_trend < -2 else 'stable'
        
        if len(humidities) > 1:
            humidity_trend = humidities[-1] - humidities[0]
            trends['humidity'] = 'increasing' if humidity_trend > 10 else 'decreasing' if humidity_trend < -10 else 'stable'
        
        if len(soil_moistures) > 1:
            moisture_trend = soil_moistures[-1] - soil_moistures[0]
            trends['soil_moisture'] = 'increasing' if moisture_trend > 50 else 'decreasing' if moisture_trend < -50 else 'stable'
        
        return trends
    
    def _generate_trend_suggestions(self, trends: dict, node_id: str) -> List[dict]:
        suggestions = []
        
        if trends.get('temperature') == 'increasing':
            suggestions.append({
                'title': 'Artan Sıcaklık Trendi',
                'description': 'Son günlerde sıcaklık artıyor. Sulama sıklığını artırın ve gölgelik sağlayın.',
                'priority': 'medium',
                'recommendation_type': 'trend_analysis',
                'confidence': 70.0
            })
        
        if trends.get('soil_moisture') == 'decreasing':
            suggestions.append({
                'title': 'Azalan Toprak Nemi',
                'description': 'Toprak nemi azalma trendinde. Sulama programını gözden geçirin.',
                'priority': 'high',
                'recommendation_type': 'trend_analysis',
                'confidence': 75.0
            })
        
        if trends.get('humidity') == 'increasing':
            suggestions.append({
                'title': 'Artan Nem Oranı',
                'description': 'Nem oranı artıyor. Havalandırma sağlayın ve mantar hastalıklarına karşı dikkatli olun.',
                'priority': 'medium',
                'recommendation_type': 'trend_analysis',
                'confidence': 65.0
            })
        
        return suggestions
