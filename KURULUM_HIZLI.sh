#!/bin/bash

# Renkler
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 LoRa Tarım Sistemi - Hızlı Kurulum${NC}"
echo "=========================================="

# Backend dizinine git
cd /home/ags/Belgeler/lora/backend

echo -e "\n${BLUE}📦 1. Sanal ortam oluşturuluyor...${NC}"
rm -rf venv
python3 -m venv venv

echo -e "${GREEN}✅ Sanal ortam oluşturuldu${NC}"

echo -e "\n${BLUE}📦 2. Sanal ortam aktif ediliyor...${NC}"
source venv/bin/activate

echo -e "${GREEN}✅ Sanal ortam aktif${NC}"

echo -e "\n${BLUE}📦 3. pip güncelleniyor...${NC}"
venv/bin/pip install --upgrade pip

echo -e "${GREEN}✅ pip güncellendi${NC}"

echo -e "\n${BLUE}📦 4. Bağımlılıklar kuruluyor (Bu 2-3 dakika sürebilir)...${NC}"
venv/bin/pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Tüm bağımlılıklar kuruldu${NC}"
else
    echo -e "${RED}❌ Bağımlılık kurulumunda hata oluştu${NC}"
    exit 1
fi

echo -e "\n${BLUE}📦 5. Veritabanı oluşturuluyor...${NC}"
venv/bin/python -c "from database.database import create_tables; create_tables()"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Veritabanı oluşturuldu${NC}"
else
    echo -e "${RED}❌ Veritabanı oluşturulurken hata oluştu${NC}"
fi

echo -e "\n${GREEN}🎉 Kurulum tamamlandı!${NC}"
echo -e "\n${BLUE}Backend'i başlatmak için:${NC}"
echo "cd /home/ags/Belgeler/lora/backend"
echo "source venv/bin/activate"
echo "uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo -e "${BLUE}Veya direkt:${NC}"
echo "venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"
