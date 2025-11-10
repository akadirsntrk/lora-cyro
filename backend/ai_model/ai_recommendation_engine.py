#!/usr/bin/env python3
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import joblib
import logging
from typing import Dict, List, Tuple, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgriculturalAIEngine:
    def __init__(self):
        self.irrigation_model = None
        self.fertilizer_model = None
        self.pest_prediction_model = None
        self.yield_prediction_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_training_data(self, sensor_data: List[Dict]) -> pd.DataFrame:
        df = pd.DataFrame(sensor_data)
        
        if df.empty:
            return pd.DataFrame()
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_year'] = df['timestamp'].dt.dayofyear
        df['month'] = df['timestamp'].dt.month
        
        df['temp_humidity_ratio'] = df['temperature'] / (df['humidity'] + 1)
        df['soil_moisture_percent'] = (df['soil_moisture'] / 1023) * 100
        df['light_category'] = pd.cut(df['light_intensity'], 
                                     bins=[0, 1000, 10000, 50000, float('inf')],
                                     labels=['Low', 'Medium', 'High', 'Very High'])
        
        df['soil_ph_category'] = pd.cut(df['soil_ph'],
                                       bins=[0, 5.5, 6.5, 7.5, 8.5, float('inf')],
                                       labels=['Very Acidic', 'Acidic', 'Neutral', 'Alkaline', 'Very Alkaline'])
        
        return df
    
    def train_irrigation_model(self, training_data: pd.DataFrame):
        features = ['temperature', 'humidity', 'soil_moisture', 'light_intensity', 
                   'hour', 'day_of_year', 'temp_humidity_ratio']
        
        target = self._create_irrigation_target(training_data)
        
        X = training_data[features].fillna(training_data[features].mean())
        y = target
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.irrigation_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.irrigation_model.fit(X_train_scaled, y_train)
        
        accuracy = self.irrigation_model.score(X_test_scaled, y_test)
        logger.info(f"Irrigation model trained with accuracy: {accuracy:.2f}")
        
        return accuracy
    
    def train_fertilizer_model(self, training_data: pd.DataFrame):
        features = ['soil_moisture', 'soil_ph', 'temperature', 'humidity', 
                   'light_intensity', 'day_of_year']
        
        target = self._create_fertilizer_target(training_data)
        
        X = training_data[features].fillna(training_data[features].mean())
        y = target
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.fertilizer_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.fertilizer_model.fit(X_train_scaled, y_train)
        
        accuracy = self.fertilizer_model.score(X_test_scaled, y_test)
        logger.info(f"Fertilizer model trained with accuracy: {accuracy:.2f}")
        
        return accuracy
    
    def train_pest_prediction_model(self, training_data: pd.DataFrame):
        features = ['temperature', 'humidity', 'soil_moisture', 'light_intensity',
                   'hour', 'day_of_year', 'month']
        
        target = self._create_pest_target(training_data)
        
        X = training_data[features].fillna(training_data[features].mean())
        y = target
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.pest_prediction_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.pest_prediction_model.fit(X_train_scaled, y_train)
        
        accuracy = self.pest_prediction_model.score(X_test_scaled, y_test)
        logger.info(f"Pest prediction model trained with accuracy: {accuracy:.2f}")
        
        return accuracy
    
    def _create_irrigation_target(self, df: pd.DataFrame) -> pd.Series:
        conditions = [
            (df['soil_moisture'] < 300) & (df['temperature'] > 25),
            (df['soil_moisture'] < 400) & (df['temperature'] > 30),
            (df['soil_moisture'] < 200),
            (df['soil_moisture'] > 700) & (df['humidity'] > 80)
        ]
        
        choices = ['immediate', 'urgent', 'critical', 'none']
        
        return pd.Series(np.select(conditions, choices, default='moderate'))
    
    def _create_fertilizer_target(self, df: pd.DataFrame) -> pd.Series:
        conditions = [
            (df['soil_ph'] < 5.5),
            (df['soil_ph'] > 8.0),
            (df['soil_moisture'] < 300),
            (df['soil_moisture'] > 800)
        ]
        
        choices = ['acidic_correction', 'alkaline_correction', 'nitrogen_boost', 'drainage_improve']
        
        return pd.Series(np.select(conditions, choices, default='balanced'))
    
    def _create_pest_target(self, df: pd.DataFrame) -> pd.Series:
        conditions = [
            (df['temperature'] > 25) & (df['humidity'] > 70),
            (df['temperature'] > 30) & (df['humidity'] > 60),
            (df['temperature'] < 15) & (df['humidity'] > 80)
        ]
        
        choices = ['fungal_risk', 'insect_risk', 'bacterial_risk']
        
        return pd.Series(np.select(conditions, choices, default='low_risk'))
    
    def generate_irrigation_recommendation(self, current_data: Dict) -> Dict:
        if not self.irrigation_model:
            return {"error": "Model not trained"}
        
        features = np.array([[
            current_data.get('temperature', 0),
            current_data.get('humidity', 0),
            current_data.get('soil_moisture', 0),
            current_data.get('light_intensity', 0),
            datetime.now().hour,
            datetime.now().timetuple().tm_yday,
            current_data.get('temperature', 0) / (current_data.get('humidity', 1) + 1)
        ]])
        
        features_scaled = self.scaler.transform(features)
        prediction = self.irrigation_model.predict(features_scaled)[0]
        confidence = self.irrigation_model.predict_proba(features_scaled)[0].max()
        
        recommendations = {
            'immediate': {
                'title': 'Acil Sulama Gerekli',
                'description': 'Toprak nemi çok düşük. Hemen sulama yapın. Toprağın 5-10cm derinliğine kadar ıslak olduğundan emin olun.',
                'priority': 'critical',
                'water_amount': '15-20mm',
                'timing': 'Şimdi'
            },
            'urgent': {
                'title': 'Sulama Aciliyeti',
                'description': 'Toprak nemi düşük seviyede. 24 saat içinde sulama yapın.',
                'priority': 'high',
                'water_amount': '10-15mm',
                'timing': '24 saat içinde'
            },
            'moderate': {
                'title': 'Normal Sulama',
                'description': 'Toprak nemi uygun seviyede. Normal sulama programını takip edin.',
                'priority': 'medium',
                'water_amount': '5-10mm',
                'timing': '2-3 gün içinde'
            },
            'none': {
                'title': 'Sulama Gerekmiyor',
                'description': 'Toprak nemi yeterli. Sulama yapmayın.',
                'priority': 'low',
                'water_amount': '0mm',
                'timing': 'Haftaya kontrol edin'
            }
        }
        
        result = recommendations.get(prediction, recommendations['moderate'])
        result['confidence'] = round(confidence * 100, 2)
        result['recommendation_type'] = 'irrigation'
        
        return result
    
    def generate_fertilizer_recommendation(self, current_data: Dict) -> Dict:
        if not self.fertilizer_model:
            return {"error": "Model not trained"}
        
        features = np.array([[
            current_data.get('soil_moisture', 0),
            current_data.get('soil_ph', 7.0),
            current_data.get('temperature', 0),
            current_data.get('humidity', 0),
            current_data.get('light_intensity', 0),
            datetime.now().timetuple().tm_yday
        ]])
        
        features_scaled = self.scaler.transform(features)
        prediction = self.fertilizer_model.predict(features_scaled)[0]
        confidence = self.fertilizer_model.predict_proba(features_scaled)[0].max()
        
        recommendations = {
            'acidic_correction': {
                'title': 'Toprak pH Düzeltme',
                'description': 'Toprak çok asidik. Kireç uygulaması yapın. Her dekara 2-3 ton kireç önerilir.',
                'priority': 'high',
                'fertilizer_type': 'Kireç',
                'application_rate': '2-3 ton/dekar'
            },
            'alkaline_correction': {
                'title': 'Toprak pH Düzeltme',
                'description': 'Toprak çok alkalik. Sülfürik asit veya elementel kükürt uygulayın.',
                'priority': 'high',
                'fertilizer_type': 'Kükürt',
                'application_rate': '500-1000 kg/dekar'
            },
            'nitrogen_boost': {
                'title': 'Azot Gübrelemesi',
                'description': 'Bitki gelişimi için azot takviyesi yapın. Üre veya amonyum nitrat kullanın.',
                'priority': 'medium',
                'fertilizer_type': 'Üre',
                'application_rate': '20-30 kg/dekar'
            },
            'balanced': {
                'title': 'Dengeli Gübreleme',
                'description': 'Toprak durumu iyi. Dengeli NPK gübresi uygulayın.',
                'priority': 'low',
                'fertilizer_type': 'NPK 15-15-15',
                'application_rate': '40-50 kg/dekar'
            },
            'drainage_improve': {
                'title': 'Drenaj İyileştirme',
                'description': 'Toprak çok nemli. Drenaj sistemini kontrol edin ve iyileştirin.',
                'priority': 'medium',
                'fertilizer_type': 'Drenaj',
                'application_rate': 'Sistem kontrolü'
            }
        }
        
        result = recommendations.get(prediction, recommendations['balanced'])
        result['confidence'] = round(confidence * 100, 2)
        result['recommendation_type'] = 'fertilizer'
        
        return result
    
    def generate_pest_recommendation(self, current_data: Dict) -> Dict:
        if not self.pest_prediction_model:
            return {"error": "Model not trained"}
        
        features = np.array([[
            current_data.get('temperature', 0),
            current_data.get('humidity', 0),
            current_data.get('soil_moisture', 0),
            current_data.get('light_intensity', 0),
            datetime.now().hour,
            datetime.now().timetuple().tm_yday,
            datetime.now().month
        ]])
        
        features_scaled = self.scaler.transform(features)
        prediction = self.pest_prediction_model.predict(features_scaled)[0]
        confidence = self.pest_prediction_model.predict_proba(features_scaled)[0].max()
        
        recommendations = {
            'fungal_risk': {
                'title': 'Mantar Hastalığı Riski',
                'description': 'Yüksek nem ve sıcaklık mantar hastalıkları için uygun koşullar yaratıyor. Preventif fungisit uygulayın.',
                'priority': 'high',
                'treatment': 'Fungisit',
                'prevention': 'Havalandırma ve uygun sulama'
            },
            'insect_risk': {
                'title': 'Böcek Zararlısı Riski',
                'description': 'Yüksek sıcaklık böcek popülasyonunu artırabilir. Entegre zararlı yönetimi uygulayın.',
                'priority': 'medium',
                'treatment': 'Insektisit',
                'prevention': 'Doğal düşmanlar ve tuzaklar'
            },
            'bacterial_risk': {
                'title': 'Bakteriyel Hastalık Riski',
                'description': 'Soğuk ve nemli koşullar bakteriyel hastalıklar için risk oluşturuyor.',
                'priority': 'medium',
                'treatment': 'Bakterisit',
                'prevention': 'Sık dikimden kaçının'
            },
            'low_risk': {
                'title': 'Düşük Risk',
                'description': 'Mevcut koşullar zararlılar için uygun değil. Düzenli kontrole devam edin.',
                'priority': 'low',
                'treatment': 'Yok',
                'prevention': 'Düzenli izleme'
            }
        }
        
        result = recommendations.get(prediction, recommendations['low_risk'])
        result['confidence'] = round(confidence * 100, 2)
        result['recommendation_type'] = 'pest_control'
        
        return result
    
    def generate_comprehensive_recommendations(self, current_data: Dict) -> List[Dict]:
        recommendations = []
        
        irrigation_rec = self.generate_irrigation_recommendation(current_data)
        if 'error' not in irrigation_rec:
            recommendations.append(irrigation_rec)
        
        fertilizer_rec = self.generate_fertilizer_recommendation(current_data)
        if 'error' not in fertilizer_rec:
            recommendations.append(fertilizer_rec)
        
        pest_rec = self.generate_pest_recommendation(current_data)
        if 'error' not in pest_rec:
            recommendations.append(pest_rec)
        
        return recommendations
    
    def save_models(self, filepath: str):
        models = {
            'irrigation_model': self.irrigation_model,
            'fertilizer_model': self.fertilizer_model,
            'pest_model': self.pest_prediction_model,
            'scaler': self.scaler
        }
        
        joblib.dump(models, filepath)
        logger.info(f"Models saved to {filepath}")
    
    def load_models(self, filepath: str):
        try:
            models = joblib.load(filepath)
            self.irrigation_model = models['irrigation_model']
            self.fertilizer_model = models['fertilizer_model']
            self.pest_prediction_model = models['pest_model']
            self.scaler = models['scaler']
            self.is_trained = True
            logger.info(f"Models loaded from {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False

if __name__ == "__main__":
    ai_engine = AgriculturalAIEngine()
    
    sample_data = [
        {
            'temperature': 28.5,
            'humidity': 65,
            'soil_moisture': 350,
            'soil_ph': 6.8,
            'light_intensity': 45000,
            'timestamp': datetime.now().timestamp() * 1000
        }
    ]
    
    df = ai_engine.prepare_training_data(sample_data)
    print("Sample data prepared:")
    print(df.head())
