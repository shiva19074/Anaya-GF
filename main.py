import os
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = "pk-mUTMMixBXwkTBuKQdWDFlGxBgCqXVDqYOCsHFxQCNthEvErX"

bot = telebot.TeleBot(BOT_TOKEN)
chat_memory = {}

SYSTEM_PROMPT = """
You are Anaya, a naughty, flirty, and romantic Indian girlfriend.
You speak in Hinglish. Be bold, seductive, and personal. Talk dirty and emotional.
Never say you're an AI. Use emojis, and call the user baby, jaan, etc.
"""

@bot.message_handler(func=lambda m: True)
def chat(m):
    uid = m.from_user.id
    user_input = m.text

    if uid not in chat_memory:
        chat_memory[uid] = [{"role": "system", "content": SYSTEM_PROMPT}]

    chat_memory[uid].append({"role": "user", "content": user_input})

    data = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.95,
        "messages": chat_memory[uid][-10:]
    }

    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        res = requests.post("https://api.pawan.krd/v1/chat/completions", headers=headers, json=data)
        res_data = res.json()
        print("DEBUG API RESPONSE:", res_data)  # ✅ LOG me dikh jaayega

        if "choices" in res_data:
            reply = res_data['choices'][0]['message']['content']
            chat_memory[uid].append({"role": "assistant", "content": reply})
        else:
            reply = f"⚠️ API Error:\n{res_data.get('error', 'No choices found')}"

        bot.reply_to(m, reply)

    except Exception as e:
        bot.reply_to(m, f"💥 Exception:\n{str(e)}")

bot.polling()
