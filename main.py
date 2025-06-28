import os, random, asyncio, datetime
from telegram import Bot
from gtts import gTTS
import word_data

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
bot = Bot(token=TOKEN)

async def send_words():
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
            await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")
            tts = gTTS(' '.join(list(w['word'].upper())))
            tts.save("audio.mp3")
            with open("audio.mp3", "rb") as audio:
                await bot.send_audio(chat_id=CHAT_ID, audio=audio)
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(send_words())
