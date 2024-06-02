import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

## Credenciales guardadas en local en (.env)

EMAIL = '###################'
KEY = '####################' 

BODY_TEMPLATE = 'Los valores umbrales para {} han sido superados.\n\nDetalles de la alerta:\n'

def send_alert(alerta):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = alerta[4]
        msg['Subject'] = f'Alarma: {alerta[1]}'

        body = BODY_TEMPLATE.format(alerta[1])
        body += f"Temperatura Máxima: {alerta[5]}\n"
        body += f"Temperatura Mínima: {alerta[6]}\n"
        body += f"Humedad Máxima: {alerta[7]}\n"
        body += f"Humedad Mínima: {alerta[8]}\n"

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(host='smtp.gmail.com', port=587) as connection:
            connection.ehlo()
            connection.starttls()
            connection.login(user=EMAIL, password=KEY)
            connection.sendmail(from_addr=EMAIL, to_addrs=alerta[4], msg=msg.as_string())
            print("Alert sent successfully.")
    except smtplib.SMTPException as smtp_err:
        print(f"SMTP error occurred: {smtp_err}")
    except Exception as e:
        print(f"Failed to send alert: {e}")