#!/usr/bin/env python

import socket
import os
from datetime import date
from cryptography.fernet import Fernet

# Datos de conexión del servidor
#TCP_IP = '0.0.0.0' # IP a recibir
TCP_PORT = 8080 # Minimo 0, Máximo 65535 (Default 80, 8080)
BUFFER_SIZE = 10240

# Abriendo conexión [IPv4 TCP Protocol]
skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Inicializado como IPv4 y TCP
skt.bind(("", TCP_PORT)) # Same as s.bind(address)
skt.listen() # Habilita el servidor a aceptar todas o ciertas conexiones
(conn, addr) = skt.accept() # Se almacena el intento de conexión

# Descifrado del contenido
def decrypt(key, info):
    fernet = Fernet(key)
    b = fernet.decrypt(info, None)
    report = b.decode()
    file = open("./reporte {}.txt".format(date.today()), "w")
    file.write(report)
    file.close()

# main
print("Direccion activa: ", addr)
# Se recibe el mensaje que se envio desde clienteTCP
while True:
    msg_received = conn.recv(BUFFER_SIZE)
    if msg_received[0] == b'1'[0]:
        print("Key received\n")
        conn.send(b'Fernet key sent.')
        k = msg_received.decode()
        key = k[1:]
    elif msg_received[0] == b'2'[0]:
        print("reporte recibido\n")
        msg = msg_received[1:]
        conn.send(b'Info sended')
    elif (msg_received.decode() == "close"):
        print("Cerrando conexión\n")
        conn.send(b'Closing connection')
        conn.close()
        break
#print(key)
decrypt(key, msg)
