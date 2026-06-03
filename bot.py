from telegram import ChatPermissions
from telegram.ext import Application, ContextTypes
from datetime import datetime
import pytz
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TOKEN = os.getenv("TOKEN")
GRUPO_ID = -1003725549983
TOPIC_ID = 17

HORA_INICIO = 19
HORA_FIN = 20

tz = pytz.timezone("Europe/Madrid")

estado = None


def cerrado():
    hora = datetime.now(tz).hour
    return hora < HORA_INICIO or hora >= HORA_FIN


async def enviar_estado(app, nuevo):

    global estado
    estado = nuevo

    if nuevo == "abierto":
        texto = "🟢 El grup està obert\n🕒 Horari: 08:00 a 21:00"
        permisos = ChatPermissions(can_send_messages=True)
    else:
        texto = "🔴 El grup està tancat\n🕒 Horari: 08:00 a 21:00"
        permisos = ChatPermissions(can_send_messages=False)

    await app.bot.set_chat_permissions(GRUPO_ID, permisos)
    await app.bot.send_message(chat_id=GRUPO_ID, text=texto)
    await app.bot.send_message(chat_id=GRUPO_ID, message_thread_id=TOPIC_ID, text=texto)


async def check(app):
    global estado

    while True:
        nuevo = "cerrado" if cerrado() else "abierto"

        print("CHECK:", datetime.now(tz), estado, "->", nuevo)

        if nuevo != estado:
            await enviar_estado(app, nuevo)

        await asyncio.sleep(60)


def web_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    HTTPServer(("0.0.0.0", 10000), Handler).serve_forever()


async def post_init(app):
    global estado

    estado = "cerrado" if cerrado() else "abierto"
    await enviar_estado(app, estado)

    import asyncio
    asyncio.create_task(check(app))


def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()

    threading.Thread(target=web_server, daemon=True).start()

    app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path=TOKEN
    )


if __name__ == "__main__":
    main()
