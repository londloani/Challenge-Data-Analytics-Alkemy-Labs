#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine

from decouple import config

def pruebaConexion():
    try:
        
        engine = create_engine('postgresql://'+config('user')+':'+config('password')+'@'+config('hostname')+'/'+config('database_name'))
        connection = engine.connect()
        connection.close()
        return True
    except Exception as e:
        print (e)
        return False


if __name__ == '__main__':

    if pruebaConexion():
        engine = create_engine('postgresql://'+config('user')+':'+config('password')+'@'+config('hostname')+'/'+config('database_name'))
        connection = engine.connect()

        with connection as cursor:
            cursor.execute(open("base.sql").read())

        connection.close()

        print ('Se han creado las tablas correctamente')
    else:
        print ('Revisa la conexion con la DB')
