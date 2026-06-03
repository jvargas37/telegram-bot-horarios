from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import asyncio
import os
from telegram import ChatPermissions
from telegram.ext import Application
from datetime import datetime
import pytz

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


async def enviar_estado(app, nuevo):
    global estado
    estado = nuevo

    if nuevo == "abierto":
        texto = "🟢 El grup està obert\n🕒 Horari: 19:00 a 20:00"
        permisos = ChatPermissions(can_send_messages=True)
    else:
        texto = "🔴 El grup està tancat\n🕒 Horari: 19:00 a 20:00"
        permisos = ChatPermissions(can_send_messages=False)

    await app.bot.set_chat_permissions(GRUPO_ID, permisos)
    await app.bot.send_message(chat_id=GRUPO_ID, text=texto)
    await app.bot.send_message(chat_id=GRUPO_ID, message_thread_id=TOPIC_ID, text=texto)


async def loop(app):
    global estado

    while True:
        nuevo = "cerrado" if cerrado() else "abierto"

        if nuevo != estado:
            await enviar_estado(app, nuevo)

        await asyncio.sleep(60)


async def main():
    # 🔥 HTTP en thread (NO bloquea deploy)
    threading.Thread(target=web_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()

    await app.initialize()
    await app.start()

    global estado
    estado = "cerrado" if cerrado() else "abierto"
    await enviar_estado(app, estado)

    asyncio.create_task(loop(app))

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
