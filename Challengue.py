#! /usr/bin/env python
# -*- coding: utf-8 -*-
import locale, time, requests, os.path

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
'''

● Obtener los 3 archivos de fuente utilizando la librería requests y almacenarse en forma local (Ten en cuenta que las urls pueden cambiar en un futuro):
o Datos Argentina - Museos
https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museo.csv
o Datos Argentina - Salas de Cine
https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv
o Datos Argentina - Bibliotecas Populares
https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv

'''

#Descarga Informacion
def ObtenerInformacion():
    print ('Descargare los archivos')
    csv_url =['https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museo.csv',
    'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv',
    'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv']

    '''
    Organizar los archivos en rutas siguiendo la siguiente estructura: 
    “categoría\año-mes\categoria-dia-mes-año.csv”
    ○ Por ejemplo: “museos\2021-noviembre\museos-03-11-2021”
    ○ Si el archivo existe debe reemplazarse. La fecha de la nomenclatura
    es la fecha de descarga.
'''
    # Fecha para nomenclatura
    time_string = (time.strftime("%Y-%B,%d-%m-%Y", time.localtime())).split(',')
    print (time_string)

    # Estrucutra de ficheros

    print (os.getcwd())


    # Museos
    # req = requests.get(csv_url[0])
    # url_content = req.content
    # csv_file = open('Museos.csv', 'wb')

    # csv_file.write(url_content)
    # csv_file.close()
    # Salas de Cine

    # Biblotecas Populares


if __name__ == '__main__':
    ObtenerInformacion()