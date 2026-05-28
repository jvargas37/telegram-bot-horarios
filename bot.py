from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("TOKEN")

HORA_INICIO = 8
HORA_FIN = 20

def es_cerrado():
    hora = datetime.now(pytz.timezone("Europe/Madrid")).hour
    return hora < HORA_INICIO or hora >= HORA_FIN

async def controlar_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat

    try:
        if es_cerrado():
            # 🔴 BLOQUEO TOTAL
            await chat.set_permissions(
                ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False
                )
            )
        else:
            # 🟢 ABRIR GRUPO
            await chat.set_permissions(
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )

    except Exception as e:
        print("ERROR:", e)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, controlar_grupo))

    print("Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()
