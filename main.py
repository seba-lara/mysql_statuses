from sql_handlers import SQLConnection
from amqp_handlers import QueueConnection
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

## Create table statuses only if not exist
show_tables = SQLConnection.show_tables(sql_connection)

if show_tables == None:
  print('No existe la tabla statuses. \nCreando tabla satatuses...')
  SQLConnection.create_table(sql_connection)
else:
  print('La tabla statuses existe.')
()

## Callback function
def callback(ch, method, properties, body):
    
    datos = body.decode('utf-8')
    data = json.loads(datos)
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    data['timestamp'] = timestamp
    _id = uuid.uuid1()
    data['_id'] = _id.hex
    insert_data_query = """INSERT INTO `statuses` (`_id`,`key`,`status`,`instant_status`,`SED_k`,`sigma_max`,`timestamp`) VALUES (%(_id)s,%(key)s,%(status)s,%(instant_status)s,%(SED_k)s,%(sigma_max)s,%(timestamp)s);"""

    SQLConnection.execute_query(sql_connection,insert_data_query,data)
    print(data,'\n')
    print('Enviando a MYSQL...')
    print('\n')

"""for result in cursor.execute(query, multi=True):
        if result.with_rows:
            print("Rows produced by statement '{}':".format(
            result.statement))
            print(result.fetchall())
        else:
            print("Number of rows affected by statement '{}': {}".format(
            result.statement, result.rowcount))"""

## Call 
QueueConnection.create_channel(amqp_connection, callback, 'status', 'catdog')

# Ejecuta una consulta
# sql_connector.execute_query(connection,create_status_table)

# Muestra las tablas
# sql_connector.show_tables(connection)
