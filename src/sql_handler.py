import mysql.connector
from mysql.connector import Error, cursor
#import datetime

class SQLConnection:
    pass
    """def __init__(self,host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        #self.database = database
        pass"""

    def connection_to_db(host,port,user,password,database):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )

            print("Connection to MySQL DB successful")
        except Error as err:
            print(f"The error '{err}' occurred")
        return connection

    def execute_query(connection, query,data):
        cursor = connection.cursor()
        try:
            cursor.execute(query,data)
            connection.commit()
            print('Query successfully')
        except Error as err:
            print(f'error: {err}')
    
    def create_table(connection):
        create_status_table = """CREATE TABLE IF NOT EXISTS `statuses` (
            `_id` varchar(32) COLLATE 'ascii_general_ci' NOT NULL,
            `key` varchar(40) COLLATE 'ascii_general_ci' NOT NULL,
            `status` int(2) COLLATE 'ascii_general_ci' NULL,
            `timestamp` date NOT NULL,
            `idler` varchar(100) COLLATE 'ascii_general_ci' NOT NULL,
            `latch_status` int(1) NULL
            ) ENGINE='InnoDB';"""
        cursor = connection.cursor()
        try:
            cursor.execute(create_status_table)
            connection.commit()
            print('Successfully')
        except Error as err:
            print(f'error: {err}')

    def show_tables(connection):
        cursor = connection.cursor()
        try:
            cursor.execute("SHOW TABLES")
            for x in cursor:
                return x
        except Error as err:
            print(f'error: {err} ')
        #return

    """def create_database(query,params):
        connection = mysql.connector.connect(params)
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            print('Database successfully')
        except Error as err:
            print(f'error: {err}')"""