from telegram import ChatPermissions
from telegram.ext import Application
from datetime import datetime
import pytz
import os
import asyncio

TOKEN = os.getenv("TOKEN")

HORA_INICIO = 8
HORA_FIN = 20

estado = None

def cerrado():
    hora = datetime.now(pytz.timezone("Europe/Madrid")).hour
    return hora < HORA_INICIO or hora >= HORA_FIN

async def controlar(app: Application):
    global estado

    while True:
        chat_id = None

        # intenta obtener chats activos desde updates (simple enfoque)
        for update in app.bot.get_updates(limit=1):
            chat_id = update.message.chat_id if update.message else None

        if chat_id:
            try:
                if cerrado() and estado != "cerrado":
                    await app.bot.set_chat_permissions(
                        chat_id,
                        ChatPermissions(can_send_messages=False)
                    )
                    estado = "cerrado"

                elif not cerrado() and estado != "abierto":
                    await app.bot.set_chat_permissions(
                        chat_id,
                        ChatPermissions(can_send_messages=True)
                    )
                    estado = "abierto"

            except Exception as e:
                print(e)

        await asyncio.sleep(60)

async def post_init(app: Application):
    asyncio.create_task(controlar(app))

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    print("Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()
