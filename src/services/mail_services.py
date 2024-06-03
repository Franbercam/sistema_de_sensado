import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

## Credenciales guardadas en local en (.env)

EMAIL = os.getenv('EMAIL')
KEY = os.getenv('KEY')

BODY_TEMPLATE = 'Los valores umbrales para {} han sido superados.\n\nDetalles de la alerta:\n'

def send_alert(alerta):
    try:
        _, alert_nombre, alert_rb, alert_mail, alert_temp_max, alert_temp_min, alert_hum_max, alert_hum_min = alerta
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = alert_mail
        msg['Subject'] = f'Alarma: {alert_nombre}'

        body = BODY_TEMPLATE.format(alert_nombre)
        body += f"Máquina: {alert_rb}\n"
        body += f"Temperatura Máxima: {alert_temp_max}\n"
        body += f"Temperatura Mínima: {alert_temp_min}\n"
        body += f"Humedad Máxima: {alert_hum_max}\n"
        body += f"Humedad Mínima: {alert_hum_min}\n"

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(host='smtp.gmail.com', port=587) as connection:
            connection.ehlo()
            connection.starttls()
            connection.login(user=EMAIL, password=KEY)
            connection.sendmail(from_addr=EMAIL, to_addrs=alert_mail, msg=msg.as_string())
            print("Alert sent successfully.")
    except smtplib.SMTPException as smtp_err:
        print(f"SMTP error occurred: {smtp_err}")
    except Exception as e:
        print(f"Failed to send alert: {e}")