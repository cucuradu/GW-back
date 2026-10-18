import os
import mysql.connector

host = os.environ.get('DB_HOST', 'localhost')
user = os.environ.get('DB_USER', 'root')
password = os.environ.get('DB_PASSWORD', '')

dataBase = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password
)

cursorObject = dataBase.cursor()
cursorObject.execute("CREATE DATABASE IF NOT EXISTS growwise")
print("Database 'growwise' created or already exists!")