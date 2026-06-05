import os
from datetime import datetime
import pytz
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

from telegram import ChatPermissions
from telegram.ext import Application

TOKEN = os.getenv("TOKEN")

GRUPO_ID = -1003725549983
TOPIC_ID = 17

HORA_INICIO = 8
HORA_FIN = 21

tz = pytz.timezone("Europe/Madrid")

estado = None
app = None


def es_cerrado():
    hora = datetime.now(tz).hour
    return hora < HORA_INICIO or hora >= HORA_FIN


async def enviar_estado(nuevo):
    global estado

    if nuevo == estado:
        return

    estado = nuevo

    if nuevo == "abierto":
        texto = "🟢 Grupo ABIERTO\n🕒 08:00 - 21:00"
        permisos = ChatPermissions(can_send_messages=True)
    else:
        texto = "🔴 Grupo CERRADO\n🕒 08:00 - 21:00"
        permisos = ChatPermissions(can_send_messages=False)

    await app.bot.set_chat_permissions(GRUPO_ID, permisos)
    await app.bot.send_message(chat_id=GRUPO_ID, text=texto)
    await app.bot.send_message(chat_id=GRUPO_ID, message_thread_id=TOPIC_ID, text=texto)


def start_http():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                import asyncio
                asyncio.run(enviar_estado("cerrado" if es_cerrado() else "abierto"))
            except Exception as e:
                print("ERROR HTTP CHECK:", e)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


async def start_bot():
    global app

    app = Application.builder().token(TOKEN).build()

    await app.initialize()
    await app.start()

    estado_inicial = "cerrado" if es_cerrado() else "abierto"
    await enviar_estado(estado_inicial)

    await asyncio.Event().wait()


def main():
    import asyncio

    threading.Thread(target=start_http, daemon=True).start()
    asyncio.run(start_bot())


if __name__ == "__main__":
    main()
