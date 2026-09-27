import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from solver import find_words

TOKEN = os.getenv("BOT_TOKEN")
user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {}
    await update.message.reply_text(
        "🤖 أهلاً بك في Binance WOTD Solver\n\n"
        "أرسل كلمة التخمين التي لعبتها.\n\n"
        "مثال: TRADE"
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip().lower()

    if user_id not in user_data:
        user_data[user_id] = {}

    if "guess" not in user_data[user_id]:
        user_data[user_id]["guess"] = text
        await update.message.reply_text(
            "✅ تم تسجيل التخمين:\n\n"
            f"🔤 {text.upper()}\n\n"
            "الآن أرسل نتيجة الحروف باستخدام:\n\n"
            "🟩 = صحيح وفي مكانه\n"
            "🟨 = موجود لكن في مكان آخر\n"
            "⬛ = غير موجود\n\n"
            "مثال: 🟩⬛🟨⬛🟩"
        )
        return

    guess = user_data[user_id]["guess"]
    result = text

    if len(result) != len(guess):
        await update.message.reply_text(
            f"❌ عدد الألوان لا يطابق عدد الحروف.\n\n"
            f"الكلمة تحتوي على {len(guess)} حروف."
        )
        return

    with open("words.txt", "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    results = find_words(guess, result, words)

    if not results:
        await update.message.reply_text(
            "❌ لم أجد كلمات مطابقة للنتيجة.\n\n"
            "تأكد من الحروف والألوان."
        )
    else:
        message = "🎯 الكلمات المحتملة:\n\n"
        for i, word in enumerate(results[:10], 1):
            message += f"{i}️⃣ {word.upper()}\n"
        message += f"\n📊 عدد الاحتمالات: {len(results)}"
        await update.message.reply_text(message)

    user_data[user_id] = {}


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN غير موجود")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
