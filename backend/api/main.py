from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from database.database import get_db, create_tables
from database.models import Node, SensorData, Recommendation, Alert, WeatherForecast, CropData
from services.ai_service import AIRecommendationService
from services.data_service import DataService
from services.weather_service import WeatherService
from api.schemas import (
    SensorDataCreate, SensorDataResponse, NodeResponse, 
    RecommendationResponse, AlertResponse, WeatherForecastResponse
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agricultural Monitoring System API",
    description="LoRa-based agricultural monitoring with AI recommendations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_service = AIRecommendationService()
data_service = DataService()
weather_service = WeatherService()

@app.on_event("startup")
async def startup_event():
    create_tables()
    logger.info("Database tables created successfully")

@app.post("/api/sensor-data", response_model=dict)
async def receive_sensor_data(
    data: SensorDataCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        sensor_data = data_service.save_sensor_data(db, data)
        
        background_tasks.add_task(
            ai_service.generate_recommendations, 
            db, data.node_id
        )
        
        background_tasks.add_task(
            data_service.check_alerts,
            db, sensor_data.id
        )
        
        logger.info(f"Data received from node {data.node_id}")
        
        return {
            "status": "success",
            "message": "Data received and processed",
            "data_id": sensor_data.id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing sensor data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/nodes", response_model=List[NodeResponse])
async def get_nodes(db: Session = Depends(get_db)):
    nodes = db.query(Node).all()
    return nodes

@app.get("/api/nodes/{node_id}", response_model=NodeResponse)
async def get_node(node_id: str, db: Session = Depends(get_db)):
    node = db.query(Node).filter(Node.node_id == node_id).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

@app.get("/api/sensor-data/{node_id}", response_model=List[SensorDataResponse])
async def get_node_sensor_data(
    node_id: str, 
    limit: int = 100,
    hours: Optional[int] = None,
    db: Session = Depends(get_db)
):
    data = data_service.get_node_data(db, node_id, limit, hours)
    return data

@app.get("/api/latest-data", response_model=List[SensorDataResponse])
async def get_latest_data(db: Session = Depends(get_db)):
    data = data_service.get_latest_data(db)
    return data

@app.get("/api/recommendations/{node_id}", response_model=List[RecommendationResponse])
async def get_recommendations(
    node_id: str,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    recommendations = ai_service.get_recommendations(db, node_id, active_only)
    return recommendations

@app.post("/api/recommendations/{recommendation_id}/complete")
async def complete_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db)
):
    success = ai_service.complete_recommendation(db, recommendation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    return {"status": "success", "message": "Recommendation marked as completed"}

@app.get("/api/alerts", response_model=List[AlertResponse])
async def get_alerts(
    active_only: bool = True,
    node_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    alerts = data_service.get_alerts(db, active_only, node_id)
    return alerts

@app.post("/api/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    success = data_service.acknowledge_alert(db, alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {"status": "success", "message": "Alert acknowledged"}

@app.get("/api/weather-forecast/{location}", response_model=List[WeatherForecastResponse])
async def get_weather_forecast(
    location: str,
    days: int = 7,
    db: Session = Depends(get_db)
):
    forecast = weather_service.get_forecast(db, location, days)
    return forecast

@app.get("/api/analytics/dashboard")
async def get_dashboard_data(db: Session = Depends(get_db)):
    analytics = data_service.get_dashboard_analytics(db)
    return analytics

@app.get("/api/analytics/trends/{node_id}")
async def get_trends(
    node_id: str,
    days: int = 30,
    db: Session = Depends(get_db)
):
    trends = data_service.get_trends(db, node_id, days)
    return trends

@app.post("/api/crops/{node_id}")
async def register_crop(
    node_id: str,
    crop_data: dict,
    db: Session = Depends(get_db)
):
    crop = data_service.register_crop(db, node_id, crop_data)
    return {"status": "success", "crop_id": crop.id}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
