#include <LoRa.h>
#include <Arduino.h>
#include <SPI.h>
#include <DHT.h>
#include <Wire.h>
#include <BH1750.h>

#define LORA_SS 10
#define LORA_RST 9
#define LORA_DIO0 2
#define DHT_PIN 3
#define DHT_TYPE DHT22
#define SOIL_MOISTURE_PIN A0
#define SOIL_TEMPERATURE_PIN A1
#define RAIN_SENSOR_PIN 2
#define RAIN_ANALOG_PIN A2
#define NODE_ID "SENSOR_12005"

DHT dht(DHT_PIN, DHT_TYPE);
BH1750 lightMeter;

volatile unsigned long rainPulseCount = 0;
unsigned long lastRainCheck = 0;

struct SensorData {
  String nodeId;
  float temperature;
  float humidity;
  float soilTemperature;
  int soilMoisture;
  float lightIntensity;
  float rainfall;
  bool isRaining;
  unsigned long timestamp;
};

void rainISR() {
  rainPulseCount++;
}

void setup() {
  Serial.begin(9600);
  while (!Serial);
  
  Serial.println("Sensor 12005 Rain & Soil Node Starting...");
  
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
  
  pinMode(SOIL_MOISTURE_PIN, INPUT);
  pinMode(SOIL_TEMPERATURE_PIN, INPUT);
  pinMode(RAIN_SENSOR_PIN, INPUT_PULLUP);
  pinMode(RAIN_ANALOG_PIN, INPUT);
  
  attachInterrupt(digitalPinToInterrupt(RAIN_SENSOR_PIN), rainISR, FALLING);
  
  Serial.println("Sensor 12005 Rain & Soil Node Ready!");
}

void loop() {
  SensorData data = readSensors();
  transmitData(data);
  
  Serial.println("Data transmitted. Sleeping for 5 minutes...");
  delay(300000);
}

SensorData readSensors() {
  SensorData data;
  
  data.nodeId = NODE_ID;
  data.temperature = dht.readTemperature();
  data.humidity = dht.readHumidity();
  data.soilTemperature = readSoilTemperature();
  data.soilMoisture = analogRead(SOIL_MOISTURE_PIN);
  data.lightIntensity = lightMeter.readLightLevel();
  data.rainfall = calculateRainfall();
  data.isRaining = digitalRead(RAIN_SENSOR_PIN) == LOW;
  data.timestamp = millis();
  
  if (isnan(data.temperature) || isnan(data.humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    data.temperature = -999;
    data.humidity = -999;
  }
  
  Serial.print("Temperature: ");
  Serial.print(data.temperature);
  Serial.println(" °C");
  Serial.print("Humidity: ");
  Serial.print(data.humidity);
  Serial.println(" %");
  Serial.print("Soil Temperature: ");
  Serial.print(data.soilTemperature);
  Serial.println(" °C");
  Serial.print("Soil Moisture: ");
  Serial.print(data.soilMoisture);
  Serial.println(" (0-1023)");
  Serial.print("Light Intensity: ");
  Serial.print(data.lightIntensity);
  Serial.println(" lx");
  Serial.print("Rainfall: ");
  Serial.print(data.rainfall);
  Serial.println(" mm");
  Serial.print("Is Raining: ");
  Serial.println(data.isRaining ? "Yes" : "No");
  
  return data;
}

float readSoilTemperature() {
  int rawValue = analogRead(SOIL_TEMPERATURE_PIN);
  float voltage = rawValue * (5.0 / 1023.0);
  float temperature = (voltage - 0.5) * 100.0;
  return temperature;
}

float calculateRainfall() {
  unsigned long currentTime = millis();
  unsigned long timeDiff = currentTime - lastRainCheck;
  
  if (timeDiff >= 60000) {
    float rainfall = (rainPulseCount * 0.2794);
    rainPulseCount = 0;
    lastRainCheck = currentTime;
    return rainfall;
  }
  
  return 0.0;
}

void transmitData(SensorData data) {
  LoRa.beginPacket();
  
  String payload = String(data.nodeId) + "|" +
                   String(data.temperature) + "|" +
                   String(data.humidity) + "|" +
                   String(data.soilTemperature) + "|" +
                   String(data.soilMoisture) + "|" +
                   String(data.lightIntensity) + "|" +
                   String(data.rainfall) + "|" +
                   String(data.isRaining ? 1 : 0) + "|" +
                   String(data.timestamp);
  
  LoRa.print(payload);
  LoRa.endPacket();
  
  Serial.println("Data transmitted via LoRa: " + payload);
}
