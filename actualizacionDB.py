#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine
from decouple import config
import pandas as pd
from datetime import datetime


def pruebaConexion():
    try:
        
        engine = create_engine('postgresql://'+config('user')+':'+config('password')+'@'+config('hostname')+'/'+config('database_name'))
        connection = engine.connect()
        connection.close()
        return True
    except Exception as e:
        print (e)
        return False

'''
Todos los registros existentes deben ser reemplazados por la nueva información.
'''
if __name__ == '__main__':
    os.system ("clear")


    if pruebaConexion():
        engine = create_engine('postgresql://'+config('user')+':'+config('password')+'@'+config('hostname')+'/'+config('database_name'))
        connection = engine.connect()

        files={'informacion':'FusionDatos.csv','cineprocesado':'CineProcesado.csv','totalespor':'TotalesPor.csv'}

        for key,value in files.items():
        
            CVS_total = pd.DataFrame()
            CVS = pd.read_csv(files[key]) #Lectura de CVS 
            CVS['fecha']=datetime.today().strftime('%d/%m/%Y')
            connection.execute('TRUNCATE TABLE '+key)
        
            CVS.to_sql(key, con=connection, if_exists='append',index=False)
        connection.close()

        print ('Se ha actualizado la base de datos correctamente')
    else:
        print ('Revisa la conexion con la DB')

