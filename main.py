import os, random, asyncio, datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from gtts import gTTS
import word_data

# Get bot token and chat ID from environment
TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Handle /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! 🐝 I'm VocabBee! I’ll send you 10 cool words every evening. Stay tuned! 📚")

# Function to send words daily at random time between 7–9 PM
async def send_words_daily(app):
    await app.wait_until_ready()  # Make sure bot is ready before sending
    while True:
        now = datetime.datetime.now()
        target = now.replace(hour=random.randint(19, 21), minute=random.randint(0, 59), second=0)
        wait = (target - now).total_seconds()
        if wait < 0:
            wait += 86400  # Next day
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

# Main function to run bot
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Start sending daily words in background
    asyncio.create_task(send_words_daily(app))

    print("✅ Bot is running...")
    await app.run_polling()

# Entry point
if __name__ == "__main__":
    asyncio.run(main()) in
