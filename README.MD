# Bot de Telegram para Agendar Citas con Xareny Farias

¡Bienvenido al repositorio de nuestro bot de Telegram! Este bot te ayudara a agendar citas de una manera super facil y rápida con Xareny Farias, nuestra ginecóloga virtual. 

## ¿Qué hace este bot?

- **Agendar consultas**: Puedes elegir entre consultas generales, ultrasonidos y otros tipos de tratamiento.
- **Consultar tu cita**: Solo necesitas tu token para obtener la información de tu cita.
- **Ver la ubicación**: Te damos un link directo a Google Maps para que encuentres la ubicación fácilmente.
- **Contactar a Xareny**: Te damos el enlace a su página de Facebook para que puedas contactarla.
![Pantalla del bot](images/xary1.png)
![Pantalla de inicio, con ubicacion y contacto](images/xary2.png)
![Pantalla de seleccion de cita y manejo de dia y horario](images/xary3.png)
![Pantalla de confirmacion de cita con su token y consultar cita con token](images/xar4.png)

## ¿Como funciona?

### 1. Iniciar el bot

Cuando inicias el bot con `/start`, Xareny te saluda y te da opciones para:
- Agendar Consulta
- Ubicación
- Contacto
- Consultar Cita

### 2. Agendar una cita

Seleccionas "Agendar Consulta" y eliges el tipo de tratamiento. Luego, seleccionas el día y la hora que más te convenga. ¡Listo! El bot te dará un token para que puedas consultar tu cita después.

### 3. Consultar tu cita

Si necesitas ver los detalles de tu cita, seleccionas "Consultar Cita" e ingresas tu token. El bot te mostrará toda la información que necesitas.

### 4. Ver la ubicacion

Seleccionas "Ubicación" y te enviamos un link de Google Maps para que no te pierdas.

### 5. Contactar a Xareny

Seleccionas "Contacto" y te enviamos el enlace a su página de Facebook.

## Como correr el bot

**Clonar este repositorio**:
   ```sh
   git clone https://github.com/fendyroiz/Bot-Telegram.git

    Actualiza con el token de tu bot, y accede a la carpeta.

    Instala las dependencias**

    Para este proyecto sera necesario tener instalado las siguientes dependencias

    pip install python-telegram-bot

    por ultimo sera necesario correrlo con python3 main.py