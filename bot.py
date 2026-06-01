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


async def loop(app):
    global estado

    while True:
        try:
            nuevo = "cerrado" if cerrado() else "abierto"

            if nuevo != estado:
                estado = nuevo

                if nuevo == "abierto":
                    await app.bot.set_chat_permissions(
                        GRUPO_ID,
                        ChatPermissions(can_send_messages=True)
                    )
                    await app.bot.send_message(GRUPO_ID, "🟢 El grup està obert\n🕒 08:00-21:00")

                else:
                    await app.bot.set_chat_permissions(
                        GRUPO_ID,
                        ChatPermissions(can_send_messages=False)
                    )
                    await app.bot.send_message(GRUPO_ID, "🔴 El grup està tancat\n🕒 08:00-21:00")

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(60)


# 🔥 SERVIDOR WEB REAL PARA RENDER
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot OK")


def start_server():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    server.serve_forever()


def main():
    app = Application.builder().token(TOKEN).build()

    print("Bot en marcha")

    # servidor web en hilo separado
    threading.Thread(target=start_server, daemon=True).start()

    # loop del bot
    asyncio.get_event_loop().create_task(loop(app))

    app.run_polling()


if __name__ == "__main__":
    main()
