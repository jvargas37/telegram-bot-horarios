import os
import time
import requests
from datetime import datetime
import pytz
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TOKEN = os.getenv("TOKEN")

GRUPO_ID = -1003725549983
TOPIC_ID = 17

HORA_INICIO = 8
HORA_FIN = 21

tz = pytz.timezone("Europe/Madrid")

estado = None


def es_cerrado():
    hora = datetime.now(tz).hour
    return hora < HORA_INICIO or hora >= HORA_FIN


def tg(method, data):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    requests.post(url, data=data)


def enviar_estado(nuevo):
    global estado

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
        "permissions": str(permisos)
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


def loop():
    while True:
        try:
            nuevo = "cerrado" if es_cerrado() else "abierto"
            print("CHECK:", datetime.now(tz), estado, "->", nuevo)
            enviar_estado(nuevo)
        except Exception as e:
            print("ERROR:", e)

        time.sleep(60)


def start_http():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


def main():
    threading.Thread(target=start_http, daemon=True).start()
    threading.Thread(target=loop, daemon=True).start()

    while True:
        time.sleep(3600)


if __name__ == "__main__":
    main()
