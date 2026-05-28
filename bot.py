from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("TOKEN")

HORA_INICIO = 8
HORA_FIN = 20

estado_actual = None  # None / "abierto" / "cerrado"

def es_fuera_de_horario():
    hora = datetime.now(pytz.timezone("Europe/Madrid")).hour
    return hora < HORA_INICIO or hora >= HORA_FIN

async def controlar_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global estado_actual
    chat = update.effective_chat

    fuera = es_fuera_de_horario()

    # Estado deseado
    nuevo_estado = "cerrado" if fuera else "abierto"

    # 🔥 SOLO ACTUAR SI CAMBIA EL ESTADO
    if nuevo_estado == estado_actual:
        return

    estado_actual = nuevo_estado

    try:
        if fuera:
            # 🔴 CERRAR GRUPO
            await chat.set_permissions(
                ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                )
            )

            await update.message.reply_text(
                "⛔ GRUPO CERRADO\n"
                f"🕒 Horario activo: {HORA_INICIO}:00 - {HORA_FIN}:00\n"
                "📵 Ahora no se pueden enviar mensajes."
            )

        else:
            # 🟢 ABRIR GRUPO
            await chat.set_permissions(
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                )
            )

            await update.message.reply_text(
                "🟢 GRUPO ABIERTO\n"
                f"🕒 Horario activo: {HORA_INICIO}:00 - {HORA_FIN}:00"
            )

    except Exception as e:
        print("ERROR:", e)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.ALL, controlar_grupo)
    )

    print("Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()
