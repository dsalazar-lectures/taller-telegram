#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

# Implementación basada del ejemplo de https://docs.python-telegram-bot.org/en/stable/examples.timerbot.html

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Funcion que responde cuando el usuario escribe start. Le envia un mensaje al usuario.
    """
    mensaje = "Hola! Utiliza /recuerdame <segundos> <usuario> <mensaje> para poner un timer"
    await update.message.reply_text(mensaje)

async def mandar_recordatorio(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Manda el mensaje como recordatorio
    """
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Recordatorio! {job.data}")

def reemplazar_recordatorio_si_existe(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Reemplaza el recordatorio existente por el nuevo. Sólo maneja uno a la vez.
    """
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def poner_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Agrega el trabajo a una cola de mensajes.
    """
    chat_id = update.effective_message.chat_id # Cada chat tiene un identificador unico.
    try:
        # La variable context.args es el texto que escribe el usuario.
        
        # El primer argumento debe tener el tiempo en segundos para el timer.
        tiempo = float(context.args[0]) # args -> lista de argumentos con un split por espacios.
        
        # Tiempo negativo es invalido!
        if tiempo < 0:
            await update.effective_message.reply_text("Lo siento, no puedo ir al pasado :(")
            return
        
        # El segundo argumento debe ser el mensaje del recordatorio. Verificamos que exista.
        if len(context.args) == 1:
            await update.effective_message.reply_text("Olvidaste el mensaje del recordatorio! Vuelve a intentarlo.")
            return
        
        # Guardamos el mensaje del recordatorio.
        message = " ".join(context.args[1:]) # Recopilamos todo lo que sobre de args por si el mensaje tiene espacios.

        # Verificamos que no haya otro recordatorio. Si lo hay, lo reemplazamos.
        mensaje_anterior_borrado = reemplazar_recordatorio_si_existe(str(chat_id), context)
        # Ponemos el timer y le decimos que mensaje enviar.
        context.job_queue.run_once(mandar_recordatorio, tiempo, chat_id=chat_id, name=str(chat_id), data=message)

        # Realizamos la respuesta momentanea al usuario de que sí se creó el timer.
        text = "Comienza el timer!"
        if mensaje_anterior_borrado:
            text += " Y había otro antes, el cual fue eliminado."
            
        # Enviamos el mensaje.
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Recuerda que el uso correcto es: /recuerdame <segundos> <mensaje>")

def main():
    """Run bot."""
    # Crea la aplicacion y utiliza el token del bot.
    token = "<TOKEN>"
    application = Application.builder().token(token).build()

    # Comandos que el bot va a responder.
    application.add_handler(CommandHandler(["start", "help", "inicio", "ayuda"], start))
    application.add_handler(CommandHandler("recuerdame", poner_timer))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()