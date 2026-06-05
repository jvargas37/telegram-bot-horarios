import os
from datetime import datetime
import pytz
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

TOKEN = os.getenv("TOKEN")

GRUPO_ID = -1003725549983
TOPIC_ID = 17

HORA_INICIO = 13
HORA_FIN = 14

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

    texto = "🟢 ABIERTO" if nuevo == "abierto" else "🔴 CERRADO"

    tg("setChatPermissions", {
        "chat_id": GRUPO_ID,
        "permissions": str({"can_send_messages": nuevo == "abierto"})
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
        self.send_response(200)
        self.end_headers()


def main():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
