from telegram import ChatPermissions
from telegram.ext import Application
import asyncio
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("TOKEN")

GRUPO_ID = -1003725549983

HORA_INICIO = 8
HORA_FIN = 21

tz = pytz.timezone("Europe/Madrid")

estado = None


def cerrado():
    hora = datetime.now(tz).hour
    return hora < HORA_INICIO or hora >= HORA_FIN


async def loop(app):
    global estado

    while True:
        try:
            nuevo = "cerrado" if cerrado() else "abierto"

            if nuevo != estado:
                estado = nuevo

                if nuevo == "abierto":
                    await app.bot.set_chat_permissions(
                        GRUPO_ID,
                        ChatPermissions(can_send_messages=True)
                    )

                    await app.bot.send_message(
                        GRUPO_ID,
                        "🟢 El grup està obert\n🕒 Horari: 08:00 a 21:00"
                    )

                else:
                    await app.bot.set_chat_permissions(
                        GRUPO_ID,
                        ChatPermissions(can_send_messages=False)
                    )

                    await app.bot.send_message(
                        GRUPO_ID,
                        "🔴 El grup està tancat\n🕒 Horari: 08:00 a 21:00"
                    )

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(60)


def main():
    app = Application.builder().token(TOKEN).build()

    print("Bot en marcha (PRODUCCIÓN)")

    # IMPORTANTE: arrancar loop SIN tocar run_polling internamente
    async def runner():
        asyncio.create_task(loop(app))
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        await asyncio.Event().wait()  # mantener vivo

    asyncio.run(runner())


if __name__ == "__main__":
    main()
