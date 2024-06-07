# Sistema de Monitoreo de Temperatura y Humedad para Sala de Servidores

Este proyecto tiene como objetivo monitorizar y controlar la temperatura y humedad en la sala de servidores de la US en Reina Mercedes mediante sensores conectados a un sistema centralizado.

## Descripción del Proyecto

El sistema consiste en:

- **Sensores**: Utilización de sensores de temperatura y humedad conectados a un Arduino para recopilar datos en tiempo real.
  
- **Raspberry Pi**: Encargada de recibir los datos de los sensores y enviarlos a una unidad central.

- **Unidad Central**: Aloja un dashboard desarrollado con Flask para visualizar y monitorear los datos de los sensores. También ofrece notificaciones por correo electrónico.

- **Bases de Datos**
   - Utilización de InfluxDB para almacenar los datos recopilados por los sensores.
   - El resto de funcionalidades serán cubiertas por SQLite

## Instalación

1. **Clonar el Repositorio**

   ```bash
   git clone https://github.com/Franbercam/sistema_de_sensado
   cd sistema_de_sensado

2. **Opcional: Activar Entorno Virtual (Recomendado)**

   Si prefieres trabajar en un entorno virtual, puedes crear uno y activarlo con los siguientes comandos:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En sistemas Unix o MacOS
   \venv\Scripts\activate    # En Windows

3. **Instalar dependencias**

   Asegúrate de tener Python y pip instalados en tu sistema. Luego, ejecuta el siguiente comando para instalar todas las dependencias necesarias:

   ```bash
   pip install -r requirements.txt

4. **Configurar InfluxDB**

   - Instalar y configurar InfluxDB en la unidad central.
   - Crear una base de datos para almacenar los datos de los sensores.


5. **Ejecutar la Aplicación**

   Puedes ejecutar la aplicación directamente con el siguiente comando:

   ```bash
   python .\index.py 

## Uso

### Raspberry pi

Por favor, siga estas instrucciones para configurar el punto de acceso:

   - Acceda al archivo de configuración "config.txt".
   - Localice y modifique la entrada correspondiente para especificar el nombre y la ubicación del punto de acceso.
   - Ejecute el script proporcionado.
   - Una vez en ejecución, el sistema permanecerá en un estado de espera para una posible conexión.
   - No es necesario realizar ninguna acción adicional en el punto de acceso después de este paso.

### Dashboard

El dashboard permite visualizar en tiempo real los datos de temperatura y humedad de los sensores. Puedes acceder al dashboard mediante un navegador web en la URL configurada en Flask.

### Notificaciones

Configura las notificaciones por correo electrónico para recibir alertas cuando los valores de temperatura y humedad superen los umbrales predefinidos.

## Estructura del Proyecto

- **arduino_code**: Código fuente para el Arduino.
- **raspberry_pi**: Scripts para la Raspberry Pi.
   - **raspberri_v03.py**: Script de configuración para la Raspberry Pi.
   - **config.txt**: Archivo de configuración necesario para la instalación.
- **central_server**: Código del servidor Flask y configuración de InfluxDB.

## Contribución

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Crea un nuevo Pull Request.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia ETSII. 

## Contacto

Para más información, puedes contactarnos a través del correo electrónico: franbercam01@gmail.com o
a traves de mi perfil de Linkedin: www.linkedin.com/in/francisco-de-as%C3%ADs-berm%C3%BAdez-campuzano-a28b322b3/




[def]: ../raspberri_v03.py