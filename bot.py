from telegram import ChatPermissions
from telegram.ext import Application
from datetime import datetime
import pytz
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time

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


def enviar_estado(app, nuevo):

    print("CAMBIO:", estado, "->", nuevo, datetime.now(tz))

    if nuevo == "abierto":
        texto = "🟢 El grup està obert\n🕒 Horari: 08:00 a 21:00"
        permisos = ChatPermissions(can_send_messages=True)
    else:
        texto = "🔴 El grup està tancat\n🕒 Horari: 08:00 a 21:00"
        permisos = ChatPermissions(can_send_messages=False)

    app.bot.set_chat_permissions(GRUPO_ID, permisos)
    app.bot.send_message(chat_id=GRUPO_ID, text=texto)
    app.bot.send_message(chat_id=GRUPO_ID, message_thread_id=TOPIC_ID, text=texto)


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


def loop(app):
    global estado

    while True:
        nuevo = "cerrado" if cerrado() else "abierto"

        print("CHECK:", datetime.now(tz), estado, "->", nuevo)

        if nuevo != estado:
            estado = nuevo
            enviar_estado(app, nuevo)

        time.sleep(60)


def main():
    global estado

    app = Application.builder().token(TOKEN).build()

    threading.Thread(target=web_server, daemon=True).start()

    estado = "cerrado" if cerrado() else "abierto"
    enviar_estado(app, estado)

    loop(app)


if __name__ == "__main__":
    main()
