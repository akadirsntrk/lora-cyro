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
#define NODE_ID "BASE_19007_1"

DHT dht(DHT_PIN, DHT_TYPE);
BH1750 lightMeter;

struct SensorData {
  String nodeId;
  float temperature;
  float humidity;
  int soilMoisture;
  float lightIntensity;
  unsigned long timestamp;
};

void setup() {
  Serial.begin(9600);
  while (!Serial);
  
  Serial.println("Base 19007 Sensor Node Starting...");
  
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
  
  Serial.println("Base 19007 Sensor Node Ready!");
}

void loop() {
  SensorData data = readSensors();
  transmitData(data);
  
  Serial.println("Data transmitted. Sleeping for 10 minutes...");
  delay(600000);
}

SensorData readSensors() {
  SensorData data;
  
  data.nodeId = NODE_ID;
  data.temperature = dht.readTemperature();
  data.humidity = dht.readHumidity();
  data.soilMoisture = analogRead(SOIL_MOISTURE_PIN);
  data.lightIntensity = lightMeter.readLightLevel();
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
  Serial.print("Soil Moisture: ");
  Serial.print(data.soilMoisture);
  Serial.println(" (0-1023)");
  Serial.print("Light Intensity: ");
  Serial.print(data.lightIntensity);
  Serial.println(" lx");
  
  return data;
}

void transmitData(SensorData data) {
  LoRa.beginPacket();
  
  String payload = String(data.nodeId) + "|" +
                   String(data.temperature) + "|" +
                   String(data.humidity) + "|" +
                   String(data.soilMoisture) + "|" +
                   String(data.lightIntensity) + "|" +
                   String(data.timestamp);
  
  LoRa.print(payload);
  LoRa.endPacket();
  
  Serial.println("Data transmitted via LoRa: " + payload);
}
