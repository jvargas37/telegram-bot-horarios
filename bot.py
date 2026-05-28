from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("TOKEN")

HORA_INICIO = 8
HORA_FIN = 20

estado_actual = None

def es_cerrado():
    hora = datetime.now(pytz.timezone("Europe/Madrid")).hour
    return hora < HORA_INICIO or hora >= HORA_FIN

async def controlar_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global estado_actual
    chat = update.effective_chat

    cerrado = es_cerrado()

    nuevo_estado = "cerrado" if cerrado else "abierto"

    # 🔥 solo actúa si cambia el estado
    if nuevo_estado == estado_actual:
        return

    estado_actual = nuevo_estado

    try:
        if cerrado:
            # 🔴 CERRAR GRUPO
            await chat.set_permissions(
                ChatPermissions(
                    can_send_messages=False
                )
            )

            await update.message.reply_text(
                "⛔ GRUPO CERRADO\n"
                "🕒 Horario: 08:00 - 20:00"
            )

        else:
            # 🟢 ABRIR GRUPO
            await chat.set_permissions(
                ChatPermissions(
                    can_send_messages=True
                )
            )

            await update.message.reply_text(
                "🟢 GRUPO ABIERTO\n"
                "🕒 Horario: 08:00 - 20:00"
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
