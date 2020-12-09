#!/usr/bin/env python

import socket
from cryptography.fernet import Fernet

# Luis Ramirez

def sender(ip, reporte):
    # Se inicializa Fernet
    key = Fernet.generate_key() # Clave de encriptación
    print(key)
    fernet = Fernet(key)
    
    # Agregar la lectura del resultado aqui
    
    while True:
        cifrado = fernet.encrypt(reporte)
        
        # Inicializar socket para su envio al servidor
        # Datos de conexión
        TCP_IP = ip # IP a la que se conectará
        TCP_PORT = 8080 # Minimo 0, Máximo 65535
        BUFFER_SIZE = 10240

        # Inicializado como IPv4 y TCP
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect((TCP_IP, TCP_PORT))
        for i in range(1, 4):
            if i == 1:
                skt.send(b'1' + key)
                response = skt.recv(BUFFER_SIZE).decode()
            if i == 2:
                skt.send(b'2' + cifrado)
                response = skt.recv(BUFFER_SIZE).decode()
            if i == 3:
                skt.send(b'close')
                response = skt.recv(BUFFER_SIZE).decode()
            print(response)
        skt.close()
        break
