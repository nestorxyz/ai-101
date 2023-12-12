import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv
import openai

load_dotenv()

tg_bot_token = os.environ["TG_BOT_TOKEN"]
openai.api_key = os.environ["OPENAI_API_KEY"]


messages = [
    {
        "role": "system",
        "content": "You are a WhatsApp assistant that help users to track their expenses.",
    }
]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages.append({"role": "user", "content": update.message.text})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    completion_answer = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": completion_answer})

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=completion_answer
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(tg_bot_token).build()

    start_handler = CommandHandler("start", start)
    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)

    application.add_handler(start_handler)
    application.add_handler(chat_handler)

    application.run_polling()
