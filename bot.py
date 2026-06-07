import os
from datetime import datetime
import pytz
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

TOKEN = os.getenv("TOKEN")

GRUPO_ID = -1003725549983
TOPIC_ID = 17

HORA_INICIO = 8
HORA_FIN = 21

tz = pytz.timezone("Europe/Madrid")

estado = None


def es_cerrado():
    return not (HORA_INICIO <= datetime.now(tz).hour < HORA_FIN)


def tg(method, data):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/{method}", data=data)


def check():
    global estado

    nuevo = "cerrado" if es_cerrado() else "abierto"

    if nuevo == estado:
        return

    estado = nuevo

    if nuevo == "abierto":
        texto = "🟢 Grupo ABIERTO\n🕒 08:00 - 21:00"
        permisos = {"can_send_messages": True}
    else:
        texto = "🔴 Grupo CERRADO\n🕒 08:00 - 21:00"
        permisos = {"can_send_messages": False}

    tg("setChatPermissions", {
        "chat_id": GRUPO_ID,
        "permissions": str(permisos).replace("'", '"')
    })

    tg("sendMessage", {
        "chat_id": GRUPO_ID,
        "text": texto
    })

    tg("sendMessage", {
        "chat_id": GRUPO_ID,
        "message_thread_id": TOPIC_ID,
        "text": texto
    })


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        check()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_HEAD(self):
        check()
        self.send_response(200)
        self.end_headers()


def main():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port)).serve_forever()


if __name__ == "__main__":
    main()
