from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("TOKEN")

HORA_INICIO = 8
HORA_FIN = 20

def es_fuera_de_horario():
    hora = datetime.now(pytz.timezone("Europe/Madrid")).hour
    return hora < HORA_INICIO or hora >= HORA_FIN

async def controlar_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat

    try:
        if es_fuera_de_horario():
            # 🔴 BLOQUEAR ESCRITURA
            await chat.set_permissions(
                ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                    can_send_audios=False,
                    can_send_documents=False,
                    can_send_photos=False,
                    can_send_videos=False,
                    can_send_video_notes=False,
                    can_send_voice_notes=False,
                )
            )

            await update.message.reply_text(
                "⛔ Grupo cerrado fuera de horario.\n"
                f"🕒 Disponible de {HORA_INICIO}:00 a {HORA_FIN}:00"
            )

        else:
            # 🟢 ABRIR CHAT
            await chat.set_permissions(
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_audios=True,
                    can_send_documents=True,
                    can_send_photos=True,
                    can_send_videos=True,
                    can_send_video_notes=True,
                    can_send_voice_notes=True,
                )
            )

    except Exception as e:
        print("ERROR:", e)

def main():
    app = Application.builder().token(TOKEN).build()

    # Se ejecuta con cualquier mensaje
    app.add_handler(
        MessageHandler(filters.ALL, controlar_grupo)
    )

    print("Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()
