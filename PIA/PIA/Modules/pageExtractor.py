#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
import requests
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract(link):
    reporte = ""
    req = requests.get(link)
    reporte = reporte + """
    
Estableciendo conexion
    
    """.format(req)
    if req.status_code != 200:
        reporte = reporte + """
Conexion rechazada o la pagina no existe
        """
        return reporte
    else:
        soup = bs(req.content, "html.parser")
        imgsrc = []

        for i in soup.find_all("img"):
            imgsrc.append(i.get("src"))
		
    os.system("mkdir images")
    n = 1

    for i in imgsrc:
        if i.startswith("http") == False:
            imgdownload = link + i
            reporte = reporte + """
{}
Descargando imagen: {}
            """.format(imgdownload, imgdownload.split("/")[-1])
            print(imgdownload)
            print("Descargando imagen: " + imgdownload.split("/")[-1])
            req = requests.get(imgdownload)
            imgfile = open("images/{}".format(imgdownload.split("/")[-1]), "wb")
            imgfile.write(req.content)
            imgfile.close()
            reporte = reporte + """Listo
            """
            print("Listo\n")
        else:
            imgdownload = i
            reporte = reporte + """
{}
Descargando imagen: {}
            """.format(imgdownload, imgdownload.split("/")[-1])
            print(imgdownload)
            print("Descargando imagen: images({}).jpg".format(imgdownload))
            req = requests.get(imgdownload)
            imgfile = open("images/{}".format(imgdownload.split("/")[-1]), "wb")
            imgfile.write(req.content)
            imgfile.close()
            reporte = reporte + """
Listo
            """
            print("Listo\n")
        n = n + 1
    return reporte

def exif_metadata(name):
    dict = {}
    img = Image.open(name)
    if hasattr(img, '_getexif'):
        exifinfo = img._getexif()
        if exifinfo is not None:
            for tag, value in exifinfo.items():
                tagss = TAGS.get(tag, tag)
                dict[tagss] = value
    gps_info(dict)
    return dict
    
    
def gps_info(dict):
    if 'GPSInfo' in dict:
        Nsec = dict['GPSInfo'][2][2]
        Nmin = dict['GPSInfo'][2][1]
        Ndeg = dict['GPSInfo'][2][0]
        Wsec = dict['GPSInfo'][4][2]
        Wmin = dict['GPSInfo'][4][1]
        Wdeg = dict['GPSInfo'][4][0]
        # Decodificación de las coordenadas
        if dict['GPSInfo'][1] == 'N':
            Nmult = 1
        else:
            Nmult = -1
        if dict['GPSInfo'][3] == 'E':
            Wmult = 1
        else:
            Wmult = -1
        Lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
        Lng = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)
        dict['GPSInfo'] = {"Lat" : Lat, "Lng" : Lng}

def metadata():
    reporte = """
Extrayendo metadata
    """
    print("Extrayendo metadata")
    os.chdir("./images")
    os.system("mkdir image_metadata")
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            try:
                exif = exif_metadata(name)
                print(exif)
                metafile = open("./image_metadata/{}.txt".format(name), "w")
                metafile.write("< Metadata info for image >\n")
                reporte = reporte + """
<Metadata info for image>
{}
""".format(exif)
                for metadata in exif:
                    metafile.write("{}: {}\n".format(metadata, exif[metadata]))
                metafile.close()
                reporte = reporte + """
Listo
"""
                print("Listo")
            except :
                reporte = reporte + """

Este no es imagen
"""
                print("Este no es imagen")
                pass
    return reporte
