from telegram import ChatPermissions
from telegram.ext import Application
import asyncio
from datetime import datetime
import pytz
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TOKEN = os.getenv("TOKEN")
GRUPO_ID = -1003725549983
TOPIC_ID = 17

HORA_INICIO = 8
HORA_FIN = 21

tz = pytz.timezone("Europe/Madrid")

estado = None


def cerrado():
    hora = datetime.now(tz).hour
    return hora < HORA_INICIO or hora >= HORA_FIN


async def enviar_estado(app, nuevo):
    if nuevo == "abierto":
        texto = "🟢 El grup està obert\n🕒 Horari: 08:00 a 21:00"

        await app.bot.set_chat_permissions(
            GRUPO_ID,
            ChatPermissions(can_send_messages=True)
        )

        await app.bot.send_message(
            chat_id=GRUPO_ID,
            text=texto
        )

        await app.bot.send_message(
            chat_id=GRUPO_ID,
            message_thread_id=TOPIC_ID,
            text=texto
        )

    else:
        texto = "🔴 El grup està tancat\n🕒 Horari: 08:00 a 21:00"

        await app.bot.set_chat_permissions(
            GRUPO_ID,
            ChatPermissions(can_send_messages=False)
        )

        await app.bot.send_message(
            chat_id=GRUPO_ID,
            text=texto
        )

        await app.bot.send_message(
            chat_id=GRUPO_ID,
            message_thread_id=TOPIC_ID,
            text=texto
        )


async def loop(app):
    global estado

    while True:
        try:
            print("LOOP:", datetime.now(tz))

            nuevo = "cerrado" if cerrado() else "abierto"

            if nuevo != estado:
                print("CAMBIO:", estado, "->", nuevo)
                estado = nuevo
                await enviar_estado(app, nuevo)

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(60)


def web_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        def do_HEAD(self):
            self.send_response(200)
            self.end_headers()

    server = HTTPServer(("0.0.0.0", 10000), Handler)
    server.serve_forever()


async def main_async():
    app = Application.builder().token(TOKEN).build()

    threading.Thread(target=web_server, daemon=True).start()

    global estado
    estado = "cerrado" if cerrado() else "abierto"

    await app.initialize()
    await app.start()

    await enviar_estado(app, estado)

    asyncio.create_task(loop(app))

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main_async())

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main_async())
