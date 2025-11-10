#!/usr/bin/env python3
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LoRa Agricultural Gateway Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SensorData(BaseModel):
    nodeId: str
    temperature: float
    humidity: float
    soilMoisture: int
    soilPh: float = 0.0
    soilTemperature: float = 0.0
    lightIntensity: float = 0.0
    pressure: float = 0.0
    altitude: float = 0.0
    rainfall: float = 0.0
    isRaining: bool = False
    timestamp: int
    receivedTime: str
    gatewayRSSI: int
    gatewaySNR: float

def init_database():
    conn = sqlite3.connect('agricultural_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_id TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            soil_moisture INTEGER,
            soil_ph REAL,
            soil_temperature REAL,
            light_intensity REAL,
            pressure REAL,
            altitude REAL,
            rainfall REAL,
            is_raining BOOLEAN,
            timestamp INTEGER,
            received_time TEXT,
            gateway_rssi INTEGER,
            gateway_snr REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_id TEXT UNIQUE NOT NULL,
            node_type TEXT,
            location TEXT,
            last_seen TIMESTAMP,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    conn.commit()
    conn.close()

def save_sensor_data(data: Dict[str, Any]):
    try:
        conn = sqlite3.connect('agricultural_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sensor_data 
            (node_id, temperature, humidity, soil_moisture, soil_ph, soil_temperature,
             light_intensity, pressure, altitude, rainfall, is_raining, timestamp,
             received_time, gateway_rssi, gateway_snr)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['nodeId'], data['temperature'], data['humidity'],
            data['soilMoisture'], data['soilPh'], data['soilTemperature'],
            data['lightIntensity'], data['pressure'], data['altitude'],
            data['rainfall'], data['isRaining'], data['timestamp'],
            data['receivedTime'], data['gatewayRSSI'], data['gatewaySNR']
        ))
        
        cursor.execute('''
            INSERT OR REPLACE INTO nodes (node_id, last_seen, status)
            VALUES (?, ?, 'active')
        ''', (data['nodeId'], datetime.now()))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Data saved for node {data['nodeId']}")
        
    except Exception as e:
        logger.error(f"Error saving data: {e}")

def get_node_type(node_id: str) -> str:
    if "BASE_19007" in node_id:
        return "Base Station"
    elif "CORE_11300" in node_id:
        return "Core Station"
    elif "SENSOR_12005" in node_id:
        return "Rain & Soil Sensor"
    else:
        return "Unknown"

@app.on_event("startup")
async def startup_event():
    init_database()
    logger.info("Database initialized successfully")

@app.post("/api/sensor-data")
async def receive_sensor_data(data: SensorData, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(save_sensor_data, data.dict())
        
        node_type = get_node_type(data.nodeId)
        
        response_data = {
            "status": "success",
            "message": "Data received successfully",
            "nodeType": node_type,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Received data from {data.nodeId}")
        return response_data
        
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/nodes")
async def get_nodes():
    try:
        conn = sqlite3.connect('agricultural_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT node_id, node_type, location, last_seen, status
            FROM nodes
            ORDER BY last_seen DESC
        ''')
        
        nodes = []
        for row in cursor.fetchall():
            nodes.append({
                "nodeId": row[0],
                "nodeType": get_node_type(row[0]) if not row[1] else row[1],
                "location": row[2],
                "lastSeen": row[3],
                "status": row[4]
            })
        
        conn.close()
        return {"nodes": nodes}
        
    except Exception as e:
        logger.error(f"Error fetching nodes: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/sensor-data/{node_id}")
async def get_node_data(node_id: str, limit: int = 100):
    try:
        conn = sqlite3.connect('agricultural_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM sensor_data
            WHERE node_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (node_id, limit))
        
        columns = [description[0] for description in cursor.description]
        data = []
        
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))
        
        conn.close()
        return {"data": data}
        
    except Exception as e:
        logger.error(f"Error fetching node data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/latest-data")
async def get_latest_data():
    try:
        conn = sqlite3.connect('agricultural_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT node_id, temperature, humidity, soil_moisture, soil_ph,
                   soil_temperature, light_intensity, pressure, rainfall,
                   is_raining, created_at
            FROM sensor_data s1
            WHERE created_at = (
                SELECT MAX(created_at)
                FROM sensor_data s2
                WHERE s2.node_id = s1.node_id
            )
            ORDER BY created_at DESC
        ''')
        
        columns = [description[0] for description in cursor.description]
        data = []
        
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))
        
        conn.close()
        return {"data": data}
        
    except Exception as e:
        logger.error(f"Error fetching latest data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
