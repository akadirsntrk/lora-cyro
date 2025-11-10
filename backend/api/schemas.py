from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SensorDataBase(BaseModel):
    node_id: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    soil_moisture: Optional[int] = None
    soil_ph: Optional[float] = None
    soil_temperature: Optional[float] = None
    light_intensity: Optional[float] = None
    pressure: Optional[float] = None
    altitude: Optional[float] = None
    rainfall: Optional[float] = None
    is_raining: Optional[bool] = False
    timestamp: Optional[int] = None
    received_time: Optional[str] = None
    gateway_rssi: Optional[int] = None
    gateway_snr: Optional[float] = None

class SensorDataCreate(SensorDataBase):
    pass

class SensorDataResponse(SensorDataBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class NodeBase(BaseModel):
    node_id: str
    node_type: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: Optional[str] = "active"

class NodeCreate(NodeBase):
    pass

class NodeResponse(NodeBase):
    id: int
    last_seen: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class RecommendationBase(BaseModel):
    node_id: str
    recommendation_type: str
    title: str
    description: str
    priority: Optional[str] = "medium"
    confidence_score: Optional[float] = None
    action_required: Optional[bool] = True
    valid_until: Optional[datetime] = None

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationResponse(RecommendationBase):
    id: int
    is_completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    node_id: str
    alert_type: str
    message: str
    severity: Optional[str] = "warning"

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: int
    is_active: bool
    acknowledged: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class WeatherForecastBase(BaseModel):
    location: str
    date: datetime
    temperature_min: Optional[float] = None
    temperature_max: Optional[float] = None
    humidity: Optional[float] = None
    precipitation_probability: Optional[float] = None
    precipitation_amount: Optional[float] = None
    wind_speed: Optional[float] = None
    description: Optional[str] = None

class WeatherForecastCreate(WeatherForecastBase):
    pass

class WeatherForecastResponse(WeatherForecastBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CropDataBase(BaseModel):
    node_id: str
    crop_type: str
    planting_date: datetime
    expected_harvest_date: Optional[datetime] = None
    growth_stage: Optional[str] = None
    health_status: Optional[str] = "healthy"
    notes: Optional[str] = None

class CropDataCreate(CropDataBase):
    pass

class CropDataResponse(CropDataBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DashboardAnalytics(BaseModel):
    total_nodes: int
    active_nodes: int
    total_data_points: int
    recent_alerts: int
    active_recommendations: int
    average_temperature: float
    average_humidity: float
    average_soil_moisture: float

class TrendData(BaseModel):
    date: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    soil_moisture: Optional[int] = None
    light_intensity: Optional[float] = None
    rainfall: Optional[float] = None

class NodeTrends(BaseModel):
    node_id: str
    trends: List[TrendData]
