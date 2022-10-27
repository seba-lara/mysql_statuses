from sql_lib import sql_connector
from amqp_lib import QueueConnection

create_status_table = """CREATE TABLE `statuses` (
  `_id` varchar(24) COLLATE 'ascii_general_ci' NOT NULL,
  `key` vaarchar(40) COLLATE 'ascii_general_ci' NOT NULL,
  `status` char(4) COLLATE 'ascii_general_ci' NULL,
  `instant_status` int(1) NOT NULL,
  `current_ewma` char(4) COLLATE 'ascii_general_ci' NULL,
  `SED_k` int(1) NOT NULL,
  `sigma_max` int(1) NOT NULL,
  `timestamp` date NOT NULL,
  `created_at` date NOT NULL
) ENGINE='InnoDB';"""

#connection = sql_connector.connection_to_db('192.168.1.60',3306,'root','tisapolines','polin')
#amqp_values = []

amqp_connection = QueueConnection.connection_to_exchange('10.75.10.166',5672,'tisa','tisa','status','cookie')


# Ejecuta una consulta
#sql_connector.execute_query(connection,create_status_table)

# Muestra las tablas
#sql_connector.show_tables(connection)

