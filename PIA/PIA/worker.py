#!/usr/bin/env python

import os
import sys
import argparse
import builtwith
from datetime import date
import time
import subprocess
from shutil import rmtree
from Modules import socketSender 
from Modules import mailSender
from Modules import pageExtractor
from Modules import hunterAPI

parserDescription = """
    Extractor de informacion web
    
    Este script permite obtener recursos de una pagina web
    
"""
parserEpilog = """
    Programacion para Ciberseguidad
    Producto Integrador de Aprendizaje (PIA)
"""

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=parserDescription, epilog=parserEpilog)

parserArgument1 = """El link que se insertara para la extraccion

Ejemplo: python worker.py -link "https://www.uanl.com.mx"

"""
parserArgument2 = """Permite que el usuario decida si quiere extraer
la metadata de los archivos extraidos o no

opciones
"si"
"no"

Ejemplo: python worker.py -link "https://www.uanl.com.mx" -meta "si"

"""
parserArgument3 = """Tipo de envio del resultado

"mail" : Envio por correo (argumento -mail requerido)
"socket" : Envio de ordenador a ordenador
           (argumento -ip requerido y el programa receiver.py activo)

Ejemplo: python worker.py -link "https://www.uanl.com.mx" -meta "si" -sender "mail"

"""
parserArgument4 = """Argumento opcional
Recibe el correo electronico a donde enviar el resultado del proceso

Ejemplo: python worker.py -link "https://www.uanl.com.mx" -meta "si" -sender "mail" [-mail "correo"]

"""

parserArgument5 = """Argumento opcional
Recibe la direccion ip a donde enviar el resultado del proceso

Ejemplo: python worker.py -link "https://www.uanl.com.mx" -meta "si" -sender "mail" [-ip "ip"]

"""

# argumento -opt ya no se requiere porque no estamos dando a elegir si imagenes o archivos
parser.add_argument("-link", required=True, help=parserArgument1)
parser.add_argument("-meta", required=True, help=parserArgument2)
parser.add_argument("-sender", required=True, help=parserArgument3)
parser.add_argument("-mail", help=parserArgument4)
parser.add_argument("-ip", help=parserArgument5)

betaArgs = parser.parse_args()

powershell = subprocess.check_output("powershell -ExecutionPolicy ByPass -File ./hash512.ps1")
print(powershell)

hunterAPI.hunter(betaArgs.link.split(".")[1])

dirt = os.getcwd()

if os.path.isdir("./images"):
    rmtree("./images")

hora = time.ctime()
hora = hora.split()

reporte = """Reporte del proceso
{} {}""".format(date.today(), hora[3])

reporte = reporte + """

Extraccion de la informacion del link
Informacion obtenida con python builtwith
"""

# Obtencion del builder de la pagina
webInfo = builtwith.parse (betaArgs.link)
for key, value in webInfo.items ():
    reporte = reporte + "\n{}: {}".format(key, value)

reporte = reporte + """

Inicializando extraccion mediante BeautifulSoup"""

reporte = reporte + """
Extrayendo desde la pagina {}""".format(betaArgs.link)

# Hagan lo mismo que la variable reporte en el de web scraping
# para que el return sea una concatenacion de los print que estan
reporte = reporte + str(pageExtractor.extract(betaArgs.link))
#pageExtractor.extract(betaArgs.link)

# Extraccion de la metadata de las imagenes
if betaArgs.meta == "si":
    reporte = reporte + str(pageExtractor.metadata())
    reporte = reporte + """
Metadata extraida
    """
elif betaArgs.meta == "no":
    reporte = reporte + """
Metadata no extraida
    """

os.chdir(dirt)

if os.path.isdir("./Reportes") == False:
    os.system("mkdir Reportes")

reportName = "{} {}.txt".format(betaArgs.link.split("//")[1], date.today())

file = open("./Reportes/{}".format(reportName), "w")
file.write(reporte)
file.close()

# Inicio del tipo de envio del resultado
if betaArgs.sender == "mail":
    # Envio del resultado por correo
    mailSender.sender(betaArgs.mail, reportName)
elif betaArgs.sender == "socket":
    # Envio del resultado de ordenador a ordenador
    file = open("./Reportes/{}".format(reportName), "rb")
    reporteBytes = file.read()
    file.close()
    socketSender.sender(betaArgs.ip, reporteBytes)
