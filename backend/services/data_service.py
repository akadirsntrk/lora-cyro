from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from datetime import datetime, timedelta

from database.models import Node, SensorData, Alert, CropData
from api.schemas import (
    SensorDataCreate, SensorDataResponse, NodeResponse, 
    AlertResponse, DashboardAnalytics, TrendData, NodeTrends
)

class DataService:
    
    def save_sensor_data(self, db: Session, data: SensorDataCreate) -> SensorData:
        sensor_data = SensorData(**data.dict())
        
        node = db.query(Node).filter(Node.node_id == data.node_id).first()
        if node:
            node.last_seen = datetime.utcnow()
        
        db.add(sensor_data)
        db.commit()
        db.refresh(sensor_data)
        
        return sensor_data
    
    def get_node_data(
        self, 
        db: Session, 
        node_id: str, 
        limit: int = 100,
        hours: Optional[int] = None
    ) -> List[SensorDataResponse]:
        query = db.query(SensorData).filter(SensorData.node_id == node_id)
        
        if hours:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            query = query.filter(SensorData.created_at >= cutoff_time)
        
        data = query.order_by(desc(SensorData.created_at)).limit(limit).all()
        return data
    
    def get_latest_data(self, db: Session) -> List[SensorDataResponse]:
        subquery = db.query(
            SensorData.node_id,
            func.max(SensorData.created_at).label('latest_time')
        ).group_by(SensorData.node_id).subquery()
        
        latest_data = db.query(SensorData).join(
            subquery,
            (SensorData.node_id == subquery.c.node_id) &
            (SensorData.created_at == subquery.c.latest_time)
        ).all()
        
        return latest_data
    
    def get_alerts(
        self, 
        db: Session, 
        active_only: bool = True,
        node_id: Optional[str] = None
    ) -> List[AlertResponse]:
        query = db.query(Alert)
        
        if active_only:
            query = query.filter(Alert.is_active == True)
        
        if node_id:
            query = query.filter(Alert.node_id == node_id)
        
        alerts = query.order_by(desc(Alert.created_at)).all()
        return alerts
    
    def acknowledge_alert(self, db: Session, alert_id: int) -> bool:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.acknowledged = True
            db.commit()
            return True
        return False
    
    def check_alerts(self, db: Session, sensor_data_id: int):
        sensor_data = db.query(SensorData).filter(SensorData.id == sensor_data_id).first()
        if not sensor_data:
            return
        
        alerts_to_create = []
        
        if sensor_data.temperature and sensor_data.temperature > 40:
            alerts_to_create.append(Alert(
                node_id=sensor_data.node_id,
                alert_type="high_temperature",
                message=f"Yüksek sıcaklık uyarısı: {sensor_data.temperature}°C",
                severity="warning"
            ))
        elif sensor_data.temperature and sensor_data.temperature < 5:
            alerts_to_create.append(Alert(
                node_id=sensor_data.node_id,
                alert_type="low_temperature",
                message=f"Düşük sıcaklık uyarısı: {sensor_data.temperature}°C",
                severity="warning"
            ))
        
        if sensor_data.soil_moisture and sensor_data.soil_moisture < 200:
            alerts_to_create.append(Alert(
                node_id=sensor_data.node_id,
                alert_type="low_soil_moisture",
                message=f"Düşük toprak nemi: {sensor_data.soil_moisture}",
                severity="critical"
            ))
        
        if sensor_data.soil_ph and (sensor_data.soil_ph < 5.5 or sensor_data.soil_ph > 8.0):
            alerts_to_create.append(Alert(
                node_id=sensor_data.node_id,
                alert_type="abnormal_ph",
                message=f"Anormal pH seviyesi: {sensor_data.soil_ph}",
                severity="warning"
            ))
        
        if sensor_data.rainfall and sensor_data.rainfall > 50:
            alerts_to_create.append(Alert(
                node_id=sensor_data.node_id,
                alert_type="heavy_rain",
                message=f"Ağır yağış uyarısı: {sensor_data.rainfall}mm",
                severity="warning"
            ))
        
        for alert in alerts_to_create:
            existing_alert = db.query(Alert).filter(
                Alert.node_id == alert.node_id,
                Alert.alert_type == alert.alert_type,
                Alert.is_active == True
            ).first()
            
            if not existing_alert:
                db.add(alert)
        
        db.commit()
    
    def register_crop(self, db: Session, node_id: str, crop_data: dict) -> CropData:
        crop = CropData(
            node_id=node_id,
            crop_type=crop_data.get("crop_type"),
            planting_date=datetime.fromisoformat(crop_data.get("planting_date")),
            expected_harvest_date=datetime.fromisoformat(crop_data.get("expected_harvest_date")) if crop_data.get("expected_harvest_date") else None,
            growth_stage=crop_data.get("growth_stage"),
            notes=crop_data.get("notes")
        )
        
        db.add(crop)
        db.commit()
        db.refresh(crop)
        
        return crop
    
    def get_dashboard_analytics(self, db: Session) -> DashboardAnalytics:
        total_nodes = db.query(Node).count()
        active_nodes = db.query(Node).filter(Node.status == "active").count()
        total_data_points = db.query(SensorData).count()
        
        recent_alerts = db.query(Alert).filter(
            Alert.is_active == True,
            Alert.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).count()
        
        active_recommendations = db.query(func.count(func.distinct(SensorData.node_id))).scalar() or 0
        
        avg_temp = db.query(func.avg(SensorData.temperature)).filter(
            SensorData.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).scalar() or 0.0
        
        avg_humidity = db.query(func.avg(SensorData.humidity)).filter(
            SensorData.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).scalar() or 0.0
        
        avg_soil_moisture = db.query(func.avg(SensorData.soil_moisture)).filter(
            SensorData.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).scalar() or 0.0
        
        return DashboardAnalytics(
            total_nodes=total_nodes,
            active_nodes=active_nodes,
            total_data_points=total_data_points,
            recent_alerts=recent_alerts,
            active_recommendations=active_recommendations,
            average_temperature=round(avg_temp, 2),
            average_humidity=round(avg_humidity, 2),
            average_soil_moisture=round(avg_soil_moisture, 2)
        )
    
    def get_trends(self, db: Session, node_id: str, days: int = 30) -> NodeTrends:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        data = db.query(SensorData).filter(
            SensorData.node_id == node_id,
            SensorData.created_at >= cutoff_date
        ).order_by(SensorData.created_at).all()
        
        trends = []
        for item in data:
            trends.append(TrendData(
                date=item.created_at,
                temperature=item.temperature,
                humidity=item.humidity,
                soil_moisture=item.soil_moisture,
                light_intensity=item.light_intensity,
                rainfall=item.rainfall
            ))
        
        return NodeTrends(node_id=node_id, trends=trends)
