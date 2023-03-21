#!/usr/bin/env python3
from sqlHandler import SQLConnection
from amqpHandler import QueueConnection
from mongoHandler import mongoConnect
import datetime, json
import uuid
import os.sys

## SQL Client
sql_connection = SQLConnection.connection_to_db('127.0.0.1',3306,'si','tisapolines','polin')

## AMQP Client
#amqp_obj = QueueConnection()
amqp_connection = QueueConnection.connection_to_exchange(
  '127.0.0.1', 5672, 'tisa', 'tisa'
)
urlmongo = "mongodb://si:tisapolines@127.0.0.1:27017/?authSource=polin&authMechanism=SCRAM-SHA-1"

## Create table statuses only if not exist
show_tables = SQLConnection.show_tables(sql_connection)

if show_tables == None:
  print('No existe la tabla statuses. \nCreando tabla satatuses...')
  SQLConnection.create_table(sql_connection)
else:
  print('La tabla statuses existe.')

## Callback function
def callback(ch, method, properties, body):

    datos = body.decode('utf-8') # Contiene el cuerpo del mensaje
    data = json.loads(datos) # Convierte el mensaje en un diccionario

    now = datetime.datetime.now() # Objeto de tiempo
    #timestamp = now.strftime('%Y-%m-%d %H:%M:%S') # String de tiempo formateado
    data['timestamp'] = now.strftime('%Y-%m-%d %H:%M:%S') #timestamp 
    #_id = uuid.uuid1() # Objeto ID
    data['_id'] = uuid.uuid1().hex #_id.hex # Agrega value 'ID' a la key '_id' del mensaje
    idler,latch_status =  mongoConnect.QueryIdlerDmi(urlmongo,data['key']) # Obtiene la ubicacion desde mongo a partir del dato key

    data['idler'] = idler
    data['latch_status'] = latch_status

    insert_data_query = """INSERT INTO `statuses` (`_id`,`key`,`status`,`timestamp`,`idler`,`latch_status`) VALUES (%(_id)s,%(key)s,%(status)s,%(timestamp)s,%(idler)s,%(latch_status)s);""" # SQL Insert

    print('\n',data,'\n')
    print('Send to MYSQL...')
    SQLConnection.execute_query(sql_connection,insert_data_query,data) # Ejecuta el insert en SQL
    print('==================')


## Invoke queue consumer
QueueConnection.create_channel(amqp_connection, callback, 'status', 'sqlstatuses')
