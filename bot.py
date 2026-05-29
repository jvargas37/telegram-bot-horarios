from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

async def detectar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat

    print("CHAT ID:", chat.id)
    print("CHAT TITLE:", chat.title)

    # solo responde si puede
    try:
        await update.message.reply_text(f"ID: {chat.id}")
    except:
        pass

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, detectar))

    print("Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()
