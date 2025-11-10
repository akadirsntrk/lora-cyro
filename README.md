# 🌾 Akıllı Tarım Sistemi - LoRa Tabanlı Tarımsal İzleme ve Yapay Zeka Destekli Öneri Platformu

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React 18+](https://img.shields.io/badge/react-18+-blue.svg)](https://reactjs.org/)
[![LoRa](https://img.shields.io/badge/LoRa-915MHz-green.svg)](https://www.lora-alliance.org/)

## 📸 Sistem Görünümü

![Dashboard Ekran Görüntüsü](img/ss.png)

*Akıllı Tarım Sistemi Dashboard - Gerçek zamanlı sensör verileri, AI önerileri ve sistem durumu*

## 📋 Proje Özeti

Bu proje, LoRa (Long Range) teknolojisi tabanlı bir tarımsal izleme sistemidir. Farklı sensör kartları (Base 19007 x2, Core 11300 x2, Sensor 12005) kullanarak tarla alanlarından gerçek zamanlı veri toplar, bu verileri yapay zeka ile analiz eder ve çiftçilere kişiselleştirilmiş tarımsal öneriler sunar.

### 🎯 Ana Hedefler
- **Gerçek zamanlı veri toplama**: Sıcaklık, nem, toprak nemi, pH, ışık şiddeti, yağış vb.
- **Yapay zeka destekli analiz**: Makine öğrenmesi ile veri analizi ve öneri üretimi
- **Web tabanlı arayüz**: Kullanıcı dostu dashboard ve analiz panelleri
- **Uzaktan izleme**: Mobil uyumlu arayüz ile her yerden erişim
- **Otomatik uyarılar**: Kritik durumlar için anında bildirimler

## 🏗️ Sistem Mimarisi

```
┌─────────────────┐    LoRa    ┌─────────────────┐    WiFi    ┌─────────────────┐
│   Sensör Nodları │ ◄───────► │   LoRa Gateway  │ ◄───────► │   Backend API   │
│                 │           │                 │           │                 │
│ • Base 19007 x2 │           │ • ESP32         │           │ • FastAPI       │
│ • Core 11300 x2 │           │ • Veri Toplama  │           │ • PostgreSQL    │
│ • Sensor 12005  │           │ • İletim        │           │ • AI Motoru     │
└─────────────────┘           └─────────────────┘           └─────────────────┘
                                                                      │
                                                               HTTP/HTTPS
                                                                      │
┌─────────────────┐           ┌─────────────────┐           ┌─────────────────┐
│   Çiftçi Web    │ ◄───────► │   React App     │ ◄───────► │   Veritabanı    │
│   Arayüzü       │           │                 │           │                 │
│                 │           │ • Dashboard     │           │ • Sensör Veri   │
│ • Gerçek Zamanlı│           │ • Analiz        │           │ • Öneriler      │
│ • Öneriler      │           │ • Grafikler     │           │ • Kullanıcılar  │
│ • Raporlar      │           │ • Mobil Uyumlu  │           │                 │
└─────────────────┘           └─────────────────┘           └─────────────────┘
```

## 🛠️ Teknolojik Altyapı

### Sensör Katmanı
- **Base 19007 x2**: Temel çevresel sensörler (sıcaklık, nem, toprak nemi, ışık)
- **Core 11300 x2**: Gelişmiş sensörler (ek olarak pH, basınç, rakım)
- **Sensor 12005**: Yağmur ve toprak sensörleri (yağış miktarı, toprak sıcaklığı)

### İletim Katmanı
- **LoRa 915MHz**: Uzun mesafe, düşük güç tüketimi
- **ESP32 Gateway**: WiFi entegrasyonu ve veri merkezi
- **Mesh Network**: Sensörler arası iletişim

### Backend Altyapısı
- **FastAPI**: Yüksek performanslı Python API
- **PostgreSQL**: Güvenilir veritabanı
- **SQLAlchemy**: ORM ve veri modelleme
- **Redis**: Cache ve mesajlaşma

### Yapay Zeka Motoru
- **Scikit-learn**: Makine öğrenmesi algoritmaları
- **Pandas**: Veri analizi ve işleme
- **NumPy**: Sayısal hesaplamalar
- **Random Forest**: Tahmin modelleri

### Frontend Arayüzü
- **React 18**: Modern JavaScript kütüphanesi
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Veri görselleştirme
- **React Query**: Veri yönetimi ve caching

## 🚀 Hızlı Başlangıç ve Sistemi Çalıştırma

### ⚡ Adım Adım Kurulum (15 Dakikada)

#### 1. Gereksinimleri Kontrol Et
```bash
# Python versiyonu kontrol
python --version  # 3.8+ olmalı

# Node.js versiyonu kontrol  
node --version    # 16+ olmalı

# Arduino IDE kurulu mu kontrol
arduino-cli version
```

#### 2. Projeyi İndir ve Hazırla
```bash
# GitHub'dan klonla
git clone https://github.com/akadirsntrk/lora-cyro.git
cd lora-cyro

# Proje yapısını gör
tree -L 2
```

#### 3. Backend'i Başlat
```bash
# Backend dizinine git
cd backend

# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları kur
pip install -r requirements.txt

# Veritabanını başlat
python -c "from database.database import create_tables; create_tables()"

# API sunucusunu çalıştır
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Başka terminalde test et
curl http://localhost:8000/health
# Beklenen çıktı: {"status":"healthy","timestamp":"...","version":"1.0.0"}
```

#### 4. Frontend'i Başlat
```bash
# Yeni terminal aç ve frontend dizinine git
cd frontend

# Node.js bağımlılıklarını kur
npm install

# Geliştirme sunucusunu başlat
npm start

# Tarayıcıda aç: http://localhost:3000
# Dashboard görülmeli
```

#### 5. LoRa Gateway'i Kur
```bash
# Gateway dizinine git
cd gateway

# Python sunucusunu başlat
python gateway_server.py

# Logları kontrol et
# INFO: Database initialized successfully
# INFO: Application startup complete
```

#### 6. Sensörleri Programla
```bash
# Arduino IDE'yi aç ve şu kütüphaneleri kur:
# - LoRa by Sandeep Mistry
# - DHT sensor library by Adafruit
# - BH1750 by Christopher Laws
# - Adafruit BMP280 Library

# Base 19007 sensörlerini yükle
arduino-cli upload --port /dev/ttyUSB0 sensor-nodes/base-19007/sensor_node.ino
arduino-cli upload --port /dev/ttyUSB1 sensor-nodes/base-19007/sensor_node_2.ino

# Core 11300 sensörlerini yükle  
arduino-cli upload --port /dev/ttyUSB2 sensor-nodes/core-11300/sensor_node.ino
arduino-cli upload --port /dev/ttyUSB3 sensor-nodes/core-11300/sensor_node_2.ino

# Sensor 12005'ü yükle
arduino-cli upload --port /dev/ttyUSB4 sensor-nodes/sensor-12005/rain_soil_node.ino

# Gateway'i yükle
arduino-cli upload --port /dev/ttyUSB5 gateway/lora_gateway.ino
```

### 🔄 Tam Sistemi Çalıştırma (Docker ile)

#### Docker Compose Hızlı Başlangıç
```bash
# Proje ana dizininde
docker-compose up -d

# Tüm servislerin durumu
docker-compose ps

# Logları izle
docker-compose logs -f

# Sistemi durdur
docker-compose down
```

#### Docker Compose Dosyası
```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/agricultural_db
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=agricultural_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

  gateway:
    build: ./gateway
    ports:
      - "8001:8000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### 📊 Sistemi Test Etme

#### 1. API Testleri
```bash
# API çalışıyor mu?
curl http://localhost:8000/health

# Sensör verisi gönder (test)
curl -X POST http://localhost:8000/api/sensor-data \
  -H "Content-Type: application/json" \
  -d '{
    "nodeId": "TEST_001",
    "temperature": 25.5,
    "humidity": 65.0,
    "soilMoisture": 450,
    "timestamp": 1699123456789
  }'

# Veriyi kontrol et
curl http://localhost:8000/api/latest-data
```

#### 2. Frontend Testleri
```bash
# Browser'da aç
http://localhost:3000

# Beklenen görüntü:
# - Dashboard yüklendi
# - "Sistem Aktif" yeşil buton
# - Sensör verileri tablosu
# - Grafikler çalışıyor
```

#### 3. LoRa İletişim Testi
```bash
# Serial monitor ile sensör verisini izle
# Arduino IDE: Tools → Serial Monitor
# Baud rate: 9600

# Beklenen çıktı:
# Base 19007 Sensor Node Ready!
# Temperature: 25.5 °C
# Humidity: 65.0 %
# Soil Moisture: 450
# Data transmitted via LoRa: BASE_19007_1|25.5|65.0|450|...
```

### 🛠️ Sorun Giderme

#### Backend Çalışmıyor
```bash
# Port kontrolü
netstat -tulpn | grep :8000

# Python modülleri kontrol
pip list | grep fastapi

# Logları kontrol et
uvicorn api.main:app --reload --log-level debug
```

#### Frontend Çalışmıyor
```bash
# Node_modules sil ve yeniden kur
rm -rf node_modules package-lock.json
npm install

# Port kontrolü
lsof -ti:3000 | xargs kill -9

# Cache temizle
npm start -- --reset-cache
```

#### LoRa İletişim Yok
```bash
# Seri portları kontrol et
ls /dev/ttyUSB*

# LoRa modülünü test et
# Arduino IDE: File → Examples → LoRa → LoRaSender

# Frekans kontrolü
# LoRa frekansı: 915MHz (ABD) / 868MHz (AB)
```

### 📈 Sistem Performansı İzleme

#### Sistem Durumu Kontrolü
```bash
# API performansı
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# Veritabanı bağlantısı
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://postgres:password@localhost/agricultural_db')
print('✅ Veritabanı bağlantısı başarılı')
"

# Redis bağlantısı
redis-cli ping
# Beklenen: PONG
```

#### Sensör Veri Akışı Testi
```bash
# WebSocket bağlantısı testi
wscat -c ws://localhost:8000/ws

# Gerçek zamanlı veri akışı izle
# {"nodeId":"BASE_19007_1","temperature":25.5,"humidity":65.0,...}
```

### 🔧 Gelişmiş Konfigürasyon

#### Production Ortamı
```bash
# Production environment variables
export DATABASE_URL="postgresql://user:pass@prod-db:5432/agricultural_db"
export REDIS_URL="redis://prod-redis:6379"
export SECRET_KEY="your-production-secret"

# Production build
cd frontend
npm run build

# Production sunucusu
cd backend
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### Monitoring ve Logging
```bash
# Log aggregation
docker-compose logs -f --tail=100

# Performance monitoring
pip install prometheus-client
# Metrics: http://localhost:8000/metrics

# Health checks
curl http://localhost:8000/health
curl http://localhost:3000/health
```

### 📱 Mobil Erişim

#### Responsive Test
```bash
# Chrome DevTools mobil modu
# F12 → Mobil ikonu → iPhone 12

# Test et:
# - Dashboard mobil görünüm
# - Grafikler dokunmatik çalışıyor
# - Menü mobil uyumlu
```

#### PWA (Progressive Web App)
```bash
# Service Worker kurulumu
# Browser'da: http://localhost:3000
# Chrome: → Install app

# Offline test
# Network → Offline
# Sayfa yenile → Çalışmalı
```

## 📊 Özellikler ve Fonksiyonlar

### 🌡️ Sensör Veri Toplama
- **Sıcaklık**: Hava ve toprak sıcaklığı izleme
- **Nem**: Bağıl nem ve toprak nemi ölçümü
- **pH**: Toprak asidite seviyesi takibi
- **Işık**: Işık şiddeti ve fotosentez uygunluğu
- **Basınç**: Atmosfer basıncı ve hava durumu
- **Yağış**: Yağmur miktarı ve yağış durumu
- **Rakım**: GPS ile konum belirleme

### 🤖 Yapay Zeka Önerileri
- **Sulama Optimizasyonu**: Toprak nemi ve hava durumu based
- **Gübreleme Zamanlaması**: pH seviyeleri ve bitki gelişimi
- **Zararlılı Tahmini**: Hava koşulları based risk analizi
- **Hasat Zamanlaması**: Bitki gelişim aşamaları
- **Verimlilik Analizi**: Tarihsel veri based öngörüler

### 📱 Web Arayüzü
- **Gerçek zamanlı Dashboard**: Anlık veri görselleştirme
- **Trend Analizleri**: Tarihsel veri grafikleri
- **Öneri Paneli**: AI tarafından üretilen öneriler
- **Uyarı Sistemi**: Kritik durum bildirimleri
- **Raporlama**: PDF ve Excel export
- **Mobil Uyumlu**: Responsive tasarım

## 🖼️ Sistem Görselleri ve Ekran Görüntüleri

### Dashboard Arayüzü
```
┌─────────────────────────────────────────────────────────────┐
│ 🌾 Akıllı Tarım Sistemi                    🟢 Sistem Aktif   │
├─────────────────────────────────────────────────────────────┤
│ Dashboard │ Sensorler │ Analiz │ Öneriler │ Ayarlar          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐             │
│ │Aktif    │ │Ortalama │ │Ortalama │ │Aktif    │             │
│ │Sensörler│ │Sıcaklık │ │Nem      │ │Öneriler │             │
│ │   5/6   │ │  25.3°C │ │  68%    │ │   12    │             │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘             │
│                                                             │
│ ┌─────────────────────────────────┐ ┌─────────────────────┐ │
│ │Son Sensör Verileri               │ │Aktif Uyarılar       │ │
│ │┌─────┬──────┬─────┬─────┬──────┐│ │🔴 Kritik: Düşük     │ │
│ ││Sensör│Sıcak │Nem  │Nem  │Işık  ││ │toprak nemi -        │ │
│ ││Base1│25.5°C│65%  │450  │35K  ││ │BASE_19007_1         │ │
│ ││Core1│26.1°C│70%  │380  │42K  ││ │🟡 Uyarı: Yüksek     │ │
│ ││Sens1│24.8°C│62%  │520  │28K  ││ │nem oranı            │ │
│ │└─────┴──────┴─────┴─────┴──────┘│ └─────────────────────┘ │
│ └─────────────────────────────────┘                       │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │Son Öneriler                                              │ │
│ │💧 Acil Sulama Gerekli - BASE_19007_1 (85% güven)        │ │
│ │🌱 Toprağı Kireçleyin - CORE_11300_2 (90% güven)         │ │
│ │🌤️ Yüksek Sıcaklık Uyarısı - SENSOR_12005 (95% güven)   │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Sensör Veri Grafiği
```
Sıcaklık Trendi (Son 24 Saat)
30°C ┤                  ╭─╮
25°C ┤     ╭─╮        ╭─╯ ╰─╮
20°C ┤ ╭─╮ ╭─╯ ╰─╮ ╭─╮╯      ╰─╮
15°C ┤ ╭─╯ ╰─╯   ╰─╯ ╰─╯         ╰─
10°C ┼─╯
     └───────────────────────────────
      00:00   06:00   12:00   18:00   24:00
```

### LoRa Ağ Topolojisi
```
          ┌─────────────┐
          │   LoRa      │
          │   Gateway   │
          │   (ESP32)   │
          └──────┬──────┘
                 │ 2-5km
        ┌────────┼────────┐
        │        │        │
   ┌────▼───┐ ┌─▼───┐ ┌──▼────┐
   │Base    │ │Core │ │Sensor │
   │19007-1 │ │11300│ │12005  │
   └────────┘ └─────┘ └───────┘
        │        │        │
   ┌────▼───┐ ┌─▼───┐ ┌──▼────┐
   │Base    │ │Core │ │Yağmur │
   │19007-2 │ │11300│ │Toprak │
   └────────┘ └─────┘ └───────┘
```

### AI Öneri Akışı
```
Sensör Verileri → Veri İşleme → AI Analiz → Öneri Üretimi
     │               │            │              │
┌────▼────┐    ┌─────▼─────┐ ┌────▼────┐   ┌─────▼─────┐
│Sıcaklık │    │Normalizasyon│ │Random   │   │Sulama     │
│25.5°C   │───▶│Filtreleme  │─▶│Forest   │──▶│Önerisi    │
│Nem 65%  │    │Temizleme   │ │Model    │   │"15-20mm"  │
│Toprak   │    │Agregasyon  │ │         │   │           │
│Nemi 450 │    │            │ │         │   │           │
└─────────┘    └───────────┘ └─────────┘   └───────────┘
```

## 🔧 Konfigürasyon

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:password@localhost/agricultural_db
API_SECRET_KEY=your-secret-key
LORA_SERVER_URL=http://localhost:8000
WEATHER_API_KEY=your-weather-api-key

# Frontend (.env)
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WEBSOCKET_URL=ws://localhost:8000/ws
```

### LoRa Konfigürasyonu
```cpp
// LoRa ayarları
#define LORA_FREQUENCY 915E6
#define LORA_SYNC_WORD 0xF3
#define LORA_TX_POWER 20
#define LORA_SPREADING_FACTOR 12
#define LORA_BANDWIDTH 125E3
```

### Sensör Kalibrasyonu
```python
# Sensör kalibrasyon değerleri
SOIL_MOISTURE_MIN = 200  # Kuru toprak
SOIL_MOISTURE_MAX = 800  # Islak toprak
PH_CALIBRATION_OFFSET = 0.1
TEMPERATURE_OFFSET = -0.5
```

## 📈 API Dokümantasyonu

### Ana Endpoints
```http
# Sensör verileri
POST /api/sensor-data
GET  /api/sensor-data/{node_id}
GET  /api/latest-data

# Nod yönetimi
GET  /api/nodes
GET  /api/nodes/{node_id}

# Öneriler
GET  /api/recommendations/{node_id}
POST /api/recommendations/{id}/complete

# Uyarılar
GET  /api/alerts
POST /api/alerts/{id}/acknowledge

# Analiz
GET  /api/analytics/dashboard
GET  /api/analytics/trends/{node_id}

# Hava durumu
GET  /api/weather-forecast/{location}
```

### Veri Formatı
```json
{
  "nodeId": "BASE_19007_1",
  "temperature": 25.5,
  "humidity": 65.2,
  "soilMoisture": 450,
  "soilPh": 6.8,
  "lightIntensity": 35000,
  "timestamp": 1699123456789,
  "gatewayRSSI": -85,
  "gatewaySNR": 9.5
}
```

## 🎯 Kullanım Senaryoları

### 1. Sulama Yönetimi
- **Otomatik tetikleme**: Toprak nemi < 300 olduğunda sulama önerisi
- **Hava durumu entegrasyonu**: Yağış tahminlerine göre sulama erteleme
- **Su verimliliği**: Optimum sulama miktarı ve zamanlaması

### 2. Gübreleme Optimizasyonu
- **pH based gübreleme**: Asidik/alkalik toprak düzeltme
- **Besin eksikliği**: NPK dengesi analizi
- **Organik gübre**: Kompost ve doğal gübre önerileri

### 3. Zararlılı Yönetimi
- **Preventif uygulamalar**: Riskli koşullarda önleyici tedbirler
- **Entegre mücadele**: Kimyasal ve biyolojik kontrol
- **Doğal düşmanlar**: Faydalı böcek kullanımı

### 4. Hasat Planlaması
- **Olgunluk takibi**: Bitki gelişim aşamaları
- **Kalite analizi**: Şeker, asit, vitamin seviyeleri
- **Depolama önerileri**: Hasat sonrası işlemler

## 🔒 Güvenlik ve Veri Koruma

### Veri Şifreleme
- **LoRa iletişim**: AES-256 şifreleme
- **API iletişim**: HTTPS/TLS 1.3
- **Veritabanı**: Şifreli depolama

### Erişim Kontrolü
- **Kullanıcı kimlik doğrulama**: JWT token
- **Rol based yetkilendirme**: Çiftçi, teknisyen, admin
- **API rate limiting**: DDoS koruması

### Veri Yedekleme
- **Otomatik yedekleme**: Günlük veri yedekleri
- **Coğrafi dağıtım**: Farklı lokasyonlarda yedek
- **Kurtarma planı**: Disaster recovery prosedürleri

## 📊 Performans Metrikleri

### Sistem Performansı
- **Veri gecikmesi**: < 5 sanie (gateway to API)
- **API yanıt süresi**: < 200ms (ortalama)
- **Veri işleme kapasitesi**: 1000+ sensör
- **Uptime**: %99.9 hedef

### Sensör Performansı
- **Pil ömrü**: 6-12 ay (normal kullanımda)
- **İletim menzili**: 2-5 km ( açık alanda)
- **Veri doğruluğu**: ±2% (sıcaklık), ±3% (nem)
- **Kalibrasyon süresi**: 6 ayda bir

## 🌍 Çevresel Etki

### Sürdürülebilirlik
- **Su tasarrufu**: %30-50 daha az su kullanımı
- **Gübre verimliliği**: %20-40 daha az kimyasal gübre
- **Enerji verimliliği**: Düşük güç tüketimli sensörler
- **Karbon ayak izi**: %25 azaltma hedefi

### Ekolojik Faydalar
- **Toprak sağlığı**: pH ve organik madde takibi
- **Biyolojik çeşitlilik**: Zararlılı kontrolü
- **Su kaynakları**: Yeraltı suyu koruması
- **İklim değişikliği**: Adaptasyon stratejileri

## 🤝 Katkı ve Geliştirme

### Geliştirme Ortamı
```bash
# Development ortamı kurulumu
git clone https://github.com/akadirsntrk/lora-cyro.git
cd lora-cyro
docker-compose up -d  # Tüm servisleri başlatır
```

### Kod Standartları
- **Python**: PEP 8 standartları
- **JavaScript**: ESLint + Prettier
- **Arduino**: Google C++ style guide
- **Documentation**: Markdown formatı

### Test Stratejisi
```bash
# Backend testleri
pytest backend/tests/

# Frontend testleri
npm test -- --coverage

# Integration testleri
python -m pytest integration/
```

## 📞 Destek ve İletişim

### Teknik Destek
- **Dokümantasyon**: [Wiki](https://github.com/akadirsntrk/lora-cyro/wiki)
- **Issue tracking**: [GitHub Issues](https://github.com/akadirsntrk/lora-cyro/issues)
- **Discord topluluğu**: [Sunucu linki](https://discord.gg/lora-cyro)

### İletişim Bilgileri
- **Proje Lideri**: Ahmet Kadir Şentürk
- **E-posta**: akadir.sntrk@example.com
- **LinkedIn**: [Profil](https://linkedin.com/in/akadirsntrk)

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında dağıtılmaktadır. Telif hakkı © 2024 Akıllı Tarım Sistemi.

---

## 🏆 Teşekkür ve Referanslar

### Destekleyen Kurumlar
- **TÜBİTAK**: Ar-Ge desteği
- **Tarım Bakanlığı**: Danışmanlık
- **Üniversiteler**: Akademik işbirliği

### Teknoloji Partnerleri
- **Semtech**: LoRa teknolojisi
- **Arduino**: Sensör platformu
- **AWS**: Bulut altyapısı

### Açık Kaynak Projeler
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - JavaScript kütüphanesi
- [Scikit-learn](https://scikit-learn.org/) - Makine öğrenmesi
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework

---

**🌱 Birlikte daha verimli tarım için!**

*Bu proje, teknoloji ve tarımın birleşimiyle sürdürülebilir geleceğe katkı sağlamayı amaçlamaktadır.*
