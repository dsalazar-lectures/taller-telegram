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

# La palabra async significa que esta función se ejecuta de forma asincrónica.
async def funcion_que_responde_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Mensaje a retornar al usuario
    mensaje = "Hola si funciono!!"
    # Await hace que la función espere a que sí se envíe el mensaje. Esta función envía el mensaje.
    await update.message.reply_text(mensaje)

def main():
    # Crea la aplicacion y utiliza el token del bot.
    token = "6036933509:AAGlz5hVjSkTNRy9lxkYRAZwlUoAPw3wTwg"
    
    # Crea la aplicación utilizando el token. Realiza el llamado API a Telegram por debajo.
    application = Application.builder().token(token).build()
    
    # El Bot reaccionará cuando el usuario escriba esta palabra
    palabra_accion = "start"

    # Comandos que el bot va a responder cuando un usuario le escriba en Telegram.
    # Noten que se pasa la función sin paréntesis. Se está pasando la referncia,
    # no queremos ejecutar la función de una vez, si no hasta que el usuario escriba la palabra clave.
    application.add_handler(CommandHandler([palabra_accion], funcion_que_responde_start))

    # Ejecuta el Bot hasta que escribamos Ctrl-C en la terminal.
    application.run_polling()


if __name__ == "__main__":
    main()