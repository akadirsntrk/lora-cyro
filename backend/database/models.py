from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Node(Base):
    __tablename__ = "nodes"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(50), unique=True, index=True, nullable=False)
    node_type = Column(String(50), nullable=False)
    location = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    last_seen = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sensor_data = relationship("SensorData", back_populates="node")
    recommendations = relationship("Recommendation", back_populates="node")

class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(50), ForeignKey("nodes.node_id"), nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    soil_moisture = Column(Integer)
    soil_ph = Column(Float)
    soil_temperature = Column(Float)
    light_intensity = Column(Float)
    pressure = Column(Float)
    altitude = Column(Float)
    rainfall = Column(Float)
    is_raining = Column(Boolean, default=False)
    timestamp = Column(Integer)
    received_time = Column(String(50))
    gateway_rssi = Column(Integer)
    gateway_snr = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    node = relationship("Node", back_populates="sensor_data")

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(50), ForeignKey("nodes.node_id"), nullable=False)
    recommendation_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(20), default="medium")
    confidence_score = Column(Float)
    action_required = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    valid_until = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    node = relationship("Node", back_populates="recommendations")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(50), ForeignKey("nodes.node_id"), nullable=False)
    alert_type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="warning")
    is_active = Column(Boolean, default=True)
    acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)
    
    node = relationship("Node")

class WeatherForecast(Base):
    __tablename__ = "weather_forecast"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(200), nullable=False)
    date = Column(DateTime, nullable=False)
    temperature_min = Column(Float)
    temperature_max = Column(Float)
    humidity = Column(Float)
    precipitation_probability = Column(Float)
    precipitation_amount = Column(Float)
    wind_speed = Column(Float)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

class CropData(Base):
    __tablename__ = "crop_data"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(50), ForeignKey("nodes.node_id"), nullable=False)
    crop_type = Column(String(100), nullable=False)
    planting_date = Column(DateTime, nullable=False)
    expected_harvest_date = Column(DateTime)
    growth_stage = Column(String(50))
    health_status = Column(String(50), default="healthy")
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    node = relationship("Node")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    farm_name = Column(String(200))
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
