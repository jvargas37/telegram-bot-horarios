from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta
import pytz
import os

TOKEN = os.getenv("TOKEN")

GRUPOS_OBJETIVO = [
    -1003725549983
]

tz = pytz.timezone("Europe/Madrid")

# 🔥 HORARIOS DE PRUEBA
hora_inicio = (datetime.now(tz) + timedelta(minutes=5)).hour
minuto_inicio = (datetime.now(tz) + timedelta(minutes=5)).minute

hora_fin = (datetime.now(tz) + timedelta(minutes=6)).hour
minuto_fin = (datetime.now(tz) + timedelta(minutes=6)).minute

estado = None

def cerrado():
    ahora = datetime.now(tz)
    actual = (ahora.hour, ahora.minute)

    inicio = (hora_inicio, minuto_inicio)
    fin = (hora_fin, minuto_fin)

    return not (inicio <= actual < fin)

async def controlar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global estado
    chat = update.effective_chat

    if chat.id not in GRUPOS_OBJETIVO:
        return

    nuevo = "cerrado" if cerrado() else "abierto"

    if nuevo == estado:
        return

    estado = nuevo

    try:
        if nuevo == "cerrado":
            await chat.set_permissions(
                ChatPermissions(can_send_messages=False)
            )

            await update.message.reply_text(
                "🔴 El grup està tancat (TEST)"
            )

        else:
            await chat.set_permissions(
                ChatPermissions(can_send_messages=True)
            )

            await update.message.reply_text(
                "🟢 El grup està obert (TEST)"
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
