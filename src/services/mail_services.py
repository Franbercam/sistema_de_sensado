import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

## Credenciales guardadas en local en (.env)

EMAIL = '###################'
KEY = '####################' 

BODY = 'Los valores umbrales para '

def send_alert(subject,dest,rb_n):
    try:
        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = dest
        msg['Subject'] = 'Alarma: '+subject
        msg.attach(MIMEText(BODY+rb_n, 'plain'))

        # Establecer conexión y enviar el correo
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as connection:
            connection.ehlo()
            connection.starttls()
            connection.login(user=EMAIL, password=KEY)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=msg.as_string())
            print("Alert sent successfully.")
    except Exception as e:
        print(f"Failed to send alert: {e}")