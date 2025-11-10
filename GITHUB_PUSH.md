# 🚀 GitHub'a Projeyi Yükleme Rehberi

## Adım 1: Git Kurulumunu Kontrol Et
```bash
# Git kurulu mu kontrol et
git --version

# Eğer kurulu değilse:
sudo apt-get update
sudo apt-get install git
```

## Adım 2: Git Yapılandırması
```bash
# Git kullanıcı bilgilerini ayarla
git config --global user.name "Ahmet Kadir Şentürk"
git config --global user.email "akadir.sntrk@example.com"

# Ayarları kontrol et
git config --list
```

## Adım 3: Yerel Git Repository'sini Başlat
```bash
# Proje dizinine git
cd /home/ags/Belgeler/lora

# Git repository'sini başlat
git init

# Tüm dosyaları ekle
git add .

# İlk commit'i yap
git commit -m "Initial commit: LoRa Agricultural Monitoring System

- Sensor nodes (Base 19007 x2, Core 11300 x2, Sensor 12005)
- LoRa Gateway with ESP32
- Backend API with FastAPI
- AI recommendation engine
- React frontend dashboard
- Complete documentation"
```

## Adım 4: GitHub Repository Oluştur
```bash
# 1. GitHub.com'a git ve giriş yap
# 2. Sağ üstteki "+" butonuna tıkla
# 3. "New repository" seç
# 4. Repository adı: lora-cyro
# 5. Description: "LoRa-based Agricultural Monitoring System with AI Recommendations"
# 6. Public seç (veya Private)
# 7. "Create repository" butonuna tıkla
```

## Adım 5: Remote Repository'yi Bağla
```bash
# GitHub repository'sini remote olarak ekle
git remote add origin https://github.com/akadirsntrk/lora-cyro.git

# Remote'u kontrol et
git remote -v
```

## Adım 6: GitHub'a Push Et
```bash
# Ana branch'i main olarak ayarla
git branch -M main

# İlk push
git push -u origin main

# Kullanıcı adı ve şifre isteyecek
# Kullanıcı adı: akadirsntrk
# Şifre: GitHub Personal Access Token (PAT) kullanmalısınız
```

## 🔐 GitHub Personal Access Token (PAT) Oluşturma

### Token Oluşturma Adımları:
1. GitHub → Settings (sağ üst profil resmi)
2. Developer settings (sol menü en alt)
3. Personal access tokens → Tokens (classic)
4. Generate new token → Generate new token (classic)
5. Note: "LoRa Project Access"
6. Expiration: 90 days (veya istediğiniz süre)
7. Select scopes:
   - ✅ repo (tüm repo erişimi)
   - ✅ workflow
8. Generate token
9. **Token'ı kopyala ve güvenli bir yere kaydet!** (Bir daha göremezsiniz)

### Token ile Push:
```bash
# Push yaparken şifre yerine token'ı kullan
git push -u origin main

# Username: akadirsntrk
# Password: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (token)
```

## 🔄 Sonraki Değişiklikler İçin

### Değişiklikleri Push Etme:
```bash
# Değişiklikleri kontrol et
git status

# Tüm değişiklikleri ekle
git add .

# Commit yap
git commit -m "Açıklayıcı commit mesajı"

# Push et
git push origin main
```

### Örnek Commit Mesajları:
```bash
git commit -m "feat: Add weather forecast integration"
git commit -m "fix: Resolve LoRa connection timeout issue"
git commit -m "docs: Update installation instructions"
git commit -m "refactor: Optimize AI recommendation algorithm"
```

## 📝 README.md Güncelleme

GitHub'da güzel görünmesi için README.md'yi kontrol edin:
```bash
# README'yi görüntüle
cat README.md

# Gerekirse düzenle
nano README.md
# veya
code README.md
```

## 🏷️ Release Oluşturma (Opsiyonel)

### İlk Release:
```bash
# Tag oluştur
git tag -a v1.0.0 -m "First stable release"

# Tag'i push et
git push origin v1.0.0
```

### GitHub'da Release:
1. GitHub repository sayfasına git
2. "Releases" → "Create a new release"
3. Tag: v1.0.0
4. Title: "v1.0.0 - Initial Release"
5. Description:
```markdown
## 🎉 First Stable Release

### Features
- ✅ Complete sensor network (5 nodes)
- ✅ LoRa gateway with ESP32
- ✅ Backend API with FastAPI
- ✅ AI-powered recommendations
- ✅ React dashboard
- ✅ Real-time monitoring
- ✅ Alert system

### Installation
See [README.md](README.md) for installation instructions.

### Documentation
Full documentation available in the repository.
```

## 🌿 Branch Stratejisi (Gelişmiş)

### Development Branch:
```bash
# Development branch oluştur
git checkout -b development

# Değişiklikleri yap
git add .
git commit -m "Development changes"

# Push et
git push origin development
```

### Feature Branch:
```bash
# Yeni özellik için branch
git checkout -b feature/weather-integration

# Değişiklikleri yap
git add .
git commit -m "Add weather API integration"

# Push et
git push origin feature/weather-integration

# GitHub'da Pull Request oluştur
```

## 🔍 Kontrol Listesi

Push etmeden önce kontrol edin:
- [ ] `.gitignore` dosyası var ve doğru
- [ ] Hassas bilgiler (şifreler, API keys) yok
- [ ] README.md güncel ve detaylı
- [ ] Tüm dosyalar commit edildi
- [ ] Commit mesajları açıklayıcı
- [ ] Kod çalışıyor ve test edildi

## 🚨 Önemli Notlar

### ❌ Asla Push Etmeyin:
- API keys ve şifreler
- `.env` dosyaları
- `node_modules/` klasörü
- `venv/` klasörü
- Veritabanı dosyaları (*.db, *.sqlite)
- Geçici dosyalar

### ✅ Push Edin:
- Kaynak kod dosyaları
- Dokümantasyon
- Konfigürasyon şablonları
- README ve LICENSE
- Docker dosyaları
- Requirements dosyaları

## 🔄 Hızlı Komutlar Özeti

```bash
# Durum kontrolü
git status

# Değişiklikleri ekle
git add .

# Commit
git commit -m "Mesaj"

# Push
git push origin main

# Pull (güncellemeleri al)
git pull origin main

# Branch değiştir
git checkout branch-name

# Yeni branch
git checkout -b new-branch

# Logları gör
git log --oneline

# Son commit'i geri al (dikkatli!)
git reset --soft HEAD~1
```

## 📞 Sorun mu Yaşıyorsunuz?

### Authentication Hatası:
```bash
# Credential helper kullan
git config --global credential.helper store

# Veya SSH kullan
ssh-keygen -t ed25519 -C "akadir.sntrk@example.com"
# SSH key'i GitHub'a ekle: Settings → SSH and GPG keys
```

### Push Reddedildi:
```bash
# Önce pull yap
git pull origin main --rebase

# Sonra push et
git push origin main
```

### Büyük Dosya Hatası:
```bash
# Git LFS kullan (Large File Storage)
git lfs install
git lfs track "*.bin"
git add .gitattributes
```

---

## 🎯 Tek Komutla Push

Hızlı push için alias oluştur:
```bash
# Bash alias ekle
echo 'alias gpush="git add . && git commit -m \"Quick update\" && git push origin main"' >> ~/.bashrc
source ~/.bashrc

# Kullanım
gpush
```

**Başarılar! 🚀**
