from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("TOKEN")

HORA_INICIO = 8
HORA_FIN = 21

GRUPOS_OBJETIVO = [
    -1003725549983
]

def cerrado():
    hora = datetime.now(pytz.timezone("Europe/Madrid")).hour
    return hora < HORA_INICIO or hora >= HORA_FIN

async def controlar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat

    if chat.id not in GRUPOS_OBJETIVO:
        return

    try:
        if cerrado():
            await chat.set_permissions(
                ChatPermissions(can_send_messages=False)
            )

            await update.message.reply_text(
                "🔴 El grup està tancat\n"
                "🕒 Horari: 08:00 a 21:00"
            )

        else:
            await chat.set_permissions(
                ChatPermissions(can_send_messages=True)
            )

            await update.message.reply_text(
                "🟢 El grup està obert\n"
                "🕒 Horari: 08:00 a 21:00"
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
