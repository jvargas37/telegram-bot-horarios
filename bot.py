import os
import asyncio
from datetime import datetime
import pytz
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

from telegram import ChatPermissions
from telegram.ext import Application, ContextTypes

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


# ---------------- HTTP SERVER (OBLIGATORIO RENDER) ----------------
def start_http():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        def do_HEAD(self):
            self.send_response(200)
            self.end_headers()

    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


# ---------------- TELEGRAM ----------------
async def enviar_estado(app, nuevo):
    global estado
    estado = nuevo

    if nuevo == "abierto":
        texto = "🟢 Grupo abierto\n🕒 20:00 - 21:00"
        permisos = ChatPermissions(can_send_messages=True)
    else:
        texto = "🔴 Grupo cerrado\n🕒 20:00 - 21:00"
        permisos = ChatPermissions(can_send_messages=False)

    await app.bot.set_chat_permissions(GRUPO_ID, permisos)

    await app.bot.send_message(chat_id=GRUPO_ID, text=texto)

    await app.bot.send_message(
        chat_id=GRUPO_ID,
        message_thread_id=TOPIC_ID,
        text=texto
    )


# ---------------- LOOP PRINCIPAL ----------------
async def loop(app):
    global estado

    while True:
        nuevo = "cerrado" if cerrado() else "abierto"

        print("CHECK:", datetime.now(tz), estado, "->", nuevo)

        if nuevo != estado:
            print("CAMBIO:", estado, "->", nuevo)
            await enviar_estado(app, nuevo)

        await asyncio.sleep(60)


# ---------------- START ----------------
async def main():
    # HTTP obligatorio para Render
    threading.Thread(target=start_http, daemon=True).start()

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
