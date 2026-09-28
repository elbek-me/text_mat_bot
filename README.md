# Daftar • Ovoz • Tarjima — Telegram bot

Telegram bot (aiogram 3) uchta imkoniyat bilan:

1. **📝 Matn yuborish** — matn yo'l-yo'l chiziqli yoki katakli daftarga qo'lda yozilgandek rasmga aylanadi.
2. **🔊 Matnni ovozga aylantirish** — qiz bola, o'g'il bola, yo'g'on va hind ovozi.
3. **🌐 Tarjima qilish** — avval matn, keyin til tanlanadi.

## Tuzilma

```
app/
├── main.py            # kirish nuqtasi
├── config.py          # sozlamalar (.env)
├── logger.py          # konsol + aylanuvchi log fayl
├── texts.py           # barcha foydalanuvchi matnlari
├── keyboards.py       # tugmalar va typed CallbackData
├── states.py          # FSM holatlari
├── utils.py
├── handlers/          # menu, handwriting, tts, translate, fallback, errors
├── services/          # handwriting (Pillow), tts (edge-tts), translator
└── middlewares/       # throttling (spamdan himoya)
tests/                 # pytest
```

Handlerlar faqat Telegram bilan ishlaydi, mantiq `services/` da — shuning uchun uni alohida test qilish oson.

## Ishga tushirish

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # BOT_TOKEN ni yozing
python -m app.main
```

### Docker

```bash
docker build -t notebook-bot .
docker run -d --name notebook-bot --restart unless-stopped --env-file .env notebook-bot
```

### Testlar

```bash
pip install -r requirements-dev.txt
pytest
```

## Sozlamalar (`.env`)

| O'zgaruvchi | Standart | Izoh |
|---|---|---|
| `BOT_TOKEN` | — | @BotFather tokeni (majburiy) |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING` |
| `MAX_HANDWRITING_CHARS` | `6000` | daftar uchun matn limiti |
| `MAX_TTS_CHARS` | `2000` | ovoz uchun matn limiti |
| `MAX_TRANSLATE_CHARS` | `4000` | tarjima uchun matn limiti |
| `MAX_PAGES` | `10` | ko'pi bilan nechta sahifa yuboriladi |
| `THROTTLE_SECONDS` | `1.0` | so'rovlar orasidagi minimal vaqt |
| `FONT_PATH` | `assets/fonts/handwriting.ttf` | qo'lyozma shrifti |

## Kengaytirish

- **Yangi ovoz**: `app/services/tts.py` dagi `VOICES` ga `Voice(...)` qo'shing (`edge-tts --list-voices` bilan ovozlar ro'yxatini ko'ring).
- **Yangi til**: `app/services/translator.py` dagi `LANGUAGES` ga qo'shing.
- **Daftar dizayni**: `PageLayout` (rang, o'lcham, qator balandligi) va `NotebookStyle`.
- **Holatni saqlash**: bot qayta ishga tushganda FSM holatlari yo'qolmasligi uchun `main.py` da `MemoryStorage` o'rniga `RedisStorage` ishlating.

## Eslatmalar

- Ovoz (edge-tts) va tarjima (Google Translate) internet talab qiladi va norasmiy xizmatlar hisoblanadi; katta yuklamali production uchun rasmiy API (Azure TTS, Google Cloud Translation) ga o'tish tavsiya etiladi.
- Shrift: Caveat (SIL OFL 1.1). Litsenziya `assets/fonts/OFL.txt` da.
