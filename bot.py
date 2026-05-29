from telegram import ChatPermissions
from telegram.ext import Application
import asyncio
from datetime import datetime, timedelta
import pytz
import os

TOKEN = os.getenv("TOKEN")

GRUPO_ID = -1003725549983

tz = pytz.timezone("Europe/Madrid")

# 🔥 TIEMPOS DE PRUEBA
ahora = datetime.now(tz)
hora_abrir = ahora + timedelta(minutes=6)
hora_cerrar = ahora + timedelta(minutes=11)

estado = None

def cerrado():
    ahora = datetime.now(tz)
    return not (hora_abrir <= ahora < hora_cerrar)

async def loop(app):
    global estado

    while True:
        try:
            nuevo_estado = "cerrado" if cerrado() else "abierto"

            if nuevo_estado != estado:
                estado = nuevo_estado

                if nuevo_estado == "cerrado":
                    await app.bot.set_chat_permissions(
                        GRUPO_ID,
                        ChatPermissions(can_send_messages=False)
                    )

                    await app.bot.send_message(
                        GRUPO_ID,
                        "🔴 TEST: grup tancat"
                    )

                else:
                    await app.bot.set_chat_permissions(
                        GRUPO_ID,
                        ChatPermissions(can_send_messages=True)
                    )

                    await app.bot.send_message(
                        GRUPO_ID,
                        "🟢 TEST: grup obert"
                    )

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(20)

async def post_init(app):
    asyncio.create_task(loop(app))

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()

    print("Bot en marcha (TEST MODE)")
    app.run_polling()

if __name__ == "__main__":
    main()
