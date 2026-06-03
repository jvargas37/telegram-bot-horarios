from telegram import ChatPermissions
from telegram.ext import Application, ContextTypes
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("TOKEN")
GRUPO_ID = -1003725549983
TOPIC_ID = 17

HORA_INICIO = 20
HORA_FIN = 21

tz = pytz.timezone("Europe/Madrid")

estado = None


def cerrado():
    hora = datetime.now(tz).hour
    return hora < HORA_INICIO or hora >= HORA_FIN


async def enviar_estado(app, nuevo):
    global estado
    estado = nuevo

    if nuevo == "abierto":
        texto = "🟢 El grup està obert\n🕒 Horari: 17:00 a 18:00"
        permisos = ChatPermissions(can_send_messages=True)
    else:
        texto = "🔴 El grup està tancat\n🕒 Horari: 17:00 a 18:00"
        permisos = ChatPermissions(can_send_messages=False)

    await app.bot.set_chat_permissions(GRUPO_ID, permisos)
    await app.bot.send_message(chat_id=GRUPO_ID, text=texto)
    await app.bot.send_message(chat_id=GRUPO_ID, message_thread_id=TOPIC_ID, text=texto)


async def job(context: ContextTypes.DEFAULT_TYPE):
    global estado

    nuevo = "cerrado" if cerrado() else "abierto"

    print("CHECK:", datetime.now(tz), estado, "->", nuevo)

    if nuevo != estado:
        await enviar_estado(context.application, nuevo)


async def post_init(app):
    global estado

    estado = "cerrado" if cerrado() else "abierto"
    await enviar_estado(app, estado)

    app.job_queue.run_repeating(job, interval=60, first=5)


def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.run_polling()


if __name__ == "__main__":
    main()
