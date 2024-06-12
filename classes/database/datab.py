import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    cnx = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        passwd=os.getenv("PASS"),
        database=os.getenv("DB"),
        auth_plugin='mysql_native_password'
    )
    return cnx

connection = create_connection()
cursor = connection.cursor()