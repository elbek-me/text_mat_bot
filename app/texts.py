"""Foydalanuvchiga ko'rsatiladigan barcha matnlar bir joyda."""

BTN_HANDWRITING = "📝 Matn yuborish"
BTN_TTS = "🔊 Matnni ovozga aylantirish"
BTN_TRANSLATE = "🌐 Tarjima qilish"

WELCOME = (
    "Assalomu alaykum, <b>{name}</b>! 👋\n\n"
    "Men matnni daftarga yozib beraman, ovozga aylantiraman va tarjima qilaman.\n"
    "Kerakli bo'limni tanlang 👇"
)
HELP = (
    "<b>Imkoniyatlar:</b>\n"
    f"{BTN_HANDWRITING} — matn qo'lda daftarga yozilgandek rasmga aylanadi\n"
    f"{BTN_TTS} — matn tanlangan ovozda o'qiladi\n"
    f"{BTN_TRANSLATE} — matn boshqa tilga tarjima qilinadi\n\n"
    "/start — bosh menyu\n"
    "/cancel — joriy amalni bekor qilish"
)
CANCELLED = "Bekor qilindi. Bosh menyu 👇"
USE_MENU = "Iltimos, quyidagi menyudan bo'lim tanlang 👇"

# Daftar
CHOOSE_NOTEBOOK = "Qaysi daftarga yozay?"
NOTEBOOK_SELECTED = "{title} tanlandi.\nEndi matnni yuboring ✍️"
HANDWRITING_MORE = "Yana matn yuborishingiz mumkin yoki menyudan boshqa bo'lim tanlang."
HANDWRITING_TRUNCATED = "⚠️ Matn uzun bo'lgani uchun faqat dastlabki {pages} sahifa yuborildi."

# Ovoz
CHOOSE_VOICE = "Qaysi ovozda o'qib beray?"
VOICE_SELECTED = "{title} tanlandi.\nEndi matnni yuboring ✍️"

# Tarjima
ASK_TRANSLATE_TEXT = "Tarjima qilinadigan matnni yuboring ✍️"
CHOOSE_LANGUAGE = "Qaysi tilga tarjima qilay?"
TRANSLATING = "Tarjima qilinmoqda..."
SEND_TEXT_FIRST = "Avval tarjima uchun matn yuboring."

# Umumiy xatolar
SEND_TEXT_ONLY = "Iltimos, matn yuboring (rasm yoki fayl emas)."
EMPTY_TEXT = "Matn bo'sh. Iltimos, matn yuboring."
TEXT_TOO_LONG = "Matn juda uzun: {length} belgi. Maksimum — {limit} belgi."
INVALID_CHOICE = "Noto'g'ri tanlov. Qaytadan urinib ko'ring."
SLOW_DOWN = "Iltimos, biroz sekinroq ⏳"
UNEXPECTED_ERROR = "Kutilmagan xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."
