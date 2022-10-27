import mysql.connector
from mysql.connector import Error, cursor
#import datetime

class sql_connector:
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
                database=database)

            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

    def create_database(query,params):
        connection = mysql.connector.connect(params)
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            print('Database successfully')
        except Error as err:
            print(f'error: {err}')
    
    def execute_query(connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print('Query successfully')
        except Error as err:
            print(f'error: {err}')
    
    def show_tables(connection):
        cursor = connection.cursor()
        try:
            cursor.execute("SHOW TABLES")
            for x in cursor:
                print(x)
        except Error as err:
            print(f'error: {err} ')
        return
