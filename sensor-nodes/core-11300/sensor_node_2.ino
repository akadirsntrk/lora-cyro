#include <LoRa.h>
#include <Arduino.h>
#include <SPI.h>
#include <DHT.h>
#include <Wire.h>
#include <BH1750.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

#define LORA_SS 10
#define LORA_RST 9
#define LORA_DIO0 2
#define DHT_PIN 3
#define DHT_TYPE DHT22
#define SOIL_MOISTURE_PIN A0
#define SOIL_PH_PIN A1
#define NODE_ID "CORE_11300_2"

DHT dht(DHT_PIN, DHT_TYPE);
BH1750 lightMeter;
Adafruit_BMP280 bmp;

struct SensorData {
  String nodeId;
  float temperature;
  float humidity;
  int soilMoisture;
  float soilPh;
  float lightIntensity;
  float pressure;
  float altitude;
  unsigned long timestamp;
};

void setup() {
  Serial.begin(9600);
  while (!Serial);
  
  Serial.println("Core 11300 Sensor Node 2 Starting...");
  
  if (!LoRa.begin(915E6)) {
    Serial.println("LoRa initialization failed!");
    while (1);
  }
  
  LoRa.setSyncWord(0xF3);
  LoRa.setTxPower(20);
  LoRa.setSpreadingFactor(12);
  LoRa.setSignalBandwidth(125E3);
  
  dht.begin();
  Wire.begin();
  
  if (!lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
    Serial.println("BH1750 initialization failed!");
    while (1);
  }
  
  if (!bmp.begin(0x76)) {
    Serial.println("BMP280 initialization failed!");
    while (1);
  }
  
  pinMode(SOIL_MOISTURE_PIN, INPUT);
  pinMode(SOIL_PH_PIN, INPUT);
  
  Serial.println("Core 11300 Sensor Node 2 Ready!");
}

void loop() {
  SensorData data = readSensors();
  transmitData(data);
  
  Serial.println("Data transmitted. Sleeping for 15 minutes...");
  delay(900000);
}

SensorData readSensors() {
  SensorData data;
  
  data.nodeId = NODE_ID;
  data.temperature = dht.readTemperature();
  data.humidity = dht.readHumidity();
  data.soilMoisture = analogRead(SOIL_MOISTURE_PIN);
  data.soilPh = readSoilPH();
  data.lightIntensity = lightMeter.readLightLevel();
  data.pressure = bmp.readPressure() / 100.0F;
  data.altitude = bmp.readAltitude(1013.25);
  data.timestamp = millis();
  
  if (isnan(data.temperature) || isnan(data.humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    data.temperature = -999;
    data.humidity = -999;
  }
  
  if (isnan(data.pressure)) {
    Serial.println("Failed to read from BMP280 sensor!");
    data.pressure = -999;
    data.altitude = -999;
  }
  
  Serial.print("Temperature: ");
  Serial.print(data.temperature);
  Serial.println(" °C");
  Serial.print("Humidity: ");
  Serial.print(data.humidity);
  Serial.println(" %");
  Serial.print("Soil Moisture: ");
  Serial.print(data.soilMoisture);
  Serial.println(" (0-1023)");
  Serial.print("Soil pH: ");
  Serial.print(data.soilPh);
  Serial.println(" (0-14)");
  Serial.print("Light Intensity: ");
  Serial.print(data.lightIntensity);
  Serial.println(" lx");
  Serial.print("Pressure: ");
  Serial.print(data.pressure);
  Serial.println(" hPa");
  Serial.print("Altitude: ");
  Serial.print(data.altitude);
  Serial.println(" m");
  
  return data;
}

float readSoilPH() {
  int rawValue = analogRead(SOIL_PH_PIN);
  float voltage = rawValue * (5.0 / 1023.0);
  float ph = 7.0 - ((voltage - 2.5) / 0.18);
  
  if (ph < 0) ph = 0;
  if (ph > 14) ph = 14;
  
  return ph;
}

void transmitData(SensorData data) {
  LoRa.beginPacket();
  
  String payload = String(data.nodeId) + "|" +
                   String(data.temperature) + "|" +
                   String(data.humidity) + "|" +
                   String(data.soilMoisture) + "|" +
                   String(data.soilPh) + "|" +
                   String(data.lightIntensity) + "|" +
                   String(data.pressure) + "|" +
                   String(data.altitude) + "|" +
                   String(data.timestamp);
  
  LoRa.print(payload);
  LoRa.endPacket();
  
  Serial.println("Data transmitted via LoRa: " + payload);
}
