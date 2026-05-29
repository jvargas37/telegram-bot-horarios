from telegram import ChatPermissions
from telegram.ext import Application, ContextTypes
from datetime import datetime
import pytz
import os
import asyncio

TOKEN = os.getenv("TOKEN")

HORA_INICIO = 8
HORA_FIN = 21

estado = None

def cerrado():
    hora = datetime.now(pytz.timezone("Europe/Madrid")).hour
    return hora < HORA_INICIO or hora >= HORA_FIN

async def controlar(app):
    global estado

    while True:
        try:
            nuevo = "cerrado" if cerrado() else "abierto"

            if nuevo != estado:
                estado = nuevo

                chat_id = YOUR_CHAT_ID  # <- luego lo ponemos fijo

                if cerrado():
                    await app.bot.set_chat_permissions(
                        chat_id,
                        ChatPermissions(can_send_messages=False)
                    )
                    await app.bot.send_message(chat_id, "🔴 El grup està tancat")

                else:
                    await app.bot.set_chat_permissions(
                        chat_id,
                        ChatPermissions(can_send_messages=True)
                    )
                    await app.bot.send_message(chat_id, "🟢 El grup està obert")

        except Exception as e:
            print(e)

        await asyncio.sleep(60)

async def post_init(app):
    asyncio.create_task(controlar(app))

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.run_polling()

if __name__ == "__main__":
    main()
