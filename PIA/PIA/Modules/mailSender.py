#!/usr/bin/env python

import smtplib
import ssl
import email
import getpass
import base64
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sender(mail, report):
    print("Enviando reporte a {}".format(mail))
    file = open("./Modules/password", "rb")
    passB64 = file.read()
    file.close()
    passwordDecoded = base64.b64decode(passB64)
    password = passwordDecoded.decode()
    
    subject = "Reporte"
    body = """
        Has elegido recibir el reporte por correo
        Aqui esta adjunto el reporte de tu extraccion
        
        Don't reply to this message
        It won't work tho
    """
    sender = "piaprueba276@gmail.com"
    
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = mail
    message["Subject"] = subject
    message["Bcc"] = mail
    
    message.attach(MIMEText(body, "plain"))
    
    with open("./Reportes/{}".format(report), "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        
    encoders.encode_base64(part)
    
    part.add_header("Content-Disposition", f"attachment; filename= {report}")
    
    message.attach(part)
    text = message.as_string()
    
    sslContext = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=sslContext) as server:
        server.login(sender, password)
        server.sendmail(sender, mail, text)
    
    print("Enviado")

#correo = "luis_6423@hotmail.com"
#sender(correo, "testEnvio.txt")