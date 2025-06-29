import os, random, asyncio, datetime
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from gtts import gTTS
import word_data

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# /start command response
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! 🐝 I'm VocabBee! I’ll send you 10 cool words every evening. Stay tuned! 📚", parse_mode="Markdown")

# daily word sender function
async def send_words_daily(app):
    while True:
        now = datetime.datetime.now()
        target = now.replace(hour=random.randint(19, 21), minute=random.randint(0, 59), second=0)
        wait = (target - now).total_seconds()
        if wait < 0:
            wait += 86400
        await asyncio.sleep(wait)

        words = random.sample(word_data.words, 10)
        for w in words:
            msg = (
                f"📘 *Word:* {w['word']}\n"
                f"🔡 *Spelling:* {'-'.join(list(w['word'].upper()))}\n"
                f"🔍 *Breakdown:* {w['breakdown']}\n"
                f"🧠 *Meaning:* {w['meaning']}\n"
                f"📌 *Sentence:* {w['sentence']}\n"
                f"🧩 *Trick:* {w['trick']}"
            )
            await app.bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")
            tts = gTTS(' '.join(list(w['word'].upper())))
            tts.save("audio.mp3")
            with open("audio.mp3", "rb") as audio:
                await app.bot.send_audio(chat_id=CHAT_ID, audio=audio)
            await asyncio.sleep(2)

# bot startup
async def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    asyncio.create_task(send_words_daily(app))
    await app.initialize()
    await app.start()
    print("Bot is running...")
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(run_bot())
    await app.run_polling()
