# Sistema de Monitoreo de Temperatura y Humedad para Sala de Servidores

Este proyecto tiene como objetivo monitorizar y controlar la temperatura y humedad en la sala de servidores de la US en Reina Mercedes mediante sensores conectados a un sistema centralizado.

## Descripción del Proyecto

El sistema consiste en:

- **Sensores**: Utilización de sensores de temperatura y humedad conectados a un Arduino para recopilar datos en tiempo real.
  
- **Raspberry Pi**: Encargada de recibir los datos de los sensores y enviarlos a una unidad central.

- **Unidad Central**: Aloja un dashboard desarrollado con Flask para visualizar y monitorear los datos de los sensores. También ofrece notificaciones por correo electrónico.

- **Base de Datos**: Utilización de InfluxDB para almacenar los datos recopilados por los sensores.

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

4. **Ejecutar la Aplicación**

   Puedes ejecutar la aplicación directamente con el siguiente comando:

   ```bash
   python .\index.py 

