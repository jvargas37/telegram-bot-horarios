from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("TOKEN")

HORA_INICIO = 8
HORA_FIN = 20

async def controlar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("MENSAJE RECIBIDO:", update.message.text)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, controlar_mensajes)
    )

    print("Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()
