from sql_handler import SQLConnection
from amqp_handler import QueueConnection
from mongo_handler import mongoConnect
import datetime, json, ast
from mysql.connector import Error, cursor
import uuid


## SQL Client
sql_connection = SQLConnection.connection_to_db('192.168.1.60',3306,'si','tisapolines','polin')

## AMQP Client
#amqp_obj = QueueConnection()
amqp_connection = QueueConnection.connection_to_exchange(
  '10.75.10.166', 5672, 'tisa', 'tisa'
)
urlmongo = "mongodb://si:tisapolines@10.75.10.166:27017/?authSource=polin&authMechanism=SCRAM-SHA-1"

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
    print(data)
    """now = datetime.datetime.now() # Objeto de tiempo 
    #timestamp = now.strftime('%Y-%m-%d %H:%M:%S') # String de tiempo formateado
    data['timestamp'] = now.strftime('%Y-%m-%d %H:%M:%S') #timestamp 
    #_id = uuid.uuid1() # Objeto ID
    data['_id'] = uuid.uuid1().hex #_id.hex # Agrega value 'ID' a la key '_id' del mensaje
    idler =  mongoConnect.QueryIdlerDmi(urlmongo,data['key']) # Obtiene la ubicacion desde mongo a partir del dato key
    
    if idler == None:
      data['idler'] = 'Sensor sin ubicacion'
    else :
      data['idler'] = idler
    insert_data_query = INSERT INTO `statuses` (`_id`,`key`,`status`,`instant_status`,`SED_k`,`sigma_max`,`timestamp`,`idler`) VALUES (%(_id)s,%(key)s,%(status)s,%(instant_status)s,%(SED_k)s,%(sigma_max)s,%(timestamp)s,%(idler)s); # SQL Insert
    
    print('\n',data,'\n')
    print('Send to MYSQL...')
    SQLConnection.execute_query(sql_connection,insert_data_query,data) # Ejecuta el insert en SQL
    print('==================')"""

"""for result in cursor.execute(query, multi=True):
        if result.with_rows:
            print("Rows produced by statement '{}':".format(
            result.statement))
            print(result.fetchall())
        else:
            print("Number of rows affected by statement '{}': {}".format(
            result.statement, result.rowcount))"""

## Invoke queue consumer 
QueueConnection.create_channel(amqp_connection, callback, 'status', 'catdog')

# Ejecuta una consulta
# sql_connector.execute_query(connection,create_status_table)

# Muestra las tablas
# sql_connector.show_tables(connection)
