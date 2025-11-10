#include <LoRa.h>
#include <Arduino.h>
#include <SPI.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

#define LORA_SS 5
#define LORA_RST 14
#define LORA_DIO0 2
#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"
#define SERVER_URL "http://your-server.com/api/sensor-data"

const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 10800;
const int daylightOffset_sec = 0;

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, ntpServer, gmtOffset_sec, daylightOffset_sec);

struct SensorData {
  String nodeId;
  float temperature;
  float humidity;
  int soilMoisture;
  float soilPh;
  float soilTemperature;
  float lightIntensity;
  float pressure;
  float altitude;
  float rainfall;
  bool isRaining;
  unsigned long timestamp;
  String receivedTime;
};

void setup() {
  Serial.begin(115200);
  while (!Serial);
  
  Serial.println("LoRa Gateway Starting...");
  
  if (!LoRa.begin(915E6)) {
    Serial.println("LoRa initialization failed!");
    while (1);
  }
  
  LoRa.setSyncWord(0xF3);
  LoRa.setTxPower(20);
  LoRa.setSpreadingFactor(12);
  LoRa.setSignalBandwidth(125E3);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nWiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  timeClient.begin();
  timeClient.update();
  
  Serial.println("LoRa Gateway Ready!");
}

void loop() {
  receiveLoRaData();
  delay(1000);
}

void receiveLoRaData() {
  int packetSize = LoRa.parsePacket();
  
  if (packetSize) {
    String receivedData = "";
    
    while (LoRa.available()) {
      receivedData += (char)LoRa.read();
    }
    
    Serial.println("Received packet: " + receivedData);
    Serial.print("RSSI: ");
    Serial.println(LoRa.packetRssi());
    Serial.print("SNR: ");
    Serial.println(LoRa.packetSnr());
    
    SensorData data = parseSensorData(receivedData);
    
    if (data.nodeId != "") {
      sendDataToServer(data);
    }
  }
}

SensorData parseSensorData(String payload) {
  SensorData data;
  String parts[12];
  int partIndex = 0;
  int startIndex = 0;
  
  for (int i = 0; i < payload.length(); i++) {
    if (payload.charAt(i) == '|') {
      parts[partIndex] = payload.substring(startIndex, i);
      startIndex = i + 1;
      partIndex++;
      
      if (partIndex >= 12) break;
    }
  }
  
  if (partIndex > 0) {
    data.nodeId = parts[0];
    data.temperature = parts[1].toFloat();
    data.humidity = parts[2].toFloat();
    data.soilMoisture = parts[3].toInt();
    data.soilPh = parts[4].toFloat();
    data.soilTemperature = parts[5].toFloat();
    data.lightIntensity = parts[6].toFloat();
    data.pressure = parts[7].toFloat();
    data.altitude = parts[8].toFloat();
    data.rainfall = parts[9].toFloat();
    data.isRaining = parts[10].toInt() == 1;
    data.timestamp = parts[11].toULong();
    data.receivedTime = timeClient.getFormattedTime();
    
    Serial.println("Parsed data for node: " + data.nodeId);
  } else {
    Serial.println("Failed to parse sensor data");
    data.nodeId = "";
  }
  
  return data;
}

void sendDataToServer(SensorData data) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");
    
    DynamicJsonDocument doc(1024);
    
    doc["nodeId"] = data.nodeId;
    doc["temperature"] = data.temperature;
    doc["humidity"] = data.humidity;
    doc["soilMoisture"] = data.soilMoisture;
    doc["soilPh"] = data.soilPh;
    doc["soilTemperature"] = data.soilTemperature;
    doc["lightIntensity"] = data.lightIntensity;
    doc["pressure"] = data.pressure;
    doc["altitude"] = data.altitude;
    doc["rainfall"] = data.rainfall;
    doc["isRaining"] = data.isRaining;
    doc["timestamp"] = data.timestamp;
    doc["receivedTime"] = data.receivedTime;
    doc["gatewayRSSI"] = LoRa.packetRssi();
    doc["gatewaySNR"] = LoRa.packetSnr();
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    Serial.println("Sending data to server: " + jsonString);
    
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println("Server response: " + response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    
    Serial.println("\nWiFi reconnected!");
  }
}
