from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("TOKEN")

HORA_INICIO = 8
HORA_FIN = 20

def cerrado():
    hora = datetime.now(pytz.timezone("Europe/Madrid")).hour
    return hora < HORA_INICIO or hora >= HORA_FIN

async def controlar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat

    try:
        if cerrado():
            await chat.set_permissions(
                ChatPermissions(can_send_messages=False)
            )
        else:
            await chat.set_permissions(
                ChatPermissions(can_send_messages=True)
            )

    except Exception as e:
        print("ERROR:", e)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, controlar))

    print("Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()
