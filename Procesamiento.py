#! /usr/bin/env python
# -*- coding: utf-8 -*-
import locale
import time
import requests
import os
import shutil
import logging
import pandas as pd

from requests.exceptions import ConnectionError


import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
logging.basicConfig( level=logging.DEBUG, filename='example.log')

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
def DescargarInformacion(categoria,csv_url):
    '''
    Organizar los archivos en rutas siguiendo la siguiente estructura: 
    “categoría\año-mes\categoria-dia-mes-año.csv”
    ○ Por ejemplo: “museos\2021-noviembre\museos-03-11-2021”
    ○ Si el archivo existe debe reemplazarse. La fecha de la nomenclatura
    es la fecha de descarga.
'''
    # Fecha para nomenclatura
    time_string = (time.strftime("%Y-%B,%d-%m-%Y", time.localtime())).split(',')
    # Ruta de archivos
    path= os.path.join(os.path.dirname(__file__),categoria,time_string[0],)

    # Borrare la carpeta para solo crear una unica carpeta con un solo archivo
    if (os.path.exists(path) ):
        try:
            shutil.rmtree(os.path.join(os.path.dirname(__file__),categoria))
            os.makedirs(path)
        except OSError as e:
            print("Error: %s : %s" % (os.path.join(os.path.dirname(__file__),categoria), e.strerror))
        
        
    else:
        os.makedirs(path)

    
    # Descarga CVS
    try:
        req = requests.get(csv_url)
        url_content = req.content
    
        csv_file = open(path+'/'+categoria+'-'+time_string[1]+'.csv', 'wb')
        csv_file.write(url_content)

        csv_file.close()
        logging.info('Descargo el archivo CVS de '+categoria)
    except ConnectionError:
        print('No existe la direccion Web de: ',categoria)
        logging.warning('Verificar la url de los CVS')
        logging.debug('Verificar la url de los CVS')


if __name__ == '__main__':
    dicc_csv_url ={
        'museos':'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museo.csv',
        'cine':'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv',
        'biblioteca_popular':'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv'        
        }

    

    # Descarga información desde Internet con las URLS ('museos',csv_url[0])
    for clave, valor in dicc_csv_url.items():
        DescargarInformacion(clave,valor)


    # Procesa los datos de los CVS para generar una única tabla CVS con los datos de los 3 archios CVS
    
    nombreColumnaEdit={'categoria':'Categoría','provincia':'Provincia','localidad':'Localidad','nombre':'Nombre','direccion':'Domicilio','Dirección':'Domicilio','telefono':'Teléfono',}
    CVS_total = pd.DataFrame()
    for clave in dicc_csv_url:
        rutaFichero= [f for f in os.listdir(clave) if not f.startswith('.')][0]
        rutaFinal = os.getcwd()+'/'+clave+'/'+rutaFichero+'/'+[f for f in os.listdir(clave+'/'+rutaFichero) if not f.startswith('.')][0]
        
        CVS = pd.read_csv(rutaFinal)    #Lectura de cada CVS
        CVS.rename(columns=nombreColumnaEdit, inplace=True) #Actualizacion de nombres de columna
            
        df= CVS[['Cod_Loc','IdProvincia','IdDepartamento','Categoría','Provincia','Localidad','Nombre','Domicilio','CP','Teléfono','Mail','Web']] #Lectura de datos por columna
        
        CVS_total = pd.concat([CVS_total,df])   #Union de contenido

    
    CVS_total.to_csv('FusionDatos.csv', index=False) #DataFrame enviado a archivo CSV

    '''
    '''
    #Procesar los datos conjuntos para poder generar una tabla con la siguiente información:
    # 1.- Cantidad de registros totales por categoría
    # 2.- Cantidad de registros totales por fuente
    # 3.- Cantidad de registros por provincia y categoria

    CVS_total = pd.DataFrame()
    CVS = pd.read_csv('FusionDatos.csv') #Lectura de CVS antes creado
    # 1.- Cantidad de registros totales por categoría   
    df_TotalesCategoria=CVS['Categoría'].value_counts()
    df_TotalesCategoria = df_TotalesCategoria.to_frame().reset_index()
    df_TotalesCategoria = df_TotalesCategoria.rename(columns= {'index': 'Categoría', 'Categoría':'Cantidad'})
    df_TotalesCategoria= df_TotalesCategoria[['Categoría','Cantidad']]
    CVS_total = pd.concat([CVS_total,df_TotalesCategoria]) 



    # 2.- Cantidad de registros totales por fuente

    df_CantidadFuente = pd.DataFrame({"Categoría":[],
                                       "Cantidad":[]})
    for clave in dicc_csv_url:
        rutaFichero= [f for f in os.listdir(clave) if not f.startswith('.')][0]
        rutaFinal = os.getcwd()+'/'+clave+'/'+rutaFichero+'/'+[f for f in os.listdir(clave+'/'+rutaFichero) if not f.startswith('.')][0]
        df_CVS = pd.read_csv(rutaFinal)    #Lectura de cada CVS
        cantidad_registros = str(df_CVS.shape[0])


        df = pd.DataFrame({"Categoría":[clave],
                    "Cantidad":[cantidad_registros]})
        df_CantidadFuente = pd.concat([df_CantidadFuente,df])
    
    CVS_total = pd.concat([CVS_total,df_CantidadFuente]) 


    # 3.- Cantidad de registros por provincia y categoria
 

    df_ProvinciaCategoria=(CVS.groupby(['Categoría','Provincia'])).size()
    df_ProvinciaCategoria = df_ProvinciaCategoria.to_frame().reset_index()
    df_ProvinciaCategoria = df_ProvinciaCategoria.rename(columns= {0: 'Cantidad'})
    df_ProvinciaCategoria['Categoría'] = df_ProvinciaCategoria['Categoría'] +' ' +df_ProvinciaCategoria['Provincia']
    df_ProvinciaCategoria= df_ProvinciaCategoria[['Categoría','Cantidad']] 

    CVS_total = pd.concat([CVS_total,df_ProvinciaCategoria]) 

    
    CVS_total.to_csv('TotalesPor.csv', index=False)
 
    '''
    '''
    '''Procesar la información de cines para poder crear una tabla que contenga:
    - Provincia
    - Cantidad de pantallas
    - Cantidad de butacas
    - Cantidad de espacios INCAA
    '''
  
    
    rutaFichero= [f for f in os.listdir('cine') if not f.startswith('.')][0]
    rutaFinal = os.getcwd()+'/'+'cine'+'/'+rutaFichero+'/'+[f for f in os.listdir('cine'+'/'+rutaFichero) if not f.startswith('.')][0]
    
    # 1ro seleccionar solo las columnas que necesito
    CVS = pd.read_csv(rutaFinal)    #Lectura de cada CVS
    df_cines= CVS[['Provincia','Pantallas','Butacas','espacio_INCAA']] #Lectura de datos por columna
    df_cines.to_csv('CineProcesado.csv', index=False)
    
    print ('Terminaron los proceso de: Descarga, procesamiento y creaciones de tablas (CVS) ')
    
    


