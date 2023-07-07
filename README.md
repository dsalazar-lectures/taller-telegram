# Introducción a APIs: Creando un Bot de Telegram

## Pre requisitos

1. Tener cuenta de Telegram y acceso a la aplicación.
2. Tener Python instalado en la computadora.
3. Repasar la presentación: [Introducción a APIs](https://6f33fa7f78ea46e2aaca-my.sharepoint.com/:p:/g/personal/daniel_salazarmora_ucr_ac_cr/EQrpKNHNZQpEjDIoR3zVOscBE-txWVaq11nFAznuaWrb-g?e=XrXIFK)

## 1. Instalaciones

Para poder crear un bot de Telegram usando Python, se debe de instalar los siguientes paquetes:

```powershell
pip install python-telegram-bot -U --pre 
pip install python-telegram-bot[job-queue]
```

Los paquetes anteriores son requeridos respectivamente para:

1. Instalar una libreria que simplifica la conexión API con Telegram al requerir únicamente un Token para conectarse.
2. Instalar una librería que facilita la creación de una Cola que almacena los mensajes a mandar. Además, controla la concurrencia para saber cuándo termina el timer para enviar un mensaje.

> Documentación: https://docs.python-telegram-bot.org/en/stable/

## 2. Crear un Bot en Telegram

El primer paso para crearlo, es abrir Telegram en el celular o computadora y buscar al siguiente usuario: ```BotFather.```

![](C:\Users\DANIEL\Downloads\botfather.png)

> IMPORTANTE: Verifiquen que el bot tenga el check azul de verificación. De lo contrario, podría ser un bot de otro usuario.

Se le debe de seleccionar la opción o escribir: 

```
/newbot
```

Siga los pasos mencionados por el bot. Usualmente solicita el nombre del Bot y un nombre único como identificador para el bot que debe terminar con la palabra ```bot```

Si los pasos anteriores fueron exitosos, el BotFather le comentará que el bot fue creado y nos dará el token. Este token es una hilera de texto que corresponde a un código único para poder relacionar al bot recién creado. 

> Es muy importante que guarden el token en un lugar seguro. Si lo pierden, no hay manera de controlar al bot creado. Si lo descuidan, cualquier otro usuario podria "robarles" el bot.

## 3. Código en Python

### 1. Imports

Se deben de importar las clases necesarias para usar el programa:

```python
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
```

### 2. Función principal (main)

Primero, debemos definir la función de main()

```python
def main():
    # Crea la aplicacion y utiliza el token del bot.
    token = "<aqui pondremos el token que nos dió BotFather>"
    
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
```



Recuerden invocar la función de main al final del archivo! 

```python
if __name__ == "__main__":
    main()
```



### 3. Funciones de respuesta a lo que escribe un usuario por Telegram

Siguiendo el ejemplo anterior, la función que se ejcutará cuando el usuario escriba la palabra clave será:

```python
# La palabra async significa que esta función se ejecuta de forma asincrónica.
async def funcion_que_responde_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Mensaje a retornar al usuario
    mensaje = "Hola si funciono!!"
    # Await hace que la función espere a que sí se envíe el mensaje. Esta función envía el mensaje.
    await update.message.reply_text(mensaje)
```

### 4. Un ejemplo de Programa

>  El ejemplo a realizar está basado en: [TimerBot](https://docs.python-telegram-bot.org/en/stable/examples.timerbot.html)

Este programa funcionará como Un Bot que hará recordatorios del mensaje que diga el usuario. El usuario deberá decirle la cantidad de segundos que el bot esperará y posteriormente el mensaje del recordatorio. Es decir, hay 2 parámetros: ```tiempo y mensaje```

```python
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
    token = "<Token>"
    application = Application.builder().token(token).build()

    # Comandos que el bot va a responder.
    application.add_handler(CommandHandler(["start", "help", "inicio", "ayuda"], start))
    application.add_handler(CommandHandler("recuerdame", poner_timer))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
```

