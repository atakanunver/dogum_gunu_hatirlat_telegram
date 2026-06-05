# 🎂 Doğum Günü Telegram Botu

Excel dosyasındaki kişilerin doğum günlerini otomatik takip eden, Telegram üzerinden metin ve sesli mesaj gönderen Python botu.

---

## 📋 Özellikler

- 📅 **Otomatik Doğum Günü Kontrolü** — Excel dosyasından her gün bugünün doğum günlerine bakar
- 📨 **Telegram Mesajı** — Bugün doğum günü olanlara Markdown formatlı kutlama mesajı gönderir
- 🎙️ **Sesli Mesaj (gTTS)** — Türkçe sesli doğum günü mesajı oluşturur ve Telegram'a sesli not olarak gönderir
- 👥 **Çoklu Alıcı** — Birden fazla Telegram kullanıcısına paralel olarak gönderim yapar
- 📝 **Loglama** — Tüm işlemler zaman damgalı olarak konsola yazılır

---

## 🖥️ Sistem Gereksinimleri

- Python **3.10+**
- Telegram Bot Token ([@BotFather](https://t.me/BotFather)'dan alınır)

---

## 📦 Kurulum

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/atakanunver/dogum-gunu-bot.git
cd dogum-gunu-bot
```

### 2. Gerekli Paketleri Yükleyin

```bash
pip install pandas openpyxl python-telegram-bot gtts
```

### 3. Ayarları Yapılandırın

`dogum_gunu_bot.py` dosyasını açarak şu iki değeri düzenleyin:

```python
BOT_TOKEN = "BURAYA_BOT_TOKENINIZI_YAZIN"

KULLANICI_IDS = [
    123456789,   # 1. kullanıcının Telegram ID'si
    987654321,   # 2. kullanıcının Telegram ID'si
]
```

> **Bot Token almak için:** Telegram'da [@BotFather](https://t.me/BotFather)'a `/newbot` gönderin.  
> **Chat ID bulmak için:** [@userinfobot](https://t.me/userinfobot)'a `/start` gönderin.

---

## 📊 Excel Dosyası Formatı

`Dogum.xlsx` dosyası `Sayfa1` adlı sayfada aşağıdaki sütunları içermelidir:

| ADI | SOYADI | DOĞUM TARİHİ | GÜN | AY |
|-----|--------|--------------|-----|----|
| Ahmet | Yılmaz | 01.06.1985 | 1 | 6 |
| Ayşe | Kaya | 15.03.1990 | 15 | 3 |

> **Önemli:** `GÜN` ve `AY` sütunları sayısal değer içermelidir.

---

## ▶️ Çalıştırma

### Manuel Başlatma

```bash
python dogum_gunu_bot.py
```

### Günlük Otomatik Çalıştırma (cron — Linux/macOS)

Her sabah saat 08:00'de çalışması için:

```bash
crontab -e
```

Aşağıdaki satırı ekleyin:

```
0 8 * * * /usr/bin/python3 /tam/yol/dogum_gunu_bot.py
```

### Windows'ta Otomatik Çalıştırma (Görev Zamanlayıcı)

1. `Görev Zamanlayıcı` → `Temel Görev Oluştur`
2. Tetikleyici: Her gün, saat 08:00
3. Eylem: `python dogum_gunu_bot.py` (tam yol ile)

---

## 📁 Dosya Yapısı

```
dogum-gunu-bot/
├── dogum_gunu_bot.py   # Ana bot kodu
├── Dogum.xlsx          # Personel/kişi listesi (⚠️ Git'e eklemeyin)
├── .gitignore
└── README.md
```

---

## 🔒 Güvenlik Notları

Token ve kişisel verilerin internete sızmaması için `.gitignore` oluşturun:

```
Dogum.xlsx
*.mp3
__pycache__/
*.pyc
```

Bot token'ını kod içine yazmak yerine ortam değişkeni olarak kullanabilirsiniz:

```python
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")
```

```bash
export BOT_TOKEN="TOKENINIZ"
```

---

## 📄 Lisans

MIT License
