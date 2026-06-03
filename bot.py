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

HORA_INICIO = 13
HORA_FIN = 14

tz = pytz.timezone("Europe/Madrid")

estado = None


def cerrado():
    hora = datetime.now(tz).hour
    return hora < HORA_INICIO or hora >= HORA_FIN


async def enviar_estado(app, nuevo):

    texto = "🟢 El grup està obert\n🕒 Horari: 08:00 a 21:00" if nuevo == "abierto" else "🔴 El grup està tancat\n🕒 Horari: 08:00 a 21:00"

    permisos = ChatPermissions(can_send_messages=(nuevo == "abierto"))

    await app.bot.set_chat_permissions(GRUPO_ID, permisos)

    await app.bot.send_message(chat_id=GRUPO_ID, text=texto)
    await app.bot.send_message(chat_id=GRUPO_ID, message_thread_id=TOPIC_ID, text=texto)


def web_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        def do_HEAD(self):
            self.send_response(200)
            self.end_headers()

    HTTPServer(("0.0.0.0", 10000), Handler).serve_forever()


async def loop(app):
    global estado

    while True:
        nuevo = "cerrado" if cerrado() else "abierto"

        if nuevo != estado:
            estado = nuevo
            await enviar_estado(app, nuevo)

        await asyncio.sleep(60)


async def main():
    app = Application.builder().token(TOKEN).build()

    threading.Thread(target=web_server, daemon=True).start()

    await app.initialize()
    await app.start()

    global estado
    estado = "cerrado" if cerrado() else "abierto"
    await enviar_estado(app, estado)

    async def runner():
        await loop(app)

    asyncio.create_task(runner())

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
