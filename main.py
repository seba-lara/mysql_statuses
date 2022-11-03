from sql_handlers import SQLConnection
from amqp_handlers import QueueConnection
import datetime, json, ast
from mysql.connector import Error, cursor

create_status_table = """CREATE TABLE IF NOT EXISTS`statuses` (
  `_id` varchar(24) COLLATE 'ascii_general_ci' NOT NULL,
  `key` varchar(40) COLLATE 'ascii_general_ci' NOT NULL,
  `status` char(4) COLLATE 'ascii_general_ci' NULL,
  `instant_status` int(1) NOT NULL,
  `SED_k` int(1) NOT NULL,
  `sigma_max` int(1) NOT NULL,
  `timestamp` date NOT NULL
) ENGINE='InnoDB';"""

tiempo = datetime.datetime.now()
timestamp = (tiempo.strftime('%Y-%m-%d %H:%M:%S'))

## SQL Client
sql_connection = SQLConnection.connection_to_db(
  '192.168.1.60',3306,'root','tisapolines','polin'
)

## AMQP Client
amqp_obj = QueueConnection()
amqp_connection = amqp_obj.connection_to_exchange(
  '10.75.10.166', 5672, 'tisa', 'tisa'
)


## Create table statuses only if not exist
get_tables = SQLConnection.show_tables(sql_connection)

if get_tables == None:
  ('La tabla satuses no existe. \nCreando tabla statuses...')
  SQLConnection.create_table(sql_connection,create_status_table)
else:
  pass

def callback(ch, method, properties, body):
    
    datos = body.decode('utf-8') #.decode('utf-8')
    data = json.loads(datos)
    data['timestamp'] = timestamp

    insert_data_query = """INSERT INTO `statuses` (`_id`,`key`,`status`,`instant_status`,`SED_k`,`sigma_max`,`timestamp`) VALUES ('_id_test',%(key)s,%(status)s,%(instant_status)s,%(SED_k)s,%(sigma_max)s,%(timestamp)s);"""
    SQLConnection.execute_query(sql_connection,insert_data_query,data)
    print(data)
    """cursor = sql_connection.cursor()
    cursor.execute(query,data)
    sql_connection.commit()"""

    #sql_connector.execute_query(sql_connection,query,data)
"""for result in cursor.execute(query, multi=True):
        if result.with_rows:
            print("Rows produced by statement '{}':".format(
            result.statement))
            print(result.fetchall())
        else:
            print("Number of rows affected by statement '{}': {}".format(
            result.statement, result.rowcount))"""
    #columns = data.keys()
    #values = ', '.join("'" + str(x) + "'" for x in data.values())
    #data_formated = json.loads(values)
    

    #columns = ('_id_prueba',)
    #sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('statuses', columns, values)
    #cursor.execute(sql, values)
    #sql_connection.commit()
    
    #cursor.close()
    #sql_connection.close()
    #sql_connector.execute_query(sql_connection, query)
    #print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Processed !')
    # print(f" {tiempo} [x] %r" % body.decode()) # its a tuple
    
    #dato = json.dumps(data)
    
    #print(f"Mensaje recibido a las {tiempo} : %r " % type(dato))

amqp_obj.create_channel(amqp_connection, callback, 'status', 'catdog')

# Ejecuta una consulta
# sql_connector.execute_query(connection,create_status_table)

# Muestra las tablas
# sql_connector.show_tables(connection)
