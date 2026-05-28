from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import datetime

TOKEN = os.getenv("TOKEN")

HORA_INICIO = 8
HORA_FIN = 22

async def controlar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hora = datetime.now().hour

    if hora < HORA_INICIO or hora >= HORA_FIN:
        try:
            await update.message.delete()
        except:
            pass

        await update.message.reply_text(
            "⛔ Este tema está cerrado fuera de horario.\n"
            f"🕒 Disponible de {HORA_INICIO}:00 a {HORA_FIN}:00"
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, controlar_mensajes))

    print("Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()
