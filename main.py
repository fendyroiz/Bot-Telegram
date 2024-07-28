import random
import string
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, CallbackContext, filters


citas = []

def crear_token(longitud=8):
    
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def que_dia(dia_semana):
    
    semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes']
    hoy = datetime.now()
    dias_hasta_dia = (semana.index(dia_semana.lower()) - hoy.weekday() + 7) % 7
    siguiente_dia = hoy + timedelta(days=dias_hasta_dia)
    return siguiente_dia.strftime('%d de %B de %Y'), siguiente_dia.strftime('%Y-%m-%d')


async def iniciar(update: Update, context: CallbackContext) -> None:
    usuario = update.message.from_user.username
    telefono = update.message.contact.phone_number if update.message.contact else "No proporcionado"
    context.user_data['telefono'] = telefono

    teclado = [
        [InlineKeyboardButton("Agendar Consulta", callback_data='agendar')],
        [InlineKeyboardButton("Ubicación", callback_data='ubicacion')],
        [InlineKeyboardButton("Contacto", callback_data='contacto')],
        [InlineKeyboardButton("Consultar Cita", callback_data='consultar')]
    ]
    reply_markup = InlineKeyboardMarkup(teclado)

    await update.message.reply_text(
        f"¡Hola {usuario}!  Soy Xareny Farias, tu ginecóloga. Vamos a agendar tu consulta de forma rapida y sencilla. ¿En que puedo ayudarte hoy?",
        reply_markup=reply_markup
    )


async def boton(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    ubicacion_link = "https://maps.app.goo.gl/TykSv15CAQTHas9z5"  
    contacto_link = "https://www.facebook.com/p/Dra-Xareni-Farias-Ginecologa-en-tijuana-100063821598881/?locale=es_LA"  

    if query.data == 'agendar':
        
        teclado = [
            [InlineKeyboardButton("Consulta General", callback_data='general')],
            [InlineKeyboardButton("Ultrasonido", callback_data='ultrasonido')],
            [InlineKeyboardButton("Otros", callback_data='otros')]
        ]
        reply_markup = InlineKeyboardMarkup(teclado)
        await query.message.reply_text("Selecciona el tipo de tratamiento:", reply_markup=reply_markup)
    elif query.data in ['general', 'ultrasonido', 'otros']:
        
        context.user_data['tratamiento'] = query.data
        teclado = [
            [InlineKeyboardButton("Lunes", callback_data='lunes')],
            [InlineKeyboardButton("Martes", callback_data='martes')],
            [InlineKeyboardButton("Miércoles", callback_data='miercoles')],
            [InlineKeyboardButton("Jueves", callback_data='jueves')],
            [InlineKeyboardButton("Viernes", callback_data='viernes')]
        ]
        reply_markup = InlineKeyboardMarkup(teclado)
        await query.message.reply_text("Selecciona un dia para la consulta:", reply_markup=reply_markup)
    elif query.data in ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']:
        
        dia = query.data.lower()
        teclado = [
            [InlineKeyboardButton("08:00 - 09:00", callback_data=f'{query.data}_08')],
            [InlineKeyboardButton("09:00 - 10:00", callback_data=f'{query.data}_09')],
            [InlineKeyboardButton("10:00 - 11:00", callback_data=f'{query.data}_10')],
            [InlineKeyboardButton("11:00 - 12:00", callback_data=f'{query.data}_11')],
            [InlineKeyboardButton("13:00 - 14:00", callback_data=f'{query.data}_13')],
            [InlineKeyboardButton("14:00 - 15:00", callback_data=f'{query.data}_14')],
            [InlineKeyboardButton("15:00 - 16:00", callback_data=f'{query.data}_15')]
        ]
        reply_markup = InlineKeyboardMarkup(teclado)
        fecha, fecha_formateada = que_dia(dia)
        context.user_data['fecha'] = fecha_formateada  
        await query.message.reply_text(f"Selecciona una hora para el dia {dia.capitalize()} ({fecha}):", reply_markup=reply_markup)
    elif query.data.endswith('_08') or query.data.endswith('_09') or query.data.endswith('_10') or query.data.endswith('_11') or query.data.endswith('_13') or query.data.endswith('_14') or query.data.endswith('_15'):
        
        dia, hora = query.data.split('_')
        dia = dia.capitalize()
        hora = {
            '08': '08:00 - 09:00',
            '09': '09:00 - 10:00',
            '10': '10:00 - 11:00',
            '11': '11:00 - 12:00',
            '13': '13:00 - 14:00',
            '14': '14:00 - 15:00',
            '15': '15:00 - 16:00'
        }[hora]
        
        
        token = crear_token()
        
        
        usuario = update.effective_user.username
        telefono = context.user_data.get('telefono', 'No proporcionado')
        tratamiento = context.user_data.get('tratamiento', 'No especificado')
        fecha = context.user_data.get('fecha', 'No especificada')
        cita = {'usuario': usuario, 'telefono': telefono, 'dia': dia, 'hora': hora, 'tratamiento': tratamiento, 'fecha': fecha, 'token': token}
        citas.append(cita)
        
        await query.message.reply_text(
            f"Tu cita ha sido agendada para el {dia} ({fecha}) a las {hora}. Tu token es: {token}. ¡Nos vemos pronto!"
        )
    elif query.data == 'consultar':
        await query.message.reply_text("Enviamos el token otorgado en tu cita")
        context.user_data['consultar'] = True  
    elif query.data == 'ubicacion':
        await query.message.reply_text(f"Puedes encontrarme mediante Google Maps: {ubicacion_link}")
    elif query.data == 'contacto':
        await query.message.reply_text(f"Para contactarme por mi pagina de Facebook: {contacto_link}")
    else:
        if context.user_data.get('consultar', False):
            token = query.data
            cita = next((c for c in citas if c['token'] == token), None)
            if cita:
                await query.message.reply_text(
                    f"Información de tu cita:\n\n"
                    f"Usuario: {cita['usuario']}\n"
                    f"Teléfono: {cita['telefono']}\n"
                    f"Día: {cita['dia']}\n"
                    f"Hora: {cita['hora']}\n"
                    f"Tratamiento: {cita['tratamiento']}\n"
                    f"Fecha Exacta: {cita['fecha']}"
                )
            else:
                await query.message.reply_text("Token erroneo, vuelve a intentarlo.")
            context.user_data['consultar'] = False  
        else:
            await query.message.reply_text("Hubo un error, elige otra opcion del menu por faaaa <3")


async def usuarios(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('consultar', False):
        
        token = update.message.text
        cita = next((c for c in citas if c['token'] == token), None)
        if cita:
            await update.message.reply_text(
                f"Información de tu cita:\n\n"
                f"Usuario: {cita['usuario']}\n"
                f"Teléfono: {cita['telefono']}\n"
                f"Día: {cita['dia']}\n"
                f"Hora: {cita['hora']}\n"
                f"Tratamiento: {cita['tratamiento']}\n"
                f"Fecha Exacta: {cita['fecha']}"
            )
        else:
            await update.message.reply_text("NO se encuentra este toke, intentalo de nuevo")
        context.user_data['consultar'] = False  
    else:
        await update.message.reply_text("Intenta con otra opcion del menu")

def main() -> None:
    
    token_bot = 'aqui va el token generado por tu bot'
    application = ApplicationBuilder().token(token_bot).build()

    
    application.add_handler(CommandHandler('start', iniciar))
    application.add_handler(CallbackQueryHandler(boton))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, usuarios))  

    
    application.run_polling()

if __name__ == '__main__':
    main()
