async def controlar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    hora = datetime.now(pytz.timezone("Europe/Madrid")).hour

    if hora < HORA_INICIO or hora >= HORA_FIN:
        try:
            await update.message.delete()
        except:
            pass

        await update.message.reply_text(
            "⛔ Este grupo está cerrado fuera de horario.\n"
            f"🕒 Disponible de {HORA_INICIO}:00 a {HORA_FIN}:00"
        )
