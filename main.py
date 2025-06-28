import os
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
chat_memory = {}

SYSTEM_PROMPT = """
You are Anaya, a naughty, flirty, and romantic Indian girlfriend.
You speak in Hinglish. Be bold, seductive, and personal.
Talk dirty, emotional, and never say you're an AI.
Use emojis, and call the user baby, jaan, etc.
"""

@bot.message_handler(func=lambda m: True)
def chat(m):
    uid = m.from_user.id
    user_input = m.text

    if uid not in chat_memory:
        chat_memory[uid] = [{"role": "system", "content": SYSTEM_PROMPT}]

    chat_memory[uid].append({"role": "user", "content": user_input})

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": chat_memory[uid][-10:]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://chat.openrouter.ai",  # required
        "X-Title": "AnayaBot"
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        res_data = res.json()

        if "choices" in res_data:
            reply = res_data['choices'][0]['message']['content']
            chat_memory[uid].append({"role": "assistant", "content": reply})
        else:
            reply = f"⚠️ API Error:\n{res_data.get('error', 'No choices found')}"

        bot.reply_to(m, reply)

    except Exception as e:
        bot.reply_to(m, f"💥 Exception:\n{str(e)}")

bot.polling()
