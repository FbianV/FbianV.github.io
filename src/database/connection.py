import mysql.connector
from mysql.connector import Error
from decouple import config

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password= config('MYSQL_PASSWORD'),
            database= config('MYSQL_DB'),
            port= config('MYSQL_PORT'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
