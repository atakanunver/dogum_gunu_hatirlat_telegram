import pandas as pd
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from gtts import gTTS
import asyncio
import os
import logging

# ========== LOGGING AYARI ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)

# ========== AYARLAR ==========
BOT_TOKEN = "82............x_s"
KULLANICI_IDS = [
    5784403,   # 1. kullanıcı ID
    9654321,    # 2. kullanıcı ID
    # 111222333,  # 3. kullanıcı (isteğe bağlı)
]
EXCEL_DOSYASI = "Dogum.xlsx"
SES_DOSYASI = "dogum_gunu.mp3"
# ==============================


def bugun_dogum_gunleri() -> list[str]:
    """Excel dosyasından bugün doğum günü olanları döndürür."""
    try:
        df = pd.read_excel(EXCEL_DOSYASI, sheet_name="Sayfa1")
    except FileNotFoundError:
        log.error(f"Excel dosyası bulunamadı: {EXCEL_DOSYASI}")
        return []
    except Exception as e:
        log.error(f"Excel okuma hatası: {e}")
        return []

    # Sütun adlarındaki baştaki/sondaki boşlukları temizle
    df.columns = df.columns.str.strip()

    gerekli_sutunlar = ["ADI", "SOYADI", "DOĞUM TARİHİ", "GÜN", "AY"]
    eksik = [s for s in gerekli_sutunlar if s not in df.columns]
    if eksik:
        log.error(f"Excel'de eksik sütunlar: {eksik}")
        log.info(f"Mevcut sütunlar: {list(df.columns)}")
        return []

    df = df[gerekli_sutunlar].copy()

    # GÜN ve AY sütunlarını sayısal tipe dönüştür
    df["GÜN"] = pd.to_numeric(df["GÜN"], errors="coerce")
    df["AY"] = pd.to_numeric(df["AY"], errors="coerce")

    bugun = datetime.today()
    filtrelenmis = df[
        (df["GÜN"] == bugun.day) & (df["AY"] == bugun.month)
    ]

    isimler = []
    for _, row in filtrelenmis.iterrows():
        try:
            ad = str(row["ADI"]).strip()
            soyad = str(row["SOYADI"]).strip()
            if ad and soyad and ad != "nan" and soyad != "nan":
                isimler.append(f"{ad} {soyad}")
        except Exception as e:
            log.warning(f"Satır işlenirken hata: {e}")

    return isimler


def mesaj_olustur(isimler: list[str]) -> str:
    """Telegram için Markdown formatlı mesaj oluşturur."""
    tarih = datetime.today().strftime("%d.%m.%Y")
    satirlar = "\n".join(f"🎂 Mutlu Yıllar {isim}!" for isim in isimler)
    return (
        f"🎉 *Bugün Doğanlar* ({tarih})\n\n"
        f"{satirlar}\n\n"
        f"Nice mutlu yıllara! 🥳"
    )


def ses_olustur(isimler: list[str]) -> str | None:
    """Türkçe sesli doğum günü mesajı oluşturur."""
    try:
        cumleler = " ".join(f"Mutlu Yıllar {isim}!" for isim in isimler)
        tam_metin = f"Bugün doğum günü olanlar. {cumleler} Nice mutlu yıllara!"
        tts = gTTS(text=tam_metin, lang="tr", slow=False)
        tts.save(SES_DOSYASI)
        log.info(f"Ses dosyası oluşturuldu: {SES_DOSYASI}")
        return SES_DOSYASI
    except Exception as e:
        log.error(f"Ses oluşturma hatası: {e}")
        return None


async def kullaniciya_gonder(bot: Bot, kullanici_id: int, mesaj: str, ses_dosyasi: str | None):
    """Tek bir kullanıcıya mesaj ve ses gönderir."""
    try:
        await bot.send_message(
            chat_id=kullanici_id,
            text=mesaj,
            parse_mode="Markdown"
        )
        log.info(f"✅ Metin mesajı gönderildi → {kullanici_id}")
    except TelegramError as e:
        log.error(f"❌ Metin gönderilemedi ({kullanici_id}): {e}")

    if ses_dosyasi and os.path.exists(ses_dosyasi):
        try:
            with open(ses_dosyasi, "rb") as ses:
                await bot.send_voice(
                    chat_id=kullanici_id,
                    voice=ses,
                    caption="🎙️ Sesli Doğum Günü Mesajı"
                )
            log.info(f"✅ Sesli mesaj gönderildi → {kullanici_id}")
        except TelegramError as e:
            log.error(f"❌ Ses gönderilemedi ({kullanici_id}): {e}")


async def gonder(mesaj: str, ses_dosyasi: str | None):
    """Tüm kullanıcılara paralel olarak mesaj gönderir."""
    async with Bot(token=BOT_TOKEN) as bot:
        gorevler = [
            kullaniciya_gonder(bot, uid, mesaj, ses_dosyasi)
            for uid in KULLANICI_IDS
        ]
        await asyncio.gather(*gorevler)


def main():
    log.info("🚀 Doğum günü botu başlatıldı.")
    isimler = bugun_dogum_gunleri()

    if not isimler:
        log.info("📅 Bugün doğum günü olan kimse yok.")
        return

    log.info(f"🎂 Bugün doğum günü olanlar: {', '.join(isimler)}")
    mesaj = mesaj_olustur(isimler)
    log.info(f"Gönderilecek mesaj:\n{mesaj}")

    ses_dosyasi = ses_olustur(isimler)

    try:
        asyncio.run(gonder(mesaj, ses_dosyasi))
    except Exception as e:
        log.error(f"Gönderim sırasında hata: {e}")
    finally:
        if ses_dosyasi and os.path.exists(ses_dosyasi):
            os.remove(ses_dosyasi)
            log.info(f"🗑️ Geçici ses dosyası silindi: {ses_dosyasi}")

    log.info("✅ Bot çalışması tamamlandı.")


if __name__ == "__main__":
    main()
