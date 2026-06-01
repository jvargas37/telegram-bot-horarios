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

HORA_INICIO = 8
HORA_FIN = 21

tz = pytz.timezone("Europe/Madrid")

estado = None


def cerrado():
    hora = datetime.now(tz).hour
    return hora < HORA_INICIO or hora >= HORA_FIN


async def enviar_estado(app, nuevo):
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


async def loop(app):
    global estado

    while True:
        try:
            nuevo = "cerrado" if cerrado() else "abierto"

            if nuevo != estado:
                estado = nuevo
                await enviar_estado(app, nuevo)

        except Exception as e:
            print(e)

        await asyncio.sleep(60)


def web_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    server = HTTPServer(("0.0.0.0", 10000), Handler)
    server.serve_forever()


async def main_async():
    app = Application.builder().token(TOKEN).build()

    threading.Thread(target=web_server, daemon=True).start()

    estado_inicial = "cerrado" if cerrado() else "abierto"
    global estado
    estado = estado_inicial
    await enviar_estado(app, estado_inicial)

    asyncio.create_task(loop(app))

    await app.initialize()
    await app.start()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main_async())
